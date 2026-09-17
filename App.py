import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import plotly.express as px
import os

st.set_page_config(
    page_title="Dashboard KPI Sales - SS Trương Thanh Tân",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CSS ======================
st.markdown("""
<style>
    .main-header {font-size: 26px; font-weight: 700; color: #1a365d; text-align: center;}
    .sub-header {font-size: 14px; color: #4a5568; text-align: center; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# ====================== ĐƯỜNG DẪN FILE CỐ ĐỊNH ======================
DATA_DIR = "data"
RPT_PATH = os.path.join(DATA_DIR, "RPT_061.xlsx")
MCP_PATH = os.path.join(DATA_DIR, "Data_MCP.xlsx")
KPI_PATH = os.path.join(DATA_DIR, "Target_KPI.xlsx")

# ====================== HÀM XỬ LÝ DỮ LIỆU ======================
@st.cache_data(ttl=3600)
def load_and_process():
    if not os.path.exists(RPT_PATH):
        st.error(f"Không tìm thấy file: {RPT_PATH}")
        st.stop()
    if not os.path.exists(MCP_PATH):
        st.error(f"Không tìm thấy file: {MCP_PATH}")
        st.stop()

    df = pd.read_excel(RPT_PATH)
    mcp = pd.read_excel(MCP_PATH)

    # Lọc đơn đã hủy
    df = df[df['Tình trạng đơn hàng'] != 'Đã hủy'].copy()
    df['Ngày tạo đơn hàng'] = pd.to_datetime(
        df['Ngày tạo đơn hàng'], format='%d/%m/%Y %H:%M:%S', errors='coerce'
    )
    df['date'] = df['Ngày tạo đơn hàng'].dt.date

    # Map kênh
    mcp_map = mcp[['Outlet_code', 'L1']].drop_duplicates(subset=['Outlet_code'])
    mcp_map['Outlet_code'] = mcp_map['Outlet_code'].astype(str)
    df['Mã CH'] = df['Mã CH'].astype(str)
    df = df.merge(mcp_map, left_on='Mã CH', right_on='Outlet_code', how='left')
    df['Tên SP lower'] = df['Tên sản phẩm'].astype(str).str.lower()

    return df, mcp


@st.cache_data(ttl=3600)
def get_targets():
    if not os.path.exists(KPI_PATH):
        return {}
    try:
        kpi_raw = pd.read_excel(KPI_PATH, header=None)
        kpi = kpi_raw.iloc[2:].copy()
        kpi.columns = [
            'Region', 'Month', 'Ship to', 'Distributor', 'SUP', 'SM pos',
            'SM code', 'SM name', 'Saleteam', 'KPI type', 'KPI Name',
            'Target', 'Thực hiện', '% actual', '% Contrib', 'Chưa ra HĐ'
        ]
        kpi = kpi.dropna(subset=['SM code'])
        kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')

        targets = {}
        for _, r in kpi.iterrows():
            sm = str(r['SM code']).strip()
            ktype = str(r['KPI type']).strip()
            kname = str(r['KPI Name']).strip()
            tgt = r['Target']
            if pd.isna(tgt):
                continue
            if ktype == 'ASO_ALL':
                targets.setdefault(sm, {})['ASO_ALL'] = int(tgt)
            elif ktype == 'PC_BT':
                targets.setdefault(sm, {})['PC_BT'] = int(tgt)
            elif ktype == 'ASO_ON':
                targets.setdefault(sm, {})['ASO_ON'] = int(tgt)
            elif ktype == 'ASO_Focus' and 'xanh' in kname.lower():
                targets.setdefault(sm, {})['ASO_CHANTE'] = int(tgt)
        return targets
    except Exception:
        return {}


def color_pct(val):
    try:
        v = float(str(val).replace('%', '').strip())
        if v >= 70:
            return 'background-color: #c6f6d5'
        elif v >= 50:
            return 'background-color: #fefcbf'
        else:
            return 'background-color: #fed7d7'
    except Exception:
        return ''


def build_report(df, report_date, targets, report_type):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())

    if report_type == 'ASO_ALL':
        # ===== LOGIC MỚI =====
        # MTD = Distinct CH có mua ít nhất 1 lần trong tháng
        # Thực hiện (Ngày) = Chỉ đếm CH lần đầu mua trong tháng rơi đúng ngày báo cáo
        off = df_mtd[df_mtd['L1'] == 'Kênh Off Premise'].copy()

        mtd = off.groupby('Mã NVBH')['Mã CH'].nunique()

        # Tìm ngày mua đầu tiên của mỗi CH
        first_buy = off.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
        first_buy.columns = ['Mã NVBH', 'Mã CH', 'first_date']

        # Chỉ lấy CH có ngày mua đầu tiên = ngày báo cáo
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby('Mã NVBH')['Mã CH'].nunique()

        team_tgt = 1200
        key = 'ASO_ALL'

    elif report_type == 'PC_BT':
        off = df_mtd[
            (df_mtd['L1'] == 'Kênh Off Premise') &
            ~df_mtd['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)
        ]
        lines = off.groupby(['Mã NVBH', 'Mã đơn hàng'])['Mã sản phẩm'].nunique()
        mtd = lines[lines >= 4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()

        # Với PC thì vẫn đếm đơn trong ngày (vì là count đơn, không phải CH)
        df_today = df[df['date'] == report_date]
        off_t = df_today[
            (df_today['L1'] == 'Kênh Off Premise') &
            ~df_today['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)
        ]
        lines_t = off_t.groupby(['Mã NVBH', 'Mã đơn hàng'])['Mã sản phẩm'].nunique()
        ngay = lines_t[lines_t >= 4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        team_tgt = 2667
        key = 'PC_BT'

    elif report_type == 'ASO_TEA':
        on = df_mtd[df_mtd['L1'] == 'Kênh On Premise']
        tea = on[on['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)].copy()
        tea['qty'] = pd.to_numeric(tea['Tổng lẻ'], errors='coerce').fillna(0)
        ch = tea.groupby(['Mã NVBH', 'Mã CH'])['qty'].sum()
        mtd = ch[ch >= 12].reset_index().groupby('Mã NVBH')['Mã CH'].nunique()

        # Có thể giữ nguyên hoặc áp dụng logic CH mới nếu cần
        df_today = df[df['date'] == report_date]
        on_t = df_today[df_today['L1'] == 'Kênh On Premise']
        tea_t = on_t[on_t['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)]
        ngay = tea_t.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt = 450
        key = 'ASO_ON'

    elif report_type == 'OMACHI':
        mask = (
            df_mtd['Tên SP lower'].str.contains('omachi', na=False) &
            df_mtd['Tên SP lower'].str.contains('trộn|tron|xào|xao', na=False)
        )
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()

        # Áp dụng logic CH mới
        omachi = df_mtd[mask].copy()
        first_buy = omachi.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
        first_buy.columns = ['Mã NVBH', 'Mã CH', 'first_date']
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby('Mã NVBH')['Mã CH'].nunique()

        team_tgt = 754
        key = None

    elif report_type == 'CHANTE':
        mask = df_mtd['Tên SP lower'].str.contains('chanté|chante', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()

        # Áp dụng logic CH mới
        chante = df_mtd[mask].copy()
        first_buy = chante.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
        first_buy.columns = ['Mã NVBH', 'Mã CH', 'first_date']
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby('Mã NVBH')['Mã CH'].nunique()

        team_tgt = 450
        key = 'ASO_CHANTE'

    else:
        return pd.DataFrame(), 0

    results = []
    for sm in all_sms:
        if key:
            tgt = targets.get(sm, {}).get(key, team_tgt // 15)
        else:
            tgt = team_tgt // 15
        m = int(mtd.get(sm, 0))
        n = int(ngay.get(sm, 0))
        pct = round(m / tgt * 100, 1) if tgt else 0
        results.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Chỉ tiêu': tgt,
            'Thực hiện (Ngày)': n,
            'MTD': m,
            '% MTD': f"{pct}%"
        })

    df_out = pd.DataFrame(results).sort_values('MTD', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))

    # Dòng TỔNG CỘNG
    total_ngay = int(df_out['Thực hiện (Ngày)'].sum())
    total_mtd = int(df_out['MTD'].sum())
    total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0

    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Trương Thanh Tân Total',
        'Chỉ tiêu': team_tgt,
        'Thực hiện (Ngày)': total_ngay,
        'MTD': total_mtd,
        '% MTD': f"{total_pct}%"
    }])

    df_out = pd.concat([df_out, total_row], ignore_index=True)
    return df_out, team_tgt


def build_combo(df, report_date):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())

    def is_combo(row):
        km = str(row.get('Hàng KM', 'N')).upper() == 'Y'
        giatri = float(pd.to_numeric(row.get('Giá trị hàng KM', 0), errors='coerce') or 0)
        ck = float(pd.to_numeric(row.get('Chiết khấu', 0), errors='coerce') or 0)
        channel = str(row.get('L1', ''))
        if channel == 'Kênh Off Premise':
            return km or giatri > 0 or ck >= 10000
        elif channel == 'Kênh On Premise':
            return km
        return False

    df_mtd = df_mtd.copy()
    df_mtd['is_c'] = df_mtd.apply(is_combo, axis=1)

    # MTD
    off_mtd = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh Off Premise')].groupby('Mã NVBH')['Mã CH'].nunique()
    on_mtd = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh On Premise')].groupby('Mã NVBH')['Mã CH'].nunique()

    # Thực hiện Ngày = CH mới (lần đầu đạt điều kiện combo trong tháng)
    off_combo = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh Off Premise')]
    first_off = off_combo.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
    first_off.columns = ['Mã NVBH', 'Mã CH', 'first_date']
    new_off = first_off[first_off['first_date'] == report_date]
    off_ngay = new_off.groupby('Mã NVBH')['Mã CH'].nunique()

    on_combo = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh On Premise')]
    first_on = on_combo.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
    first_on.columns = ['Mã NVBH', 'Mã CH', 'first_date']
    new_on = first_on[first_on['first_date'] == report_date]
    on_ngay = new_on.groupby('Mã NVBH')['Mã CH'].nunique()

    rows = []
    for sm in all_sms:
        rows.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Phát sinh Ngày (OFF)': int(off_ngay.get(sm, 0)),
            'MTD (OFF)': int(off_mtd.get(sm, 0)),
            'Phát sinh Ngày (ON)': int(on_ngay.get(sm, 0)),
            'MTD (ON)': int(on_mtd.get(sm, 0)),
        })

    df_out = pd.DataFrame(rows).sort_values('MTD (OFF)', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))

    # Dòng TỔNG CỘNG
    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Trương Thanh Tân Total',
        'Phát sinh Ngày (OFF)': int(df_out['Phát sinh Ngày (OFF)'].sum()),
        'MTD (OFF)': int(df_out['MTD (OFF)'].sum()),
        'Phát sinh Ngày (ON)': int(df_out['Phát sinh Ngày (ON)'].sum()),
        'MTD (ON)': int(df_out['MTD (ON)'].sum()),
    }])
    df_out = pd.concat([df_out, total_row], ignore_index=True)
    return df_out


# ====================== GIAO DIỆN ======================
st.markdown('<p class="main-header">📊 DASHBOARD KPI SALES</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">SS Trương Thanh Tân | Tháng 09/2026</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Cấu hình")
    report_date = st.date_input("Ngày báo cáo", value=date(2026, 9, 16))
    st.markdown("---")
    st.success("Data đang lấy từ thư mục `data/` trên GitHub")
    if st.button("🔄 Reload data (xóa cache)"):
        st.cache_data.clear()
        st.rerun()

with st.spinner("Đang load data từ GitHub..."):
    df, mcp = load_and_process()
    targets = get_targets()

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "1. ASO ALL OFF",
    "2. PC 4-line",
    "3. ASO Tea ON",
    "4. Omachi Trộn",
    "5. Chanté",
    "6+7. Combo",
    "📈 Tổng quan"
])

report_list = [
    ('ASO_ALL', 'ASO ALL Kênh OFF', tab1),
    ('PC_BT', 'PC BT ≥ 4 Line', tab2),
    ('ASO_TEA', 'ASO Tea ON ≥ 12 chai', tab3),
    ('OMACHI', 'Omachi Trộn', tab4),
    ('CHANTE', 'Chanté', tab5),
]

for rtype, title, tab in report_list:
    with tab:
        df_r, team_tgt = build_report(df, report_date, targets, rtype)

        total_row = df_r.iloc[-1]
        total_mtd = int(total_row['MTD'])
        total_ngay = int(total_row['Thực hiện (Ngày)'])
        pct_team = total_row['% MTD']

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Target Team", f"{team_tgt:,}")
        c2.metric("MTD", f"{total_mtd:,}")
        c3.metric("% MTD", pct_team)
        c4.metric("Phát sinh Ngày", f"+{total_ngay}")

        st.dataframe(
            df_r.style.map(color_pct, subset=['% MTD']),
            use_container_width=True,
            hide_index=True
        )

        top3 = df_r.iloc[:-1].head(3)
        top3_text = ", ".join(
            [f"{row['Tên NVBH']} ({row['MTD']})" for _, row in top3.iterrows()]
        )
        st.success(f"**Top 3:** {top3_text}")

# ----- Tab Combo -----
with tab6:
    df_combo = build_combo(df, report_date)

    total_row = df_combo.iloc[-1]
    total_off = int(total_row['MTD (OFF)'])
    total_on = int(total_row['MTD (ON)'])
    ngay_off = int(total_row['Phát sinh Ngày (OFF)'])
    ngay_on = int(total_row['Phát sinh Ngày (ON)'])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("MTD OFF", f"{total_off} / 1092", f"{round(total_off/1092*100,1)}%")
    c2.metric("MTD ON", f"{total_on} / 1092", f"{round(total_on/1092*100,1)}%")
    c3.metric("Ngày OFF", f"+{ngay_off}")
    c4.metric("Ngày ON", f"+{ngay_on}")

    st.dataframe(df_combo, use_container_width=True, hide_index=True)

# ----- Tab Tổng quan -----
with tab7:
    st.subheader("Tổng hợp tiến độ các KPI")
    summary_rows = []
    for rtype, title, _ in report_list:
        df_r, team_tgt = build_report(df, report_date, targets, rtype)
        total_row = df_r.iloc[-1]
        summary_rows.append({
            'Báo cáo': title,
            'Target': team_tgt,
            'MTD': int(total_row['MTD']),
            '% MTD': total_row['% MTD']
        })
    summary_rows.append({
        'Báo cáo': 'Combo OFF',
        'Target': 1092,
        'MTD': total_off,
        '% MTD': f"{round(total_off / 1092 * 100, 1)}%"
    })
    summary_rows.append({
        'Báo cáo': 'Combo ON',
        'Target': 1092,
        'MTD': total_on,
        '% MTD': f"{round(total_on / 1092 * 100, 1)}%"
    })

    df_sum = pd.DataFrame(summary_rows)
    st.dataframe(
        df_sum.style.map(color_pct, subset=['% MTD']),
        use_container_width=True,
        hide_index=True
    )

    df_chart = df_sum.copy()
    df_chart['pct_num'] = df_chart['% MTD'].str.replace('%', '').astype(float)
    fig = px.bar(
        df_chart,
        x='Báo cáo',
        y='pct_num',
        color='pct_num',
        color_continuous_scale=['#fed7d7', '#fefcbf', '#c6f6d5'],
        title='% Hoàn thành các KPI'
    )
    fig.update_layout(yaxis_title='% MTD', xaxis_tickangle=-25)
    st.plotly_chart(fig, use_container_width=True)
