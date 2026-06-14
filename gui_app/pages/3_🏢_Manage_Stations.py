import os
import sys
import uuid

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db_config import run_query, run_write


st.set_page_config(page_title="Manage Stations", page_icon="🏢", layout="wide")
st.title("Manage Stations")
st.caption("View, add, update, and delete station records in MySQL.")


with st.sidebar:
    st.header("Filters")
    search_name = st.text_input("Station name contains", "")
    filter_rent = st.selectbox("Renting status", ["All", "Renting", "Not renting"])
    min_bikes = st.slider("Minimum available bikes", 0, 50, 0)
    limit = st.slider("Rows to show", 10, 200, 50, 10)


def build_where():
    conds, params = [], []
    if search_name.strip():
        conds.append("name LIKE %s")
        params.append(f"%{search_name.strip()}%")
    if filter_rent == "Renting":
        conds.append("is_renting = 1")
    elif filter_rent == "Not renting":
        conds.append("is_renting = 0")
    if min_bikes > 0:
        conds.append("num_bikes_available >= %s")
        params.append(min_bikes)
    where = "WHERE " + " AND ".join(conds) if conds else ""
    return where, params


@st.cache_data(ttl=15)
def fetch_stations(where, params_tuple, limit):
    sql = f"""
        SELECT station_id, name, short_name,
               ROUND(lat, 6) AS lat, ROUND(lon, 6) AS lon,
               capacity, num_bikes_available, num_docks_available,
               is_installed, is_renting, is_returning, last_reported
        FROM citibike_stations_clean
        {where}
        ORDER BY name ASC
        LIMIT {int(limit)}
    """
    return run_query(sql, list(params_tuple))


def int_or_none(value):
    return None if value is None else int(value)


def float_or_none(value):
    return None if value is None else float(value)


where, params = build_where()
df = fetch_stations(where, tuple(params), limit)

tab_table, tab_create, tab_update, tab_delete, tab_map = st.tabs(
    ["Table", "Add", "Update", "Delete", "Map"]
)

with tab_table:
    st.info(f"Showing {len(df)} station records")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download current rows as CSV",
        df.to_csv(index=False).encode("utf-8"),
        "stations_export.csv",
        "text/csv",
    )

with tab_create:
    st.subheader("Add Station")
    with st.form("add_station_form", clear_on_submit=True):
        station_id = st.text_input(
            "Station ID",
            value="ST_" + str(uuid.uuid4()).replace("-", "").upper()[:8],
        )
        name = st.text_input("Name")
        short_name = st.text_input("Short name")
        c1, c2, c3 = st.columns(3)
        with c1:
            lat = st.number_input("Latitude", value=40.0, format="%.6f")
            capacity = st.number_input("Capacity", min_value=0, value=0, step=1)
        with c2:
            lon = st.number_input("Longitude", value=-74.0, format="%.6f")
            bikes = st.number_input("Available bikes", min_value=0, value=0, step=1)
        with c3:
            docks = st.number_input("Available docks", min_value=0, value=0, step=1)
            is_installed = st.checkbox("Installed", value=True)
            is_renting = st.checkbox("Renting", value=True)
            is_returning = st.checkbox("Returning", value=True)

        submitted = st.form_submit_button("Add station", type="primary")

    if submitted:
        if not station_id.strip() or not name.strip():
            st.error("Station ID and name are required.")
        else:
            run_write(
                """
                INSERT INTO citibike_stations_clean
                  (station_id, name, short_name, lat, lon, capacity,
                   num_bikes_available, num_docks_available,
                   is_installed, is_renting, is_returning, last_reported)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
                """,
                (
                    station_id.strip(),
                    name.strip(),
                    short_name.strip() or None,
                    float_or_none(lat),
                    float_or_none(lon),
                    int_or_none(capacity),
                    int_or_none(bikes),
                    int_or_none(docks),
                    1 if is_installed else 0,
                    1 if is_renting else 0,
                    1 if is_returning else 0,
                ),
            )
            st.cache_data.clear()
            st.success("Station added.")
            st.rerun()

with tab_update:
    st.subheader("Update Station")
    if df.empty:
        st.info("No rows match the current filters.")
    else:
        options = df["station_id"].tolist()
        selected_id = st.selectbox(
            "Select station",
            options,
            format_func=lambda sid: f"{sid} - {df.loc[df['station_id'] == sid, 'name'].iloc[0]}",
        )
        row = df.loc[df["station_id"] == selected_id].iloc[0]

        with st.form("update_station_form"):
            name = st.text_input("Name", value=str(row.get("name") or ""))
            short_name = st.text_input("Short name", value=str(row.get("short_name") or ""))
            c1, c2, c3 = st.columns(3)
            with c1:
                lat = st.number_input("Latitude", value=float(row.get("lat") or 0), format="%.6f")
                capacity = st.number_input("Capacity", min_value=0, value=int(row.get("capacity") or 0), step=1)
            with c2:
                lon = st.number_input("Longitude", value=float(row.get("lon") or 0), format="%.6f")
                bikes = st.number_input("Available bikes", min_value=0, value=int(row.get("num_bikes_available") or 0), step=1)
            with c3:
                docks = st.number_input("Available docks", min_value=0, value=int(row.get("num_docks_available") or 0), step=1)
                is_installed = st.checkbox("Installed", value=bool(row.get("is_installed")))
                is_renting = st.checkbox("Renting", value=bool(row.get("is_renting")))
                is_returning = st.checkbox("Returning", value=bool(row.get("is_returning")))

            submitted = st.form_submit_button("Save changes", type="primary")

        if submitted:
            run_write(
                """
                UPDATE citibike_stations_clean
                SET name=%s, short_name=%s, lat=%s, lon=%s, capacity=%s,
                    num_bikes_available=%s, num_docks_available=%s,
                    is_installed=%s, is_renting=%s, is_returning=%s,
                    last_reported=NOW()
                WHERE station_id=%s
                """,
                (
                    name.strip() or None,
                    short_name.strip() or None,
                    float_or_none(lat),
                    float_or_none(lon),
                    int_or_none(capacity),
                    int_or_none(bikes),
                    int_or_none(docks),
                    1 if is_installed else 0,
                    1 if is_renting else 0,
                    1 if is_returning else 0,
                    selected_id,
                ),
            )
            st.cache_data.clear()
            st.success("Station updated.")
            st.rerun()

with tab_delete:
    st.subheader("Delete Station")
    if df.empty:
        st.info("No rows match the current filters.")
    else:
        selected_id = st.selectbox("Station to delete", df["station_id"].tolist(), key="delete_station_id")
        st.warning("This deletes one station record from MySQL.")
        confirm = st.checkbox("I understand and want to delete this row")
        if st.button("Delete station", type="primary", disabled=not confirm):
            run_write("DELETE FROM citibike_stations_clean WHERE station_id=%s", (selected_id,))
            st.cache_data.clear()
            st.success("Station deleted.")
            st.rerun()

with tab_map:
    st.subheader("Station Map")

    @st.cache_data(ttl=60)
    def fetch_map_data():
        return run_query(
            """
            SELECT name, lat, lon, capacity,
                   num_bikes_available, num_docks_available, is_renting
            FROM citibike_stations_clean
            WHERE lat IS NOT NULL AND lon IS NOT NULL
            LIMIT 500
            """
        )

    df_map = fetch_map_data()
    if df_map.empty:
        st.info("No map data available.")
    else:
        df_map["lat"] = pd.to_numeric(df_map["lat"], errors="coerce")
        df_map["lon"] = pd.to_numeric(df_map["lon"], errors="coerce")
        df_map = df_map.dropna(subset=["lat", "lon"])
        fig = px.scatter_mapbox(
            df_map,
            lat="lat",
            lon="lon",
            hover_name="name",
            hover_data={
                "num_bikes_available": True,
                "num_docks_available": True,
                "capacity": True,
            },
            color="num_bikes_available",
            color_continuous_scale="RdYlGn",
            size="capacity",
            size_max=15,
            zoom=11,
            height=520,
            mapbox_style="carto-positron",
        )
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
