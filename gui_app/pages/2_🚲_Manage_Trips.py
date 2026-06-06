"""
pages/2_🚲_Manage_Trips.py - Interactive CRUD cho bảng citibike_trips_clean
"""
import streamlit as st
import pandas as pd
import sys, os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db_config import run_query, run_write

st.set_page_config(page_title="Quản lý Chuyến đi", page_icon="🚲", layout="wide")
st.title("🚲 Quản lý Chuyến Đi (Interactive CRUD)")
st.caption("Thao tác trực tiếp trên bảng: Click đúp vào ô để **Sửa**, bấm icon ➕ dưới cùng để **Thêm**, chọn dòng và bấm Delete để **Xóa**.")

# ── Sidebar filter ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Bộ lọc")
    filter_type = st.selectbox("Loại xe", ["Tất cả", "electric_bike", "classic_bike"])
    filter_member = st.selectbox("Loại KH", ["Tất cả", "member", "casual"])
    search_station = st.text_input("Tìm theo trạm xuất phát", "")
    limit = st.slider("Số dòng hiển thị", 10, 200, 50, 10)

# ── Build WHERE ───────────────────────────────────────────────────────────────
def build_where():
    conds, params = [], []
    if filter_type != "Tất cả":
        conds.append("rideable_type = %s"); params.append(filter_type)
    if filter_member != "Tất cả":
        conds.append("member_casual = %s"); params.append(filter_member)
    if search_station.strip():
        conds.append("start_station_name LIKE %s"); params.append(f"%{search_station.strip()}%")
    where = ("WHERE " + " AND ".join(conds)) if conds else ""
    return where, params

where, params = build_where()

@st.cache_data(ttl=15)
def fetch_trips(where, params_tuple, limit):
    sql = f"""
        SELECT ride_id, rideable_type,
               started_at, ended_at,
               ROUND(duration_minutes,2) AS duration_minutes,
               start_station_name, end_station_name, member_casual
        FROM citibike_trips_clean
        {where}
        ORDER BY started_at DESC
        LIMIT {limit}
    """
    return run_query(sql, list(params_tuple))

# Kéo dữ liệu gốc lên
df = fetch_trips(where, tuple(params), limit)

# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE DATA EDITOR (CRUD Tích hợp)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📋 Bảng Dữ Liệu Tương Tác")

with st.form("editor_form"):
    # Cấu hình các cột để trải nghiệm nhập liệu chuyên nghiệp hơn (Dropdown thay vì gõ text)
    edited_df = st.data_editor(
        df,
        num_rows="dynamic", # Cho phép thêm/xóa dòng
        key="trips_editor",
        use_container_width=True,
        hide_index=True,
        column_config={
            "ride_id": st.column_config.TextColumn("Ride ID", required=True, disabled=True), # Khóa không cho sửa ID cũ
            "rideable_type": st.column_config.SelectboxColumn("Loại xe", options=["electric_bike", "classic_bike"], required=True),
            "member_casual": st.column_config.SelectboxColumn("Loại KH", options=["member", "casual"], required=True),
            "duration_minutes": st.column_config.NumberColumn("Thời gian (phút)", min_value=0.0, format="%.2f"),
        }
    )
    
    # Nút bấm để xác nhận toàn bộ thay đổi đẩy xuống Database
    submit_button = st.form_submit_button("💾 Lưu tất cả thay đổi", type="primary")

if submit_button:
    # Lấy ra bộ nhớ đệm (những ô/dòng mà người dùng vừa tương tác)
    changes = st.session_state["trips_editor"]
    
    try:
        # 1. Xử lý DELETE (Xóa dòng)
        for row_idx in changes.get("deleted_rows", []):
            ride_id_del = df.iloc[row_idx]['ride_id']
            run_write("DELETE FROM citibike_trips_clean WHERE ride_id=%s", (ride_id_del,))

        # 2. Xử lý UPDATE (Sửa ô)
        for row_idx, edits in changes.get("edited_rows", {}).items():
            ride_id_upd = df.iloc[row_idx]['ride_id']
            # Tự động render chuỗi truy vấn dựa trên cột bị sửa (VD: "duration_minutes = %s")
            set_clause = ", ".join([f"{k} = %s" for k in edits.keys()])
            values = list(edits.values())
            values.append(ride_id_upd)
            sql = f"UPDATE citibike_trips_clean SET {set_clause} WHERE ride_id = %s"
            run_write(sql, tuple(values))

        # 3. Xử lý CREATE (Thêm dòng mới)
        for new_row in changes.get("added_rows", []):
            # Tự động tạo mã Ride ID ngẫu nhiên (16 ký tự) cho chuyến đi mới
            if "ride_id" not in new_row or not new_row["ride_id"]:
                new_row["ride_id"] = str(uuid.uuid4()).replace("-", "").upper()[:16]
                
            # Lọc bỏ các cột trống, lấy đúng cột người dùng đã điền
            cols = list(new_row.keys())
            placeholders = ", ".join(["%s"] * len(cols))
            col_names = ", ".join(cols)
            values = tuple(new_row.values())
            sql = f"INSERT INTO citibike_trips_clean ({col_names}) VALUES ({placeholders})"
            run_write(sql, values)
            
        st.success("✅ Cập nhật dữ liệu thành công!")
        st.cache_data.clear() # Xóa cache để load lại bảng mới
        st.rerun()          # Tự động tải lại trang ngay lập tức
        
    except Exception as e:
        st.error(f"❌ Có lỗi xảy ra trong quá trình lưu dữ liệu: {e}")

# ── Nút tải CSV vẫn giữ nguyên ─────────────────────────────────────────────────
st.divider()
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Tải dữ liệu hiện tại (CSV)", csv, "trips_export.csv", "text/csv")