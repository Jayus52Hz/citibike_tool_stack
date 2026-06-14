import os
import sys
import uuid
from datetime import datetime, time

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db_config import run_query, run_write


st.set_page_config(page_title="Manage Trips", page_icon="🚲", layout="wide")
st.title("Manage Trips")
st.caption("View, add, update, and delete trip records in MySQL.")


with st.sidebar:
    st.header("Filters")
    filter_type = st.selectbox("Bike type", ["All", "electric_bike", "classic_bike"])
    filter_member = st.selectbox("Customer type", ["All", "member", "casual"])
    search_station = st.text_input("Start station contains", "")
    limit = st.slider("Rows to show", 10, 200, 50, 10)


def build_where():
    conds, params = [], []
    if filter_type != "All":
        conds.append("rideable_type = %s")
        params.append(filter_type)
    if filter_member != "All":
        conds.append("member_casual = %s")
        params.append(filter_member)
    if search_station.strip():
        conds.append("start_station_name LIKE %s")
        params.append(f"%{search_station.strip()}%")
    where = "WHERE " + " AND ".join(conds) if conds else ""
    return where, params


@st.cache_data(ttl=15)
def fetch_trips(where, params_tuple, limit):
    sql = f"""
        SELECT ride_id, rideable_type, started_at, ended_at,
               ROUND(duration_minutes, 2) AS duration_minutes,
               start_station_name, end_station_name, member_casual
        FROM citibike_trips_clean
        {where}
        ORDER BY started_at DESC
        LIMIT {int(limit)}
    """
    return run_query(sql, list(params_tuple))


def combine_dt(date_value, time_value):
    return datetime.combine(date_value, time_value)


where, params = build_where()
df = fetch_trips(where, tuple(params), limit)

tab_table, tab_create, tab_update, tab_delete = st.tabs(["Table", "Add", "Update", "Delete"])

with tab_table:
    st.info(f"Showing {len(df)} trip records")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download current rows as CSV",
        df.to_csv(index=False).encode("utf-8"),
        "trips_export.csv",
        "text/csv",
    )

with tab_create:
    st.subheader("Add Trip")
    now = datetime.now().replace(second=0, microsecond=0)
    with st.form("add_trip_form", clear_on_submit=True):
        ride_id = st.text_input("Ride ID", value=str(uuid.uuid4()).replace("-", "").upper()[:16])
        rideable_type = st.selectbox("Bike type", ["electric_bike", "classic_bike"])
        member_casual = st.selectbox("Customer type", ["member", "casual"])
        c1, c2 = st.columns(2)
        with c1:
            start_date = st.date_input("Started date", value=now.date())
            start_time = st.time_input("Started time", value=now.time().replace(second=0, microsecond=0))
            start_station_name = st.text_input("Start station name")
        with c2:
            end_date = st.date_input("Ended date", value=now.date())
            end_time = st.time_input("Ended time", value=time(hour=min(now.hour + 1, 23), minute=now.minute))
            end_station_name = st.text_input("End station name")
        duration_minutes = st.number_input("Duration minutes", min_value=0.0, value=10.0, step=0.5)
        submitted = st.form_submit_button("Add trip", type="primary")

    if submitted:
        if not ride_id.strip():
            st.error("Ride ID is required.")
        else:
            run_write(
                """
                INSERT INTO citibike_trips_clean
                  (ride_id, rideable_type, started_at, ended_at, duration_minutes,
                   start_station_name, end_station_name, member_casual)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    ride_id.strip(),
                    rideable_type,
                    combine_dt(start_date, start_time),
                    combine_dt(end_date, end_time),
                    float(duration_minutes),
                    start_station_name.strip() or None,
                    end_station_name.strip() or None,
                    member_casual,
                ),
            )
            st.cache_data.clear()
            st.success("Trip added.")
            st.rerun()

with tab_update:
    st.subheader("Update Trip")
    if df.empty:
        st.info("No rows match the current filters.")
    else:
        selected_id = st.selectbox("Select trip", df["ride_id"].tolist())
        row = df.loc[df["ride_id"] == selected_id].iloc[0]
        with st.form("update_trip_form"):
            rideable_type = st.selectbox(
                "Bike type",
                ["electric_bike", "classic_bike"],
                index=0 if row.get("rideable_type") == "electric_bike" else 1,
            )
            member_casual = st.selectbox(
                "Customer type",
                ["member", "casual"],
                index=0 if row.get("member_casual") == "member" else 1,
            )
            duration_minutes = st.number_input(
                "Duration minutes",
                min_value=0.0,
                value=float(row.get("duration_minutes") or 0),
                step=0.5,
            )
            start_station_name = st.text_input("Start station name", value=str(row.get("start_station_name") or ""))
            end_station_name = st.text_input("End station name", value=str(row.get("end_station_name") or ""))
            submitted = st.form_submit_button("Save changes", type="primary")

        if submitted:
            run_write(
                """
                UPDATE citibike_trips_clean
                SET rideable_type=%s, duration_minutes=%s,
                    start_station_name=%s, end_station_name=%s, member_casual=%s
                WHERE ride_id=%s
                """,
                (
                    rideable_type,
                    float(duration_minutes),
                    start_station_name.strip() or None,
                    end_station_name.strip() or None,
                    member_casual,
                    selected_id,
                ),
            )
            st.cache_data.clear()
            st.success("Trip updated.")
            st.rerun()

with tab_delete:
    st.subheader("Delete Trip")
    if df.empty:
        st.info("No rows match the current filters.")
    else:
        selected_id = st.selectbox("Trip to delete", df["ride_id"].tolist(), key="delete_trip_id")
        st.warning("This deletes one trip record from MySQL.")
        confirm = st.checkbox("I understand and want to delete this row")
        if st.button("Delete trip", type="primary", disabled=not confirm):
            run_write("DELETE FROM citibike_trips_clean WHERE ride_id=%s", (selected_id,))
            st.cache_data.clear()
            st.success("Trip deleted.")
            st.rerun()
