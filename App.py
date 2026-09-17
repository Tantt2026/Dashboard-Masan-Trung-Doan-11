import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
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
    .main-header {
        background: linear-gradient(90deg, #1a365d 0%, #2b6cb0 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .main-header h1 { margin: 0; font-size: 20px; font-weight: 700; }
    .main-header h2 { margin: 4px 0 0 0; font-size: 15px; font-weight: 500; color: #fefcbf; }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px 14px;
    }

    .note-box {
        background: #ebf8ff;
        border-left: 5px solid #3182ce;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-top: 14px;
        font-size: 13.5px;
        line-height: 1.55;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ====================== ĐƯỜNG DẪN FILE ======================
DATA_DIR = "data"

RPT_PATH   = os.path.join(DATA_DIR, "RPT_061.xlsx")
MCP_PATH   = os.path.join(DATA_DIR, "Data_MCP.xlsx")
KPI_PATH   = os.path.join(DATA_DIR, "Target_KPI.xlsx")
CAT_PATH   = os.path.join(DATA_DIR, "Data_Cat.xlsx")
BRAND_PATH = os.path.join(DATA_DIR, "Data_Brand.xlsx")

# ====================== LOAD DATA ======================
@st.cache_data(ttl=600)
def load_main_data():
    missing = []
    if not os.path.exists(RPT_PATH): missing.append("RPT_061.xlsx")
    if not os.path.exists(MCP_PATH): missing.append("Data_MCP.xlsx")
    if missing:
        st.error(f"Thiếu file: {', '.join(missing)} trong thư mục data/")
        st.stop()

    df = pd.read_excel(RPT_PATH)
    mcp = pd.read_excel(MCP_PATH)

    df = df[df['Tình trạng đơn hàng'] != 'Đã hủy'].copy()
    df['Ngày tạo đơn hàng'] = pd.to_datetime(
        df['Ngày tạo đơn hàng'], format='%d/%m/%Y %H:%M:%S', errors='coerce'
    )
    df['date'] = df['Ngày tạo đơn hàng'].dt.date

    mcp_map = mcp[['Outlet_code', 'L1']].drop_duplicates('Outlet_code')
    mcp_map['Outlet_code'] = mcp_map['Outlet_code'].astype(str)
    df['Mã CH'] = df['Mã CH'].astype(str)
    df = df.merge(mcp_map, left_on='Mã CH', right_on='Outlet_code', how='left')
    df['Tên SP lower'] = df['Tên sản phẩm'].astype(str).str.lower()
    return df, mcp


@st.cache_data(ttl=600)
def load_cat_data():
    possible_names = ["Data_Cat.xlsx", "data_cat.xlsx", "Data_CAT.xlsx", "CAT.xlsx"]
    for name in possible_names:
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path):
            try:
                return pd.read_excel(path)
            except Exception as e:
                st.warning(f"Lỗi đọc {name}: {e}")
                return pd.DataFrame()
    return pd.DataFrame()


@st.cache_data(ttl=600)
def load_brand_data():
    possible_names = ["Data_Brand.xlsx", "data_brand.xlsx", "Data_BRAND.xlsx", "Brand.xlsx"]
    for name in possible_names:
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path):
            try:
                return pd.read_excel(path)
            except Exception as e:
                st.warning(f"Lỗi đọc {name}: {e}")
                return pd.DataFrame()
    return pd.DataFrame()


@st.cache_data(ttl=600)
def get_targets():
    if not os.path.exists(KPI_PATH):
        return {}
    try:
        kpi_raw = pd.read_excel(KPI_PATH, header=None)
        kpi = kpi_raw.iloc[2:].copy()
        kpi.columns = [
            'Region','Month','Ship to','Distributor','SUP','SM pos','SM code','SM name',
            'Saleteam','KPI type','KPI Name','Target','Thực hiện','% actual','% Contrib','Chưa ra HĐ'
        ]
        kpi = kpi.dropna(subset=['SM code'])
        kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')
        targets = {}
        for _, r in kpi.iterrows():
            sm = str(r['SM code']).strip()
            ktype = str(r['KPI type']).strip()
            kname = str(r['KPI Name']).strip()
            tgt = r['Target']
            if pd.isna(tgt): continue
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
        v = float(str(val).replace('%','').strip())
        if v >= 70:
            return 'background-color: #c6f6d5; color:#22543d; font-weight:600'
        elif v >= 50:
            return 'background-color: #fefcbf; color:#744210; font-weight:600'
        else:
            return 'background-color: #fed7d7; color:#742a2a; font-weight:600'
    except:
        return ''


def format_number_vn(x):
    try:
        if pd.isnull(x):
            return ""
        return f"{float(x):,.0f}".replace(",", ".")
    except:
        return x


def find_col(df, candidates):
    """Tìm cột theo danh sách tên có thể có"""
    cols_lower = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None


# ====================== LOGIC KPI ======================
def build_report(df, report_date, targets, report_type, filter_nv=None):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()

    if filter_nv and filter_nv != "Tất cả ĐDKD":
        df_mtd = df_mtd[df_mtd['Tên NVBH'] == filter_nv]

    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())

    if report_type == 'ASO_ALL':
        off = df_mtd[df_mtd['L1'] == 'Kênh Off Premise'].copy()
        mtd = off.groupby('Mã NVBH')['Mã CH'].nunique()
        first_buy = off.groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
        first_buy.columns = ['Mã NVBH','Mã CH','first_date']
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt, key = 1200, 'ASO_ALL'
        title = "5. ASO ALL KÊNH OFF"

    elif report_type == 'PC_BT':
        off = df_mtd[
            (df_mtd['L1']=='Kênh Off Premise') &
            ~df_mtd['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)
        ]
        lines = off.groupby(['Mã NVBH','Mã đơn hàng'])['Mã sản phẩm'].nunique()
        mtd = lines[lines>=4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        df_today = df[df['date']==report_date]
        if filter_nv and filter_nv != "Tất cả ĐDKD":
            df_today = df_today[df_today['Tên NVBH'] == filter_nv]
        off_t = df_today[
            (df_today['L1']=='Kênh Off Premise') &
            ~df_today['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)
        ]
        lines_t = off_t.groupby(['Mã NVBH','Mã đơn hàng'])['Mã sản phẩm'].nunique()
        ngay = lines_t[lines_t>=4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        team_tgt, key = 2667, 'PC_BT'
        title = "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)"

    elif report_type == 'ASO_TEA':
        on = df_mtd[df_mtd['L1']=='Kênh On Premise']
        tea = on[on['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)].copy()
        tea['qty'] = pd.to_numeric(tea['Tổng lẻ'], errors='coerce').fillna(0)
        ch = tea.groupby(['Mã NVBH','Mã CH'])['qty'].sum()
        mtd = ch[ch>=12].reset_index().groupby('Mã NVBH')['Mã CH'].nunique()
        df_today = df[df['date']==report_date]
        if filter_nv and filter_nv != "Tất cả ĐDKD":
            df_today = df_today[df_today['Tên NVBH'] == filter_nv]
        on_t = df_today[df_today['L1']=='Kênh On Premise']
        tea_t = on_t[on_t['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)]
        ngay = tea_t.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt, key = 450, 'ASO_ON'
        title = "3. ASO TEA KÊNH ON PREMISE"

    elif report_type == 'OMACHI':
        mask = (
            df_mtd['Tên SP lower'].str.contains('omachi', na=False) &
            df_mtd['Tên SP lower'].str.contains('trộn|tron|xào|xao', na=False)
        )
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        omachi = df_mtd[mask].copy()
        first_buy = omachi.groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
        first_buy.columns = ['Mã NVBH','Mã CH','first_date']
        new_today = first_buy[first_buy['first_date']==report_date]
        ngay = new_today.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt, key = 754, None
        title = "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN"

    elif report_type == 'CHANTE':
        mask = df_mtd['Tên SP lower'].str.contains('chanté|chante', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        chante = df_mtd[mask].copy()
        first_buy = chante.groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
        first_buy.columns = ['Mã NVBH','Mã CH','first_date']
        new_today = first_buy[first_buy['first_date']==report_date]
        ngay = new_today.groupby('Mã NVBH')['Mã CH'].nunique()
        team_tgt, key = 450, 'ASO_CHANTE'
        title = "1. ASO FOCUS TOTAL NHÃN CHANTÉ"

    else:
        return pd.DataFrame(), 0, ""

    results = []
    for sm in all_sms:
        tgt = targets.get(sm, {}).get(key, team_tgt//15) if key else team_tgt//15
        m = int(mtd.get(sm, 0))
        n = int(ngay.get(sm, 0))
        pct = round(m/tgt*100, 1) if tgt else 0
        results.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Chỉ Tiêu KPI': tgt,
            'Thực Hiện Ngày': n,
            'MTD': m,
            '% MTD': f"{pct}%"
        })

    df_out = pd.DataFrame(results).sort_values('MTD', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out)+1))

    total_ngay = int(df_out['Thực Hiện Ngày'].sum()) if not df_out.empty else 0
    total_mtd = int(df_out['MTD'].sum()) if not df_out.empty else 0
    total_pct = round(total_mtd/team_tgt*100, 1) if team_tgt else 0

    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Trương Thanh Tân Total' if filter_nv == "Tất cả ĐDKD" else filter_nv,
        'Chỉ Tiêu KPI': team_tgt if filter_nv == "Tất cả ĐDKD" else (results[0]['Chỉ Tiêu KPI'] if results else 0),
        'Thực Hiện Ngày': total_ngay,
        'MTD': total_mtd,
        '% MTD': f"{total_pct}%"
    }])
    df_out = pd.concat([df_out, total_row], ignore_index=True)
    return df_out, team_tgt, title


def build_combo(df, report_date, filter_nv=None):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
    if filter_nv and filter_nv != "Tất cả ĐDKD":
        df_mtd = df_mtd[df_mtd['Tên NVBH'] == filter_nv]

    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())

    def is_combo(row):
        km = str(row.get('Hàng KM','N')).upper()=='Y'
        giatri = float(pd.to_numeric(row.get('Giá trị hàng KM',0), errors='coerce') or 0)
        ck = float(pd.to_numeric(row.get('Chiết khấu',0), errors='coerce') or 0)
        ch = str(row.get('L1',''))
        if ch == 'Kênh Off Premise': return km or giatri>0 or ck>=10000
        if ch == 'Kênh On Premise': return km
        return False

    df_mtd = df_mtd.copy()
    df_mtd['is_c'] = df_mtd.apply(is_combo, axis=1)

    off_mtd = df_mtd[(df_mtd['is_c']) & (df_mtd['L1']=='Kênh Off Premise')].groupby('Mã NVBH')['Mã CH'].nunique()
    on_mtd  = df_mtd[(df_mtd['is_c']) & (df_mtd['L1']=='Kênh On Premise')].groupby('Mã NVBH')['Mã CH'].nunique()

    off_c = df_mtd[(df_mtd['is_c']) & (df_mtd['L1']=='Kênh Off Premise')]
    first_off = off_c.groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
    first_off.columns = ['Mã NVBH','Mã CH','first_date']
    off_ngay = first_off[first_off['first_date']==report_date].groupby('Mã NVBH')['Mã CH'].nunique()

    on_c = df_mtd[(df_mtd['is_c']) & (df_mtd['L1']=='Kênh On Premise')]
    first_on = on_c.groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
    first_on.columns = ['Mã NVBH','Mã CH','first_date']
    on_ngay = first_on[first_on['first_date']==report_date].groupby('Mã NVBH')['Mã CH'].nunique()

    rows = []
    for sm in all_sms:
        rows.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm,''),
            'Phát sinh Ngày (OFF)': int(off_ngay.get(sm,0)),
            'MTD (OFF)': int(off_mtd.get(sm,0)),
            'Phát sinh Ngày (ON)': int(on_ngay.get(sm,0)),
            'MTD (ON)': int(on_mtd.get(sm,0)),
        })
    df_out = pd.DataFrame(rows).sort_values('MTD (OFF)', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out)+1))

    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Trương Thanh Tân Total' if filter_nv=="Tất cả ĐDKD" else filter_nv,
        'Phát sinh Ngày (OFF)': int(df_out['Phát sinh Ngày (OFF)'].sum()) if not df_out.empty else 0,
        'MTD (OFF)': int(df_out['MTD (OFF)'].sum()) if not df_out.empty else 0,
        'Phát sinh Ngày (ON)': int(df_out['Phát sinh Ngày (ON)'].sum()) if not df_out.empty else 0,
        'MTD (ON)': int(df_out['MTD (ON)'].sum()) if not df_out.empty else 0,
    }])
    return pd.concat([df_out, total_row], ignore_index=True)


# ====================== GIAO DIỆN ======================
st.markdown("""
<div class="main-header">
    <h1>SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</h1>
    <h2>TRACKING KPI ĐDKD - TEAM SS TRƯƠNG THANH TÂN TOTAL</h2>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🔄 Xóa Cache & Reload Data"):
    st.cache_data.clear()
    st.rerun()

with st.spinner("Đang tải dữ liệu từ GitHub..."):
    df, mcp = load_main_data()
    targets = get_targets()
    df_cat = load_cat_data()
    df_brand = load_brand_data()

nv_list = ["Tất cả ĐDKD"] + sorted(df['Tên NVBH'].dropna().unique().tolist())

# ========== FILTER BAR (chung cho KPI) ==========
f1, f2, f3, f4, f5 = st.columns([1.1, 1.2, 2.3, 1.4, 1.5])
with f1:
    st.selectbox("MONTH", ["Tháng 09/2026"], key="month")
with f2:
    report_date = st.date_input("NGÀY", value=date(2026, 9, 16), key="ngay")
with f3:
    kpi_map = {
        "1. ASO FOCUS TOTAL NHÃN CHANTÉ": "CHANTE",
        "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN": "OMACHI",
        "3. ASO TEA KÊNH ON PREMISE": "ASO_TEA",
        "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)": "PC_BT",
        "5. ASO ALL KÊNH OFF": "ASO_ALL",
        "6. BÁO CÁO ĐƠN HÀNG COMBO": "COMBO",
    }
    selected_name = st.selectbox("KPI NAME", list(kpi_map.keys()), key="kpi")
    selected_kpi = kpi_map[selected_name]
with f4:
    st.selectbox("SALE SUP", ["Trương Thanh Tân Total"], key="sup")
with f5:
    filter_nv = st.selectbox("ĐDKD (Nhân viên)", nv_list, key="ddkd")

st.markdown("---")

# ========== TABS ==========
tab_kpi, tab_mcp, tab_cat, tab_brand = st.tabs([
    "📊 BÁO CÁO KPI",
    "🗺️ MCP VISIT",
    "📦 TRACKING MBS - CAT",
    "🏷️ TRACKING MBS - BRAND"
])

# ----- TAB KPI -----
with tab_kpi:
    if selected_kpi != "COMBO":
        df_r, team_tgt, title = build_report(df, report_date, targets, selected_kpi, filter_nv)
        total_row = df_r.iloc[-1]
        total_mtd = int(total_row['MTD'])
        total_ngay = int(total_row['Thực Hiện Ngày'])
        pct_team = total_row['% MTD']

        st.subheader(f"{title} - THÁNG {report_date.strftime('%m/%Y')}")
        st.caption(f"⚡ Ngày: {report_date.strftime('%d/%m/%Y')} | Lọc: {filter_nv}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🎯 Target", f"{team_tgt:,}")
        c2.metric("📈 MTD", f"{total_mtd:,}")
        c3.metric("📊 % MTD", pct_team)
        c4.metric("🆕 Phát sinh Ngày", f"+{total_ngay}")

        st.dataframe(
            df_r.style.map(color_pct, subset=['% MTD']),
            use_container_width=True, hide_index=True, height=500
        )

        top3 = df_r.iloc[:-1].head(3)
        top3_text = ", ".join([f"{r['Tên NVBH']} ({r['MTD']})" for _, r in top3.iterrows()])
        st.markdown(f"""
        <div class="note-box">
            <b>NHẬN XÉT ({title} - {report_date.strftime('%d/%m/%Y')}):</b><br>
            • Tiến độ MTD: <b>{total_mtd}/{team_tgt} ({pct_team})</b>. Phát sinh ngày: <b>+{total_ngay}</b>.<br>
            • Top 3: <b>{top3_text}</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        df_combo = build_combo(df, report_date, filter_nv)
        total_row = df_combo.iloc[-1]
        total_off = int(total_row['MTD (OFF)'])
        total_on = int(total_row['MTD (ON)'])
        ngay_off = int(total_row['Phát sinh Ngày (OFF)'])
        ngay_on = int(total_row['Phát sinh Ngày (ON)'])

        st.subheader(f"6. BÁO CÁO ĐƠN HÀNG COMBO - THÁNG {report_date.strftime('%m/%Y')}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("MTD OFF", f"{total_off}", f"{round(total_off/1092*100,1)}%" if filter_nv=="Tất cả ĐDKD" else "")
        c2.metric("MTD ON", f"{total_on}", f"{round(total_on/1092*100,1)}%" if filter_nv=="Tất cả ĐDKD" else "")
        c3.metric("Ngày OFF", f"+{ngay_off}")
        c4.metric("Ngày ON", f"+{ngay_on}")
        st.dataframe(df_combo, use_container_width=True, hide_index=True, height=500)

# ----- TAB MCP VISIT -----
with tab_mcp:
    st.subheader("🗺️ MCP VISIT & MAPPING DOANH SỐ BÁN HÀNG")

    if mcp.empty:
        st.warning("Chưa có dữ liệu MCP")
    else:
        # Tìm cột
        col_nv = find_col(mcp, ['SM name', 'SM Name', 'Tên NVBH', 'Nhân viên', 'Sale name', 'Position name'])
        col_ma = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH', 'Mã khách hàng', 'Poscode', 'Ship to'])
        col_ten = find_col(mcp, ['Outlet_name', 'Outlet Name', 'Tên CH', 'Tên khách hàng', 'Customer name'])
        col_thu = find_col(mcp, ['Frequency', 'Tần suất', 'Thứ', 'Visit day', 'Ngày ghé'])

        # Bộ lọc
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            nv_opts = ["Tất cả ĐDKD"]
            if col_nv:
                nv_opts += sorted(mcp[col_nv].dropna().astype(str).unique().tolist())
            f_nv = st.selectbox("👤 Lọc Nhân Viên (ĐDKD)", nv_opts, key="mcp_nv")
        with c2:
            f_ma = st.text_input("🆔 Lọc Mã Khách Hàng", key="mcp_ma")
        with c3:
            f_ten = st.text_input("🏪 Lọc Tên Khách Hàng", key="mcp_ten")
        with c4:
            thu_opts = ["Tất cả các thứ", "2", "3", "4", "5", "6", "7", "25", "36", "47"]
            f_thu = st.selectbox("📅 Lọc Theo Thứ", thu_opts, key="mcp_thu")

        # Apply filter
        df_f = mcp.copy()
        if f_nv != "Tất cả ĐDKD" and col_nv:
            df_f = df_f[df_f[col_nv].astype(str) == f_nv]
        if f_ma and col_ma:
            df_f = df_f[df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)]
        if f_ten and col_ten:
            df_f = df_f[df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)]
        if f_thu != "Tất cả các thứ" and col_thu:
            df_f = df_f[df_f[col_thu].astype(str).str.contains(f_thu, na=False)]

        st.dataframe(df_f, use_container_width=True, height=550)
        st.caption(f"Hiển thị: {len(df_f):,} / {len(mcp):,} cửa hàng")

# ----- TAB CAT -----
with tab_cat:
    st.subheader("🎯 TRACKING MBS - THEO NGÀNH HÀNG (CATEGORY)")

    if df_cat.empty:
        st.error("❌ Không tìm thấy file Data_Cat.xlsx")
        st.code(f"Đường dẫn: {CAT_PATH}")
    else:
        st.success(f"✅ Đã load Data_Cat.xlsx – {len(df_cat):,} dòng")

        col_nv = find_col(df_cat, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên', 'Sale name'])
        col_ma = find_col(df_cat, ['Outlet Code', 'Outlet_code', 'Mã CH', 'Mã khách hàng', 'Poscode'])
        col_ten = find_col(df_cat, ['Outlet Name', 'Outlet_name', 'Tên CH', 'Tên khách hàng'])

        c1, c2, c3 = st.columns(3)
        with c1:
            nv_opts = ["Tất cả ĐDKD"]
            if col_nv:
                nv_opts += sorted(df_cat[col_nv].dropna().astype(str).unique().tolist())
            f_nv = st.selectbox("👤 Lọc Nhân Viên (ĐDKD)", nv_opts, key="cat_nv")
        with c2:
            f_ma = st.text_input("🆔 Lọc Mã Khách Hàng", key="cat_ma")
        with c3:
            f_ten = st.text_input("🏪 Lọc Tên Khách Hàng", key="cat_ten")

        df_f = df_cat.copy()
        if f_nv != "Tất cả ĐDKD" and col_nv:
            df_f = df_f[df_f[col_nv].astype(str) == f_nv]
        if f_ma and col_ma:
            df_f = df_f[df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)]
        if f_ten and col_ten:
            df_f = df_f[df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)]

        # Format doanh số
        for col in df_f.columns:
            if "doanh số" in col.lower() or "doanhso" in col.lower().replace(" ", ""):
                df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(format_number_vn)

        st.dataframe(df_f, use_container_width=True, height=550)
        st.caption(f"Hiển thị: {len(df_f):,} / {len(df_cat):,} dòng")

# ----- TAB BRAND -----
with tab_brand:
    st.subheader("🏷️ TRACKING MBS - THEO THƯƠNG HIỆU (BRAND)")

    if df_brand.empty:
        st.error("❌ Không tìm thấy file Data_Brand.xlsx")
        st.code(f"Đường dẫn: {BRAND_PATH}")
    else:
        st.success(f"✅ Đã load Data_Brand.xlsx – {len(df_brand):,} dòng")

        col_nv = find_col(df_brand, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên', 'Sale name'])
        col_ma = find_col(df_brand, ['Outlet Code', 'Outlet_code', 'Mã CH', 'Mã khách hàng', 'Poscode'])
        col_ten = find_col(df_brand, ['Outlet Name', 'Outlet_name', 'Tên CH', 'Tên khách hàng'])

        c1, c2, c3 = st.columns(3)
        with c1:
            nv_opts = ["Tất cả ĐDKD"]
            if col_nv:
                nv_opts += sorted(df_brand[col_nv].dropna().astype(str).unique().tolist())
            f_nv = st.selectbox("👤 Lọc Nhân Viên (ĐDKD)", nv_opts, key="brand_nv")
        with c2:
            f_ma = st.text_input("🆔 Lọc Mã Khách Hàng", key="brand_ma")
        with c3:
            f_ten = st.text_input("🏪 Lọc Tên Khách Hàng", key="brand_ten")

        df_f = df_brand.copy()
        if f_nv != "Tất cả ĐDKD" and col_nv:
            df_f = df_f[df_f[col_nv].astype(str) == f_nv]
        if f_ma and col_ma:
            df_f = df_f[df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)]
        if f_ten and col_ten:
            df_f = df_f[df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)]

        # Format doanh số
        for col in df_f.columns:
            if "doanh số" in col.lower() or "doanhso" in col.lower().replace(" ", ""):
                df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(format_number_vn)

        st.dataframe(df_f, use_container_width=True, height=550)
        st.caption(f"Hiển thị: {len(df_f):,} / {len(df_brand):,} dòng")
