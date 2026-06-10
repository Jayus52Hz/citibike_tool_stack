"""
pages/1_📊_Dashboard.py - Dashboard MapReduce Results (Table + Chart mode)
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db_config import run_query

st.set_page_config(page_title="MR Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.dash-header {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 16px; padding: 28px 36px; margin-bottom: 24px; color: white;
}
.dash-header h1 { font-size: 2rem; font-weight: 700; margin: 0; }
.dash-header p  { color: #a0c4d8; margin: 6px 0 0; font-size: 0.95rem; }

.section-label {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #64748b; margin-bottom: 4px;
}
.kpi-row { display: flex; gap: 16px; margin-bottom: 24px; }
.kpi-card {
    flex: 1; background: #1e293b; border: 1px solid #334155;
    border-radius: 12px; padding: 18px 20px; color: white;
}
.kpi-card .val { font-size: 1.9rem; font-weight: 700; color: #38bdf8; }
.kpi-card .lbl { font-size: 0.78rem; color: #94a3b8; margin-top: 2px; }
.no-data {
    background: #1e293b; border: 1px dashed #334155; border-radius: 10px;
    padding: 20px; text-align: center; color: #64748b; font-size: 0.85rem;
}
.job-header {
    display: flex; align-items: center; gap: 10px;
    background: #1e293b; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px;
}
.job-badge {
    background: #0f3460; color: #38bdf8; font-weight: 700;
    font-size: 0.78rem; padding: 4px 10px; border-radius: 6px; white-space: nowrap;
}
.job-title { color: #e2e8f0; font-weight: 600; font-size: 0.95rem; }
.job-desc  { color: #64748b; font-size: 0.78rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <h1>📊 MapReduce Analysis Dashboard</h1>
  <p>8 Hadoop MapReduce jobs • Citi Bike NYC — chọn chế độ hiển thị bên dưới</p>
</div>
""", unsafe_allow_html=True)

# ── Toggle chế độ toàn cục ───────────────────────────────────────────────────
col_toggle, col_info = st.columns([2, 5])
with col_toggle:
    view_mode = st.radio(
        "Chế độ hiển thị",
        ["📋 Bảng dữ liệu", "📊 Biểu đồ"],
        horizontal=True,
        label_visibility="collapsed"
    )

is_chart = (view_mode == "📊 Biểu đồ")

DARK_BG  = "#0f172a"
GRID_CLR = "#1e293b"

def chart_layout(fig, height=320):
    fig.update_layout(
        height=height, paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG,
        font=dict(color="#cbd5e1", family="DM Sans"),
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
    )
    return fig

def safe_query(sql):
    try:
        df = run_query(sql)
        return df if not df.empty else None
    except:
        return None

def no_data(label):
    st.markdown(f'<div class="no-data">⏳ Chưa có dữ liệu — {label}</div>', unsafe_allow_html=True)

def job_header(num, title, desc):
    st.markdown(f"""
    <div class="job-header">
      <span class="job-badge">MR{num}</span>
      <div>
        <div class="job-title">{title}</div>
        <div class="job-desc">{desc}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def show_table(df, key="mr", height=300):
    st.dataframe(
        df, use_container_width=True, hide_index=True,
        height=height
    )
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Tải CSV", csv, f"{key}_data.csv", "text/csv",
        use_container_width=True, key=f"dl_{key}"
    )

# ── KPI từ MR1 ────────────────────────────────────────────────────────────────
df1_kpi = safe_query("SELECT * FROM rpt_mr1_user_behavior")
if df1_kpi is not None:
    total = df1_kpi["total_trips"].sum()
    avg_d = (df1_kpi["avg_duration"] * df1_kpi["total_trips"]).sum() / total if total else 0
    n_types = df1_kpi["user_and_bike_type"].nunique()
    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-card"><div class="val">{total:,}</div><div class="lbl">Tổng chuyến đi</div></div>
      <div class="kpi-card"><div class="val">{avg_d:.1f} phút</div><div class="lbl">Avg duration</div></div>
      <div class="kpi-card"><div class="val">{n_types}</div><div class="lbl">Nhóm user × loại xe</div></div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# MR1 + MR2
# ═══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns(2)

with col1:
    job_header(1, "Hành vi người dùng theo loại xe",
               "Avg duration & số chuyến theo member/casual × bike type")
    df = safe_query("SELECT * FROM rpt_mr1_user_behavior ORDER BY total_trips DESC")
    if df is not None:
        if not is_chart:
            show_table(df, key="mr1")
        else:
            df[["user_type","bike_type"]] = df["user_and_bike_type"].str.split(",", n=1, expand=True)
            fig = px.bar(df, x="user_and_bike_type", y="total_trips",
                         color="user_type", text="total_trips",
                         color_discrete_map={"member":"#38bdf8","casual":"#f472b6"},
                         labels={"user_and_bike_type":"","total_trips":"Số chuyến"})
            fig.update_traces(textposition="outside")
            st.plotly_chart(chart_layout(fig, 280), use_container_width=True)

            fig2 = px.bar(df, x="user_and_bike_type", y="avg_duration",
                          color="bike_type", text_auto=".1f",
                          color_discrete_sequence=["#34d399","#fb923c"],
                          labels={"user_and_bike_type":"","avg_duration":"Avg (phút)"})
            fig2.update_traces(textposition="outside")
            st.caption("⏱ Thời gian trung bình (phút)")
            st.plotly_chart(chart_layout(fig2, 220), use_container_width=True)
    else:
        no_data("MR1")

with col2:
    job_header(2, "Top tuyến đường phổ biến nhất",
               "Các tuyến start → end được đi nhiều nhất")
    df = safe_query("SELECT * FROM rpt_mr2_top_routes ORDER BY trip_count DESC LIMIT 10")
    if df is not None:
        if not is_chart:
            show_table(df, key="mr2")
        else:
            df["short"] = df["route_name"].str[:48]
            fig = px.bar(df, x="trip_count", y="short", orientation="h",
                         color="trip_count", color_continuous_scale="Blues",
                         labels={"trip_count":"Số chuyến","short":""},
                         text_auto=True)
            fig.update_layout(yaxis={"categoryorder":"total ascending"}, coloraxis_showscale=False)
            fig.update_traces(textposition="outside")
            st.plotly_chart(chart_layout(fig, 420), use_container_width=True)
    else:
        no_data("MR2")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# MR3 + MR4
# ═══════════════════════════════════════════════════════════════════════════════
col3, col4 = st.columns(2)

with col3:
    job_header(3, "Giờ cao điểm trong ngày (0–23h)",
               "Phân bố số chuyến đi theo từng khung giờ")
    df = safe_query("SELECT * FROM rpt_mr3_hourly_trends ORDER BY hour_of_day")
    if df is not None:
        if not is_chart:
            show_table(df, key="mr3")
        else:
            peak = df.loc[df["total_trips"].idxmax(), "hour_of_day"]
            st.caption(f"⚡ Peak hour: **{peak}:00** — {df['total_trips'].max():,} chuyến")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["hour_of_day"], y=df["total_trips"],
                mode="lines+markers",
                line=dict(color="#38bdf8", width=2.5),
                marker=dict(size=6, color="#f472b6"),
                fill="tozeroy", fillcolor="rgba(56,189,248,0.12)"
            ))
            fig.update_layout(xaxis_title="Giờ", yaxis_title="Số chuyến",
                              xaxis=dict(tickmode="linear", dtick=2))
            st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
    else:
        no_data("MR3")

with col4:
    job_header(4, "Phân tích theo ngày trong tuần",
               "Member vs Casual qua các ngày Monday → Sunday")
    df = safe_query("SELECT * FROM rpt_mr4_weekly_analysis")
    if df is not None:
        if not is_chart:
            show_table(df, key="mr4")
        else:
            DAY_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            df["day_of_week"] = pd.Categorical(df["day_of_week"], categories=DAY_ORDER, ordered=True)
            df = df.sort_values("day_of_week")
            fig = px.bar(df, x="day_of_week", y="total_trips", color="user_type",
                         barmode="group",
                         color_discrete_map={"member":"#38bdf8","casual":"#f472b6"},
                         labels={"day_of_week":"","total_trips":"Số chuyến","user_type":"Loại KH"},
                         text_auto=True)
            fig.update_traces(textposition="outside", textfont_size=9)
            st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
    else:
        no_data("MR4")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# MR5 + MR6
# ═══════════════════════════════════════════════════════════════════════════════
col5, col6 = st.columns(2)

with col5:
    job_header(5, "Khoảng cách trung bình theo tuyến",
               "Avg distance (km) và số chuyến mỗi tuyến")
    df = safe_query("SELECT * FROM rpt_mr5_distance_calc ORDER BY avg_distance_km DESC LIMIT 10")
    if df is not None:
        if not is_chart:
            show_table(df, key="mr5")
        else:
            df["short"] = df["route_name"].str[:40]
            fig = px.bar(df, x="avg_distance_km", y="short", orientation="h",
                         color="avg_distance_km", color_continuous_scale="Greens",
                         labels={"avg_distance_km":"Km","short":""},
                         text_auto=".2f")
            fig.update_layout(yaxis={"categoryorder":"total ascending"}, coloraxis_showscale=False)
            st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
    else:
        no_data("MR5")

with col6:
    job_header(6, "Phân bố thời lượng chuyến đi",
               "Nhóm duration_minutes để nhìn nhanh hành vi sử dụng")
    df = safe_query("""
        SELECT duration_bucket, COUNT(*) AS trip_count
        FROM (
            SELECT
                CASE
                    WHEN duration_minutes < 5 THEN '< 5 phút'
                    WHEN duration_minutes < 10 THEN '5-10 phút'
                    WHEN duration_minutes < 20 THEN '10-20 phút'
                    WHEN duration_minutes < 30 THEN '20-30 phút'
                    WHEN duration_minutes < 60 THEN '30-60 phút'
                    ELSE '>= 60 phút'
                END AS duration_bucket,
                CASE
                    WHEN duration_minutes < 5 THEN 1
                    WHEN duration_minutes < 10 THEN 2
                    WHEN duration_minutes < 20 THEN 3
                    WHEN duration_minutes < 30 THEN 4
                    WHEN duration_minutes < 60 THEN 5
                    ELSE 6
                END AS bucket_order
            FROM citibike_trips_clean
            WHERE duration_minutes IS NOT NULL
        ) x
        GROUP BY duration_bucket, bucket_order
        ORDER BY bucket_order
    """)
    if df is not None:
        if not is_chart:
            show_table(df, key="mr6")
        else:
            fig = px.bar(
                df,
                x="duration_bucket",
                y="trip_count",
                color="trip_count",
                color_continuous_scale=["#38bdf8", "#f472b6"],
                text="trip_count",
                labels={"duration_bucket": "", "trip_count": "Số chuyến"},
            )
            fig.update_layout(
                coloraxis_showscale=False,
                margin=dict(t=20, b=40, l=10, r=20),
                xaxis_title="Nhóm thời lượng",
                yaxis_title="Số chuyến",
            )
            fig.update_traces(
                textposition="outside",
                cliponaxis=False,
                hovertemplate="<b>%{x}</b><br>Số chuyến: %{y}<extra></extra>",
            )
            st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
    else:
        no_data("MR6")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# MR7 + MR8
# ═══════════════════════════════════════════════════════════════════════════════
col7, col8 = st.columns(2)

with col7:
    job_header(7, "Phân loại trạm theo capacity",
               "Small / Medium / Large station distribution")
    df = safe_query("SELECT * FROM rpt_mr7_station_capacity ORDER BY station_count DESC")
    if df is not None:
        if not is_chart:
            show_table(df, key="mr7")
        else:
            fig = px.pie(df, names="capacity_group", values="station_count",
                         color_discrete_sequence=["#38bdf8","#34d399","#f472b6"],
                         hole=0.45)
            fig.update_traces(textposition="outside", textinfo="label+value")
            fig.update_layout(showlegend=False)
            st.plotly_chart(chart_layout(fig, 340), use_container_width=True)
    else:
        no_data("MR7")

with col8:
    job_header(8, "Trạng thái hoạt động trạm xe",
               "Active vs Maintenance/Locked stations")
    df = safe_query("SELECT * FROM rpt_mr8_station_status_check ORDER BY status_count DESC")
    if df is not None:
        if not is_chart:
            show_table(df, key="mr8")
        else:
            total_s = df["status_count"].sum()
            if not is_chart:
                show_table(df, key="mr8b")
            else:
                # Status cards + bar
                for _, row in df.iterrows():
                    pct   = row["status_count"] / total_s * 100
                    color = "#34d399" if "ACTIVE" in row["station_status"] else "#f87171"
                    st.markdown(f"""
                    <div style="background:#1e293b;border-radius:10px;padding:12px 16px;
                                margin-bottom:8px;border-left:4px solid {color}">
                        <div style="color:{color};font-weight:700;font-size:1.2rem">{row['status_count']:,}</div>
                        <div style="color:#94a3b8;font-size:0.8rem">{row['station_status']} — {pct:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                fig = px.bar(df, x="station_status", y="status_count",
                             color="station_status",
                             color_discrete_map={
                                 "ACTIVE_STATION":"#34d399",
                                 "MAINTENANCE_OR_LOCKED_STATION":"#f87171"
                             },
                             text_auto=True,
                             labels={"station_status":"","status_count":"Số trạm"})
                fig.update_layout(showlegend=False)
                fig.update_traces(textposition="outside", textfont_size=14)
                st.plotly_chart(chart_layout(fig, 240), use_container_width=True)
    else:
        no_data("MR8")

st.divider()
st.caption("🔄 Dữ liệu từ MySQL • Cập nhật sau mỗi lần chạy MapReduce + Sqoop Export")
