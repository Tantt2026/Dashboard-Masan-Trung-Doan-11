import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(
    page_title="Dashboard KPI Sales - SS Trương Thanh Tân",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CSS ======================
st.markdown("""
<style>
    .main-header {font-size: 28px; font-weight: 700; color: #1a365d; text-align: center;}
    .sub-header {font-size: 14px; color: #4a5568; text-align: center; margin-bottom: 20px;}
    .metric-card {background: #f7fafc; border-radius: 10px; padding: 15px; border-left: 5px solid #2b6cb0;}
    .stDataFrame {font-size: 13px;}
</style>
""", unsafe_allow_html=True)

# ====================== LOGIC XỬ LÝ ======================
def load_and_process(rpt_file, mcp_file, kpi_file=None):
    df = pd.read_excel(rpt_file)
    mcp = pd.read_excel(mcp_file)

    # Lọc hủy
    df = df[df['Tình trạng đơn hàng'] != 'Đã hủy'].copy()
    df['Ngày tạo đơn hàng'] = pd.to_datetime(df['Ngày tạo đơn hàng'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    df['date'] = df['Ngày tạo đơn hàng'].dt.date

    # Map kênh
    mcp_map = mcp[['Outlet_code', 'L1']].drop_duplicates('Outlet_code')
    mcp_map['Outlet_code'] = mcp_map['Outlet_code'].astype(str)
    df['Mã CH'] = df['Mã CH'].astype(str)
    df = df.merge(mcp_map, left_on='Mã CH', right_on='Outlet_code', how='left')
    df['Tên SP lower'] = df['Tên sản phẩm'].astype(str).str.lower()

    return df, mcp

def get_targets(kpi_file):
    if kpi_file is None:
        return {}
    kpi_raw = pd.read_excel(kpi_file, header=None)
    kpi = kpi_raw.iloc[2:].copy()
    kpi.columns = ['Region','Month','Ship to','Distributor','SUP','SM pos','SM code','SM name',
                   'Saleteam','KPI type','KPI Name','Target','Thực hiện','% actual','% Contrib','Chưa ra HĐ']
    kpi = kpi.dropna(subset=['SM code'])
    kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')
    targets = {}
    for _, r in kpi.iterrows():
        sm = str(r['SM code']).strip()
        ktype = str(r['KPI type']).strip()
        kname = str(r['KPI Name']).strip()
        tgt = r['Target']
        if pd.isna(tgt): continue
        if ktype == 'ASO_ALL': targets.setdefault(sm, {})['ASO_ALL'] = int(tgt)
        elif ktype == 'PC_BT': targets.setdefault(sm, {})['PC_BT'] = int(tgt)
        elif ktype == 'ASO_ON': targets.setdefault(sm, {})['ASO_ON'] = int(tgt)
        elif ktype == 'ASO_Focus' and 'xanh' in kname.lower(): targets.setdefault(sm, {})['ASO_CHANTE'] = int(tgt)
    return targets

def color_pct(val):
    try:
        v = float(str(val).replace('%',''))
        if v >= 70: return 'background-color: #c6f6d5'
        elif v >= 50: return 'background-color: #fefcbf'
        else: return 'background-color: #fed7d7'
    except:
        return ''

def build_report(df, report_date, targets, report_type):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
    df_today = df[df['date'] == report_date].copy()
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())

    results = []

    if report_type == 'ASO_ALL':
        off = df_mtd[df_mtd['L1']=='Kênh Off Premise']
        mtd = off.groupby('Mã NVBH')['Mã CH'].nunique()
        ngay = df_today[df_today['L1']=='Kênh Off Premise'].groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt = 1200
        key = 'ASO_ALL'
    elif report_type == 'PC_BT':
        off = df_mtd[(df_mtd['L1']=='Kênh Off Premise') & ~df_mtd['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)]
        lines = off.groupby(['Mã NVBH','Mã đơn hàng'])['Mã sản phẩm'].nunique()
        mtd = lines[lines>=4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        off_t = df_today[(df_today['L1']=='Kênh Off Premise') & ~df_today['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)]
        lines_t = off_t.groupby(['Mã NVBH','Mã đơn hàng'])['Mã sản phẩm'].nunique()
        ngay = lines_t[lines_t>=4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        team_tgt = 2667
        key = 'PC_BT'
    elif report_type == 'ASO_TEA':
        on = df_mtd[df_mtd['L1']=='Kênh On Premise']
        tea = on[on['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)].copy()
        tea['qty'] = pd.to_numeric(tea['Tổng lẻ'], errors='coerce').fillna(0)
        ch = tea.groupby(['Mã NVBH','Mã CH'])['qty'].sum()
        mtd = ch[ch>=12].reset_index().groupby('Mã NVBH')['Mã CH'].nunique()
        on_t = df_today[df_today['L1']=='Kênh On Premise']
        tea_t = on_t[on_t['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)]
        ngay = tea_t.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt = 450
        key = 'ASO_ON'
    elif report_type == 'OMACHI':
        mask = df_mtd['Tên SP lower'].str.contains('omachi', na=False) & df_mtd['Tên SP lower'].str.contains('trộn|tron|xào|xao', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        mask_t = df_today['Tên SP lower'].str.contains('omachi', na=False) & df_today['Tên SP lower'].str.contains('trộn|tron|xào|xao', na=False)
        ngay = df_today[mask_t].groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt = 754
        key = None
    elif report_type == 'CHANTE':
        mask = df_mtd['Tên SP lower'].str.contains('chanté|chante', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        mask_t = df_today['Tên SP lower'].str.contains('chanté|chante', na=False)
        ngay = df_today[mask_t].groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt = 450
        key = 'ASO_CHANTE'
    else:
        return pd.DataFrame()

    for sm in all_sms:
        tgt = targets.get(sm, {}).get(key, team_tgt // 15) if key else (team_tgt // 15)
        m = int(mtd.get(sm, 0))
        n = int(ngay.get(sm, 0))
        pct = round(m / tgt * 100, 1) if tgt else 0
        results.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Chỉ tiêu': tgt,
            'Thực hiện (Ngày)': n,
            'MTD': m,
            '% MTD': pct
        })

    df_out = pd.DataFrame(results).sort_values('MTD', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out)+1))
    return df_out, team_tgt

def build_combo(df, report_date):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
    df_today = df[df['date'] == report_date].copy()
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())

    def is_combo(row):
        km = str(row.get('Hàng KM','N')).upper() == 'Y'
        giatri = float(pd.to_numeric(row.get('Giá trị hàng KM', 0), errors='coerce') or 0)
        ck = float(pd.to_numeric(row.get('Chiết khấu', 0), errors='coerce') or 0)
        channel = str(row.get('L1', ''))
        if channel == 'Kênh Off Premise':
            return km or giatri > 0 or ck >= 10000
        elif channel == 'Kênh On Premise':
            return km
        return False

    df_mtd['is_c'] = df_mtd.apply(is_combo, axis=1)
    df_today['is_c'] = df_today.apply(is_combo, axis=1)

    off_mtd = df_mtd[(df_mtd['is_c']) & (df_mtd['L1']=='Kênh Off Premise')].groupby('Mã NVBH')['Mã CH'].nunique()
    off_ngay = df_today[(df_today['is_c']) & (df_today['L1']=='Kênh Off Premise')].groupby('Mã NVBH')['Mã CH'].nunique()
    on_mtd = df_mtd[(df_mtd['is_c']) & (df_mtd['L1']=='Kênh On Premise')].groupby('Mã NVBH')['Mã CH'].nunique()
    on_ngay = df_today[(df_today['is_c']) & (df_today['L1']=='Kênh On Premise')].groupby('Mã NVBH')['Mã CH'].nunique()

    rows = []
    for sm in all_sms:
        rows.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Phát sinh 16/09 (OFF)': int(off_ngay.get(sm, 0)),
            'MTD (OFF)': int(off_mtd.get(sm, 0)),
            'Phát sinh 16/09 (ON)': int(on_ngay.get(sm, 0)),
            'MTD (ON)': int(on_mtd.get(sm, 0)),
        })
    df_out = pd.DataFrame(rows).sort_values('MTD (OFF)', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out)+1))
    return df_out

# ====================== UI ======================
st.markdown('<p class="main-header">📊 DASHBOARD KPI SALES</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">SS Trương Thanh Tân | Tháng 09/2026 | Cập nhật theo data RPT_061</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Cấu hình")
    rpt_file = st.file_uploader("1. Upload RPT_061.xlsx", type=['xlsx'])
    mcp_file = st.file_uploader("2. Upload Data_MCP.xlsx", type=['xlsx'])
    kpi_file = st.file_uploader("3. Upload Target_KPI.xlsx (optional)", type=['xlsx'])
    report_date = st.date_input("Ngày báo cáo", value=date(2026, 9, 16))
    st.markdown("---")
    st.info("Upload 2 file bắt buộc (RPT + MCP) rồi chọn báo cáo bên dưới.")

if rpt_file and mcp_file:
    with st.spinner("Đang xử lý dữ liệu..."):
        df, mcp = load_and_process(rpt_file, mcp_file)
        targets = get_targets(kpi_file) if kpi_file else {}

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "1. ASO ALL OFF", "2. PC 4-line", "3. ASO Tea ON",
        "4. Omachi Trộn", "5. Chanté", "6+7. Combo", "📈 Tổng quan"
    ])

    reports = {
        'ASO_ALL': ("ASO ALL Kênh OFF", tab1),
        'PC_BT': ("PC BT ≥ 4 Line", tab2),
        'ASO_TEA': ("ASO Tea ON ≥12 chai", tab3),
        'OMACHI': ("Omachi Trộn", tab4),
        'CHANTE': ("Chanté", tab5),
    }

    for rtype, (title, tab) in reports.items():
        with tab:
            df_r, team_tgt = build_report(df, report_date, targets, rtype)
            total_mtd = df_r['MTD'].sum()
            total_ngay = df_r['Thực hiện (Ngày)'].sum()
            pct_team = round(total_mtd / team_tgt * 100, 1)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Target Team", f"{team_tgt:,}")
            c2.metric("MTD", f"{total_mtd:,}")
            c3.metric("% MTD", f"{pct_team}%")
            c4.metric("Phát sinh Ngày", f"+{total_ngay}")

            st.dataframe(
                df_r.style.map(color_pct, subset=['% MTD']),
                use_container_width=True,
                hide_index=True
            )

            top3 = df_r.head(3)
            st.success(f"**Top 3:** {', '.join([f\"{r['Tên NVBH']} ({r['MTD']})\" for _, r in top3.iterrows()])}")

    # Combo tab
    with tab6:
        df_combo = build_combo(df, report_date)
        total_off = df_combo['MTD (OFF)'].sum()
        total_on = df_combo['MTD (ON)'].sum()
        ngay_off = df_combo['Phát sinh 16/09 (OFF)'].sum()
        ngay_on = df_combo['Phát sinh 16/09 (ON)'].sum()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("MTD OFF", f"{total_off} / 1092", f"{round(total_off/1092*100,1)}%")
        c2.metric("MTD ON", f"{total_on} / 1092", f"{round(total_on/1092*100,1)}%")
        c3.metric("Ngày OFF", f"+{ngay_off}")
        c4.metric("Ngày ON", f"+{ngay_on}")

        st.dataframe(df_combo, use_container_width=True, hide_index=True)

    # Tổng quan
    with tab7:
        st.subheader("Tổng hợp tiến độ 7 KPI")
        summary = []
        for rtype, (title, _) in reports.items():
            df_r, team_tgt = build_report(df, report_date, targets, rtype)
            summary.append({
                'Báo cáo': title,
                'Target': team_tgt,
                'MTD': df_r['MTD'].sum(),
                '%': round(df_r['MTD'].sum()/team_tgt*100, 1)
            })
        summary.append({'Báo cáo': 'Combo OFF', 'Target': 1092, 'MTD': total_off, '%': round(total_off/1092*100,1)})
        summary.append({'Báo cáo': 'Combo ON', 'Target': 1092, 'MTD': total_on, '%': round(total_on/1092*100,1)})
        df_sum = pd.DataFrame(summary)
        st.dataframe(df_sum.style.map(color_pct, subset=['%']), use_container_width=True, hide_index=True)

        fig = px.bar(df_sum, x='Báo cáo', y='%', color='%',
                     color_continuous_scale=['#fed7d7', '#fefcbf', '#c6f6d5'],
                     title='% Hoàn thành các KPI')
        fig.update_layout(yaxis_title='% MTD', xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("👈 Vui lòng upload **RPT_061.xlsx** và **Data_MCP.xlsx** ở sidebar để bắt đầu.")
    st.markdown("""
    ### Hướng dẫn deploy lên Streamlit Cloud + GitHub
    1. Tạo repo GitHub mới
    2. Upload 2 file: `streamlit_app.py` + `requirements.txt`
    3. Vào [share.streamlit.io](https://share.streamlit.io) → New app → chọn repo
    4. Main file path: `streamlit_app.py`
    5. Deploy xong là dùng được ngay (upload file excel mỗi lần chạy)
    """)