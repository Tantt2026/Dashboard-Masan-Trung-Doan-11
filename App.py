import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import plotly.express as px
import os

st.set_page_config(
    page_title="TRACKING KPI ĐDKD - SS Trương Thanh Tân",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== CSS ======================
st.markdown("""
<style>
    /* Header */
    .main-header {
        background: linear-gradient(90deg, #1a365d 0%, #2b6cb0 100%);
        color: white;
        padding: 18px 24px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .main-header h1 {
        margin: 0;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .main-header h2 {
        margin: 6px 0 0 0;
        font-size: 16px;
        font-weight: 500;
        color: #fefcbf;
    }

    /* Filter bar */
    .filter-box {
        background: #f7fafc;
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* Table */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Note box */
    .note-box {
        background: #ebf8ff;
        border-left: 5px solid #3182ce;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-top: 16px;
        font-size: 14px;
        line-height: 1.6;
    }

    /* Hide Streamlit default */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ====================== ĐƯỜNG DẪN FILE ======================
DATA_DIR = "data"
RPT_PATH = os.path.join(DATA_DIR, "RPT_061.xlsx")
MCP_PATH = os.path.join(DATA_DIR, "Data_MCP.xlsx")
KPI_PATH = os.path.join(DATA_DIR, "Target_KPI.xlsx")

# ====================== HÀM XỬ LÝ ======================
@st.cache_data(ttl=3600)
def load_and_process():
    if not os.path.exists(RPT_PATH) or not os.path.exists(MCP_PATH):
        st.error("Không tìm thấy file data trong thư mục `data/`. Vui lòng kiểm tra lại.")
        st.stop()

    df = pd.read_excel(RPT_PATH)
    mcp = pd.read_excel(MCP_PATH)

    df = df[df['Tình trạng đơn hàng'] != 'Đã hủy'].copy()
    df['Ngày tạo đơn hàng'] = pd.to_datetime(
        df['Ngày tạo đơn hàng'], format='%d/%m/%Y %H:%M:%S', errors='coerce'
    )
    df['date'] = df['Ngày tạo đơn hàng'].dt.date

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
            return 'background-color: #c6f6d5; color: #22543d; font-weight: 600'
        elif v >= 50:
            return 'background-color: #fefcbf; color: #744210; font-weight: 600'
        else:
            return 'background-color: #fed7d7; color: #742a2a; font-weight: 600'
    except Exception:
        return ''


def build_report(df, report_date, targets, report_type):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())

    if report_type == 'ASO_ALL':
        off = df_mtd[df_mtd['L1'] == 'Kênh Off Premise'].copy()
        mtd = off.groupby('Mã NVBH')['Mã CH'].nunique()
        first_buy = off.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
        first_buy.columns = ['Mã NVBH', 'Mã CH', 'first_date']
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt = 1200
        key = 'ASO_ALL'
        title = "5. ASO ALL KÊNH OFF"

    elif report_type == 'PC_BT':
        off = df_mtd[
            (df_mtd['L1'] == 'Kênh Off Premise') &
            ~df_mtd['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)
        ]
        lines = off.groupby(['Mã NVBH', 'Mã đơn hàng'])['Mã sản phẩm'].nunique()
        mtd = lines[lines >= 4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        df_today = df[df['date'] == report_date]
        off_t = df_today[
            (df_today['L1'] == 'Kênh Off Premise') &
            ~df_today['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)
        ]
        lines_t = off_t.groupby(['Mã NVBH', 'Mã đơn hàng'])['Mã sản phẩm'].nunique()
        ngay = lines_t[lines_t >= 4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        team_tgt = 2667
        key = 'PC_BT'
        title = "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)"

    elif report_type == 'ASO_TEA':
        on = df_mtd[df_mtd['L1'] == 'Kênh On Premise']
        tea = on[on['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)].copy()
        tea['qty'] = pd.to_numeric(tea['Tổng lẻ'], errors='coerce').fillna(0)
        ch = tea.groupby(['Mã NVBH', 'Mã CH'])['qty'].sum()
        mtd = ch[ch >= 12].reset_index().groupby('Mã NVBH')['Mã CH'].nunique()
        df_today = df[df['date'] == report_date]
        on_t = df_today[df_today['L1'] == 'Kênh On Premise']
        tea_t = on_t[on_t['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)]
        ngay = tea_t.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt = 450
        key = 'ASO_ON'
        title = "3. ASO TEA KÊNH ON PREMISE"

    elif report_type == 'OMACHI':
        mask = (
            df_mtd['Tên SP lower'].str.contains('omachi', na=False) &
            df_mtd['Tên SP lower'].str.contains('trộn|tron|xào|xao', na=False)
        )
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        omachi = df_mtd[mask].copy()
        first_buy = omachi.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
        first_buy.columns = ['Mã NVBH', 'Mã CH', 'first_date']
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt = 754
        key = None
        title = "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN"

    elif report_type == 'CHANTE':
        mask = df_mtd['Tên SP lower'].str.contains('chanté|chante', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        chante = df_mtd[mask].copy()
        first_buy = chante.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
        first_buy.columns = ['Mã NVBH', 'Mã CH', 'first_date']
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt = 450
        key = 'ASO_CHANTE'
        title = "1. ASO FOCUS TOTAL NHÃN CHANTÉ"

    else:
        return pd.DataFrame(), 0, ""

    results = []
    for sm in all_sms:
        tgt = targets.get(sm, {}).get(key, team_tgt // 15) if key else (team_tgt // 15)
        m = int(mtd.get(sm, 0))
        n = int(ngay.get(sm, 0))
        pct = round(m / tgt * 100, 1) if tgt else 0
        results.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Chỉ Tiêu KPI': tgt,
            'Thực Hiện Ngày': n,
            'MTD': m,
            '% MTD': f"{pct}%"
        })

    df_out = pd.DataFrame(results).sort_values('MTD', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))

    total_ngay = int(df_out['Thực Hiện Ngày'].sum())
    total_mtd = int(df_out['MTD'].sum())
    total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0

    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Trương Thanh Tân Total',
        'Chỉ Tiêu KPI': team_tgt,
        'Thực Hiện Ngày': total_ngay,
        'MTD': total_mtd,
        '% MTD': f"{total_pct}%"
    }])
    df_out = pd.concat([df_out, total_row], ignore_index=True)
    return df_out, team_tgt, title


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

    off_mtd = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh Off Premise')].groupby('Mã NVBH')['Mã CH'].nunique()
    on_mtd = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh On Premise')].groupby('Mã NVBH')['Mã CH'].nunique()

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
# Header
st.markdown("""
<div class="main-header">
    <h1>SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</h1>
    <h2>TRACKING KPI ĐDKD - TEAM SS TRƯƠNG THANH TÂN TOTAL</h2>
</div>
""", unsafe_allow_html=True)

# Load data
with st.spinner("Đang tải dữ liệu..."):
    df, mcp = load_and_process()
    targets = get_targets()

# Filter bar
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    report_date = st.date_input("📅 Ngày báo cáo", value=date(2026, 9, 16))
with col2:
    st.selectbox("📅 Tháng", ["Tháng 09/2026"], disabled=True)
with col3:
    kpi_options = {
        "1. ASO FOCUS TOTAL NHÃN CHANTÉ": "CHANTE",
        "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN": "OMACHI",
        "3. ASO TEA KÊNH ON PREMISE": "ASO_TEA",
        "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)": "PC_BT",
        "5. ASO ALL KÊNH OFF": "ASO_ALL",
        "6. BÁO CÁO ĐƠN HÀNG COMBO": "COMBO",
    }
    selected_kpi_name = st.selectbox("📌 KPI NAME", list(kpi_options.keys()))
    selected_kpi = kpi_options[selected_kpi_name]

st.markdown("---")

# ====================== HIỂN THỊ BÁO CÁO ======================
if selected_kpi != "COMBO":
    df_r, team_tgt, title = build_report(df, report_date, targets, selected_kpi)

    total_row = df_r.iloc[-1]
    total_mtd = int(total_row['MTD'])
    total_ngay = int(total_row['Thực Hiện Ngày'])
    pct_team = total_row['% MTD']

    # Title
    st.subheader(f"{title} - THÁNG {report_date.strftime('%m/%Y')}")
    st.caption(f"⚡ Dữ liệu tự động cập nhật ĐỘNG theo Ngày Chọn: {report_date.strftime('%d/%m/%Y')}")

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🎯 Target Team", f"{team_tgt:,}")
    m2.metric("📈 MTD", f"{total_mtd:,}")
    m3.metric("📊 % MTD", pct_team)
    m4.metric("🆕 Phát sinh Ngày", f"+{total_ngay}")

    # Table
    st.dataframe(
        df_r.style.map(color_pct, subset=['% MTD']),
        use_container_width=True,
        hide_index=True,
        height=520
    )

    # Nhận xét
    top3 = df_r.iloc[:-1].head(3)
    top3_text = ", ".join([f"{r['Tên NVBH']} ({r['MTD']})" for _, r in top3.iterrows()])

    st.markdown(f"""
    <div class="note-box">
        <b>NHẬN XÉT & ĐỀ XUẤT CHỦ LỰ TỪ GIÁM SÁT BÁN HÀNG ({title} - NGÀY {report_date.strftime('%d/%m/%Y')}):</b><br>
        • Tiến độ lũy kế MTD đến ngày {report_date.strftime('%d/%m')}: Toàn team đạt <b>{total_mtd}/{team_tgt} ASO ({pct_team})</b>.<br>
        • Phát sinh thực tế trong ngày {report_date.strftime('%d/%m')}: Chốt được <b>+{total_ngay} ASO mới</b>.<br>
        • Top 3 dẫn đầu: <b>{top3_text}</b>.<br>
        • Định hướng tiếp theo: Tiếp tục bám sát tuyến đường, đẩy mạnh chào hàng đúng chuẩn SKU để tối đa tỷ lệ cán mốc 100% KPI tháng!
    </div>
    """, unsafe_allow_html=True)

else:
    # Combo report
    df_combo = build_combo(df, report_date)
    total_row = df_combo.iloc[-1]
    total_off = int(total_row['MTD (OFF)'])
    total_on = int(total_row['MTD (ON)'])
    ngay_off = int(total_row['Phát sinh Ngày (OFF)'])
    ngay_on = int(total_row['Phát sinh Ngày (ON)'])

    st.subheader(f"6. BÁO CÁO ĐƠN HÀNG COMBO - THÁNG {report_date.strftime('%m/%Y')}")
    st.caption(f"⚡ Dữ liệu tự động cập nhật ĐỘNG theo Ngày Chọn: {report_date.strftime('%d/%m/%Y')}")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("MTD OFF", f"{total_off} / 1092", f"{round(total_off/1092*100,1)}%")
    m2.metric("MTD ON", f"{total_on} / 1092", f"{round(total_on/1092*100,1)}%")
    m3.metric("Ngày OFF", f"+{ngay_off}")
    m4.metric("Ngày ON", f"+{ngay_on}")

    st.dataframe(df_combo, use_container_width=True, hide_index=True, height=520)

    st.markdown(f"""
    <div class="note-box">
        <b>NHẬN XÉT BÁO CÁO COMBO - NGÀY {report_date.strftime('%d/%m/%Y')}:</b><br>
        • Kênh OFF: Lũy kế <b>{total_off}/1092 CH ({round(total_off/1092*100,1)}%)</b> | Phát sinh ngày: <b>+{ngay_off} CH</b>.<br>
        • Kênh ON: Lũy kế <b>{total_on}/1092 CH ({round(total_on/1092*100,1)}%)</b> | Phát sinh ngày: <b>+{ngay_on} CH</b>.<br>
        • Định hướng: Tập trung đẩy mạnh Combo OFF để cải thiện tỷ lệ hoàn thành.
    </div>
    """, unsafe_allow_html=True)
