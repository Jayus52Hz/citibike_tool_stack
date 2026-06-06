"""
app.py - Trang chủ Citi Bike Data Management System
"""
import streamlit as st
import pandas as pd
from db_config import run_query, check_connection

st.set_page_config(
    page_title="Citi Bike Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS tùy chỉnh ─────────────────────────────────────────────────────────────
st.markdown("""
            
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        color: white;
    }
    .metric-card .value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #e94560;
    }
    .metric-card .label {
        font-size: 0.85rem;
        color: #a0a0b0;
        margin-top: 4px;
    }
    .status-ok  { color: #00d4aa; font-weight: 600; }
    .status-err { color: #e94560; font-weight: 600; }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #e94560, #0f3460);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🚲 Citi Bike NYC</div>', unsafe_allow_html=True)
st.markdown("**Big Data Pipeline — Quản lý & Phân tích dữ liệu xe đạp công cộng**")
st.divider()

# ── DB Status ─────────────────────────────────────────────────────────────────
db_ok = check_connection()
if db_ok:
    st.markdown('<span class="status-ok">● Database MySQL: Kết nối thành công</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="status-err">● Database MySQL: Mất kết nối</span>', unsafe_allow_html=True)
    st.stop()

st.markdown("---")

# ── Metrics tổng quan ─────────────────────────────────────────────────────────
st.subheader("📈 Tổng quan dữ liệu")

col1, col2, col3, col4 = st.columns(4)

@st.cache_data(ttl=60)
def get_metrics():
    try:
        trips    = run_query("SELECT COUNT(*) AS cnt FROM citibike_trips_clean")
        stations = run_query("SELECT COUNT(*) AS cnt FROM citibike_stations_clean")
        members  = run_query("SELECT COUNT(*) AS cnt FROM citibike_trips_clean WHERE member_casual='member'")
        duration = run_query("SELECT ROUND(AVG(duration_minutes),1) AS avg_dur FROM citibike_trips_clean")
        return (
            int(trips["cnt"].iloc[0]),
            int(stations["cnt"].iloc[0]),
            int(members["cnt"].iloc[0]),
            float(duration["avg_dur"].iloc[0]) if duration["avg_dur"].iloc[0] else 0,
        )
    except Exception:
        return (0, 0, 0, 0)

total_trips, total_stations, total_members, avg_dur = get_metrics()

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="value">{total_trips:,}</div>
        <div class="label">Tổng chuyến đi</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="value">{total_stations:,}</div>
        <div class="label">Trạm xe</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="value">{total_members:,}</div>
        <div class="label">Chuyến của Member</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="value">{avg_dur}</div>
        <div class="label">Avg Duration (phút)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Pipeline Overview ─────────────────────────────────────────────────────────
st.subheader("🔧 Kiến trúc Pipeline")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    **Batch Pipeline**
    ```
    S3 CSV → HDFS Raw
           → Spark Clean
           → HDFS Processed (Parquet)
           → HDFS Exports (TSV)
           → MapReduce Analysis
           → Sqoop → MySQL
    ```
    """)
with c2:
    st.markdown("""
    **Realtime Pipeline**
    ```
    GBFS Station Status JSON
           → Kafka Topic
           → Consumer
           → MySQL Stream Table
    ```
    """)

st.markdown("---")

# ── Bảng dữ liệu gần nhất ────────────────────────────────────────────────────
st.subheader("🗓️ 10 chuyến đi gần nhất")

@st.cache_data(ttl=30)
def get_recent_trips():
    return run_query("""
        SELECT ride_id, rideable_type, started_at, ended_at,
               ROUND(duration_minutes,1) AS duration_minutes,
               start_station_name, end_station_name, member_casual
        FROM citibike_trips_clean
        ORDER BY started_at DESC
        LIMIT 10
    """)

df = get_recent_trips()
if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Chưa có dữ liệu chuyến đi.")

