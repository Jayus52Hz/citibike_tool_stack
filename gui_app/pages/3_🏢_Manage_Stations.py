"""
pages/3_🏢_Manage_Stations.py - Interactive CRUD cho bảng citibike_stations_clean
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db_config import run_query, run_write

st.set_page_config(page_title="Quản lý Trạm xe", page_icon="🏢", layout="wide")
st.title("🏢 Quản lý Trạm Xe (Interactive CRUD)")
st.caption("Thao tác trực tiếp trên bảng: Click đúp vào ô để **Sửa**, bấm icon ➕ dưới cùng để **Thêm**, chọn dòng và bấm Delete để **Xóa**.")

# ── Sidebar filter ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Bộ lọc")
    search_name  = st.text_input("Tìm theo tên trạm", "")
    filter_rent  = st.selectbox("Đang cho thuê?", ["Tất cả", "Có", "Không"])
    min_bikes    = st.slider("Số xe khả dụng tối thiểu", 0, 50, 0)
    limit        = st.slider("Số dòng hiển thị", 10, 200, 50, 10)

# ── Tab layout ────────────────────────────────────────────────────────────────
tab_data, tab_map = st.tabs(["📋 Bảng dữ liệu tương tác", "🗺️ Bản đồ vị trí"])

# ── Build WHERE ───────────────────────────────────────────────────────────────
def build_where():
    conds, params = [], []
    if search_name.strip():
        conds.append("name LIKE %s"); params.append(f"%{search_name.strip()}%")
    if filter_rent == "Có":
        conds.append("is_renting = 1")
    elif filter_rent == "Không":
        conds.append("is_renting = 0")
    if min_bikes > 0:
        conds.append("num_bikes_available >= %s"); params.append(min_bikes)
    where = ("WHERE " + " AND ".join(conds)) if conds else ""
    return where, params

where, params = build_where()

# ═══════════════════════════════════════════════════════════════════════════════
# DATA EDITOR (CRUD Tích hợp)
# ═══════════════════════════════════════════════════════════════════════════════
with tab_data:
    @st.cache_data(ttl=15)
    def fetch_stations(where, params_tuple, limit):
        sql = f"""
            SELECT station_id, name, ROUND(lat,6) AS lat, ROUND(lon,6) AS lon,
                   capacity, num_bikes_available, num_docks_available,
                   CAST(is_installed AS UNSIGNED) AS is_installed, 
                   CAST(is_renting AS UNSIGNED) AS is_renting, 
                   CAST(is_returning AS UNSIGNED) AS is_returning
            FROM citibike_stations_clean
            {where}
            ORDER BY name ASC
            LIMIT {limit}
        """
        return run_query(sql, list(params_tuple))

    df = fetch_stations(where, tuple(params), limit)
    
    # Ép kiểu dữ liệu boolean để hiển thị Checkbox cho đẹp
    for col in ['is_installed', 'is_renting', 'is_returning']:
        if col in df.columns:
            df[col] = df[col].astype(bool)

    st.info(f"Đang hiển thị {len(df)} trạm")

    with st.form("station_editor_form"):
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            key="stations_editor",
            use_container_width=True,
            hide_index=True,
            column_config={
                "station_id": st.column_config.TextColumn("Station ID", disabled=True),
                "name": st.column_config.TextColumn("Tên trạm", required=True),
                "lat": st.column_config.NumberColumn("Latitude", format="%.6f"),
                "lon": st.column_config.NumberColumn("Longitude", format="%.6f"),
                "capacity": st.column_config.NumberColumn("Capacity", min_value=0, step=1),
                "num_bikes_available": st.column_config.NumberColumn("Xe trống", min_value=0, step=1),
                "num_docks_available": st.column_config.NumberColumn("Dock trống", min_value=0, step=1),
                "is_installed": st.column_config.CheckboxColumn("Đã lắp đặt?"),
                "is_renting": st.column_config.CheckboxColumn("Cho thuê?"),
                "is_returning": st.column_config.CheckboxColumn("Nhận trả?"),
            }
        )
        
        submit_button = st.form_submit_button("💾 Lưu tất cả thay đổi", type="primary")

    if submit_button:
        changes = st.session_state["stations_editor"]
        try:
            # 1. Xử lý DELETE
            for row_idx in changes.get("deleted_rows", []):
                del_id = df.iloc[row_idx]['station_id']
                run_write("DELETE FROM citibike_stations_clean WHERE station_id=%s", (del_id,))

            # 2. Xử lý UPDATE
            for row_idx, edits in changes.get("edited_rows", {}).items():
                upd_id = df.iloc[row_idx]['station_id']
                # Xử lý True/False thành 1/0 cho MySQL
                for k, v in edits.items():
                    if isinstance(v, bool): edits[k] = 1 if v else 0
                        
                set_clause = ", ".join([f"{k} = %s" for k in edits.keys()])
                values = list(edits.values())
                values.append(upd_id)
                sql = f"UPDATE citibike_stations_clean SET {set_clause} WHERE station_id = %s"
                run_write(sql, tuple(values))

            # 3. Xử lý CREATE
            for new_row in changes.get("added_rows", []):
                if "station_id" not in new_row or not new_row["station_id"]:
                    new_row["station_id"] = "ST_" + str(uuid.uuid4()).replace("-", "").upper()[:8]
                
                for k, v in new_row.items():
                    if isinstance(v, bool): new_row[k] = 1 if v else 0
                        
                cols = list(new_row.keys())
                placeholders = ", ".join(["%s"] * len(cols))
                col_names = ", ".join(cols)
                values = tuple(new_row.values())
                sql = f"INSERT INTO citibike_stations_clean ({col_names}) VALUES ({placeholders})"
                run_write(sql, values)
                
            st.success("✅ Cập nhật dữ liệu trạm thành công!")
            st.cache_data.clear()
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra trong quá trình lưu: {e}")

    # Nút tải CSV
    st.divider()
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Tải dữ liệu hiện tại (CSV)", csv, "stations_export.csv", "text/csv")


# ═══════════════════════════════════════════════════════════════════════════════
# MAP
# ═══════════════════════════════════════════════════════════════════════════════
with tab_map:
    st.subheader("🗺️ Bản đồ vị trí trạm xe")

    @st.cache_data(ttl=60)
    def fetch_map_data():
        return run_query("""
            SELECT name, lat, lon, capacity,
                   num_bikes_available, num_docks_available, is_renting
            FROM citibike_stations_clean
            WHERE lat IS NOT NULL AND lon IS NOT NULL
            LIMIT 500
        """)

    df_map = fetch_map_data()
    if not df_map.empty:
        df_map["lat"] = pd.to_numeric(df_map["lat"], errors="coerce")
        df_map["lon"] = pd.to_numeric(df_map["lon"], errors="coerce")
        df_map = df_map.dropna(subset=["lat","lon"])

        fig = px.scatter_mapbox(
            df_map, lat="lat", lon="lon",
            hover_name="name",
            hover_data={"num_bikes_available":True,"num_docks_available":True,"capacity":True},
            color="num_bikes_available",
            color_continuous_scale="RdYlGn",
            size="capacity", size_max=15,
            zoom=11, height=500,
            mapbox_style="carto-positron",
            labels={"num_bikes_available":"Xe khả dụng"}
        )
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🟢 Xanh = nhiều xe | 🔴 Đỏ = ít xe")
    else:
        st.info("Không có dữ liệu để hiển thị bản đồ.")