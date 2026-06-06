USE testdb;

CREATE TABLE IF NOT EXISTS rpt_mr1_user_behavior (user_and_bike_type VARCHAR(100), avg_duration FLOAT, total_trips INT);
CREATE TABLE IF NOT EXISTS rpt_mr2_top_routes (route_name VARCHAR(255), trip_count INT);
CREATE TABLE IF NOT EXISTS rpt_mr3_hourly_trends (hour_of_day INT, total_trips INT);
CREATE TABLE IF NOT EXISTS rpt_mr4_weekly_analysis (day_of_week VARCHAR(20), user_type VARCHAR(50), total_trips INT);
CREATE TABLE IF NOT EXISTS rpt_mr5_distance_calc (route_name VARCHAR(255), avg_distance_km FLOAT, total_trips INT);
CREATE TABLE IF NOT EXISTS rpt_mr6_anomaly_detection (error_type VARCHAR(100), error_count INT);
CREATE TABLE IF NOT EXISTS rpt_mr7_station_capacity (capacity_group VARCHAR(100), station_count INT);
CREATE TABLE IF NOT EXISTS rpt_mr8_station_status_check (station_status VARCHAR(100), status_count INT);