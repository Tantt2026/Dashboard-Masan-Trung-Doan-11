import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import os

st.set_page_config(
    page_title="TRACKING KPI ĐDKD - SS Nguyễn Thị Tường Vy",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== LOGO ======================
logo_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 158.15 61.91" width="110" height="42">
<title>Masan Group logo</title>
<path d="M490.29,502.16s17.83-12.81,45.76-12.93c25.9-.11,30.18,8.14,38,10.79,0,0-3.8,5.82-5.78,9.63s-13.32,17.93-26.5,22.21c0,0,18.71-15.72,21.55-27.57,0,0-26.87-20.43-73.26-1.92" transform="translate(-432.92 -481.05)" style="fill:#f36f21"/>
<path d="M521.55,489.11c42-10.64,59.59,9.56,59.59,9.56A60.39,60.39,0,0,1,561,521.3c11.28-1.28,21.79-13,24-16.69s6.16-9.17,6.16-9.17c-7.12-3.22-13.13-12-35.93-14.22-16.3-1.59-33.6,7.88-33.6,7.88" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M454.12,528V512.92a58.92,58.92,0,0,1-.15-6.31l-.06,0-7.1,21.11h-3.41l-7.25-21h-.09c0,2.33.1,5.52.09,6.28v15h-3.24V502.39h4.8L445.1,524h.07l7.17-21.31h5V528Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M465.15,515c.21-1.42.7-3.56,4.21-3.58,2.94,0,4.35,1,4.37,3s-.87,2.12-1.62,2.19l-5.11.65c-5.13.67-5.58,4.26-5.57,5.81,0,3.16,2.42,5.3,5.8,5.29a8.32,8.32,0,0,0,6.64-3c.12,1.42.55,2.82,3.3,2.81a6.24,6.24,0,0,0,1.69-.36v-2.26a4.84,4.84,0,0,1-1,.14c-.63,0-1-.3-1-1.09l-.05-10.6c0-4.73-5.37-5.13-6.85-5.13-4.54,0-7.47,1.76-7.6,6.17Zm8.42,6.37c0,2.48-2.85,4.35-5.74,4.36-2.35,0-3.38-1.17-3.39-3.19,0-2.32,2.42-2.8,4-3,3.86-.52,4.64-.78,5.15-1.18Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M492.47,514.47c0-1.17-.47-3.12-4.44-3.1-1,0-3.7.34-3.7,2.64,0,1.53,1,1.88,3.4,2.46l3.14.77c3.89.94,5.27,2.35,5.27,4.87,0,3.83-3.15,6.14-7.37,6.16-7.39,0-7.94-4.21-8-6.44h3c.11,1.45.55,3.78,5,3.75,2.24,0,4.27-.89,4.26-3,0-1.47-1-2-3.72-2.63l-3.65-.88c-2.59-.62-4.31-1.91-4.34-4.46,0-4.09,3.39-6,7.05-6,6.66,0,7.17,4.87,7.17,5.78Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M502.6,514.75c.2-1.42.68-3.58,4.2-3.6,2.91,0,4.33,1.06,4.33,3s-.86,2.13-1.61,2.18l-5.1.66c-5.11.65-5.57,4.27-5.56,5.79,0,3.19,2.41,5.31,5.79,5.31a8.34,8.34,0,0,0,6.63-3c.11,1.41.53,2.83,3.28,2.8a5.87,5.87,0,0,0,1.68-.35l0-2.26a6.5,6.5,0,0,1-1,.15c-.62,0-1-.32-1-1.1l0-10.61c0-4.72-5.35-5.11-6.83-5.11-4.53,0-7.44,1.76-7.56,6.16Zm8.36,6.49c0,2.47-2.82,4.36-5.74,4.37-2.35,0-3.37-1.18-3.39-3.18,0-2.34,2.44-2.8,4-3,3.87-.51,4.65-.8,5.14-1.2Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M534.55,527.71h-3v-11.5c-.13-3.2-1.07-4.83-4.13-4.81-1.77,0-4.88,1.15-4.7,6.15v10.16h-3.24l-.07-18.56h2.72l0,2.66h.07a6.85,6.85,0,0,1,5.67-3.19c2.91,0,6.58,1.15,6.6,6.45Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M468,533.85a1.19,1.19,0,0,1,.07.34.6.6,0,0,1-.19.46.81.81,0,0,1-.51.21l-.54-.18q-.45-.15-.75-.23a2.37,2.37,0,0,0-.59-.08,2.27,2.27,0,0,0-1.47.49,3.1,3.1,0,0,0-.92,1.27,4.89,4.89,0,0,0-.35,1.64,5.25,5.25,0,0,0,.56,2.41,2.27,2.27,0,0,0,1.91,1.26.77.77,0,0,1,.27,0l.43-.06.37-.1.37-.15L467,541a1,1,0,0,1,.4-.11.54.54,0,0,1,.42.19.69.69,0,0,1,.17.48,1,1,0,0,1-.82,1,5.35,5.35,0,0,1-1.69.27,4.1,4.1,0,0,1-2.28-.63,4.15,4.15,0,0,1-1.5-1.71,5.52,5.52,0,0,1-.55-2.35,7.3,7.3,0,0,1,.25-1.93,5,5,0,0,1,.76-1.63,3.74,3.74,0,0,1,1.34-1.14,4.33,4.33,0,0,1,1.91-.45,4.73,4.73,0,0,1,1.68.27,1.72,1.72,0,0,1,.91.62" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M470.75,537.9a4.78,4.78,0,0,0,.63,2.45,2.13,2.13,0,0,0,2,1.1,2.3,2.3,0,0,0,1.48-.48,2.78,2.78,0,0,0,.88-1.28,5.69,5.69,0,0,0,.31-1.78,5.11,5.11,0,0,0-.3-1.78,2.94,2.94,0,0,0-.89-1.29,2.21,2.21,0,0,0-1.44-.48,2.3,2.3,0,0,0-1.44.46,2.82,2.82,0,0,0-.91,1.27,5.12,5.12,0,0,0-.31,1.82m-1.59,0a5.74,5.74,0,0,1,.54-2.53,4.26,4.26,0,0,1,1.51-1.76,4,4,0,0,1,4.42.06,4.39,4.39,0,0,1,1.47,1.8,5.8,5.8,0,0,1,.51,2.43,5.89,5.89,0,0,1-.51,2.46,4.25,4.25,0,0,1-1.47,1.79,4.11,4.11,0,0,1-4.49,0,4.31,4.31,0,0,1-1.48-1.8,5.85,5.85,0,0,1-.51-2.44" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M479.44,534.07a.79.79,0,0,1,.21-.58.7.7,0,0,1,.52-.21.73.73,0,0,1,.53.21.78.78,0,0,1,.22.59v.14l0,0a3,3,0,0,1,1.13-.91,3.31,3.31,0,0,1,1.43-.32,3.46,3.46,0,0,1,1.63.4,3,3,0,0,1,1.21,1.21,4,4,0,0,1,.46,2V542a.68.68,0,0,1-.22.54.77.77,0,0,1-.53.19.73.73,0,0,1-.51-.19.69.69,0,0,1-.21-.53v-5.36a2.16,2.16,0,0,0-.65-1.67,2.21,2.21,0,0,0-1.55-.6,2.32,2.32,0,0,0-1.09.26,2,2,0,0,0-.82.79,2.41,2.41,0,0,0-.31,1.25v5.05a.81.81,0,0,1-.2.59.68.68,0,0,1-.51.21.74.74,0,0,1-.54-.22.77.77,0,0,1-.23-.58Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M488.69,541.75a1.05,1.05,0,0,1-.44-.77.7.7,0,0,1,.2-.49.64.64,0,0,1,.49-.21,1,1,0,0,1,.46.13,6.25,6.25,0,0,1,.57.37,3.06,3.06,0,0,0,.49.31,3,3,0,0,0,1.34.36,2.88,2.88,0,0,0,1.37-.32,1.06,1.06,0,0,0,.6-1A1.24,1.24,0,0,0,493,539a9.34,9.34,0,0,0-1.39-.65q-1-.4-1.55-.68a3.05,3.05,0,0,1-1-.79,1.94,1.94,0,0,1-.42-1.28,2.36,2.36,0,0,1,.39-1.31,2.79,2.79,0,0,1,1.11-1,4,4,0,0,1,1.64-.4,5,5,0,0,1,1.71.3,3.57,3.57,0,0,1,1.22.66,1.1,1.1,0,0,1,.38.74.65.65,0,0,1-.21.47.78.78,0,0,1-.5.23,4.06,4.06,0,0,1-.89-.41c-.39-.22-.67-.38-.86-.46a1.78,1.78,0,0,0-.69-.15,2,2,0,0,0-1.28.35,1.16,1.16,0,0,0-.46.86,1.34,1.34,0,0,0,.42.75,2.92,2.92,0,0,0,.78.52q.44.2,1.07.41c.42.14.71.25.87.32a3.77,3.77,0,0,1,1.54,1,2.2,2.2,0,0,1,.47,1.42,2.72,2.72,0,0,1-.42,1.37,2.86,2.86,0,0,1-1.19,1,4.49,4.49,0,0,1-2,.41,4.67,4.67,0,0,1-3.14-1.06" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M496.81,533.76a.74.74,0,0,1,.21-.56.71.71,0,0,1,.52-.21.74.74,0,0,1,.53.2.73.73,0,0,1,.22.56V539a2.75,2.75,0,0,0,.58,1.85,2.16,2.16,0,0,0,1.74.69q2.38,0,2.38-2.53v-5.22a.74.74,0,0,1,.21-.56.71.71,0,0,1,.51-.21.74.74,0,0,1,.53.2.73.73,0,0,1,.22.56v5.3a4.35,4.35,0,0,1-.4,1.86,3.14,3.14,0,0,1-1.27,1.38,4.23,4.23,0,0,1-2.22.53,4,4,0,0,1-2.11-.51,3.14,3.14,0,0,1-1.25-1.37,4.36,4.36,0,0,1-.4-1.88Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M506.53,533.81a.7.7,0,0,1,.22-.53.76.76,0,0,1,.54-.21.68.68,0,0,1,.51.2.84.84,0,0,1,.2.61v.3h.94a2.69,2.69,0,0,1,2.29-1.15,2.75,2.75,0,0,1,2.4,1.62,3.7,3.7,0,0,1,1.29-1.26,3.26,3.26,0,0,1,1.53-.36,3,3,0,0,1,1.52.44,3,3,0,0,1,1.1,1.21,3.92,3.92,0,0,1,.41,1.84v5.58a.74.74,0,0,1-.22.57.74.74,0,0,1-.53.21.7.7,0,0,1-.5-.22.76.76,0,0,1-.22-.56v-5.54a2.57,2.57,0,0,0-.27-1.21,1.78,1.78,0,0,0-.72-.76,2.08,2.08,0,0,0-1-.25,2.2,2.2,0,0,0-1.51.53,2.14,2.14,0,0,0-.6,1.69v5.5a.62.62,0,0,1-.22.51.8.8,0,0,1-.53.18.75.75,0,0,1-.5-.18.63.63,0,0,1-.22-.5v-5.34a2.48,2.48,0,0,0-.63-1.87,2.18,2.18,0,0,0-1.57-.6,2.85,2.85,0,0,0-1.12.26,1.84,1.84,0,0,0-.8.74,2.45,2.45,0,0,0-.3,1.28v5.57a.75.75,0,0,1-.22.57.73.73,0,0,1-.52.21.7.7,0,0,1-.51-.22.75.75,0,0,1-.22-.56Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M522.43,537.42h5.42a3.31,3.31,0,0,0-.7-2.13,2.38,2.38,0,0,0-1.86-.83,2.53,2.53,0,0,0-1.94.78,3.25,3.25,0,0,0-.79,2.18m-1.59.47a6.14,6.14,0,0,1,.56-2.34,4.52,4.52,0,0,1,1.46-1.79,3.92,3.92,0,0,1,4.43,0,4.44,4.44,0,0,1,1.49,1.78,5.34,5.34,0,0,1,.53,2.31q0,.78-.88.78h-6a3.22,3.22,0,0,0,.41,1.62,2.5,2.5,0,0,0,1.05,1,3.23,3.23,0,0,0,1.46.33,3.91,3.91,0,0,0,2.58-1,1.26,1.26,0,0,1,.6-.29.49.49,0,0,1,.41.2.78.78,0,0,1,.15.47.9.9,0,0,1-.23.58,4.46,4.46,0,0,1-1.5,1,5.2,5.2,0,0,1-2.09.42,4.42,4.42,0,0,1-2-.44,3.84,3.84,0,0,1-1.39-1.17,5,5,0,0,1-.77-1.58,6.65,6.65,0,0,1-.26-1.72l0-.06v0" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M531,534a.83.83,0,0,1,.21-.59.69.69,0,0,1,.52-.22.72.72,0,0,1,.53.22.81.81,0,0,1,.22.6v.81h0a4.3,4.3,0,0,1,.87-1.13,1.77,1.77,0,0,1,1.13-.53.85.85,0,0,1,.59.23.76.76,0,0,1,.26.58.69.69,0,0,1-.26.6,2.4,2.4,0,0,1-.76.33,3.19,3.19,0,0,0-.65.23,2.54,2.54,0,0,0-1.2,2.4v4.66a.84.84,0,0,1-.2.6.68.68,0,0,1-.51.21.73.73,0,0,1-.54-.22.86.86,0,0,1-.22-.63Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
</svg>
"""

# ====================== CSS ======================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a365d 0%, #2b6cb0 100%);
        color: white;
        padding: 10px 16px;
        border-radius: 10px;
        margin-bottom: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.12);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-header .logo {
        flex-shrink: 0;
        background: white;
        border-radius: 6px;
        padding: 4px 8px;
        display: flex;
        align-items: center;
    }
    .main-header .title-block { flex: 1; text-align: center; }
    .main-header h1 {
        margin: 0;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    .main-header h2 {
        margin: 4px 0 0 0;
        font-size: 14px;
        font-weight: 600;
        color: #fefcbf;
        letter-spacing: 0.3px;
    }
    
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column;
            text-align: center;
            padding: 10px;
        }
        .main-header h1 { font-size: 18px; }
        .main-header h2 { font-size: 12px; }
    }

    .filter-label {
        font-weight: 700 !important;
        color: #c53030 !important;
        font-size: 12px !important;
        margin-bottom: 2px;
    }

    .note-box {
        background: #ebf8ff;
        border-left: 4px solid #3182ce;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        margin-top: 12px;
        font-size: 13px;
        line-height: 1.5;
    }
    #MainMenu, footer, header {visibility: hidden;}
    
    .custom-kpi-table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #e2e8f0 !important;
        font-family: sans-serif;
        font-size: 13px;
        background-color: #ffffff;
    }
    .custom-kpi-table th {
        background-color: #ffffff !important;
        color: #9b2c2c !important;
        font-weight: bold !important;
        text-align: center !important;
        border: 1px solid #e2e8f0 !important;
        padding: 6px;
    }
    .custom-kpi-table td {
        border: 1px solid #e2e8f0 !important;
        padding: 5px 6px;
    }
</style>
""", unsafe_allow_html=True)

def render_metric_card(label, value):
    st.markdown(f"""
    <div style="background: #ebf8ff; border: 1px solid #bee3f8; border-radius: 8px; padding: 10px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.04); margin-bottom: 8px;">
        <div style="color: #c53030; font-weight: 800; font-size: 1.1rem; margin-bottom: 4px;">{label}</div>
        <div style="color: #c53030; font-weight: 800; font-size: 2rem;">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ====================== ĐƯỜNG DẪN ======================
DATA_DIR = "data"
RPT_PATH   = os.path.join(DATA_DIR, "RPT_061.xlsx")
MCP_PATH   = os.path.join(DATA_DIR, "Data_MCP.xlsx")
KPI_PATH   = os.path.join(DATA_DIR, "Target_KPI.xlsx")
CAT_PATH   = os.path.join(DATA_DIR, "Data_Cat.xlsx")
BRAND_PATH = os.path.join(DATA_DIR, "Data_Brand.xlsx")

# ====================== LOAD ======================
@st.cache_data(ttl=600)
def load_main_data():
    if not os.path.exists(RPT_PATH) or not os.path.exists(MCP_PATH):
        st.error("Thiếu file RPT_061.xlsx hoặc Data_MCP.xlsx")
        st.stop()
    df = pd.read_excel(RPT_PATH)
    mcp = pd.read_excel(MCP_PATH)
    df = df[df['Tình trạng đơn hàng'] != 'Đã hủy'].copy()
    df['Ngày tạo đơn hàng'] = pd.to_datetime(df['Ngày tạo đơn hàng'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    df['date'] = df['Ngày tạo đơn hàng'].dt.date
    mcp_map = mcp[['Outlet_code', 'L1']].drop_duplicates('Outlet_code')
    mcp_map['Outlet_code'] = mcp_map['Outlet_code'].astype(str)
    df['Mã CH'] = df['Mã CH'].astype(str)
    df = df.merge(mcp_map, left_on='Mã CH', right_on='Outlet_code', how='left')
    df['Tên SP lower'] = df['Tên sản phẩm'].astype(str).str.lower()
    return df, mcp

@st.cache_data(ttl=600)
def load_cat_data():
    for name in ["Data_Cat.xlsx", "data_cat.xlsx"]:
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path):
            try: return pd.read_excel(path)
            except: pass
    return pd.DataFrame()

@st.cache_data(ttl=600)
def load_brand_data():
    for name in ["Data_Brand.xlsx", "data_brand.xlsx"]:
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path):
            try: return pd.read_excel(path)
            except: pass
    return pd.DataFrame()

@st.cache_data(ttl=600)
def get_targets():
    if not os.path.exists(KPI_PATH): return {}
    try:
        kpi = pd.read_excel(KPI_PATH, header=None).iloc[2:]
        kpi.columns = ['Region','Month','Ship to','Distributor','SUP','SM pos','SM code','SM name',
                       'Saleteam','KPI type','KPI Name','Target','Thực hiện','% actual','% Contrib','Chưa ra HĐ']
        kpi = kpi.dropna(subset=['SM code'])
        kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')
        targets = {}
        for _, r in kpi.iterrows():
            sm, ktype, kname, tgt = str(r['SM code']).strip(), str(r['KPI type']).strip(), str(r['KPI Name']).strip(), r['Target']
            if pd.isna(tgt): continue
            ktype_lower, kname_lower = ktype.lower(), kname.lower()
            
            if ktype_lower == 'aso_all': 
                targets.setdefault(sm, {})['ASO_ALL'] = int(tgt)
            elif ktype_lower == 'pc_bt': 
                targets.setdefault(sm, {})['PC_BT'] = int(tgt)
            elif ktype_lower == 'aso_on': 
                targets.setdefault(sm, {})['ASO_ON'] = int(tgt)
            elif ktype_lower == 'aso_focus' or 'xanh' in kname_lower: 
                targets.setdefault(sm, {})['ASO_CHANTE'] = int(tgt)
            elif ktype_lower == 'aso_focus_2' or 'vàng' in kname_lower or 'trận vàng' in kname_lower: 
                targets.setdefault(sm, {})['ASO_OMACHI'] = int(tgt)
        return targets
    except: return {}

def color_pct_bg(val):
    try:
        v = float(str(val).replace('%','').strip())
        if v >= 70: return 'background-color: #c6f6d5; color:#22543d; font-weight:600;'
        elif v >= 50: return 'background-color: #fefcbf; color:#744210; font-weight:600;'
        else: return 'background-color: #fed7d7; color:#742a2a; font-weight:600;'
    except: return ''

def format_number_vn(x):
    try:
        if pd.isnull(x) or str(x).lower() in ["none","nan",""]: return ""
        return f"{float(x):,.0f}".replace(",", ".")
    except: return x

def find_col(df, candidates):
    cols = {c.lower().strip(): c for c in df.columns}
    for c in candidates:
        if c.lower() in cols: return cols[c.lower()]
    return None

# ====================== KPI LOGIC CHUẨN ======================
def build_report(df, report_date, targets, report_type, filter_nv=None):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
    if filter_nv and filter_nv != "Tất cả ĐDKD":
        df_mtd = df_mtd[df_mtd['Tên NVBH'] == filter_nv]
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())

    if report_type == 'ASO_ALL':
        off = df_mtd[df_mtd['L1']=='Kênh Off Premise'].copy()
        mtd = off.groupby('Mã NVBH')['Mã CH'].nunique()
        first = off.groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
        first.columns = ['Mã NVBH','Mã CH','first_date']
        ngay = first[first['first_date']==report_date].groupby('Mã NVBH')['Mã CH'].nunique()
        key, title = 'ASO_ALL', "5. ASO ALL KÊNH OFF"

    elif report_type == 'PC_BT':
        off = df_mtd[(df_mtd['L1']=='Kênh Off Premise') & ~df_mtd['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)]
        lines = off.groupby(['Mã NVBH','Mã đơn hàng'])['Mã sản phẩm'].nunique()
        mtd = lines[lines>=4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        df_today = df[df['date']==report_date]
        if filter_nv and filter_nv != "Tất cả ĐDKD": df_today = df_today[df_today['Tên NVBH']==filter_nv]
        off_t = df_today[(df_today['L1']=='Kênh Off Premise') & ~df_today['Sub Division'].astype(str).str.contains('Beer|Bia', case=False, na=False)]
        lines_t = off_t.groupby(['Mã NVBH','Mã đơn hàng'])['Mã sản phẩm'].nunique()
        ngay = lines_t[lines_t>=4].reset_index().groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        key, title = 'PC_BT', "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)"

    elif report_type == 'ASO_TEA':
        on = df_mtd[df_mtd['L1']=='Kênh On Premise']
        tea = on[on['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)].copy()
        tea['qty'] = pd.to_numeric(tea['Tổng lẻ'], errors='coerce').fillna(0)
        ch = tea.groupby(['Mã NVBH','Mã CH'])['qty'].sum()
        mtd = ch[ch>=12].reset_index().groupby('Mã NVBH')['Mã CH'].nunique()
        df_today = df[df['date']==report_date]
        if filter_nv and filter_nv != "Tất cả ĐDKD": df_today = df_today[df_today['Tên NVBH']==filter_nv]
        on_t = df_today[df_today['L1']=='Kênh On Premise']
        tea_t = on_t[on_t['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)]
        ngay = tea_t.groupby('Mã NVBH')['Mã CH'].nunique()
        key, title = 'ASO_ON', "3. ASO TEA KÊNH ON PREMISE"

    elif report_type == 'OMACHI':
        mask = df_mtd['Tên SP lower'].str.contains('omachi', na=False) & df_mtd['Tên SP lower'].str.contains('trộn|tron|xào|xao', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        first = df_mtd[mask].groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
        first.columns = ['Mã NVBH','Mã CH','first_date']
        ngay = first[first['first_date']==report_date].groupby('Mã NVBH')['Mã CH'].nunique()
        key, title = 'ASO_OMACHI', "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN"

    elif report_type == 'CHANTE':
        mask = df_mtd['Tên SP lower'].str.contains('chanté|chante', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        first = df_mtd[mask].groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
        first.columns = ['Mã NVBH','Mã CH','first_date']
        ngay = first[first['first_date']==report_date].groupby('Mã NVBH')['Mã CH'].nunique()
        key, title = 'ASO_CHANTE', "1. ASO FOCUS TOTAL NHÃN CHANTÉ"
    else:
        return pd.DataFrame(), 0, ""

    results = []
    for sm in all_sms:
        tgt = targets.get(sm, {}).get(key, 0)
        m = int(mtd.get(sm, 0))
        n = int(ngay.get(sm, 0))
        pct = round(m/tgt*100, 1) if tgt else 0
        results.append({'Mã NVBH':sm, 'Tên NVBH':sm_names.get(sm,''), 'Chỉ Tiêu KPI':tgt, 'Thực Hiện Ngày':n, 'MTD':m, '% MTD':f"{pct}%", '_ratio': (m/tgt if tgt else 0)})

    df_out = pd.DataFrame(results).sort_values('_ratio', ascending=True).drop(columns=['_ratio']).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out)+1))

    total_ngay = int(df_out['Thực Hiện Ngày'].sum()) if not df_out.empty else 0
    total_mtd = int(df_out['MTD'].sum()) if not df_out.empty else 0
    team_tgt = int(df_out['Chỉ Tiêu KPI'].sum()) if not df_out.empty else 0
    total_pct = round(total_mtd/team_tgt*100, 1) if team_tgt else 0

    total_row = pd.DataFrame([{'STT':'-', 'Mã NVBH':'TỔNG CỘNG',
        'Tên NVBH':'SS Trương Thanh Tân Total' if filter_nv=="Tất cả ĐDKD" else filter_nv,
        'Chỉ Tiêu KPI': team_tgt,
        'Thực Hiện Ngày':total_ngay, 'MTD':total_mtd, '% MTD':f"{total_pct}%"}])
    return pd.concat([df_out, total_row], ignore_index=True), team_tgt, title

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
        if ch=='Kênh Off Premise': return km or giatri>0 or ck>=10000
        if ch=='Kênh On Premise': return km
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
        rows.append({'Mã NVBH':sm, 'Tên NVBH':sm_names.get(sm,''),
            'Phát sinh Ngày (OFF)':int(off_ngay.get(sm,0)), 'MTD (OFF)':int(off_mtd.get(sm,0)),
            'Phát sinh Ngày (ON)':int(on_ngay.get(sm,0)), 'MTD (ON)':int(on_mtd.get(sm,0))})
    df_out = pd.DataFrame(rows).sort_values('MTD (OFF)', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out)+1))
    total_row = pd.DataFrame([{'STT':'-', 'Mã NVBH':'TỔNG CỘNG',
        'Tên NVBH':'SS Trương Thanh Tân Total' if filter_nv=="Tất cả ĐDKD" else filter_nv,
        'Phát sinh Ngày (OFF)':int(df_out['Phát sinh Ngày (OFF)'].sum()) if not df_out.empty else 0,
        'MTD (OFF)':int(df_out['MTD (OFF)'].sum()) if not df_out.empty else 0,
        'Phát sinh Ngày (ON)':int(df_out['Phát sinh Ngày (ON)'].sum()) if not df_out.empty else 0,
        'MTD (ON)':int(df_out['MTD (ON)'].sum()) if not df_out.empty else 0}])
    return pd.concat([df_out, total_row], ignore_index=True)

def render_html_table(df):
    html = ['<div style="overflow-x: auto;"><table class="custom-kpi-table">']
    html.append('<thead><tr>')
    for col in df.columns:
        html.append(f'<th>{col}</th>')
    html.append('</tr></thead>')
    
    html.append('<tbody>')
    for _, row in df.iterrows():
        is_total = str(row.get('Mã NVBH', '')).strip() == 'TỔNG CỘNG'
        html.append('<tr>')
        for col in df.columns:
            val = row[col]
            if pd.isna(val): val = ""
            
            if col == '% MTD':
                style_bg = color_pct_bg(val)
                if is_total:
                    html.append(f'<td style="{style_bg} text-align: center; font-weight: bold;">{val}</td>')
                else:
                    html.append(f'<td style="{style_bg} text-align: center;">{val}</td>')
            elif is_total:
                if col == 'Tên NVBH':
                    html.append(f'<td style="background-color: #ffffff; color: #9b2c2c; font-weight: bold; text-align: left; white-space: nowrap;">{val}</td>')
                else:
                    html.append(f'<td style="background-color: #ffffff; color: #9b2c2c; font-weight: bold; text-align: center; white-space: nowrap;">{val}</td>')
            elif col == 'Tên NVBH':
                html.append(f'<td style="color: #1a365d; text-align: left; white-space: nowrap;">{val}</td>')
            else:
                align = 'center' if col in ['STT', 'Mã NVBH', 'Thực Hiện Ngày', 'MTD', 'Phát sinh Ngày (OFF)', 'MTD (OFF)', 'Phát sinh Ngày (ON)', 'MTD (ON)', 'Chỉ Tiêu KPI'] else 'left'
                html.append(f'<td style="text-align: {align}; white-space: nowrap;">{val}</td>')
        html.append('</tr>')
    html.append('</tbody>')
    html.append('</table></div>')
    return "".join(html)

# ====================== GIAO DIỆN ======================
st.markdown(f"""
<div class="main-header">
    <div class="logo">{logo_svg}</div>
    <div class="title-block">
        <h1>SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</h1>
        <h2>TRACKING KPI ĐDKD - TEAM SS Nguyễn Thị Tường Vy</h2>
    </div>
</div>
""", unsafe_allow_html=True)

# Nút Xóa Cache & Reload Data hiện trực tiếp trên màn hình chính
col_reload, col_empty = st.columns([2, 5])
with col_reload:
    if st.button("🔄 Xóa Cache & Reload Dữ Liệu"):
        st.cache_data.clear()
        st.rerun()

with st.spinner("Đang tải dữ liệu..."):
    df, mcp = load_main_data()
    targets = get_targets()
    df_cat = load_cat_data()
    df_brand = load_brand_data()

nv_list = ["Tất cả ĐDKD"] + sorted(df['Tên NVBH'].dropna().unique().tolist())

# Compact filter bar
f1, f2, f3 = st.columns([1, 1, 1.3])
with f1:
    st.markdown('<p class="filter-label">MONTH</p>', unsafe_allow_html=True)
    st.selectbox("", ["Tháng 09/2026"], key="month", label_visibility="collapsed")
with f2:
    st.markdown('<p class="filter-label">NGÀY</p>', unsafe_allow_html=True)
    report_date = st.date_input("", value=date(2026, 9, 17), key="ngay", label_visibility="collapsed")
with f3:
    st.markdown('<p class="filter-label">KPI NAME</p>', unsafe_allow_html=True)
    kpi_map = {
        "1. ASO FOCUS TOTAL NHÃN CHANTÉ": "CHANTE",
        "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN": "OMACHI",
        "3. ASO TEA KÊNH ON PREMISE": "ASO_TEA",
        "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)": "PC_BT",
        "5. ASO ALL KÊNH OFF": "ASO_ALL",
        "6. BÁO CÁO ĐƠN HÀNG COMBO": "COMBO",
    }
    selected_name = st.selectbox("", list(kpi_map.keys()), key="kpi", label_visibility="collapsed")
    selected_kpi = kpi_map[selected_name]

f4, f5 = st.columns([1, 1])
with f4:
    st.markdown('<p class="filter-label">SALE SUP</p>', unsafe_allow_html=True)
    st.selectbox("", ["Trương Thanh Tân Total"], key="sup", label_visibility="collapsed")
with f5:
    st.markdown('<p class="filter-label">ĐDKD (Nhân viên)</p>', unsafe_allow_html=True)
    filter_nv = st.selectbox("", nv_list, key="ddkd", label_visibility="collapsed")

st.markdown("---")

tab_kpi, tab_mcp, tab_cat, tab_brand = st.tabs([
    "📊 BÁO CÁO KPI", "🗺️ MCP VISIT", "📦 TRACKING MBS - CAT", "🏷️ TRACKING MBS - BRAND"
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
        with c1: render_metric_card("🎯 Target", f"{team_tgt:,}")
        with c2: render_metric_card("📈 MTD", f"{total_mtd:,}")
        with c3: render_metric_card("📊 % MTD", pct_team)
        with c4: render_metric_card("🆕 Ngày", f"+{total_ngay}")

        st.markdown(render_html_table(df_r), unsafe_allow_html=True)

        top3 = df_r.iloc[:-1].head(3)
        bottom3 = df_r.iloc[:-1].tail(3)
        top3_text = ", ".join([f"{r['Tên NVBH']} ({r['MTD']})" for _, r in top3.iterrows()])
        bottom3_text = ", ".join([f"{r['Tên NVBH']} ({r['MTD']})" for _, r in bottom3.iterrows()])

        st.markdown(f"""
        <div class="note-box">
            <b>NHẬN XÉT ({title} - {report_date.strftime('%d/%m/%Y')}):</b><br>
            • Tiến độ MTD: <b>{total_mtd}/{team_tgt} ({pct_team})</b>. Phát sinh ngày: <b>+{total_ngay}</b>.<br>
            • <b>Top 3:</b> {top3_text}<br>
            • <b>Bottom 3:</b> {bottom3_text}
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
        with c1: render_metric_card("MTD OFF", f"{total_off}")
        with c2: render_metric_card("MTD ON", f"{total_on}")
        with c3: render_metric_card("Ngày OFF", f"+{ngay_off}")
        with c4: render_metric_card("Ngày ON", f"+{ngay_on}")

        st.markdown(render_html_table(df_combo), unsafe_allow_html=True)

# ----- TAB MCP -----
with tab_mcp:
    st.subheader("🗺️ MCP VISIT & MAPPING DOANH SỐ BÁN HÀNG")
    if mcp.empty:
        st.warning("Chưa có dữ liệu MCP")
    else:
        col_nv = find_col(mcp, ['SM name','SM Name','Tên NVBH','Nhân viên','Sale name','Position name'])
        col_ma = find_col(mcp, ['Outlet_code','Outlet Code','Mã CH','Mã khách hàng','Poscode'])
        col_ten = find_col(mcp, ['Outlet_name','Outlet Name','Tên CH','Tên khách hàng'])
        col_thu = find_col(mcp, ['Thứ','Frequency','Tần suất'])

        c1,c2 = st.columns(2)
        with c1:
            st.markdown('<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD)</p>', unsafe_allow_html=True)
            nv_opts = ["Tất cả ĐDKD"] + (sorted(mcp[col_nv].dropna().astype(str).unique().tolist()) if col_nv else [])
            f_nv = st.selectbox("", nv_opts, key="mcp_nv", label_visibility="collapsed")
        with c2:
            st.markdown('<p class="filter-label">📅 Lọc Theo Thứ</p>', unsafe_allow_html=True)
            f_thu = st.selectbox("", ["Tất cả các thứ","2","3","4","5","6","7","25","36","47"], key="mcp_thu", label_visibility="collapsed")

        c3,c4 = st.columns(2)
        with c3:
            st.markdown('<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>', unsafe_allow_html=True)
            f_ma = st.text_input("", key="mcp_ma", label_visibility="collapsed")
        with c4:
            st.markdown('<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>', unsafe_allow_html=True)
            f_ten = st.text_input("", key="mcp_ten", label_visibility="collapsed")

        df_f = mcp.copy()
        if f_nv != "Tất cả ĐDKD" and col_nv: df_f = df_f[df_f[col_nv].astype(str)==f_nv]
        if f_ma and col_ma: df_f = df_f[df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)]
        if f_ten and col_ten: df_f = df_f[df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)]
        if f_thu != "Tất cả các thứ" and col_thu:
            thu_s = df_f[col_thu].astype(str).str.strip()
            if f_thu in ["2","3","4","5","6","7"]: df_f = df_f[thu_s==f_thu]
            elif f_thu=="25": df_f = df_f[thu_s.isin(["2","5","25"])]
            elif f_thu=="36": df_f = df_f[thu_s.isin(["3","6","36"])]
            elif f_thu=="47": df_f = df_f[thu_s.isin(["4","7","47"])]

        for col in df_f.columns:
            if any(x in col.lower().replace(" ","") for x in ["3msales","3msales","doanh số","doanhso","sales"]):
                df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(format_number_vn)

        st.dataframe(df_f, use_container_width=True, height=450, hide_index=True)
        st.caption(f"Hiển thị: {len(df_f):,} / {len(mcp):,} cửa hàng")

# ----- TAB CAT -----
with tab_cat:
    st.subheader("🎯 TRACKING MBS - THEO NGÀNH HÀNG (CATEGORY)")
    if df_cat.empty:
        st.error("❌ Không tìm thấy Data_Cat.xlsx")
    else:
        col_nv = find_col(df_cat, ['SM Name','SM name','Tên NVBH','Nhân viên'])
        col_ma = find_col(df_cat, ['Outlet Code','Outlet_code','Mã CH','Mã khách hàng'])
        col_ten = find_col(df_cat, ['Outlet Name','Outlet_name','Tên CH','Tên khách hàng'])

        c1,c2 = st.columns(2)
        with c1:
            st.markdown('<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD)</p>', unsafe_allow_html=True)
            nv_opts = ["Tất cả ĐDKD"] + (sorted(df_cat[col_nv].dropna().astype(str).unique().tolist()) if col_nv else [])
            f_nv = st.selectbox("", nv_opts, key="cat_nv", label_visibility="collapsed")
        with c2:
            st.markdown('<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>', unsafe_allow_html=True)
            f_ma = st.text_input("", key="cat_ma", label_visibility="collapsed")

        st.markdown('<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>', unsafe_allow_html=True)
        f_ten = st.text_input("", key="cat_ten", label_visibility="collapsed")

        df_f = df_cat.copy()
        if f_nv != "Tất cả ĐDKD" and col_nv: df_f = df_f[df_f[col_nv].astype(str)==f_nv]
        if f_ma and col_ma: df_f = df_f[df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)]
        if f_ten and col_ten: df_f = df_f[df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)]

        for col in df_f.columns:
            if "doanh số" in col.lower() or "doanhso" in col.lower().replace(" ",""):
                df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(format_number_vn)

        st.dataframe(df_f, use_container_width=True, height=450, hide_index=True)
        st.caption(f"Hiển thị: {len(df_f):,} / {len(df_cat):,} dòng")

# ----- TAB BRAND -----
with tab_brand:
    st.subheader("🏷️ TRACKING MBS - THEO THƯƠNG HIỆU (BRAND)")
    if df_brand.empty:
        st.error("❌ Không tìm thấy Data_Brand.xlsx")
    else:
        col_nv = find_col(df_brand, ['SM Name','SM name','Tên NVBH','Nhân viên'])
        col_ma = find_col(df_brand, ['Outlet Code','Outlet_code','Mã CH','Mã khách hàng'])
        col_ten = find_col(df_brand, ['Outlet Name','Outlet_name','Tên CH','Tên khách hàng'])

        c1,c2 = st.columns(2)
        with c1:
            st.markdown('<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD)</p>', unsafe_allow_html=True)
            nv_opts = ["Tất cả ĐDKD"] + (sorted(df_brand[col_nv].dropna().astype(str).unique().tolist()) if col_nv else [])
            f_nv = st.selectbox("", nv_opts, key="brand_nv", label_visibility="collapsed")
        with c2:
            st.markdown('<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>', unsafe_allow_html=True)
            f_ma = st.text_input("", key="brand_ma", label_visibility="collapsed")

        st.markdown('<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>', unsafe_allow_html=True)
        f_ten = st.text_input("", key="brand_ten", label_visibility="collapsed")

        df_f = df_brand.copy()
        if f_nv != "Tất cả ĐDKD" and col_nv: df_f = df_f[df_f[col_nv].astype(str)==f_nv]
        if f_ma and col_ma: df_f = df_f[df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)]
        if f_ten and col_ten: df_f = df_f[df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)]

        for col in df_f.columns:
            if "doanh số" in col.lower() or "doanhso" in col.lower().replace(" ",""):
                df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(format_number_vn)

        st.dataframe(df_f, use_container_width=True, height=450, hide_index=True)
        st.caption(f"Hiển thị: {len(df_f):,} / {len(df_brand):,} dòng")
