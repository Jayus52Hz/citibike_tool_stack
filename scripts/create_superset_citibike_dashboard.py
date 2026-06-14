import json

from superset.app import create_app


DATABASE_NAME = "CitiBike Analytics MySQL"
DASHBOARD_TITLE = "Citi Bike Analytics Dashboard"


def metric_sum(column_name):
    return {
        "aggregate": "SUM",
        "column": {"column_name": column_name},
        "expressionType": "SIMPLE",
        "label": f"SUM({column_name})",
    }


def metric_count():
    return {
        "aggregate": "COUNT",
        "column": None,
        "expressionType": "SIMPLE",
        "label": "COUNT(*)",
    }


def metric_avg(column_name):
    return {
        "aggregate": "AVG",
        "column": {"column_name": column_name},
        "expressionType": "SIMPLE",
        "label": f"AVG({column_name})",
    }


def ensure_dataset(database, table_name):
    dataset = (
        db.session.query(SqlaTable)
        .filter_by(database_id=database.id, table_name=table_name, schema=None)
        .one_or_none()
    )
    if dataset is None:
        dataset = SqlaTable(table_name=table_name, database=database, schema=None)
        db.session.add(dataset)
        db.session.flush()
    dataset.fetch_metadata()
    db.session.commit()
    return dataset


def upsert_chart(name, dataset, viz_type, form_data):
    chart = db.session.query(Slice).filter_by(slice_name=name).one_or_none()
    datasource = f"{dataset.id}__table"
    form_data = {
        "datasource": datasource,
        "viz_type": viz_type,
        "adhoc_filters": [],
        "row_limit": 1000,
        "time_range": "No filter",
        **form_data,
    }
    if chart is None:
        chart = Slice(slice_name=name)
        db.session.add(chart)
    chart.viz_type = viz_type
    chart.datasource_id = dataset.id
    chart.datasource_type = "table"
    chart.params = json.dumps(form_data)
    db.session.commit()
    return chart


def build_position_json(charts):
    root_id = "ROOT_ID"
    grid_id = "GRID_ID"
    position = {
        "DASHBOARD_VERSION_KEY": "v2",
        root_id: {"type": "ROOT", "id": root_id, "children": [grid_id]},
        grid_id: {"type": "GRID", "id": grid_id, "children": [], "parents": [root_id]},
    }
    for row_index in range(0, len(charts), 2):
        row_id = f"ROW-{row_index // 2 + 1}"
        row_charts = charts[row_index : row_index + 2]
        position[grid_id]["children"].append(row_id)
        position[row_id] = {
            "type": "ROW",
            "id": row_id,
            "children": [],
            "meta": {"background": "BACKGROUND_TRANSPARENT"},
            "parents": [root_id, grid_id],
        }
        for chart in row_charts:
            chart_id = f"CHART-{chart.id}"
            position[row_id]["children"].append(chart_id)
            position[chart_id] = {
                "type": "CHART",
                "id": chart_id,
                "children": [],
                "meta": {
                    "chartId": chart.id,
                    "height": 50,
                    "width": 6,
                    "sliceName": chart.slice_name,
                    "uuid": str(chart.uuid),
                },
                "parents": [root_id, grid_id, row_id],
            }
    return json.dumps(position)


app = create_app()

with app.app_context():
    from superset import db
    from superset.connectors.sqla.models import SqlaTable
    from superset.models.core import Database
    from superset.models.dashboard import Dashboard
    from superset.models.slice import Slice

    database = db.session.query(Database).filter_by(database_name=DATABASE_NAME).one()

    trips = ensure_dataset(database, "citibike_trips_clean")
    mr1 = ensure_dataset(database, "rpt_mr1_user_behavior")
    mr2 = ensure_dataset(database, "rpt_mr2_top_routes")
    mr7 = ensure_dataset(database, "rpt_mr7_station_capacity")

    charts = [
        upsert_chart(
            "01 - Trips by Day",
            trips,
            "echarts_timeseries_line",
            {
                "granularity_sqla": "started_at",
                "time_grain_sqla": "P1D",
                "metrics": [metric_count()],
                "groupby": [],
            },
        ),
        upsert_chart(
            "02 - Average Duration by Day",
            trips,
            "echarts_timeseries_bar",
            {
                "granularity_sqla": "started_at",
                "time_grain_sqla": "P1D",
                "metrics": [metric_avg("duration_minutes")],
                "groupby": [],
            },
        ),
        upsert_chart(
            "03 - User and Bike Type Trips",
            mr1,
            "echarts_timeseries_bar",
            {
                "x_axis": "user_and_bike_type",
                "metrics": [metric_sum("total_trips")],
                "groupby": [],
            },
        ),
        upsert_chart(
            "04 - Top Routes",
            mr2,
            "echarts_timeseries_bar",
            {
                "x_axis": "route_name",
                "metrics": [metric_sum("trip_count")],
                "groupby": [],
                "row_limit": 10,
            },
        ),
        upsert_chart(
            "05 - Station Capacity Mix",
            mr7,
            "pie",
            {
                "groupby": ["capacity_group"],
                "metric": metric_sum("station_count"),
                "donut": True,
                "show_labels": True,
            },
        ),
    ]

    dashboard = db.session.query(Dashboard).filter_by(dashboard_title=DASHBOARD_TITLE).one_or_none()
    if dashboard is None:
        dashboard = Dashboard(dashboard_title=DASHBOARD_TITLE)
        db.session.add(dashboard)
    dashboard.slug = "citibike-analytics-dashboard"
    dashboard.slices = charts
    dashboard.position_json = build_position_json(charts)
    dashboard.json_metadata = json.dumps({"timed_refresh_immune_slices": []})
    db.session.commit()

    print(f"Created/updated dashboard: {DASHBOARD_TITLE}")
    for chart in charts:
        print(f"- {chart.id}: {chart.slice_name} ({chart.viz_type})")
