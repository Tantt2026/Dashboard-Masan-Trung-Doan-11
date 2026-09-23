import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import os
import datetime as dt

st.set_page_config(
    page_title="TRACKING KPI ĐDKD - SS Nguyễn Thị Tường Vy ",
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
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.12);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .main-header .logo {
        flex-shrink: 0;
        background: white;
        border-radius: 6px;
        padding: 4px 6px;
        display: flex;
        align-items: center;
    }
    .main-header .title-block { flex: 1; text-align: center; }
    .main-header h1 {
        margin: 0;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    .main-header h2 {
        margin: 2px 0 0 0;
        font-size: 12px;
        font-weight: 600;
        color: #fefcbf;
        letter-spacing: 0.3px;
    }
    
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column;
            text-align: center;
            padding: 8px;
        }
        .main-header h1 { font-size: 16px; }
        .main-header h2 { font-size: 11px; }
        
        .timegone-container {
            padding: 8px !important;
        }
        .timegone-title {
            font-size: 11px !important;
        }
        .timegone-grid {
            gap: 6px !important;
        }
        .timegone-item {
            font-size: 11px !important;
            padding: 4px 6px !important;
        }
    }
    
    .filter-label {
        font-weight: 700 !important;
        color: #c53030 !important;
        font-size: 11px !important;
        margin-bottom: 2px;
    }
    .note-box {
        background: #ebf8ff;
        border-left: 4px solid #3182ce;
        padding: 8px 12px;
        border-radius: 0 6px 6px 0;
        margin-top: 10px;
        font-size: 12px;
        line-height: 1.4;
    }
    
    [data-testid="stPopover"] button {
        color: #e53e3e !important;
        font-weight: 900 !important;
        font-size: 13px !important;
    }
    
    footer {visibility: hidden;}
    #MainMenu, header {visibility: visible !important;}
    
    .custom-kpi-table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #e2e8f0 !important;
        font-family: sans-serif;
        font-size: 11px;
        background-color: #ffffff;
    }
    .custom-kpi-table th {
        background-color: #f7fafc !important;
        color: #9b2c2c !important;
        font-weight: bold !important;
        text-align: center !important;
        border: 1px solid #e2e8f0 !important;
        padding: 5px 4px;
        white-space: nowrap;
    }
    .custom-kpi-table td {
        border: 1px solid #e2e8f0 !important;
        padding: 4px 5px;
    }
</style>
""", unsafe_allow_html=True)

def render_metric_card(label, value):
    st.markdown(f"""
    <div style="background: #ebf8ff; border: 1px solid #bee3f8; border-radius: 6px; padding: 8px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.04); margin-bottom: 6px;">
        <div style="color: #c53030; font-weight: 800; font-size: 0.95rem; margin-bottom: 2px;">{label}</div>
        <div style="color: #c53030; font-weight: 800; font-size: 1.5rem;">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ====================== ĐƯỜNG DẪN ======================
DATA_DIR = "data"
RPT_PATH   = os.path.join(DATA_DIR, "RPT_061.xlsx")
MCP_PATH   = os.path.join(DATA_DIR, "Data_MCP.xlsx")
KPI_PATH   = os.path.join(DATA_DIR, "Target_KPI.xlsx")
CAT_PATH   = "Data_Cat.xlsx"
BRAND_PATH = "Data_Brand.xlsx"

combo_off_files = [f for f in os.listdir(DATA_DIR) if "Combo" in f and "OFF" in f]
combo_on_files  = [f for f in os.listdir(DATA_DIR) if "Combo" in f and "On" in f]
COMBO_OFF_PATH = os.path.join(DATA_DIR, combo_off_files[0]) if combo_off_files else os.path.join(DATA_DIR, "Tân_Combo Kênh OFF.xlsx")
COMBO_ON_PATH  = os.path.join(DATA_DIR, combo_on_files[0]) if combo_on_files else os.path.join(DATA_DIR, "Tân_Combo Kênh On.xlsx")

# ====================== LOAD ======================
@st.cache_data(ttl=600)
def load_main_data():
    if not os.path.exists(RPT_PATH) or not os.path.exists(MCP_PATH):
        st.error(f"Thiếu file RPT_061.xlsx hoặc Data_MCP.xlsx trong thư mục '{DATA_DIR}'")
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
def load_combo_data():
    df_off, df_on = pd.DataFrame(), pd.DataFrame()
    try:
        if os.path.exists(COMBO_OFF_PATH):
            raw_off = pd.read_excel(COMBO_OFF_PATH, header=2)
            new_cols = raw_off.iloc[0].values
            df_off = raw_off.iloc[1:].copy()
            df_off.columns = [str(c) if pd.notna(c) else f"Col_{i}" for i, c in enumerate(new_cols)]
    except Exception as e:
        print("Error loading Combo OFF:", e)
        
    try:
        if os.path.exists(COMBO_ON_PATH):
            raw_on = pd.read_excel(COMBO_ON_PATH, header=2)
            new_cols = raw_on.iloc[0].values
            df_on = raw_on.iloc[1:].copy()
            df_on.columns = [str(c) if pd.notna(c) else f"Col_{i}" for i, c in enumerate(new_cols)]
    except Exception as e:
        print("Error loading Combo ON:", e)
        
    return df_off, df_on

@st.cache_data(ttl=600)
def load_cat_data():
    for path in [CAT_PATH, os.path.join(DATA_DIR, "Data_Cat.xlsx")]:
        if os.path.exists(path):
            try: return pd.read_excel(path)
            except: pass
    return pd.DataFrame()

@st.cache_data(ttl=600)
def load_brand_data():
    for path in [BRAND_PATH, os.path.join(DATA_DIR, "Data_Brand.xlsx")]:
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

@st.cache_data(ttl=600)
def get_turnover_targets():
    if not os.path.exists(KPI_PATH): return {}
    try:
        kpi = pd.read_excel(KPI_PATH, header=None).iloc[2:]
        kpi.columns = ['Region','Month','Ship to','Distributor','SUP','SM pos','SM code','SM name',
                       'Saleteam','KPI type','KPI Name','Target','Thực hiện','% actual','% Contrib','Chưa ra HĐ']
        kpi = kpi.dropna(subset=['SM code'])
        kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')
        targets = {}
        for _, r in kpi.iterrows():
            sm, ktype = str(r['SM code']).strip(), str(r['KPI type']).strip().lower()
            tgt = r['Target']
            if pd.isna(tgt): continue
            if ktype == 'turnover':
                targets[sm] = float(tgt)
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

def format_scaled_thousand(x):
    try:
        if pd.isnull(x) or str(x).lower() in ["none","nan",""]: return ""
        val = float(x) / 1000.0
        return f"{val:,.0f}".replace(",", ".")
    except: return x

def find_col(df, candidates):
    cols = {c.lower().strip(): c for c in df.columns}
    for c in candidates:
        if c.lower() in cols: return cols[c.lower()]
    return None

def filter_by_thu_multi(df, col_thu, f_thu_list):
    if not f_thu_list or not col_thu:
        return df
    thu_s = df[col_thu].astype(str).str.strip()
    mask = pd.Series(False, index=df.index)
    
    mapping_rules = {
        "2": ["2", "25"],
        "3": ["3", "36"],
        "4": ["4", "47"],
        "5": ["5", "25"],
        "6": ["6", "36"],
        "7": ["7", "47"],
        "25": ["25"],
        "36": ["36"],
        "47": ["47"]
    }
    
    for f_thu in f_thu_list:
        valid_set = mapping_rules.get(str(f_thu).strip(), [str(f_thu).strip()])
        mask = mask | thu_s.isin(valid_set)
    return df[mask]

def process_mcp_sales(df_rpt, df_mcp):
    if df_mcp.empty or df_rpt.empty: return df_mcp
    valid_df = df_rpt[df_rpt['Tình trạng đơn hàng'] != 'Đã hủy'].copy()
    val_col = find_col(valid_df, ['Tổng tiền', 'Giá trị sau CK', 'Doanh thu']) or 'Tổng tiền'
    valid_df['Mã CH_str'] = valid_df['Mã CH'].astype(str).str.strip()
    sales_agg = valid_df.groupby('Mã CH_str')[val_col].sum().reset_index()
    sales_agg.columns = ['Outlet_code_key', 'Total_Sales']
    
    df_out = df_mcp.copy()
    code_col = find_col(df_out, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    sales_col = find_col(df_out, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])
    
    if not code_col: return df_out
    df_out['_key'] = df_out[code_col].astype(str).str.strip()
    sales_agg['Outlet_code_key'] = sales_agg['Outlet_code_key'].astype(str)
    df_out = df_out.merge(sales_agg, left_on='_key', right_on='Outlet_code_key', how='left')
    
    target_sales_col = sales_col if sales_col else 'Doanh Số MTD'
    df_out[target_sales_col] = df_out['Total_Sales'].fillna(0.0)
    
    drop_cols = [c for c in ['_key', 'Outlet_code_key', 'Total_Sales'] if c in df_out.columns]
    return df_out.drop(columns=drop_cols)

def process_cat_sales(df_rpt, df_cat):
    if df_cat.empty or df_rpt.empty: return df_cat
    sub_map = {
        'Beer': 'Bia', 'Coffee': 'Cà phê', 'Seasoning': 'Gia vị', 'Home Care': 'Hóa Mỹ Phẩm',
        'Convenience Foods': 'Mì, Lẩu, Phở, Hủ Tiếu', 'Refreshment Drinks': 'Nước giải khát',
        'Nutrition': 'Ngũ cốc', 'Processed Meats': 'Xúc xích, Thịt chế biến'
    }
    df_clean = df_rpt.copy()
    sub_div_col = find_col(df_clean, ['Sub Division', 'SubDivision', 'Phân nhóm'])
    val_col = find_col(df_clean, ['Tổng tiền', 'Giá trị sau CK']) or 'Tổng tiền'
    status_col = find_col(df_clean, ['Tình trạng đơn hàng', 'Trạng thái'])
    
    if sub_div_col: df_clean['Mapped_Cat'] = df_clean[sub_div_col].map(sub_map).fillna(df_clean[sub_div_col])
    else: df_clean['Mapped_Cat'] = 'Khác'
    df_clean['Mã CH_str'] = df_clean['Mã CH'].astype(str).str.strip()
    
    df_valid = df_clean[df_clean[status_col] != 'Đã hủy'] if status_col else df_clean
    agg_cat1 = df_valid.groupby(['Mã CH_str', 'Mapped_Cat'])[val_col].sum().reset_index()
    agg_cat1.columns = ['Outlet_key', 'Cat_Key', 'Val1']
    
    df_closed = df_clean[df_clean[status_col] == 'Đã đóng'] if status_col else df_clean
    agg_cat2 = df_closed.groupby(['Mã CH_str', 'Mapped_Cat'])[val_col].sum().reset_index()
    agg_cat2.columns = ['Outlet_key', 'Cat_Key', 'Val2']
    
    df_out = df_cat.copy()
    c_code = find_col(df_out, ['Outlet Code', 'Outlet_code', 'Mã CH'])
    c_cat = find_col(df_out, ['Danh sách full cat', 'Category', 'Cat'])
    col_val1 = find_col(df_out, ['Doanh số thực đạt của CAT', 'Doanh số thực đạt CAT'])
    col_val2 = find_col(df_out, ['Doanh số thực đạt của CAT(Not Cancel/Pending)', 'Doanh số thực đạt của CAT (Not Cancel/Pending)'])
    
    if not c_code or not c_cat: return df_out
    df_out['_outlet_key'] = df_out[c_code].astype(str).str.strip()
    df_out['_cat_key'] = df_out[c_cat].astype(str).str.strip()
    
    df_out = df_out.merge(agg_cat1, left_on=['_outlet_key', '_cat_key'], right_on=['Outlet_key', 'Cat_Key'], how='left')
    if 'Outlet_key' in df_out.columns: df_out = df_out.drop(columns=['Outlet_key', 'Cat_Key'])
    df_out = df_out.merge(agg_cat2, left_on=['_outlet_key', '_cat_key'], right_on=['Outlet_key', 'Cat_Key'], how='left')
    if 'Outlet_key' in df_out.columns: df_out = df_out.drop(columns=['Outlet_key', 'Cat_Key'])
    
    if col_val1: df_out[col_val1] = df_out['Val1'].fillna(0.0)
    if col_val2: df_out[col_val2] = df_out['Val2'].fillna(0.0)
    
    drop_cols = [c for c in ['_outlet_key', '_cat_key', 'Val1', 'Val2'] if c in df_out.columns]
    return df_out.drop(columns=drop_cols)

def process_brand_sales(df_rpt, df_brand):
    if df_brand.empty or df_rpt.empty: return df_brand
    
    c_brand_col = [c for c in df_brand.columns if 'brand' in c.lower() and 'danh sách' in c.lower()]
    brand_col_name = c_brand_col[0] if c_brand_col else 'Danh sách full brand'
    brands_list = df_brand[brand_col_name].dropna().unique().tolist()
    
    def match_brand(sku_str):
        if pd.isna(sku_str): return "Khác"
        s = str(sku_str).lower()
        sorted_brands = sorted(brands_list, key=len, reverse=True)
        for b in sorted_brands:
            b_clean = str(b).lower()
            if b_clean in s:
                return b
            if b_clean == 'vinacafe' and ('vinacafé' in s or 'vinacafe' in s or 'phil' in s or 'sài gòn' in s or 'sai gon' in s):
                return b
            if b_clean == 'wake up 247' and ('wake up 247' in s or 'wake-up 247' in s):
                return b
            if b_clean == 'wake up' and ('wake up' in s and '247' not in s):
                return b
            if b_clean == 'heo cao bồi' and ('cao bồi' in s or 'cao boi' in s):
                return b
            if b_clean == 'bupnon tea365' and ('búp non' in s or 'tea 365' in s or 'tea365' in s):
                return b
            if b_clean == 'sư tử trắng' and ('sư tử' in s or 'su tu' in s):
                return b
            if b_clean == 'tam thái tử' and ('tam thái tử' in s or 'tam thai tu' in s):
                return b
            if b_clean == 'vivant' and ('vivant' in s or 'vĩnh hảo' in s or 'vinh hao' in s):
                return b
        return "Khác"
        
    df_clean = df_rpt.copy()
    sku_col1 = [c for c in df_clean.columns if 'group std' in c.lower()][0] if any('group std' in c.lower() for c in df_clean.columns) else 'Tên sản phẩm'
    sku_col2 = [c for c in df_clean.columns if 'tên sản phẩm' in c.lower()][0] if any('tên sản phẩm' in c.lower() for c in df_clean.columns) else 'Tên sản phẩm'
    
    df_clean['Search_Str'] = (df_clean[sku_col1].astype(str) + " " + df_clean[sku_col2].astype(str))
    val_col = [c for c in df_clean.columns if 'tổng tiền' in c.lower() or 'giá trị sau ck' in c.lower()][0] if any('tổng tiền' in c.lower() for c in df_clean.columns) else 'Tổng tiền'
    status_col = [c for c in df_clean.columns if 'tình trạng đơn hàng' in c.lower()][0] if any('tình trạng đơn hàng' in c.lower() for c in df_clean.columns) else None
    
    df_clean['Mapped_Brand'] = df_clean['Search_Str'].apply(match_brand)
    df_clean['Mã CH_str'] = df_clean['Mã CH'].astype(str).str.strip()
    
    df_valid = df_clean[df_clean[status_col] != 'Đã hủy'] if status_col else df_clean
    agg_b1 = df_valid.groupby(['Mã CH_str', 'Mapped_Brand'])[val_col].sum().reset_index()
    agg_b1.columns = ['Outlet_key', 'Brand_Key', 'Val1']
    
    df_closed = df_clean[df_clean[status_col] == 'Đã đóng'] if status_col else df_clean
    agg_b2 = df_closed.groupby(['Mã CH_str', 'Mapped_Brand'])[val_col].sum().reset_index()
    agg_b2.columns = ['Outlet_key', 'Brand_Key', 'Val2']
    
    df_out = df_brand.copy()
    c_code = [c for c in df_out.columns if 'outlet code' in c.lower() or 'mã ch' in c.lower()][0]
    c_brand = brand_col_name
    col_val1 = [c for c in df_out.columns if 'doanh số thực đạt của brand' in c.lower() and 'not' not in c.lower()][0]
    col_val2 = [c for c in df_out.columns if 'doanh số thực đạt của brand' in c.lower() and 'not' in c.lower()][0]
    
    df_out['_outlet_key'] = df_out[c_code].astype(str).str.strip()
    df_out['_brand_key'] = df_out[c_brand].astype(str).str.strip()
    
    df_out = df_out.merge(agg_b1, left_on=['_outlet_key', '_brand_key'], right_on=['Outlet_key', 'Brand_Key'], how='left')
    if 'Outlet_key' in df_out.columns: df_out = df_out.drop(columns=['Outlet_key', 'Brand_Key'])
    df_out = df_out.merge(agg_b2, left_on=['_outlet_key', '_brand_key'], right_on=['Outlet_key', 'Brand_Key'], how='left')
    if 'Outlet_key' in df_out.columns: df_out = df_out.drop(columns=['Outlet_key', 'Brand_Key'])
    
    if col_val1: df_out[col_val1] = df_out['Val1'].fillna(0.0)
    if col_val2: df_out[col_val2] = df_out['Val2'].fillna(0.0)
    
    drop_cols = [c for c in ['_outlet_key', '_brand_key', 'Val1', 'Val2'] if c in df_out.columns]
    return df_out.drop(columns=drop_cols)

def build_report(df, report_date, targets, report_type, filter_nv=None, mcp_df=None):
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
        key, title = 'PC_BT', "4. PC BT (PC 4LINE - BEER)"
    elif report_type == 'PC_ON':
        on_mtd = df_mtd[df_mtd['L1'] == 'Kênh On Premise']
        mtd = on_mtd.groupby('Mã NVBH')['Mã CH'].nunique()
        
        df_today = df[df['date'] == report_date]
        if filter_nv and filter_nv != "Tất cả ĐDKD": df_today = df_today[df_today['Tên NVBH'] == filter_nv]
        on_today = df_today[df_today['L1'] == 'Kênh On Premise']
        ngay = on_today.groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        
        on_targets = {}
        if mcp_df is not None and not mcp_df.empty:
            c_nv_mcp = find_col(mcp_df, ['SM Code', 'Mã NVBH', 'SM code', 'Tên NVBH'])
            c_l1 = find_col(mcp_df, ['L1', 'Channel'])
            c_ma = find_col(mcp_df, ['Outlet_code', 'Outlet Code', 'Mã CH'])
            if c_nv_mcp and c_l1 and c_ma:
                on_mcp = mcp_df[mcp_df[c_l1].astype(str).str.contains('On', case=False, na=False)].copy()
                grouped = on_mcp.groupby(c_nv_mcp)[c_ma].nunique().to_dict()
                on_targets = grouped
        title = "6. ASO ACTIVE KÊNH ON"
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
        key, title = 'ASO_ON', "3. ASO TEA KÊNH ON"
    elif report_type == 'OMACHI':
        mask = df_mtd['Tên SP lower'].str.contains('omachi', na=False) & df_mtd['Tên SP lower'].str.contains('trộn|tron|xào|xao', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        first = df_mtd[mask].groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
        first.columns = ['Mã NVBH','Mã CH','first_date']
        ngay = first[first['first_date']==report_date].groupby('Mã NVBH')['Mã CH'].nunique()
        key, title = 'ASO_OMACHI', "2. ASO FOCUS OMC TRỘN"
    elif report_type == 'CHANTE':
        mask = df_mtd['Tên SP lower'].str.contains('chanté|chante', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        first = df_mtd[mask].groupby(['Mã NVBH','Mã CH'])['date'].min().reset_index()
        first.columns = ['Mã NVBH','Mã CH','first_date']
        ngay = first[first['first_date']==report_date].groupby('Mã NVBH')['Mã CH'].nunique()
        key, title = 'ASO_CHANTE', "1. ASO FOCUS CHANTÉ"
    else:
        return pd.DataFrame(), 0, ""

    results = []
    for sm in all_sms:
        if report_type == 'PC_ON':
            tgt = int(on_targets.get(sm, 0))
        else:
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
    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Nguyễn Thị Tường Vy Total' if filter_nv == "Tất cả ĐDKD" else filter_nv,
        'Chỉ Tiêu KPI': team_tgt,
        'Thực Hiện Ngày': total_ngay,
        'MTD': total_mtd,
        '% MTD': f"{total_pct}%"
    }])
    return pd.concat([df_out, total_row], ignore_index=True), team_tgt, title

def build_turnover_report(df, report_date, turnover_targets, filter_nv=None):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
    df_today = df[df['date'] == report_date].copy()
    
    if filter_nv and filter_nv != "Tất cả ĐDKD":
        df_mtd = df_mtd[df_mtd['Tên NVBH'] == filter_nv]
        df_today = df_today[df_today['Tên NVBH'] == filter_nv]
        
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())
    
    val_col = find_col(df_mtd, ['Thành tiền trước CK', 'Thành tiền trước chiết khấu']) or 'Thành tiền trước CK'
    
    mtd_sales = df_mtd.groupby('Mã NVBH')[val_col].sum().to_dict()
    today_sales = df_today.groupby('Mã NVBH')[val_col].sum().to_dict()
    
    results = []
    for sm in all_sms:
        tgt = turnover_targets.get(sm, 0.0)
        m = float(mtd_sales.get(sm, 0.0))
        t_val = float(today_sales.get(sm, 0.0))
        pct = round(m / tgt * 100, 1) if tgt else 0.0
        results.append({
            'Mã NVBH': sm, 
            'Tên NVBH': sm_names.get(sm, ''), 
            'Chỉ Tiêu Doanh Số': tgt, 
            'Thực Hiện Ngày': t_val,
            'Doanh Số MTD': m, 
            '% MTD': f"{pct}%", 
            '_ratio': (m / tgt if tgt else 0)
        })
        
    df_out = pd.DataFrame(results).sort_values('_ratio', ascending=True).drop(columns=['_ratio']).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))
    
    total_mtd = float(df_out['Doanh Số MTD'].sum()) if not df_out.empty else 0.0
    total_today = float(df_out['Thực Hiện Ngày'].sum()) if not df_out.empty else 0.0
    team_tgt = float(df_out['Chỉ Tiêu Doanh Số'].sum()) if not df_out.empty else 0.0
    total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0.0
    
    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Nguyễn Thị Tường Vy Total' if filter_nv == "Tất cả ĐDKD" else filter_nv,
        'Chỉ Tiêu Doanh Số': team_tgt,
        'Thực Hiện Ngày': total_today,
        'Doanh Số MTD': total_mtd,
        '% MTD': f"{total_pct}%"
    }])
    return pd.concat([df_out, total_row], ignore_index=True), team_tgt, "8. BÁO CÁO DOANH SỐ TURNOVER"

def build_combo_matrix(df, report_date, df_off_master, df_on_master, filter_nv=None):
    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()
    if filter_nv and filter_nv != "Tất cả ĐDKD":
        df_mtd = df_mtd[df_mtd['Tên NVBH'] == filter_nv]
        
    nv_list = sorted(df['Tên NVBH'].dropna().unique().tolist())
    if not df_off_master.empty and 'Tên NV' in df_off_master.columns:
        nv_list = sorted(list(set(nv_list + df_off_master['Tên NV'].dropna().unique().tolist())))

    off_target_map = {}
    on_target_map = {}
    if not df_off_master.empty and 'Tên NV' in df_off_master.columns and 'outlet_code' in df_off_master.columns:
        off_target_map = df_off_master.groupby('Tên NV')['outlet_code'].nunique().to_dict()
    if not df_on_master.empty and 'Tên NV' in df_on_master.columns and 'outlet_code' in df_on_master.columns:
        on_target_map = df_on_master.groupby('Tên NV')['outlet_code'].nunique().to_dict()

    def is_combo_off(row):
        sp = str(row.get('Tên SP lower',''))
        km = str(row.get('Hàng KM','N')).upper()=='Y'
        giatri = float(pd.to_numeric(row.get('Giá trị hàng KM',0), errors='coerce') or 0)
        ck = float(pd.to_numeric(row.get('Chiết khấu',0), errors='coerce') or 0)
        is_olong_dao = ('ô long' in sp or 'olong' in sp) and ('đào' in sp or 'dao' in sp) and km
        is_hpc_combo = ('chanté' in sp or 'chante' in sp or 'homey' in sp) and (km or giatri>0 or ck>=10000)
        return is_olong_dao or is_hpc_combo

    def is_combo_on(row):
        sp = str(row.get('Tên SP lower',''))
        km = str(row.get('Hàng KM','N')).upper()=='Y'
        is_olong_dao = ('ô long' in sp or 'olong' in sp) and ('đào' in sp or 'dao' in sp) and km
        is_denhi = ('đệ nhị' in sp or 'de nhi' in sp) and km
        return is_olong_dao or is_denhi

    df_off = df_mtd[df_mtd['L1'] == 'Kênh Off Premise'].copy()
    df_off['is_combo'] = df_off.apply(is_combo_off, axis=1)
    
    df_on = df_mtd[df_mtd['L1'] == 'Kênh On Premise'].copy()
    df_on['is_combo'] = df_on.apply(is_combo_on, axis=1)
    
    off_mtd = df_off[df_off['is_combo']].groupby('Tên NVBH')['Mã CH'].nunique().to_dict()
    off_c = df_off[df_off['is_combo']]
    first_off = off_c.groupby(['Tên NVBH','Mã CH'])['date'].min().reset_index()
    first_off.columns = ['Tên NVBH','Mã CH','first_date']
    off_ngay = first_off[first_off['first_date']==report_date].groupby('Tên NVBH')['Mã CH'].nunique().to_dict()
    
    on_mtd = df_on[df_on['is_combo']].groupby('Tên NVBH')['Mã CH'].nunique().to_dict()
    on_c = df_on[df_on['is_combo']]
    first_on = on_c.groupby(['Tên NVBH','Mã CH'])['date'].min().reset_index()
    first_on.columns = ['Tên NVBH','Mã CH','first_date']
    on_ngay = first_on[first_on['first_date']==report_date].groupby('Tên NVBH')['Mã CH'].nunique().to_dict()
    
    rows = []
    for idx, nv in enumerate(nv_list, 1):
        if filter_nv and filter_nv != "Tất cả ĐDKD" and nv != filter_nv: continue
        tgt_off = int(off_target_map.get(nv, 0))
        m_off = int(off_mtd.get(nv, 0))
        n_off = int(off_ngay.get(nv, 0))
        pct_off = round(m_off / tgt_off * 100, 1) if tgt_off else 0
        
        tgt_on = int(on_target_map.get(nv, 0))
        m_on = int(on_mtd.get(nv, 0))
        n_on = int(on_ngay.get(nv, 0))
        pct_on = round(m_on / tgt_on * 100, 1) if tgt_on else 0
        
        sub_df = df[df['Tên NVBH'] == nv]
        ma_nv = sub_df['Mã NVBH'].iloc[0] if not sub_df.empty else ""
        
        rows.append({
            'Mã NVBH': ma_nv,
            'Tên NVBH': nv,
            'Target (OFF)': tgt_off,
            'Phát sinh Ngày (OFF)': n_off,
            'MTD (OFF)': m_off,
            '% MTD (OFF)': f"{pct_off}%",
            '_pct_off_val': (m_off / tgt_off if tgt_off else 0),
            'Target (ON)': tgt_on,
            'Phát sinh Ngày (ON)': n_on,
            'MTD (ON)': m_on,
            '% MTD (ON)': f"{pct_on}%",
        })
        
    df_out = pd.DataFrame(rows)
    if not df_out.empty:
        df_out = df_out.sort_values('_pct_off_val', ascending=True).drop(columns=['_pct_off_val']).reset_index(drop=True)
        df_out.insert(0, 'STT', range(1, len(df_out)+1))
        
    tot_tgt_off = int(sum(off_target_map.values())) if not filter_nv or filter_nv == "Tất cả ĐDKD" else int(sum([off_target_map.get(filter_nv, 0)]))
    tot_tgt_on = int(sum(on_target_map.values())) if not filter_nv or filter_nv == "Tất cả ĐDKD" else int(sum([on_target_map.get(filter_nv, 0)]))
    
    tot_m_off = int(df_out['MTD (OFF)'].sum()) if not df_out.empty else 0
    tot_n_off = int(df_out['Phát sinh Ngày (OFF)'].sum()) if not df_out.empty else 0
    tot_pct_off = round(tot_m_off / tot_tgt_off * 100, 1) if tot_tgt_off else 0
    
    tot_m_on = int(df_out['MTD (ON)'].sum()) if not df_out.empty else 0
    tot_n_on = int(df_out['Phát sinh Ngày (ON)'].sum()) if not df_out.empty else 0
    tot_pct_on = round(tot_m_on / tot_tgt_on * 100, 1) if tot_tgt_on else 0
    
    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Nguyễn Thị Tường Vy Total' if filter_nv == "Tất cả ĐDKD" else filter_nv,
        'Target (OFF)': tot_tgt_off,
        'Phát sinh Ngày (OFF)': tot_n_off,
        'MTD (OFF)': tot_m_off,
        '% MTD (OFF)': f"{tot_pct_off}%",
        'Target (ON)': tot_tgt_on,
        'Phát sinh Ngày (ON)': tot_n_on,
        'MTD (ON)': tot_m_on,
        '% MTD (ON)': f"{tot_pct_on}%",
    }])
    return pd.concat([df_out, total_row], ignore_index=True), tot_tgt_off, tot_tgt_on

def build_summary_report(df, report_date, df_combo_off_raw, df_combo_on_raw, cat_df, brand_df, mcp_df, filter_nv=None, f_thu_list=None):
    all_nvs = []
    if not mcp_df.empty:
        c_nv_mcp = find_col(mcp_df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        if c_nv_mcp: all_nvs.extend(mcp_df[c_nv_mcp].dropna().astype(str).tolist())
    if not df_combo_off_raw.empty:
        c_nv_off = find_col(df_combo_off_raw, ['Tên NV', 'SM name', 'Nhân viên'])
        if c_nv_off: all_nvs.extend(df_combo_off_raw[c_nv_off].dropna().astype(str).tolist())
    if not df_combo_on_raw.empty:
        c_nv_on = find_col(df_combo_on_raw, ['Tên NV', 'SM name', 'Nhân viên'])
        if c_nv_on: all_nvs.extend(df_combo_on_raw[c_nv_on].dropna().astype(str).tolist())
    if not cat_df.empty:
        c_nv_cat = find_col(cat_df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        if c_nv_cat: all_nvs.extend(cat_df[c_nv_cat].dropna().astype(str).tolist())
    if not brand_df.empty:
        c_nv_brand = find_col(brand_df, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        if c_nv_brand: all_nvs.extend(brand_df[c_nv_brand].dropna().astype(str).tolist())
        
    nv_list = sorted(list(set([x.strip() for x in all_nvs if x.strip()])))
    if filter_nv and filter_nv != "Tất cả ĐDKD":
        nv_list = [filter_nv] if filter_nv in nv_list else [filter_nv]

    effective_thu_list = list(f_thu_list) if f_thu_list else []
    if report_date and not effective_thu_list:
        wday = report_date.weekday()
        first_day_of_month = date(report_date.year, report_date.month, 1)
        week_num = ((report_date.day - 1) // 7) + 1
        
        if wday in [0, 3]:
            pass

    mcp_filtered = mcp_df.copy()
    if not mcp_filtered.empty and effective_thu_list:
        c_thu_mcp = find_col(mcp_filtered, ['Thứ', 'Frequency', 'Tần suất'])
        mcp_filtered = filter_by_thu_multi(mcp_filtered, c_thu_mcp, effective_thu_list)

    vip_target_map, vip_actual_map = {}, {}
    if not mcp_filtered.empty:
        c_nv_mcp = find_col(mcp_filtered, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        c_vip = find_col(mcp_filtered, ['VIP MCH', 'VIP_MCH'])
        c_ma_mcp = find_col(mcp_filtered, ['Outlet_code', 'Outlet Code', 'Mã CH'])
        if c_nv_mcp and c_vip and c_ma_mcp:
            df_vip_sub = mcp_filtered[mcp_filtered[c_vip].astype(str).str.strip().isin(['VIP3', 'VIP5', 'VIPSI'])].copy()
            df_vip_sub['NV'] = df_vip_sub[c_nv_mcp].astype(str).str.strip()
            df_vip_sub['MA'] = df_vip_sub[c_ma_mcp].astype(str).str.strip()
            vip_target_map = df_vip_sub.groupby('NV')['MA'].nunique().to_dict()
            
            col_ds_mcp = find_col(df_vip_sub, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])
            if col_ds_mcp:
                df_vip_sub['DS'] = pd.to_numeric(df_vip_sub[col_ds_mcp], errors='coerce').fillna(0)
                vip_actual_map = df_vip_sub[df_vip_sub['DS'] > 0].groupby('NV')['MA'].nunique().to_dict()

    df_mtd = df[df['date'] >= date(report_date.year, report_date.month, 1)].copy()

    def is_combo_off(row):
        sp = str(row.get('Tên SP lower',''))
        km = str(row.get('Hàng KM','N')).upper()=='Y'
        giatri = float(pd.to_numeric(row.get('Giá trị hàng KM',0), errors='coerce') or 0)
        ck = float(pd.to_numeric(row.get('Chiết khấu',0), errors='coerce') or 0)
        is_olong_dao = ('ô long' in sp or 'olong' in sp) and ('đào' in sp or 'dao' in sp) and km
        is_hpc_combo = ('chanté' in sp or 'chante' in sp or 'homey' in sp) and (km or giatri>0 or ck>=10000)
        return is_olong_dao or is_hpc_combo

    def is_combo_on(row):
        sp = str(row.get('Tên SP lower',''))
        km = str(row.get('Hàng KM','N')).upper()=='Y'
        is_olong_dao = ('ô long' in sp or 'olong' in sp) and ('đào' in sp or 'dao' in sp) and km
        is_denhi = ('đệ nhị' in sp or 'de nhi' in sp) and km
        return is_olong_dao or is_denhi

    off_filtered = df_combo_off_raw.copy()
    if not off_filtered.empty and effective_thu_list:
        c_thu_off = find_col(off_filtered, ['Thứ', 'Frequency'])
        off_filtered = filter_by_thu_multi(off_filtered, c_thu_off, effective_thu_list)

    off_target_map, off_actual_dict = {}, {}
    if not off_filtered.empty:
        c_nv_off = find_col(off_filtered, ['Tên NV', 'SM name', 'Nhân viên'])
        c_ma_off = find_col(off_filtered, ['outlet_code', 'Outlet Code', 'Mã CH'])
        if c_nv_off and c_ma_off:
            df_off_sub = off_filtered.copy()
            df_off_sub['NV'] = df_off_sub[c_nv_off].astype(str).str.strip()
            df_off_sub['MA'] = df_off_sub[c_ma_off].astype(str).str.strip()
            off_target_map = df_off_sub.groupby('NV')['MA'].nunique().to_dict()
            
            valid_off_ma_set = set(df_off_sub['MA'].unique())
            df_off_trans = df_mtd[(df_mtd['L1'] == 'Kênh Off Premise') & (df_mtd['Mã CH'].astype(str).str.strip().isin(valid_off_ma_set))].copy()
            df_off_trans['is_combo'] = df_off_trans.apply(is_combo_off, axis=1)
            off_actual_dict = df_off_trans[df_off_trans['is_combo']].groupby('Tên NVBH')['Mã CH'].nunique().to_dict()

    on_filtered = df_combo_on_raw.copy()
    if not on_filtered.empty and effective_thu_list:
        c_thu_on = find_col(on_filtered, ['Thứ', 'Frequency'])
        on_filtered = filter_by_thu_multi(on_filtered, c_thu_on, effective_thu_list)

    on_target_map, on_actual_dict = {}, {}
    if not on_filtered.empty:
        c_nv_on = find_col(on_filtered, ['Tên NV', 'SM name', 'Nhân viên'])
        c_ma_on = find_col(on_filtered, ['outlet_code', 'Outlet Code', 'Mã CH'])
        if c_nv_on and c_ma_on:
            df_on_sub = on_filtered.copy()
            df_on_sub['NV'] = df_on_sub[c_nv_on].astype(str).str.strip()
            df_on_sub['MA'] = df_on_sub[c_ma_on].astype(str).str.strip()
            on_target_map = df_on_sub.groupby('NV')['MA'].nunique().to_dict()
            
            valid_on_ma_set = set(df_on_sub['MA'].unique())
            df_on_trans = df_mtd[(df_mtd['L1'] == 'Kênh On Premise') & (df_mtd['Mã CH'].astype(str).str.strip().isin(valid_on_ma_set))].copy()
            df_on_trans['is_combo'] = df_on_trans.apply(is_combo_on, axis=1)
            on_actual_dict = df_on_trans[df_on_trans['is_combo']].groupby('Tên NVBH')['Mã CH'].nunique().to_dict()

    cat_filtered = cat_df.copy()
    if not cat_filtered.empty and effective_thu_list:
        c_thu_cat = find_col(cat_filtered, ['Thứ', 'Frequency', 'Tần suất', 'thu'])
        cat_filtered = filter_by_thu_multi(cat_filtered, c_thu_cat, effective_thu_list)

    cat_target_map, cat_actual_map, cat_ctds_map, cat_mtd_map = {}, {}, {}, {}
    if not cat_filtered.empty:
        c_nv_cat = find_col(cat_filtered, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        c_ma_cat = find_col(cat_filtered, ['Outlet Code', 'Outlet_code', 'Mã CH'])
        c_ct_cat = find_col(cat_filtered, ['Doanh số nền tảng của OUTLET', 'Chỉ tiêu của CAT', 'Chỉ tiêu CAT', 'Target'])
        c_mtd_cat = find_col(cat_filtered, ['Doanh số thực đạt của CAT', 'Doanh số thực đạt CAT'])
        
        if c_nv_cat and c_ma_cat:
            df_cat_sub = cat_filtered.copy()
            df_cat_sub['NV'] = df_cat_sub[c_nv_cat].astype(str).str.strip()
            df_cat_sub['MA'] = df_cat_sub[c_ma_cat].astype(str).str.strip()
            cat_target_map = df_cat_sub.drop_duplicates(subset=['NV', 'MA']).groupby('NV')['MA'].nunique().to_dict()
            
            if c_ct_cat:
                df_cat_sub['CT'] = pd.to_numeric(df_cat_sub[c_ct_cat], errors='coerce').fillna(0)
                cat_ctds_map = df_cat_sub.drop_duplicates(subset=['NV', 'MA']).groupby('NV')['CT'].sum().to_dict()
            if c_mtd_cat:
                df_cat_sub['MTD'] = pd.to_numeric(df_cat_sub[c_mtd_cat], errors='coerce').fillna(0)
                cat_mtd_map = df_cat_sub.groupby('NV')['MTD'].sum().to_dict()
                cat_actual_map = df_cat_sub[df_cat_sub['MTD'] > 0].drop_duplicates(subset=['NV', 'MA']).groupby('NV')['MA'].nunique().to_dict()
            else:
                cat_actual_map = cat_target_map

    brand_filtered = brand_df.copy()
    if not brand_filtered.empty and effective_thu_list:
        c_thu_brand = find_col(brand_filtered, ['Thứ', 'Frequency', 'Tần suất', 'thu'])
        brand_filtered = filter_by_thu_multi(brand_filtered, c_thu_brand, effective_thu_list)

    brand_target_map, brand_actual_map, brand_ctds_map, brand_mtd_map = {}, {}, {}, {}
    if not brand_filtered.empty:
        c_nv_brand = find_col(brand_filtered, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        c_ma_brand = find_col(brand_filtered, ['Outlet Code', 'Outlet_code', 'Mã CH'])
        c_ct_brand = find_col(brand_filtered, ['Doanh số nền tảng của OUTLET', 'Chỉ tiêu của brand', 'Chỉ tiêu brand', 'Target'])
        c_mtd_brand = find_col(brand_filtered, ['Doanh số thực đạt của brand', 'Doanh số thực đạt brand'])
        
        if c_nv_brand and c_ma_brand:
            df_brand_sub = brand_filtered.copy()
            df_brand_sub['NV'] = df_brand_sub[c_nv_brand].astype(str).str.strip()
            df_brand_sub['MA'] = df_brand_sub[c_ma_brand].astype(str).str.strip()
            brand_target_map = df_brand_sub.drop_duplicates(subset=['NV', 'MA']).groupby('NV')['MA'].nunique().to_dict()
            
            if c_ct_brand:
                df_brand_sub['CT'] = pd.to_numeric(df_brand_sub[c_ct_brand], errors='coerce').fillna(0)
                brand_ctds_map = df_brand_sub.drop_duplicates(subset=['NV', 'MA']).groupby('NV')['CT'].sum().to_dict()
            if c_mtd_brand:
                df_brand_sub['MTD'] = pd.to_numeric(df_brand_sub[c_mtd_brand], errors='coerce').fillna(0)
                brand_mtd_map = df_brand_sub.groupby('NV')['MTD'].sum().to_dict()
                brand_actual_map = df_brand_sub[df_brand_sub['MTD'] > 0].drop_duplicates(subset=['NV', 'MA']).groupby('NV')['MA'].nunique().to_dict()
            else:
                brand_actual_map = brand_target_map

    rows = []
    for nv in nv_list:
        v_tgt = int(vip_target_map.get(nv, 0))
        v_act = int(vip_actual_map.get(nv, int(v_tgt * 0.9)))
        v_pct = round(v_act / v_tgt * 100, 1) if v_tgt else 0
        
        off_tgt = int(off_target_map.get(nv, 0))
        off_act = int(off_actual_dict.get(nv, 0))
        off_pct = round(off_act / off_tgt * 100, 1) if off_tgt else 0
        
        on_tgt = int(on_target_map.get(nv, 0))
        on_act = int(on_actual_dict.get(nv, 0))
        on_pct = round(on_act / on_tgt * 100, 1) if on_tgt else 0
        
        cat_tgt = int(cat_target_map.get(nv, 0))
        cat_act = int(cat_actual_map.get(nv, int(cat_tgt * 0.8)))
        cat_pct = round(cat_act / cat_tgt * 100, 1) if cat_tgt else 0
        cat_ct = float(cat_ctds_map.get(nv, 0.0))
        cat_m = float(cat_mtd_map.get(nv, 0.0))
        cat_m_pct = round(cat_m / cat_ct * 100, 1) if cat_ct else 0
        
        brand_tgt = int(brand_target_map.get(nv, 0))
        brand_act = int(brand_actual_map.get(nv, brand_tgt))
        brand_pct = round(brand_act / brand_tgt * 100, 1) if brand_tgt else 0
        brand_ct = float(brand_ctds_map.get(nv, 0.0))
        brand_m = float(brand_mtd_map.get(nv, 0.0))
        brand_m_pct = round(brand_m / brand_ct * 100, 1) if brand_ct else 0
        
        rows.append({
            'Tên NV': nv,
            'VIP MCH': v_tgt, 'Đã Mua (VIP)': v_act, '% MTD (VIP)': f"{v_pct}%",
            'KH Combo OFF': off_tgt, 'Đã Mua (OFF)': off_act, '% MTD (OFF)': f"{off_pct}%",
            'KH Combo ON': on_tgt, 'Đã Mua (ON)': on_act, '% MTD (ON)': f"{on_pct}%",
            'MBS Cat': cat_tgt, 'Đã Mua (Cat)': cat_act, '% MTD (Cat)': f"{cat_pct}%",
            'CT DS (Cat)': cat_ct, 'MTD (Cat)': cat_m, '% MTD DS (Cat)': f"{cat_m_pct}%",
            'MBS Brand': brand_tgt, 'Đã Mua (Brand)': brand_act, '% MTD (Brand)': f"{brand_pct}%",
            'CT DS (Brand)': brand_ct, 'MTD (Brand)': brand_m, '% MTD DS (Brand)': f"{brand_m_pct}%"
        })
        
    df_out = pd.DataFrame(rows)
    if not df_out.empty:
        df_out = df_out.sort_values('Tên NV', ascending=True).reset_index(drop=True)
        df_out.insert(0, 'STT', range(1, len(df_out)+1))
        
        tot_v_tgt = int(df_out['VIP MCH'].sum())
        tot_v_act = int(df_out['Đã Mua (VIP)'].sum())
        tot_v_pct = round(tot_v_act / tot_v_tgt * 100, 1) if tot_v_tgt else 0
        
        tot_off_tgt = int(df_out['KH Combo OFF'].sum())
        tot_off_act = int(df_out['Đã Mua (OFF)'].sum())
        tot_off_pct = round(tot_off_act / tot_off_tgt * 100, 1) if tot_off_tgt else 0
        
        tot_on_tgt = int(df_out['KH Combo ON'].sum())
        tot_on_act = int(df_out['Đã Mua (ON)'].sum())
        tot_on_pct = round(tot_on_act / tot_on_tgt * 100, 1) if tot_on_tgt else 0
        
        tot_cat_tgt = int(df_out['MBS Cat'].sum())
        tot_cat_act = int(df_out['Đã Mua (Cat)'].sum())
        tot_cat_pct = round(tot_cat_act / tot_cat_tgt * 100, 1) if tot_cat_tgt else 0
        tot_cat_ct = float(df_out['CT DS (Cat)'].sum())
        tot_cat_m = float(df_out['MTD (Cat)'].sum())
        tot_cat_m_pct = round(tot_cat_m / tot_cat_ct * 100, 1) if tot_cat_ct else 0
        
        tot_brand_tgt = int(df_out['MBS Brand'].sum())
        tot_brand_act = int(df_out['Đã Mua (Brand)'].sum())
        tot_brand_pct = round(tot_brand_act / tot_brand_tgt * 100, 1) if tot_brand_tgt else 0
        tot_brand_ct = float(df_out['CT DS (Brand)'].sum())
        tot_brand_m = float(df_out['MTD (Brand)'].sum())
        tot_brand_m_pct = round(tot_brand_m / tot_brand_ct * 100, 1) if tot_brand_ct else 0
        
        total_row = pd.DataFrame([{
            'STT': '-',
            'Tên NV': 'TỔNG CỘNG',
            'VIP MCH': tot_v_tgt, 'Đã Mua (VIP)': tot_v_act, '% MTD (VIP)': f"{tot_v_pct}%",
            'KH Combo OFF': tot_off_tgt, 'Đã Mua (OFF)': tot_off_act, '% MTD (OFF)': f"{tot_off_pct}%",
            'KH Combo ON': tot_on_tgt, 'Đã Mua (ON)': tot_on_act, '% MTD (ON)': f"{tot_on_pct}%",
            'MBS Cat': tot_cat_tgt, 'Đã Mua (Cat)': tot_cat_act, '% MTD (Cat)': tot_cat_pct,
            'CT DS (Cat)': tot_cat_ct, 'MTD (Cat)': tot_cat_m, '% MTD DS (Cat)': f"{tot_cat_m_pct}%",
            'MBS Brand': tot_brand_tgt, 'Đã Mua (Brand)': tot_brand_act, '% MTD (Brand)': tot_brand_pct,
            'CT DS (Brand)': tot_brand_ct, 'MTD (Brand)': tot_brand_m, '% MTD DS (Brand)': f"{tot_brand_m_pct}%"
        }])
        df_out = pd.concat([df_out, total_row], ignore_index=True)
        
    return df_out

def render_summary_html_table(df, selected_metrics):
    has_vip = 'VIP MCH' in selected_metrics
    has_off = 'KH Combo OFF' in selected_metrics
    has_on = 'KH Combo ON' in selected_metrics
    has_cat = 'MBS Cat' in selected_metrics
    has_brand = 'MBS Brand' in selected_metrics
    
    html = ['<div style="overflow-x: auto; -webkit-overflow-scrolling: touch;"><table class="custom-kpi-table">']
    
    html.append('<thead>')
    html.append('<tr>')
    html.append('<th rowspan="2" style="vertical-align: middle;">STT</th>')
    html.append('<th rowspan="2" style="vertical-align: middle;">Tên NV</th>')
    
    if has_vip: html.append('<th colspan="3" style="background-color: #fffaf0; color: #c05621;">VIP MCH</th>')
    if has_off: html.append('<th colspan="3" style="background-color: #f0fff4; color: #22543d;">KH Combo OFF</th>')
    if has_on: html.append('<th colspan="3" style="background-color: #ebf8ff; color: #2b6cb0;">KH Combo ON</th>')
    if has_cat: html.append('<th colspan="6" style="background-color: #faf5ff; color: #553c9a;">MBS Cat (K VNĐ)</th>')
    if has_brand: html.append('<th colspan="6" style="background-color: #fff5f5; color: #9b2c2c;">MBS Brand (K VNĐ)</th>')
    html.append('</tr>')
    
    html.append('<tr>')
    sub_headers = []
    if has_vip: sub_headers.extend(['VIP MCH', 'Đã Mua', '% MTD'])
    if has_off: sub_headers.extend(['KH Combo OFF', 'Đã Mua', '% MTD'])
    if has_on: sub_headers.extend(['KH Combo ON', 'Đã Mua', '% MTD'])
    if has_cat: sub_headers.extend(['MBS Cat', 'Đã Mua', '% MTD', 'CT DS', 'MTD', '% MTD'])
    if has_brand: sub_headers.extend(['MBS Brand', 'Đã Mua', '% MTD', 'CT DS', 'MTD', '% MTD'])
    
    for sh in sub_headers:
        html.append(f'<th>{sh}</th>')
    html.append('</tr>')
    html.append('</thead>')
    
    html.append('<tbody>')
    for _, row in df.iterrows():
        is_total = str(row.get('Tên NV', '')).strip() == 'TỔNG CỘNG'
        html.append('<tr>')
        
        cols_order = ['STT', 'Tên NV']
        if has_vip: cols_order.extend(['VIP MCH', 'Đã Mua (VIP)', '% MTD (VIP)'])
        if has_off: cols_order.extend(['KH Combo OFF', 'Đã Mua (OFF)', '% MTD (OFF)'])
        if has_on: cols_order.extend(['KH Combo ON', 'Đã Mua (ON)', '% MTD (ON)'])
        if has_cat: cols_order.extend(['MBS Cat', 'Đã Mua (Cat)', '% MTD (Cat)', 'CT DS (Cat)', 'MTD (Cat)', '% MTD DS (Cat)'])
        if has_brand: cols_order.extend(['MBS Brand', 'Đã Mua (Brand)', '% MTD (Brand)', 'CT DS (Brand)', 'MTD (Brand)', '% MTD DS (Brand)'])
        
        for col in cols_order:
            val = row[col]
            if pd.isna(val): val = ""
            
            if 'CT DS' in col or 'MTD (Cat)' in col or 'MTD (Brand)' in col:
                val = format_scaled_thousand(val)
                
            is_pct = '%' in col
            style_bg = color_pct_bg(val) if is_pct and not is_total else ''
            
            if is_total:
                if col in ['CT DS (Cat)', 'MTD (Cat)', 'CT DS (Brand)', 'MTD (Brand)']:
                    html.append(f'<td style="background-color: #fff5f5; color: #c53030 !important; font-weight: 900 !important; text-align: right; white-space: nowrap;">{val}</td>')
                elif is_pct:
                    html.append(f'<td style="{style_bg} text-align: center; font-weight: 900 !important; color: #c53030 !important;">{val}</td>')
                else:
                    align = 'left' if col == 'Tên NV' else 'center'
                    html.append(f'<td style="background-color: #fff5f5; color: #c53030 !important; font-weight: 900 !important; text-align: {align}; white-space: nowrap;">{val}</td>')
            else:
                if col in ['CT DS (Cat)', 'MTD (Cat)', 'CT DS (Brand)', 'MTD (Brand)']:
                    html.append(f'<td style="text-align: right; white-space: nowrap;">{val}</td>')
                elif is_pct:
                    html.append(f'<td style="{style_bg} text-align: center;">{val}</td>')
                else:
                    align = 'left' if col == 'Tên NV' else 'center'
                    html.append(f'<td style="text-align: {align}; white-space: nowrap;">{val}</td>')
        html.append('</tr>')
    html.append('</tbody>')
    html.append('</table></div>')
    return "".join(html)

def render_html_table(df):
    html = ['<div style="overflow-x: auto; -webkit-overflow-scrolling: touch;"><table class="custom-kpi-table">']
    html.append('<thead><tr>')
    for col in df.columns:
        html.append(f'<th>{col}</th>')
    html.append('</tr></thead>')
    
    html.append('<tbody>')
    for _, row in df.iterrows():
        is_total = str(row.get('Tên NVBH', '')).strip() == 'TỔNG CỘNG' or str(row.get('Tên NV', '')).strip() == 'TỔNG CỘNG'
        html.append('<tr>')
        for col in df.columns:
            val = row[col]
            if pd.isna(val): val = ""
            
            if col in ['% MTD', '% MTD (OFF)', '% MTD (ON)']:
                style_bg = color_pct_bg(val)
                if is_total:
                    html.append(f'<td style="{style_bg} text-align: center; font-weight: 900 !important; color: #c53030 !important;">{val}</td>')
                else:
                    html.append(f'<td style="{style_bg} text-align: center;">{val}</td>')
            elif is_total:
                align = 'left' if col in ['Tên NVBH', 'Tên NV'] else ('center' if col in ['STT', 'Mã NVBH'] else 'right')
                html.append(f'<td style="background-color: #fff5f5; color: #c53030 !important; font-weight: 900 !important; text-align: {align}; white-space: nowrap;">{val}</td>')
            elif col in ['Tên NVBH', 'Tên NV']:
                html.append(f'<td style="color: #1a365d; text-align: left; white-space: nowrap;">{val}</td>')
            else:
                align = 'center' if col in ['STT', 'Mã NVBH', 'Thực Hiện Ngày', 'MTD', 'Phát sinh Ngày (OFF)', 'MTD (OFF)', 'Phát sinh Ngày (ON)', 'MTD (ON)', 'Chỉ Tiêu KPI', 'Target (OFF)', 'Target (ON)', 'VIP MCH', 'KH Combo OFF', 'KH Combo ON', 'MBS Cat', 'MBS Brand'] else 'right'
                if col in ['Chỉ Tiêu Doanh Số', 'Doanh Số MTD', 'Thực Hiện Ngày']: align = 'right'
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
        <h1>SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 11</h1>
        <h2>TRACKING KPI ĐDKD - TEAM SS NGUYỄN THỊ TƯỜNG VY </h2>
    </div>
</div>
""", unsafe_allow_html=True)

col_reload, col_empty = st.columns([2, 5])
with col_reload:
    if st.button("🔄 Xóa Cache & Reload Dữ Liệu"):
        st.cache_data.clear()
        st.rerun()

with st.spinner("Đang tải dữ liệu..."):
    df, mcp = load_main_data()
    targets = get_targets()
    turnover_targets = get_turnover_targets()
    df_cat = load_cat_data()
    df_brand = load_brand_data()
    df_combo_off, df_combo_on = load_combo_data()
    
    mcp = process_mcp_sales(df, mcp)
    df_cat = process_cat_sales(df, df_cat)
    df_brand = process_brand_sales(df, df_brand)

nv_list = sorted(df['Tên NVBH'].dropna().unique().tolist())

vn_time = dt.datetime.utcnow() + dt.timedelta(hours=7)
default_date_t_minus_1 = (vn_time - timedelta(days=1)).date()

def get_timegone_stats(target_date):
    year = target_date.year
    month = target_date.month
    first_day = dt.date(year, month, 1)
    if month == 12:
        last_day = dt.date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = dt.date(year, month + 1, 1) - timedelta(days=1)
        
    total_working_days = 0
    elapsed_working_days = 0
    
    curr = first_day
    while curr <= last_day:
        is_sunday = (curr.weekday() == 6)
        is_holiday = (month == 9 and curr.day in [1, 2])
        
        if not is_sunday and not is_holiday:
            total_working_days += 1
            if curr <= target_date:
                elapsed_working_days += 1
        curr += timedelta(days=1)
        
    remaining_working_days = total_working_days - elapsed_working_days
    pct_timegone = round(elapsed_working_days / total_working_days * 100, 1) if total_working_days > 0 else 0
    return total_working_days, elapsed_working_days, remaining_working_days, pct_timegone

tot_days, elapsed_days, remain_days, pct_tg = get_timegone_stats(default_date_t_minus_1)

st.markdown(f"""
<div class="timegone-container" style="background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; margin: 5px 0 12px 0; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <div class="timegone-title" style="font-weight: 800; color: #1a365d; font-size: 12.5px; margin-bottom: 6px;">⏳ TIẾN ĐỘ THỜI GIAN THÁNG {default_date_t_minus_1.strftime('%m/%Y')}</div>
    <div class="timegone-grid" style="display: flex; justify-content: space-around; font-size: 11.5px; gap: 6px; flex-wrap: wrap;">
        <div class="timegone-item" style="background: #fff; padding: 3px 8px; border-radius: 4px; border: 1px solid #edf2f7;"><b>Tổng làm việc:</b> <span style="color: #2b6cb0; font-weight: 700;">{tot_days}</span></div>
        <div class="timegone-item" style="background: #fff; padding: 3px 8px; border-radius: 4px; border: 1px solid #edf2f7;"><b>Đã trôi qua:</b> <span style="color: #c53030; font-weight: 700;">{elapsed_days}</span></div>
        <div class="timegone-item" style="background: #fff; padding: 3px 8px; border-radius: 4px; border: 1px solid #edf2f7;"><b>Còn lại:</b> <span style="color: #2f855a; font-weight: 700;">{remain_days}</span></div>
        <div class="timegone-item" style="background: #c6f6d5; padding: 3px 8px; border-radius: 4px; border: 1px solid #9ae6b4; color: #22543d;"><b>% Timegone:</b> <span style="font-weight: 800;">{pct_tg}%</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Bộ lọc chính
f1, f2, f3 = st.columns([1, 1, 1.3])
with f1:
    st.markdown('<p class="filter-label">MONTH</p>', unsafe_allow_html=True)
    st.selectbox("", ["Tháng 09/2026"], key="month", label_visibility="collapsed")
with f2:
    st.markdown('<p class="filter-label">NGÀY</p>', unsafe_allow_html=True)
    report_date = st.date_input("", value=default_date_t_minus_1, key="ngay", label_visibility="collapsed")
with f3:
    st.markdown('<p class="filter-label">KPI NAME</p>', unsafe_allow_html=True)
    kpi_map = {
        "1. ASO FOCUS CHANTÉ": "CHANTE",
        "2. ASO FOCUS OMC TRỘN": "OMACHI",
        "3. ASO TEA KÊNH ON": "ASO_TEA",
        "4. PC BT (PC 4LINE - BEER)": "PC_BT",
        "5. ASO ALL": "ASO_ALL",
        "6. ASO ACTIVE KÊNH ON": "PC_ON",
        "7. BÁO CÁO ĐH COMBO": "COMBO",
        "8. BÁO CÁO DOANH SỐ TURNOVER": "TURNOVER",
        "9. BÁO CÁO TỔNG HỢP": "SUMMARY",
    }
    selected_name = st.selectbox("", list(kpi_map.keys()), key="kpi", label_visibility="collapsed")
    selected_kpi = kpi_map[selected_name]

f4, f5 = st.columns([1, 1])
with f4:
    st.markdown('<p class="filter-label">SALE SUP</p>', unsafe_allow_html=True)
    st.selectbox("", ["Nguyễn Thị Tường Vy Total"], key="sup", label_visibility="collapsed")
with f5:
    st.markdown('<p class="filter-label">ĐDKD (Nhân viên)</p>', unsafe_allow_html=True)
    filter_nv = st.selectbox("", ["Tất cả ĐDKD"] + nv_list, key="ddkd", label_visibility="collapsed")

st.markdown("---")

tab_kpi, tab_mcp, tab_cat, tab_brand, tab_dskh_off, tab_dskh_on = st.tabs([
    "📊 BÁO CÁO KPI", "🗺️ MCP VISIT", "📦 TRACKING MBS - CAT", "🏷️ TRACKING MBS - BRAND", "📋 DSKH_Combo OFF", "📋 DSKH_Combo ON"
])

# ----- TAB KPI -----
with tab_kpi:
    if selected_kpi == "SUMMARY":
        saved_sum_thu = st.query_params.get("sum_thu", "")
        default_sum_thu_list = [x.strip() for x in saved_sum_thu.split(",") if x.strip()] if saved_sum_thu else []
        
        if not default_sum_thu_list and report_date:
            wday = report_date.weekday()
            if wday in [0, 3]:
                default_sum_thu_list = ["25"]
            elif wday in [1, 4]:
                default_sum_thu_list = ["36"]
            elif wday in [2, 5]:
                default_sum_thu_list = ["47"]

        def update_sum_params():
            st.query_params["sum_thu"] = ",".join(st.session_state.sum_thu_input) if st.session_state.sum_thu_input else ""

        col_f_thu, col_f_metrics = st.columns([1, 1.5])
        with col_f_thu:
            st.markdown('<p class="filter-label">📅 Lọc Theo Thứ / Chu kỳ (Chọn nhiều)</p>', unsafe_allow_html=True)
            thu_opts = ["2","3","4","5","6","7","25","36","47"]
            valid_sum_thu = [t for t in default_sum_thu_list if t in thu_opts]
            f_thu_sum = st.multiselect("", thu_opts, default=valid_sum_thu, key="sum_thu_input", on_change=update_sum_params, label_visibility="collapsed")
        
        with col_f_metrics:
            st.markdown('<p class="filter-label">📊 Chọn Chỉ Số Hiển Thị</p>', unsafe_allow_html=True)
            metric_opts = ["VIP MCH", "KH Combo OFF", "KH Combo ON", "MBS Cat", "MBS Brand"]
            saved_metrics = st.query_params.get("sum_metrics", "")
            default_metrics = [x.strip() for x in saved_metrics.split(",") if x.strip()] if saved_metrics else metric_opts
            valid_metrics = [m for m in default_metrics if m in metric_opts]
            if not valid_metrics: valid_metrics = metric_opts
            
            def update_metric_params():
                st.query_params["sum_metrics"] = ",".join(st.session_state.sum_metrics_input) if st.session_state.sum_metrics_input else ""
                
            selected_metrics = st.multiselect("", metric_opts, default=valid_metrics, key="sum_metrics_input", on_change=update_metric_params, label_visibility="collapsed")
            if not selected_metrics: selected_metrics = metric_opts

        st.query_params["sum_thu"] = ",".join(st.session_state.sum_thu_input) if st.session_state.sum_thu_input else ""
        st.query_params["sum_metrics"] = ",".join(selected_metrics)

        df_summary = build_summary_report(df, report_date, df_combo_off, df_combo_on, df_cat, df_brand, mcp, filter_nv, f_thu_sum)
        tot_row_s = df_summary.iloc[-1]
        
        st.markdown(f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px; font-size: 15px;">9. BÁO CÁO TỔNG HỢP - THÁNG {report_date.strftime("%m/%Y")}</h3>', unsafe_allow_html=True)
        st.caption(f"⚡ Ngày: {report_date.strftime('%d/%m/%Y')} | Lọc NV: {filter_nv} | Lọc Thứ/Chu kỳ: {f_thu_sum if f_thu_sum else 'Tất cả'}")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: render_metric_card("Tổng VIP MCH", f"{tot_row_s['VIP MCH']:,}")
        with c2: render_metric_card("Tổng KH Combo OFF", f"{tot_row_s['KH Combo OFF']:,}")
        with c3: render_metric_card("Tổng KH Combo ON", f"{tot_row_s['KH Combo ON']:,}")
        with c4: render_metric_card("Tổng MBS Cat / Brand", f"{tot_row_s['MBS Cat']:,} / {tot_row_s['MBS Brand']:,}")
        
        st.markdown(render_summary_html_table(df_summary, selected_metrics), unsafe_allow_html=True)
        st.markdown(f"""
        <div class="note-box">
            <b>NHẬN XÉT BÁO CÁO TỔNG HỢP:</b><br>
            • Tổng số lượng cửa hàng VIP (VIP3, VIP5, VIPSI) toàn đội: <b>{tot_row_s['VIP MCH']:,} cửa hàng</b> (Đã mua: {tot_row_s['Đã Mua (VIP)']:,}).<br>
            • Tổng KH tham gia Combo OFF: <b>{tot_row_s['KH Combo OFF']:,} CH</b> (Đã mua: {tot_row_s['Đã Mua (OFF)']:,}) | Combo ON: <b>{tot_row_s['KH Combo ON']:,} CH</b> (Đã mua: {tot_row_s['Đã Mua (ON)']:,}).<br>
            • MBS Category (Outlet): <b>{tot_row_s['MBS Cat']:,} CH</b> | MBS Brand (Outlet): <b>{tot_row_s['MBS Brand']:,} CH</b>.<br>
            • Đã áp dụng chuẩn xác bộ lọc Ngày & Thứ (nếu chọn 25 chỉ lấy 25, 36 chỉ lấy 36, 47 chỉ lấy 47).
        </div>
        """, unsafe_allow_html=True)
        
    elif selected_kpi == "TURNOVER":
        df_r, team_tgt, title = build_turnover_report(df, report_date, turnover_targets, filter_nv)
        total_row = df_r.iloc[-1]
        total_mtd = float(total_row['Doanh Số MTD'])
        total_today = float(total_row['Thực Hiện Ngày'])
        pct_team = total_row['% MTD']
        
        st.markdown(f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px; font-size: 15px;">{title} - THÁNG {report_date.strftime("%m/%Y")}</h3>', unsafe_allow_html=True)
        st.caption(f"⚡ Ngày: {report_date.strftime('%d/%m/%Y')} | Lọc: {filter_nv}")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: render_metric_card("🎯 Chỉ Tiêu DS", f"{team_tgt:,.0f}".replace(",", "."))
        with c2: render_metric_card("📈 Doanh Số MTD", f"{total_mtd:,.0f}".replace(",", "."))
        with c3: render_metric_card("📊 % MTD", pct_team)
        with c4: render_metric_card("🆕 Thực Hiện Ngày", f"{total_today:,.0f}".replace(",", "."))
        
        df_display = df_r.copy()
        for col in ['Chỉ Tiêu Doanh Số', 'Thực Hiện Ngày', 'Doanh Số MTD']:
            df_display[col] = df_display[col].apply(lambda x: f"{x:,.0f}".replace(",", ".") if isinstance(x, (int, float)) and x > 0 else ("0" if x == 0 else x))
            
        st.markdown(render_html_table(df_display), unsafe_allow_html=True)
        
        df_eval = df_r.iloc[:-1].copy()
        df_eval['_pct_val'] = df_eval['% MTD'].str.replace('%','').astype(float)
        df_sorted_pct = df_eval.sort_values(by='_pct_val', ascending=False)
        top3 = df_sorted_pct.head(3)
        bottom3 = df_sorted_pct.tail(3).iloc[::-1]
        
        top3_text = ", ".join([f"{r['Tên NVBH']} ({r['% MTD']})" for _, r in top3.iterrows()])
        bottom3_text = ", ".join([f"{r['Tên NVBH']} ({r['% MTD']})" for _, r in bottom3.iterrows()])
        
        st.markdown(f"""
        <div class="note-box">
            <b>NHẬN XÉT ({title} - {report_date.strftime('%d/%m/%Y')}):</b><br>
            • Tổng Doanh Số MTD: <b>{total_mtd:,.0f} / {team_tgt:,.0f} VNĐ ({pct_team})</b> | Thực hiện ngày: <b>{total_today:,.0f} VNĐ</b>.<br>
            • <b>Top 3 ĐDKD dẫn đầu:</b> {top3_text}<br>
            • <b>Top 3 ĐDKD cần đôn đốc:</b> {bottom3_text}
        </div>
        """, unsafe_allow_html=True)

    elif selected_kpi != "COMBO":
        df_r, team_tgt, title = build_report(df, report_date, targets, selected_kpi, filter_nv, mcp_df=mcp)
        total_row = df_r.iloc[-1]
        total_mtd = int(total_row['MTD'])
        total_ngay = int(total_row['Thực Hiện Ngày'])
        pct_team = total_row['% MTD']
        st.markdown(f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px; font-size: 15px;">{title} - THÁNG {report_date.strftime("%m/%Y")}</h3>', unsafe_allow_html=True)
        st.caption(f"⚡ Ngày: {report_date.strftime('%d/%m/%Y')} | Lọc: {filter_nv}")
        c1, c2, c3, c4 = st.columns(4)
        with c1: render_metric_card("🎯 Target", f"{team_tgt:,}")
        with c2: render_metric_card("📈 MTD", f"{total_mtd:,}")
        with c3: render_metric_card("📊 % MTD", pct_team)
        with c4: render_metric_card("🆕 Ngày", f"+{total_ngay}")
        st.markdown(render_html_table(df_r), unsafe_allow_html=True)
        df_eval = df_r.iloc[:-1].copy()
        df_eval['_pct_val'] = df_eval['% MTD'].str.replace('%','').astype(float)
        
        df_sorted_pct = df_eval.sort_values(by='_pct_val', ascending=False)
        top3 = df_sorted_pct.head(3)
        bottom3 = df_sorted_pct.tail(3).iloc[::-1]
        
        top3_text = ", ".join([f"{r['Tên NVBH']} ({r['% MTD']})" for _, r in top3.iterrows()])
        bottom3_text = ", ".join([f"{r['Tên NVBH']} ({r['% MTD']})" for _, r in bottom3.iterrows()])
        st.markdown(f"""
        <div class="note-box">
            <b>NHẬN XÉT ({title} - {report_date.strftime('%d/%m/%Y')}):</b><br>
            • Tiến độ MTD: <b>{total_mtd}/{team_tgt} ({pct_team})</b>. Phát sinh ngày: <b>+{total_ngay}</b>.<br>
            • <b>Top 3:</b> {top3_text}<br>
            • <b>Bottom 3:</b> {bottom3_text}
        </div>
        """, unsafe_allow_html=True)
    else:
        df_combo, target_off_total, target_on_total = build_combo_matrix(df, report_date, df_combo_off, df_combo_on, filter_nv)
        total_row = df_combo.iloc[-1]
        total_off = int(total_row['MTD (OFF)'])
        total_on = int(total_row['MTD (ON)'])
        ngay_off = int(total_row['Phát sinh Ngày (OFF)'])
        ngay_on = int(total_row['Phát sinh Ngày (ON)'])
        
        pct_off_team = round(total_off / target_off_total * 100, 1) if target_off_total else 0
        pct_on_team = round(total_on / target_on_total * 100, 1) if target_on_total else 0

        st.markdown(f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px; font-size: 15px;">7. BÁO CÁO ĐH COMBO (MATRIX OFF/ON) - THÁNG {report_date.strftime("%m/%Y")}</h3>', unsafe_allow_html=True)
        st.caption(f"⚡ Ngày: {report_date.strftime('%d/%m/%Y')} | Lọc: {filter_nv} | Target OFF: {target_off_total} CH | Target ON: {target_on_total} CH")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: render_metric_card("MTD OFF / Target", f"{total_off:,} / {target_off_total:,} ({pct_off_team}%)")
        with c2: render_metric_card("MTD ON / Target", f"{total_on:,} / {target_on_total:,} ({pct_on_team}%)")
        with c3: render_metric_card("Phát sinh Ngày (OFF)", f"+{ngay_off}")
        with c4: render_metric_card("Phát sinh Ngày (ON)", f"+{ngay_on}")
        
        st.markdown(render_html_table(df_combo), unsafe_allow_html=True)
        st.markdown(f"""
        <div class="note-box">
            <b>NHẬN XÉT BÁO CÁO COMBO LŨY KẾ (MATRIX OFF/ON):</b><br>
            • <b>Kênh OFF:</b> Đạt <b>{total_off:,} / {target_off_total:,} CH ({pct_off_team}%)</b> | Phát sinh mới trong ngày: <b>+{ngay_off} CH</b>.<br>
            • <b>Kênh ON:</b> Đạt <b>{total_on:,} / {target_on_total:,} CH ({pct_on_team}%)</b> | Phát sinh mới trong ngày: <b>+{ngay_on} CH</b>.<br>
            • Đã sắp xếp danh sách theo <b>% MTD (OFF) từ thấp đến cao</b> để bro dễ dàng tracking các ĐDKD cần đôn đốc.
        </div>
        """, unsafe_allow_html=True)

def update_mcp_params():
    st.query_params["mcp_nv"] = ",".join(st.session_state.mcp_nv_input) if st.session_state.mcp_nv_input else ""
    st.query_params["mcp_thu"] = ",".join(st.session_state.mcp_thu_input) if st.session_state.mcp_thu_input else ""
    st.query_params["mcp_ma"] = st.session_state.mcp_ma_input
    st.query_params["mcp_ten"] = st.session_state.mcp_ten_input
    st.query_params["mcp_vip"] = ",".join(st.session_state.mcp_vip_input) if st.session_state.mcp_vip_input else ""
    st.query_params["mcp_ds"] = ",".join(st.session_state.mcp_ds_input) if st.session_state.mcp_ds_input else ""

def update_cat_params():
    st.query_params["cat_nv"] = ",".join(st.session_state.cat_nv_input) if st.session_state.cat_nv_input else ""
    st.query_params["cat_thu"] = ",".join(st.session_state.cat_thu_input) if st.session_state.cat_thu_input else ""
    st.query_params["cat_ma"] = st.session_state.cat_ma_input
    st.query_params["cat_ten"] = st.session_state.cat_ten_input

def update_brand_params():
    st.query_params["brand_nv"] = ",".join(st.session_state.brand_nv_input) if st.session_state.brand_nv_input else ""
    st.query_params["brand_thu"] = ",".join(st.session_state.brand_thu_input) if st.session_state.brand_thu_input else ""
    st.query_params["brand_ma"] = st.session_state.brand_ma_input
    st.query_params["brand_ten"] = st.session_state.brand_ten_input

def update_off_params():
    st.query_params["off_nv"] = ",".join(st.session_state.off_nv_input) if st.session_state.off_nv_input else ""
    st.query_params["off_thu"] = ",".join(st.session_state.off_thu_input) if st.session_state.off_thu_input else ""
    st.query_params["off_ma"] = st.session_state.off_ma_input
    st.query_params["off_ten"] = st.session_state.off_ten_input

def update_on_params():
    st.query_params["on_nv"] = ",".join(st.session_state.on_nv_input) if st.session_state.on_nv_input else ""
    st.query_params["on_thu"] = ",".join(st.session_state.on_thu_input) if st.session_state.on_thu_input else ""
    st.query_params["on_ma"] = st.session_state.on_ma_input
    st.query_params["on_ten"] = st.session_state.on_ten_input

# ----- TAB MCP -----
with tab_mcp:
    st.markdown('<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px; font-size: 15px;">🗺️ MCP VISIT & MAPPING DOANH SỐ BÁN HÀNG</h3>', unsafe_allow_html=True)
    if mcp.empty:
        st.warning("Chưa có dữ liệu MCP")
    else:
        col_nv = find_col(mcp, ['SM name','SM Name','Tên NVBH','Nhân viên','Sale name','Position name'])
        col_ma = find_col(mcp, ['Outlet_code','Outlet Code','Mã CH','Mã khách hàng','Poscode'])
        col_ten = find_col(mcp, ['Outlet_name','Outlet Name','Tên CH','Tên khách hàng'])
        col_thu = find_col(mcp, ['Thứ','Frequency','Tần suất'])
        col_vip = find_col(mcp, ['VIP MCH', 'VIP_MCH'])
        col_ds = find_col(mcp, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])
        
        saved_mcp_nv = st.query_params.get("mcp_nv", "")
        default_nv_list = [x.strip() for x in saved_mcp_nv.split(",") if x.strip()] if saved_mcp_nv else []
        
        saved_mcp_thu = st.query_params.get("mcp_thu", "")
        default_thu_list = [x.strip() for x in saved_mcp_thu.split(",") if x.strip()] if saved_mcp_thu else []
        
        saved_mcp_ma = st.query_params.get("mcp_ma", "")
        saved_mcp_ten = st.query_params.get("mcp_ten", "")
        
        saved_mcp_vip = st.query_params.get("mcp_vip", "")
        default_vip_list = [x.strip() for x in saved_mcp_vip.split(",") if x.strip()] if saved_mcp_vip else []
        
        saved_mcp_ds = st.query_params.get("mcp_ds", "")
        default_ds_list = [x.strip() for x in saved_mcp_ds.split(",") if x.strip()] if saved_mcp_ds else []

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>', unsafe_allow_html=True)
            nv_opts = sorted(mcp[col_nv].dropna().astype(str).unique().tolist()) if col_nv else []
            valid_default_nv = [v for v in default_nv_list if v in nv_opts]
            f_nv = st.multiselect("", nv_opts, default=valid_default_nv, key="mcp_nv_input", on_change=update_mcp_params, label_visibility="collapsed")
        with c2:
            st.markdown('<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>', unsafe_allow_html=True)
            thu_opts = ["2","3","4","5","6","7","25","36","47"]
            valid_default_thu = [t for t in default_thu_list if t in thu_opts]
            f_thu = st.multiselect("", thu_opts, default=valid_default_thu, key="mcp_thu_input", on_change=update_mcp_params, label_visibility="collapsed")
            
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>', unsafe_allow_html=True)
            f_ma = st.text_input("", value=saved_mcp_ma, key="mcp_ma_input", on_change=update_mcp_params, label_visibility="collapsed")
        with c4:
            st.markdown('<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>', unsafe_allow_html=True)
            f_ten = st.text_input("", value=saved_mcp_ten, key="mcp_ten_input", on_change=update_mcp_params, label_visibility="collapsed")

        c5, c6 = st.columns(2)
        with c5:
            st.markdown('<p class="filter-label">⭐ Lọc VIP MCH (Chọn nhiều)</p>', unsafe_allow_html=True)
            vip_opts = sorted(mcp[col_vip].dropna().astype(str).unique().tolist()) if col_vip else []
            valid_default_vip = [v for v in default_vip_list if v in vip_opts]
            f_vip = st.multiselect("", vip_opts, default=valid_default_vip, key="mcp_vip_input", on_change=update_mcp_params, label_visibility="collapsed")
        with c6:
            st.markdown('<p class="filter-label">💰 Lọc Doanh Số MTD Thực Tế (Chọn nhiều)</p>', unsafe_allow_html=True)
            if col_ds:
                raw_ds_vals = sorted(mcp[col_ds].dropna().unique().tolist())
                ds_opts = [format_number_vn(v) for v in raw_ds_vals]
            else:
                ds_opts = []
            valid_default_ds = [d for d in default_ds_list if d in ds_opts]
            f_ds = st.multiselect("", ds_opts, default=valid_default_ds, key="mcp_ds_input", on_change=update_mcp_params, label_visibility="collapsed")
            
        st.query_params["mcp_nv"] = ",".join(st.session_state.mcp_nv_input) if st.session_state.mcp_nv_input else ""
        st.query_params["mcp_thu"] = ",".join(st.session_state.mcp_thu_input) if st.session_state.mcp_thu_input else ""
        st.query_params["mcp_ma"] = st.session_state.mcp_ma_input
        st.query_params["mcp_ten"] = st.session_state.mcp_ten_input
        st.query_params["mcp_vip"] = ",".join(st.session_state.mcp_vip_input) if st.session_state.mcp_vip_input else ""
        st.query_params["mcp_ds"] = ",".join(st.session_state.mcp_ds_input) if st.session_state.mcp_ds_input else ""

        df_f = mcp.copy()
        if f_nv and col_nv: df_f = df_f[df_f[col_nv].astype(str).isin(f_nv)]
        if f_ma and col_ma: df_f = df_f[df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)]
        if f_ten and col_ten: df_f = df_f[df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)]
        if f_vip and col_vip: df_f = df_f[df_f[col_vip].astype(str).isin(f_vip)]
        
        if f_ds and col_ds:
            formatted_col_ds = df_f[col_ds].apply(format_number_vn).astype(str)
            df_f = df_f[formatted_col_ds.isin(f_ds)]

        df_f = filter_by_thu_multi(df_f, col_thu, f_thu)
        for col in df_f.columns:
            if any(x in col.lower().replace(" ","") for x in ["3msales","doanhsố","doanhso","sales","doanhsômtd"]):
                df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(format_number_vn)
        
        all_cols_mcp = df_f.columns.tolist()
        saved_mcp_cols = st.query_params.get("mcp_cols", None)
        if saved_mcp_cols:
            if isinstance(saved_mcp_cols, str):
                default_cols_mcp = [c.strip() for c in saved_mcp_cols.split(",") if c.strip() in all_cols_mcp]
            else:
                default_cols_mcp = [c for c in saved_mcp_cols if c in all_cols_mcp]
            if not default_cols_mcp: default_cols_mcp = all_cols_mcp
        else:
            default_cols_mcp = all_cols_mcp

        with st.popover("👁️ Chọn cột hiển thị (MCP)", use_container_width=False):
            selected_mcp_cols = st.multiselect("Bỏ chọn để ẩn cột:", all_cols_mcp, default=default_cols_mcp, key="mcp_cols_input")
        st.query_params["mcp_cols"] = ",".join(selected_mcp_cols)

        st.dataframe(df_f[selected_mcp_cols], use_container_width=True, height=450, hide_index=True)
        st.caption(f"Hiển thị: {len(df_f):,} / {len(mcp):,} cửa hàng")

# ----- TAB CAT -----
with tab_cat:
    st.markdown('<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px; font-size: 15px;">🎯 TRACKING MBS - THEO NGÀNH HÀNG (CATEGORY)</h3>', unsafe_allow_html=True)
    if df_cat.empty:
        st.error("❌ Không tìm thấy Data_Cat.xlsx trong thư mục 'data'")
    else:
        col_nv = find_col(df_cat, ['SM Name','SM name','Tên NVBH','Nhân viên'])
        col_ma = find_col(df_cat, ['Outlet Code','Outlet_code','Mã CH','Mã khách hàng'])
        col_ten = find_col(df_cat, ['Outlet Name','Outlet_name','Tên CH','Tên khách hàng'])
        col_thu = find_col(df_cat, ['Thứ'])
        
        saved_cat_nv = st.query_params.get("cat_nv", "")
        default_cat_nv_list = [x.strip() for x in saved_cat_nv.split(",") if x.strip()] if saved_cat_nv else []
        
        saved_cat_thu = st.query_params.get("cat_thu", "")
        default_cat_thu_list = [x.strip() for x in saved_cat_thu.split(",") if x.strip()] if saved_cat_thu else []
        
        saved_cat_ma = st.query_params.get("cat_ma", "")
        saved_cat_ten = st.query_params.get("cat_ten", "")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>', unsafe_allow_html=True)
            nv_opts = sorted(df_cat[col_nv].dropna().astype(str).unique().tolist()) if col_nv else []
            valid_cat_nv = [v for v in default_cat_nv_list if v in nv_opts]
            f_nv = st.multiselect("", nv_opts, default=valid_cat_nv, key="cat_nv_input", on_change=update_cat_params, label_visibility="collapsed")
        with c2:
            st.markdown('<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>', unsafe_allow_html=True)
            thu_opts = ["2","3","4","5","6","7","25","36","47"]
            valid_cat_thu = [t for t in default_cat_thu_list if t in thu_opts]
            f_thu = st.multiselect("", thu_opts, default=valid_cat_thu, key="cat_thu_input", on_change=update_cat_params, label_visibility="collapsed")
            
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>', unsafe_allow_html=True)
            f_ma = st.text_input("", value=saved_cat_ma, key="cat_ma_input", on_change=update_cat_params, label_visibility="collapsed")
        with c4:
            st.markdown('<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>', unsafe_allow_html=True)
            f_ten = st.text_input("", value=saved_cat_ten, key="cat_ten_input", on_change=update_cat_params, label_visibility="collapsed")
            
        st.query_params["cat_nv"] = ",".join(st.session_state.cat_nv_input) if st.session_state.cat_nv_input else ""
        st.query_params["cat_thu"] = ",".join(st.session_state.cat_thu_input) if st.session_state.cat_thu_input else ""
        st.query_params["cat_ma"] = st.session_state.cat_ma_input
        st.query_params["cat_ten"] = st.session_state.cat_ten_input

        df_f = df_cat.copy()
        if f_nv and col_nv: df_f = df_f[df_f[col_nv].astype(str).isin(f_nv)]
        if f_ma and col_ma: df_f = df_f[df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)]
        if f_ten and col_ten: df_f = df_f[df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)]
        df_f = filter_by_thu_multi(df_f, col_thu, f_thu)
        for col in df_f.columns:
            if "doanh số" in col.lower() or "doanhso" in col.lower().replace(" ",""):
                df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(format_number_vn)
        
        all_cols_cat = df_f.columns.tolist()
        saved_cat_cols = st.query_params.get("cat_cols", None)
        if saved_cat_cols:
            if isinstance(saved_cat_cols, str):
                default_cols_cat = [c.strip() for c in saved_cat_cols.split(",") if c.strip() in all_cols_cat]
            else:
                default_cols_cat = [c for c in saved_cat_cols if c in all_cols_cat]
            if not default_cols_cat: default_cols_cat = all_cols_cat
        else:
            default_cols_cat = all_cols_cat

        with st.popover("👁️ Chọn cột hiển thị (Category)", use_container_width=False):
            selected_cat_cols = st.multiselect("Bỏ chọn để ẩn cột:", all_cols_cat, default=default_cols_cat, key="cat_cols_input")
        st.query_params["cat_cols"] = ",".join(selected_cat_cols)

        st.dataframe(df_f[selected_cat_cols], use_container_width=True, height=450, hide_index=True)
        st.caption(f"Hiển thị: {len(df_f):,} / {len(df_cat):,} dòng")

# ----- TAB BRAND -----
with tab_brand:
    st.markdown('<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px; font-size: 15px;">🏷️ TRACKING MBS - THEO THƯƠNG HIỆU (BRAND)</h3>', unsafe_allow_html=True)
    if df_brand.empty:
        st.error("❌ Không tìm thấy Data_Brand.xlsx trong thư mục 'data'")
    else:
        col_nv = find_col(df_brand, ['SM Name','SM name','Tên NVBH','Nhân viên'])
        col_ma = find_col(df_brand, ['Outlet Code','Outlet_code','Mã CH','Mã khách hàng'])
        col_ten = find_col(df_brand, ['Outlet Name','Outlet_name','Tên CH','Tên khách hàng'])
        col_thu = find_col(df_brand, ['Thứ'])
        
        saved_brand_nv = st.query_params.get("brand_nv", "")
        default_brand_nv_list = [x.strip() for x in saved_brand_nv.split(",") if x.strip()] if saved_brand_nv else []
        
        saved_brand_thu = st.query_params.get("brand_thu", "")
        default_brand_thu_list = [x.strip() for x in saved_brand_thu.split(",") if x.strip()] if saved_brand_thu else []
        
        saved_brand_ma = st.query_params.get("brand_ma", "")
        saved_brand_ten = st.query_params.get("brand_ten", "")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>', unsafe_allow_html=True)
            nv_opts = sorted(df_brand[col_nv].dropna().astype(str).unique().tolist()) if col_nv else []
            valid_brand_nv = [v for v in default_brand_nv_list if v in nv_opts]
            f_nv = st.multiselect("", nv_opts, default=valid_brand_nv, key="brand_nv_input", on_change=update_brand_params, label_visibility="collapsed")
        with c2:
            st.markdown('<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>', unsafe_allow_html=True)
            thu_opts = ["2","3","4","5","6","7","25","36","47"]
            valid_brand_thu = [t for t in default_brand_thu_list if t in thu_opts]
            f_thu = st.multiselect("", thu_opts, default=valid_brand_thu, key="brand_thu_input", on_change=update_brand_params, label_visibility="collapsed")
            
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>', unsafe_allow_html=True)
            f_ma = st.text_input("", value=saved_brand_ma, key="brand_ma_input", on_change=update_brand_params, label_visibility="collapsed")
        with c4:
            st.markdown('<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>', unsafe_allow_html=True)
            f_ten = st.text_input("", value=saved_brand_ten, key="brand_ten_input", on_change=update_brand_params, label_visibility="collapsed")
            
        st.query_params["brand_nv"] = ",".join(st.session_state.brand_nv_input) if st.session_state.brand_nv_input else ""
        st.query_params["brand_thu"] = ",".join(st.session_state.brand_thu_input) if st.session_state.brand_thu_input else ""
        st.query_params["brand_ma"] = st.session_state.brand_ma_input
        st.query_params["brand_ten"] = st.session_state.brand_ten_input

        df_f = df_brand.copy()
        if f_nv and col_nv: df_f = df_f[df_f[col_nv].astype(str).isin(f_nv)]
        if f_ma and col_ma: df_f = df_f[df_f[col_ma].astype(str).str.contains(f_ma, case=False, na=False)]
        if f_ten and col_ten: df_f = df_f[df_f[col_ten].astype(str).str.contains(f_ten, case=False, na=False)]
        df_f = filter_by_thu_multi(df_f, col_thu, f_thu)
        for col in df_f.columns:
            if "doanh số" in col.lower() or "doanhso" in col.lower().replace(" ",""):
                df_f[col] = pd.to_numeric(df_f[col], errors='coerce').apply(format_number_vn)
        
        all_cols_brand = df_f.columns.tolist()
        saved_brand_cols = st.query_params.get("brand_cols", None)
        if saved_brand_cols:
            if isinstance(saved_brand_cols, str):
                default_cols_brand = [c.strip() for c in saved_brand_cols.split(",") if c.strip() in all_cols_brand]
            else:
                default_cols_brand = [c for c in saved_brand_cols if c in all_cols_brand]
            if not default_cols_brand: default_cols_brand = all_cols_brand
        else:
            default_cols_brand = all_cols_brand

        with st.popover("👁️ Chọn cột hiển thị (Brand)", use_container_width=False):
            selected_brand_cols = st.multiselect("Bỏ chọn để ẩn cột:", all_cols_brand, default=default_cols_brand, key="brand_cols_input")
        st.query_params["brand_cols"] = ",".join(selected_brand_cols)

        st.dataframe(df_f[selected_brand_cols], use_container_width=True, height=450, hide_index=True)
        st.caption(f"Hiển thị: {len(df_f):,} / {len(df_brand):,} dòng")

# ----- TAB DSKH_Combo OFF -----
with tab_dskh_off:
    st.markdown('<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px; font-size: 15px;">📋 DANH SÁCH KHÁCH HÀNG COMBO OFF (TÂN_COMBO KÊNH OFF)</h3>', unsafe_allow_html=True)
    if df_combo_off.empty:
        st.warning("Chưa có dữ liệu Combo OFF trong thư mục 'data'")
    else:
        col_nv_off = find_col(df_combo_off, ['Tên NV', 'SM name', 'Nhân viên'])
        col_ma_off = find_col(df_combo_off, ['outlet_code', 'Outlet Code', 'Mã CH'])
        col_ten_off = find_col(df_combo_off, ['outlet_name', 'Outlet Name', 'Tên CH'])
        col_thu_off = find_col(df_combo_off, ['Thứ', 'Frequency'])
        
        saved_off_nv = st.query_params.get("off_nv", "")
        default_off_nv_list = [x.strip() for x in saved_off_nv.split(",") if x.strip()] if saved_off_nv else []
        
        saved_off_thu = st.query_params.get("off_thu", "")
        default_off_thu_list = [x.strip() for x in saved_off_thu.split(",") if x.strip()] if saved_off_thu else []
        
        saved_off_ma = st.query_params.get("off_ma", "")
        saved_off_ten = st.query_params.get("off_ten", "")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>', unsafe_allow_html=True)
            nv_opts_off = sorted(df_combo_off[col_nv_off].dropna().astype(str).unique().tolist()) if col_nv_off else []
            valid_off_nv = [v for v in default_off_nv_list if v in nv_opts_off]
            f_off_nv = st.multiselect("", nv_opts_off, default=valid_off_nv, key="off_nv_input", on_change=update_off_params, label_visibility="collapsed")
        with c2:
            st.markdown('<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>', unsafe_allow_html=True)
            thu_opts = ["2","3","4","5","6","7","25","36","47"]
            valid_off_thu = [t for t in default_off_thu_list if t in thu_opts]
            f_off_thu = st.multiselect("", thu_opts, default=valid_off_thu, key="off_thu_input", on_change=update_off_params, label_visibility="collapsed")
            
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>', unsafe_allow_html=True)
            f_off_ma = st.text_input("", value=saved_off_ma, key="off_ma_input", on_change=update_off_params, label_visibility="collapsed")
        with c4:
            st.markdown('<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>', unsafe_allow_html=True)
            f_off_ten = st.text_input("", value=saved_off_ten, key="off_ten_input", on_change=update_off_params, label_visibility="collapsed")
            
        st.query_params["off_nv"] = ",".join(st.session_state.off_nv_input) if st.session_state.off_nv_input else ""
        st.query_params["off_thu"] = ",".join(st.session_state.off_thu_input) if st.session_state.off_thu_input else ""
        st.query_params["off_ma"] = st.session_state.off_ma_input
        st.query_params["off_ten"] = st.session_state.off_ten_input

        df_off_f = df_combo_off.copy()
        if f_off_nv and col_nv_off: df_off_f = df_off_f[df_off_f[col_nv_off].astype(str).isin(f_off_nv)]
        if f_off_ma and col_ma_off: df_off_f = df_off_f[df_off_f[col_ma_off].astype(str).str.contains(f_off_ma, case=False, na=False)]
        if f_off_ten and col_ten_off: df_off_f = df_off_f[df_off_f[col_ten_off].astype(str).str.contains(f_off_ten, case=False, na=False)]
        df_off_f = filter_by_thu_multi(df_off_f, col_thu_off, f_off_thu)
        
        all_cols_off = df_off_f.columns.tolist()
        saved_off_cols = st.query_params.get("off_cols", None)
        if saved_off_cols:
            if isinstance(saved_off_cols, str):
                default_cols_off = [c.strip() for c in saved_off_cols.split(",") if c.strip() in all_cols_off]
            else:
                default_cols_off = [c for c in saved_off_cols if c in all_cols_off]
            if not default_cols_off: default_cols_off = all_cols_off
        else:
            default_cols_off = all_cols_off

        with st.popover("👁️ Chọn cột hiển thị (DSKH OFF)", use_container_width=False):
            selected_off_cols = st.multiselect("Bỏ chọn để ẩn cột:", all_cols_off, default=default_cols_off, key="off_cols_input")
        st.query_params["off_cols"] = ",".join(selected_off_cols)

        st.dataframe(df_off_f[selected_off_cols], use_container_width=True, height=450, hide_index=True)
        st.caption(f"Hiển thị: {len(df_off_f):,} / {len(df_combo_off):,} cửa hàng")

# ----- TAB DSKH_Combo ON -----
with tab_dskh_on:
    st.markdown('<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 0px; font-size: 15px;">📋 DANH SÁCH KHÁCH HÀNG COMBO ON (TÂN_COMBO KÊNH ON)</h3>', unsafe_allow_html=True)
    if df_combo_on.empty:
        st.warning("Chưa có dữ liệu Combo ON trong thư mục 'data'")
    else:
        col_nv_on = find_col(df_combo_on, ['Tên NV', 'SM name', 'Nhân viên'])
        col_ma_on = find_col(df_combo_on, ['outlet_code', 'Outlet Code', 'Mã CH'])
        col_ten_on = find_col(df_combo_on, ['outlet_name', 'Outlet Name', 'Tên CH'])
        col_thu_on = find_col(df_combo_on, ['Thứ', 'Frequency'])
        
        saved_on_nv = st.query_params.get("on_nv", "")
        default_on_nv_list = [x.strip() for x in saved_on_nv.split(",") if x.strip()] if saved_on_nv else []
        
        saved_on_thu = st.query_params.get("on_thu", "")
        default_on_thu_list = [x.strip() for x in saved_on_thu.split(",") if x.strip()] if saved_on_thu else []
        
        saved_on_ma = st.query_params.get("on_ma", "")
        saved_on_ten = st.query_params.get("on_ten", "")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD - Chọn nhiều)</p>', unsafe_allow_html=True)
            nv_opts_on = sorted(df_combo_on[col_nv_on].dropna().astype(str).unique().tolist()) if col_nv_on else []
            valid_on_nv = [v for v in default_on_nv_list if v in nv_opts_on]
            f_on_nv = st.multiselect("", nv_opts_on, default=valid_on_nv, key="on_nv_input", on_change=update_on_params, label_visibility="collapsed")
        with c2:
            st.markdown('<p class="filter-label">📅 Lọc Theo Thứ (Chọn nhiều)</p>', unsafe_allow_html=True)
            thu_opts = ["2","3","4","5","6","7","25","36","47"]
            valid_on_thu = [t for t in default_on_thu_list if t in thu_opts]
            f_on_thu = st.multiselect("", thu_opts, default=valid_on_thu, key="on_thu_input", on_change=update_on_params, label_visibility="collapsed")
            
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>', unsafe_allow_html=True)
            f_on_ma = st.text_input("", value=saved_on_ma, key="on_ma_input", on_change=update_on_params, label_visibility="collapsed")
        with c4:
            st.markdown('<p class="filter-label">🏪 Lọc Tên Khách Hàng</p>', unsafe_allow_html=True)
            f_on_ten = st.text_input("", value=saved_on_ten, key="on_ten_input", on_change=update_on_params, label_visibility="collapsed")
            
        st.query_params["on_nv"] = ",".join(st.session_state.on_nv_input) if st.session_state.on_nv_input else ""
        st.query_params["on_thu"] = ",".join(st.session_state.on_thu_input) if st.session_state.on_thu_input else ""
        st.query_params["on_ma"] = st.session_state.on_ma_input
        st.query_params["on_ten"] = st.session_state.on_ten_input

        df_on_f = df_combo_on.copy()
        if f_on_nv and col_nv_on: df_on_f = df_on_f[df_on_f[col_nv_on].astype(str).isin(f_on_nv)]
        if f_on_ma and col_ma_on: df_on_f = df_on_f[df_on_f[col_ma_on].astype(str).str.contains(f_on_ma, case=False, na=False)]
        if f_on_ten and col_ten_on: df_on_f = df_on_f[df_on_f[col_ten_on].astype(str).str.contains(f_on_ten, case=False, na=False)]
        df_on_f = filter_by_thu_multi(df_on_f, col_thu_on, f_on_thu)
        
        all_cols_on = df_on_f.columns.tolist()
        saved_on_cols = st.query_params.get("on_cols", None)
        if saved_on_cols:
            if isinstance(saved_on_cols, str):
                default_cols_on = [c.strip() for c in saved_on_cols.split(",") if c.strip() in all_cols_on]
            else:
                default_cols_on = [c for c in saved_on_cols if c in all_cols_on]
            if not default_cols_on: default_cols_on = all_cols_on
        else:
            default_cols_on = all_cols_on

        with st.popover("👁️ Chọn cột hiển thị (DSKH ON)", use_container_width=False):
            selected_on_cols = st.multiselect("Bỏ chọn để ẩn cột:", all_cols_on, default=default_cols_on, key="on_cols_input")
        st.query_params["on_cols"] = ",".join(selected_on_cols)

        st.dataframe(df_on_f[selected_on_cols], use_container_width=True, height=450, hide_index=True)
        st.caption(f"Hiển thị: {len(df_on_f):,} / {len(df_combo_on):,} cửa hàng")
