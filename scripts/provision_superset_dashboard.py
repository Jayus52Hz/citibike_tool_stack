"""
Provision the Citi Bike Superset dashboard from the processed MySQL report tables.

Run this script inside the Superset container. The companion PowerShell wrapper
`provision-superset-dashboard.ps1` copies it into the container and executes it.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from superset.app import create_app


DATABASE_NAME = "MySQL testdb"
DATABASE_URI = "mysql+pymysql://testuser:testpass@mysql:3306/testdb"
DASHBOARD_TITLE = "Citi Bike MapReduce Report"
DASHBOARD_SLUG = "citibike-mapreduce-report"


DASHBOARD_CSS = """
.dashboard {
  background:
    linear-gradient(135deg, rgba(11, 37, 69, 0.06), rgba(0, 166, 153, 0.05)),
    #f5f7fb;
}

.dashboard-header-container {
  margin: 12px 18px 4px;
  border-radius: 18px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  background:
    linear-gradient(135deg, rgba(16, 32, 51, 0.98), rgba(15, 76, 92, 0.96));
  color: #ffffff;
  box-shadow: 0 16px 42px rgba(15, 23, 42, 0.16);
}

.dashboard-header-container .dashboard-component-header,
.dashboard-header-container h1,
.dashboard-header-container span,
.dashboard-header-container div {
  color: #ffffff;
}

.dashboard-header-container button,
.dashboard-header-container a {
  border-radius: 999px;
}

.dashboard .dashboard-grid {
  max-width: 1440px;
  margin: 0 auto;
  padding: 12px 18px 40px;
}

.dashboard .dashboard-component.dashboard-component-chart-holder {
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 18px !important;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

.dashboard .dashboard-component.dashboard-component-chart-holder::before {
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: linear-gradient(90deg, #00a699, #2b6cb0, #f59e0b);
  z-index: 2;
}

.dashboard .dashboard-component.dashboard-component-chart-holder:hover {
  transform: translateY(-2px);
  border-color: rgba(0, 166, 153, 0.28);
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.12);
}

.dashboard .dashboard-chart-id-1::before { background: linear-gradient(90deg, #00a699, #34d399); }
.dashboard .dashboard-chart-id-2::before { background: linear-gradient(90deg, #2b6cb0, #60a5fa); }
.dashboard .dashboard-chart-id-3::before { background: linear-gradient(90deg, #f06c64, #f59e0b); }
.dashboard .dashboard-chart-id-4::before { background: linear-gradient(90deg, #0f4c5c, #00a699); }
.dashboard .dashboard-chart-id-5::before { background: linear-gradient(90deg, #f59e0b, #ef4444); }
.dashboard .dashboard-chart-id-6::before { background: linear-gradient(90deg, #475569, #94a3b8); }
.dashboard .dashboard-chart-id-7::before { background: linear-gradient(90deg, #00a699, #f06c64); }

.dashboard .dashboard-component-chart-holder .chart-header,
.dashboard .dashboard-component-chart-holder .header {
  padding: 14px 18px 4px;
}

.dashboard .dashboard-component-chart-holder .header-title,
.dashboard .dashboard-component-chart-holder .chart-header .editable-title {
  color: #102033;
  font-weight: 800;
  letter-spacing: 0;
}

.dashboard .dashboard-component-chart-holder .slice_container {
  padding: 0 10px 10px;
}

.dashboard .dashboard-component-chart-holder svg text {
  fill: #42526a;
  font-weight: 500;
}

.dashboard .dashboard-component-chart-holder .nv-axis path,
.dashboard .dashboard-component-chart-holder .nv-axis line {
  stroke: rgba(66, 82, 106, 0.18);
}

.dashboard .dashboard-component-chart-holder .nv-bar text {
  fill: #102033;
  font-weight: 700;
}

.dashboard .dashboard-component-markdown {
  border-radius: 18px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: #ffffff;
  box-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
}

.dashboard .dashboard-component-markdown .markdown {
  padding: 18px 22px;
}

.dashboard .dashboard-component-markdown h1 {
  margin: 0 0 8px;
  color: #102033;
  font-size: 30px;
  font-weight: 900;
  line-height: 1.15;
}

.dashboard .dashboard-component-markdown h2 {
  margin: 4px 0 8px;
  color: #102033;
  font-size: 18px;
  font-weight: 850;
}

.dashboard .dashboard-component-markdown p {
  margin: 0;
  color: #526173;
  font-size: 13px;
  line-height: 1.55;
}

.dashboard .dashboard-component-markdown strong {
  color: #006d77;
  font-weight: 850;
}

.dashboard .dashboard-component-markdown ul {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
}

.dashboard .dashboard-component-markdown li {
  padding: 8px 12px;
  border-radius: 999px;
  background: #eef7f6;
  color: #0f4c5c;
  font-size: 12px;
  font-weight: 750;
}

.dashboard .dashboard-component-row {
  margin-bottom: 12px;
}
"""


TABLES = [
    "citibike_trips_clean",
    "rpt_mr1_user_behavior",
    "rpt_mr2_top_routes",
    "rpt_mr3_hourly_trends",
    "rpt_mr4_weekly_analysis",
    "rpt_mr5_distance_calc",
    "rpt_mr6_anomaly_detection",
    "rpt_mr7_station_capacity",
    "rpt_mr8_station_status_check",
]


def metric(label: str, expression: str) -> dict[str, str]:
    return {"label": label, "expressionType": "SQL", "sqlExpression": expression}


def base_params(viz_type: str, datasource: str, **kwargs: Any) -> dict[str, Any]:
    params: dict[str, Any] = {
        "datasource": datasource,
        "viz_type": viz_type,
        "adhoc_filters": [],
        "row_limit": 10000,
        "color_scheme": "supersetColors",
        "show_legend": True,
        "show_controls": False,
    }
    params.update(kwargs)
    return params


def query_context(
    datasource_id: int,
    form_data: dict[str, Any],
    columns: list[str] | None = None,
    groupby: list[str] | None = None,
    metrics: list[dict[str, str]] | None = None,
    orderby: list[list[Any]] | None = None,
    is_timeseries: bool = False,
) -> dict[str, Any]:
    query: dict[str, Any] = {
        "filters": [],
        "extras": {"having": "", "where": ""},
        "applied_time_extras": {},
        "columns": columns or [],
        "metrics": metrics or [],
        "orderby": orderby or [],
        "annotation_layers": [],
        "row_limit": form_data.get("row_limit", 10000),
        "series_limit": 0,
        "order_desc": form_data.get("order_desc", True),
        "is_timeseries": is_timeseries,
        "url_params": {},
        "custom_params": {},
        "custom_form_data": {},
    }
    if is_timeseries:
        query["extras"]["time_grain_sqla"] = form_data.get("time_grain_sqla", "P1D")
        query["time_range"] = form_data.get("time_range", "No filter")
        query["granularity"] = form_data.get("granularity_sqla")
        query["series_columns"] = groupby or []

    return {
        "datasource": {"id": datasource_id, "type": "table"},
        "force": False,
        "queries": [query],
        "form_data": form_data,
        "result_format": "json",
        "result_type": "full",
    }


def chart_node(chart_id: int, height: int, width: int = 6) -> dict[str, Any]:
    return {
        "type": "CHART",
        "id": f"CHART-{chart_id}",
        "children": [],
        "meta": {"chartId": chart_id, "height": height, "width": width},
    }


def row_node(row_id: str, children: list[str]) -> dict[str, Any]:
    return {
        "type": "ROW",
        "id": row_id,
        "children": children,
        "meta": {"background": "BACKGROUND_TRANSPARENT"},
    }


def layout_for_charts(chart_ids: list[int]) -> dict[str, Any]:
    root_id = "ROOT_ID"
    grid_id = "GRID_ID"
    row_ids = [f"ROW-{idx}" for idx in range(1, 5)]

    position: dict[str, Any] = {
        root_id: {"type": "ROOT", "id": root_id, "children": [grid_id]},
        grid_id: {"type": "GRID", "id": grid_id, "children": row_ids},
    }

    chart_nodes = [f"CHART-{chart_id}" for chart_id in chart_ids]
    chart_heights = [48, 50, 52, 48, 50, 42, 42]
    chart_widths = [6, 6, 6, 12, 6, 6, 6]
    for chart_id, height, width in zip(chart_ids, chart_heights, chart_widths):
        position[f"CHART-{chart_id}"] = chart_node(chart_id, height, width)

    row_children = [
        [chart_nodes[0], chart_nodes[2]],
        [chart_nodes[3]],
        [chart_nodes[1], chart_nodes[4]],
        [chart_nodes[5], chart_nodes[6]],
    ]
    for row_id, children in zip(row_ids, row_children):
        position[row_id] = row_node(row_id, children)

    return position


def main() -> None:
    app = create_app()
    with app.app_context():
        from flask_appbuilder.security.sqla.models import User

        from superset import db
        from superset.connectors.sqla.models import SqlaTable
        from superset.models.core import Database
        from superset.models.dashboard import Dashboard
        from superset.models.slice import Slice

        admin = db.session.query(User).filter_by(username="admin").first()
        database = (
            db.session.query(Database).filter_by(database_name=DATABASE_NAME).first()
        )
        if database is None:
            database = Database(database_name=DATABASE_NAME, sqlalchemy_uri=DATABASE_URI)
            db.session.add(database)
        else:
            database.sqlalchemy_uri = DATABASE_URI
        database.expose_in_sqllab = True
        db.session.commit()

        datasets: dict[str, SqlaTable] = {}
        for table_name in TABLES:
            dataset = (
                db.session.query(SqlaTable)
                .filter_by(database_id=database.id, table_name=table_name, schema=None)
                .first()
            )
            if dataset is None:
                dataset = SqlaTable(table_name=table_name, database=database)
                db.session.add(dataset)
                db.session.flush()
            if table_name == "citibike_trips_clean":
                dataset.main_dttm_col = "started_at"
            dataset.owners = [admin] if admin else []
            dataset.fetch_metadata(commit=False)
            datasets[table_name] = dataset
        db.session.commit()

        def datasource(table_name: str) -> str:
            return f"{datasets[table_name].id}__table"

        chart_specs = [
            {
                "name": "MR1 - Lượng chuyến theo khách hàng và loại xe",
                "old_names": [
                    "MR1 - Luong chuyen theo khach hang va loai xe",
                    "MR1 - Trip Volume by User and Bike Type",
                ],
                "table": "rpt_mr1_user_behavior",
                "viz_type": "dist_bar",
                "params": base_params(
                    "dist_bar",
                    datasource("rpt_mr1_user_behavior"),
                    groupby=["user_and_bike_type"],
                    columns=[],
                    metrics=[metric("Total trips", "SUM(total_trips)")],
                    timeseries_limit_metric=metric(
                        "Total trips", "SUM(total_trips)"
                    ),
                    order_desc=True,
                    x_axis_label="Nhóm khách x loại xe",
                    y_axis_label="Số chuyến",
                    show_bar_value=True,
                    show_legend=False,
                ),
                "columns": ["user_and_bike_type"],
                "metrics": [metric("Total trips", "SUM(total_trips)")],
            },
            {
                "name": "MR2 - Top 15 tuyến đường phổ biến",
                "old_names": [
                    "MR2 - Top 15 tuyen duong pho bien",
                    "MR2 - Top 15 Most Used Routes",
                ],
                "table": "rpt_mr2_top_routes",
                "viz_type": "dist_bar",
                "params": base_params(
                    "dist_bar",
                    datasource("rpt_mr2_top_routes"),
                    groupby=["route_name"],
                    columns=[],
                    metrics=[metric("Trips", "SUM(trip_count)")],
                    timeseries_limit_metric=metric("Trips", "SUM(trip_count)"),
                    row_limit=15,
                    order_desc=True,
                    x_axis_label="Tuyến đường",
                    y_axis_label="Số chuyến",
                    show_bar_value=True,
                    show_legend=False,
                ),
                "columns": ["route_name"],
                "metrics": [metric("Trips", "SUM(trip_count)")],
            },
            {
                "name": "Dữ liệu clean - Xu hướng chuyến đi theo ngày",
                "old_names": [
                    "Du lieu clean - Xu huong chuyen di theo ngay",
                    "Clean Data - Daily Trips by Customer Type",
                ],
                "table": "citibike_trips_clean",
                "viz_type": "line",
                "params": base_params(
                    "line",
                    datasource("citibike_trips_clean"),
                    granularity_sqla="started_at",
                    time_grain_sqla="P1D",
                    time_range="No filter",
                    groupby=["member_casual"],
                    metrics=[metric("Trips", "COUNT(*)")],
                    order_desc=False,
                    x_axis_label="Ngày",
                    y_axis_label="Số chuyến",
                    rich_tooltip=True,
                    line_interpolation="linear",
                    show_brush=False,
                ),
                "groupby": ["member_casual"],
                "metrics": [metric("Trips", "COUNT(*)")],
                "is_timeseries": True,
            },
            {
                "name": "MR4 - Bản đồ nhiệt nhu cầu theo thứ",
                "old_names": [
                    "MR4 - Ban do nhiet nhu cau theo thu",
                    "MR4 - Weekday Demand Heatmap",
                ],
                "table": "rpt_mr4_weekly_analysis",
                "viz_type": "heatmap",
                "params": base_params(
                    "heatmap",
                    datasource("rpt_mr4_weekly_analysis"),
                    all_columns_x="day_of_week",
                    all_columns_y="user_type",
                    metric=metric("Trips", "SUM(total_trips)"),
                    normalize_across="heatmap",
                    sort_by_metric=False,
                    linear_color_scheme="blue_white_yellow",
                    xscale_interval="1",
                    yscale_interval="1",
                ),
                "columns": ["day_of_week", "user_type"],
                "metrics": [metric("Trips", "SUM(total_trips)")],
            },
            {
                "name": "MR5 - Tuyến có khoảng cách trung bình lớn",
                "old_names": [
                    "MR5 - Tuyen co khoang cach trung binh lon",
                    "MR5 - Longest Average Routes",
                ],
                "table": "rpt_mr5_distance_calc",
                "viz_type": "dist_bar",
                "params": base_params(
                    "dist_bar",
                    datasource("rpt_mr5_distance_calc"),
                    groupby=["route_name"],
                    columns=[],
                    metrics=[metric("Avg distance km", "AVG(avg_distance_km)")],
                    timeseries_limit_metric=metric(
                        "Avg distance km", "AVG(avg_distance_km)"
                    ),
                    row_limit=15,
                    order_desc=True,
                    x_axis_label="Tuyến đường",
                    y_axis_label="Khoảng cách TB (km)",
                    show_bar_value=True,
                    show_legend=False,
                ),
                "columns": ["route_name"],
                "metrics": [metric("Avg distance km", "AVG(avg_distance_km)")],
            },
            {
                "name": "MR7 - Phân bổ capacity trạm xe",
                "old_names": [
                    "MR7 - Phan bo capacity tram xe",
                    "MR7 - Station Capacity Distribution",
                ],
                "table": "rpt_mr7_station_capacity",
                "viz_type": "dist_bar",
                "params": base_params(
                    "dist_bar",
                    datasource("rpt_mr7_station_capacity"),
                    groupby=["capacity_group"],
                    columns=[],
                    metrics=[metric("Stations", "SUM(station_count)")],
                    timeseries_limit_metric=metric("Stations", "SUM(station_count)"),
                    order_desc=True,
                    x_axis_label="Nhóm capacity",
                    y_axis_label="Số trạm",
                    show_bar_value=True,
                    show_legend=False,
                ),
                "columns": ["capacity_group"],
                "metrics": [metric("Stations", "SUM(station_count)")],
            },
            {
                "name": "MR8 - Trạng thái vận hành trạm",
                "old_names": [
                    "MR8 - Trang thai van hanh tram",
                    "MR8 - Station Operational Status",
                ],
                "table": "rpt_mr8_station_status_check",
                "viz_type": "dist_bar",
                "params": base_params(
                    "dist_bar",
                    datasource("rpt_mr8_station_status_check"),
                    groupby=["station_status"],
                    columns=[],
                    metrics=[metric("Stations", "SUM(status_count)")],
                    timeseries_limit_metric=metric("Stations", "SUM(status_count)"),
                    order_desc=True,
                    x_axis_label="Trạng thái",
                    y_axis_label="Số trạm",
                    show_bar_value=True,
                    show_legend=False,
                ),
                "columns": ["station_status"],
                "metrics": [metric("Stations", "SUM(status_count)")],
            },
        ]

        charts: list[Slice] = []
        for spec in chart_specs:
            dataset = datasets[spec["table"]]
            params = spec["params"]
            candidate_names = [spec["name"], *spec.get("old_names", [])]
            chart = (
                db.session.query(Slice)
                .filter(Slice.slice_name.in_(candidate_names))
                .first()
            )
            if chart is None:
                chart = Slice(
                    slice_name=spec["name"],
                    datasource_id=dataset.id,
                    datasource_type="table",
                    datasource_name=dataset.table_name,
                    viz_type=spec["viz_type"],
                )
                db.session.add(chart)

            chart.slice_name = spec["name"]
            chart.datasource_id = dataset.id
            chart.datasource_type = "table"
            chart.datasource_name = dataset.table_name
            chart.viz_type = spec["viz_type"]
            chart.params = json.dumps(params, sort_keys=True)
            chart.query_context = json.dumps(
                query_context(
                    dataset.id,
                    params,
                    columns=spec.get("columns"),
                    groupby=spec.get("groupby"),
                    metrics=spec.get("metrics"),
                    orderby=[
                        [spec["metrics"][0], not params.get("order_desc", True)]
                    ],
                    is_timeseries=spec.get("is_timeseries", False),
                ),
                sort_keys=True,
            )
            chart.owners = [admin] if admin else []
            chart.description = (
                "Created automatically from processed Citi Bike MySQL report tables."
            )
            chart.last_saved_at = datetime.now(timezone.utc)
            if admin:
                chart.last_saved_by_fk = admin.id
            charts.append(chart)
        db.session.commit()

        dashboard = db.session.query(Dashboard).filter_by(slug=DASHBOARD_SLUG).first()
        if dashboard is None:
            dashboard = Dashboard(dashboard_title=DASHBOARD_TITLE, slug=DASHBOARD_SLUG)
            db.session.add(dashboard)
            db.session.flush()

        dashboard.dashboard_title = DASHBOARD_TITLE
        dashboard.published = True
        dashboard.owners = [admin] if admin else []
        dashboard.slices = charts
        dashboard.position_json = json.dumps(
            layout_for_charts([chart.id for chart in charts]), sort_keys=True
        )
        dashboard.css = DASHBOARD_CSS
        chart_ids = [chart.id for chart in charts]
        dashboard.json_metadata = json.dumps(
            {
                "label_colors": {
                    "member": "#00a699",
                    "casual": "#f06c64",
                    "Total trips": "#00a699",
                    "Trips": "#2b6cb0",
                    "Avg distance km": "#f59e0b",
                    "Stations": "#475569",
                    "ACTIVE_STATION": "#00a699",
                    "MAINTENANCE_OR_LOCKED_STATION": "#f06c64",
                },
                "chart_configuration": {},
                "global_chart_configuration": {
                    "scope": {"rootPath": ["ROOT_ID"], "excluded": []},
                    "chartsInScope": chart_ids,
                },
                "native_filter_configuration": [],
                "timed_refresh_immune_slices": [],
                "expanded_slices": {},
                "refresh_frequency": 0,
                "color_namespace": "citibike_mapreduce",
            },
            sort_keys=True,
        )
        dashboard.description = (
            "Meaningful Superset report built from the processed Citi Bike dataset "
            "and MapReduce report tables used by the Streamlit dashboard."
        )
        db.session.commit()

        print(f"Dashboard: {DASHBOARD_TITLE}")
        print(f"Slug: {DASHBOARD_SLUG}")
        print(f"Charts: {len(charts)}")
        for chart in charts:
            print(f"- [{chart.id}] {chart.slice_name} ({chart.viz_type})")


if __name__ == "__main__":
    main()
