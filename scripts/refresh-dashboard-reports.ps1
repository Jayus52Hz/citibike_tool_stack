param()

$Sql = @"
TRUNCATE TABLE rpt_mr1_user_behavior;
TRUNCATE TABLE rpt_mr2_top_routes;
TRUNCATE TABLE rpt_mr3_hourly_trends;
TRUNCATE TABLE rpt_mr4_weekly_analysis;
TRUNCATE TABLE rpt_mr5_distance_calc;
TRUNCATE TABLE rpt_mr6_anomaly_detection;
TRUNCATE TABLE rpt_mr7_station_capacity;
TRUNCATE TABLE rpt_mr8_station_status_check;

INSERT INTO rpt_mr1_user_behavior
SELECT CONCAT(member_casual, ',', rideable_type), ROUND(AVG(duration_minutes), 2), COUNT(*)
FROM citibike_trips_clean
WHERE member_casual IS NOT NULL AND rideable_type IS NOT NULL
GROUP BY member_casual, rideable_type;

INSERT INTO rpt_mr2_top_routes
SELECT CONCAT(COALESCE(start_station_name, 'Unknown'), ' -> ', COALESCE(end_station_name, 'Unknown')), COUNT(*)
FROM citibike_trips_clean
GROUP BY start_station_name, end_station_name
ORDER BY COUNT(*) DESC
LIMIT 100;

INSERT INTO rpt_mr3_hourly_trends
SELECT HOUR(started_at), COUNT(*)
FROM citibike_trips_clean
WHERE started_at IS NOT NULL
GROUP BY HOUR(started_at)
ORDER BY HOUR(started_at);

INSERT INTO rpt_mr4_weekly_analysis
SELECT DAYNAME(started_at), member_casual, COUNT(*)
FROM citibike_trips_clean
WHERE started_at IS NOT NULL AND member_casual IS NOT NULL
GROUP BY DAYNAME(started_at), member_casual;

INSERT INTO rpt_mr5_distance_calc
SELECT
  CONCAT(COALESCE(start_station_name, 'Unknown'), ' -> ', COALESCE(end_station_name, 'Unknown')),
  ROUND(AVG(6371 * ACOS(LEAST(1, GREATEST(-1,
    COS(RADIANS(start_lat)) * COS(RADIANS(end_lat)) *
    COS(RADIANS(end_lng) - RADIANS(start_lng)) +
    SIN(RADIANS(start_lat)) * SIN(RADIANS(end_lat))
  )))), 2),
  COUNT(*)
FROM citibike_trips_clean
WHERE start_lat IS NOT NULL AND start_lng IS NOT NULL
  AND end_lat IS NOT NULL AND end_lng IS NOT NULL
GROUP BY start_station_name, end_station_name
ORDER BY AVG(6371 * ACOS(LEAST(1, GREATEST(-1,
  COS(RADIANS(start_lat)) * COS(RADIANS(end_lat)) *
  COS(RADIANS(end_lng) - RADIANS(start_lng)) +
  SIN(RADIANS(start_lat)) * SIN(RADIANS(end_lat))
)))) DESC
LIMIT 100;

INSERT INTO rpt_mr6_anomaly_detection
SELECT error_type, error_count
FROM (
  SELECT 'NON_POSITIVE_DURATION' AS error_type, COUNT(*) AS error_count
  FROM citibike_trips_clean
  WHERE duration_minutes <= 0
  UNION ALL
  SELECT 'LONG_DURATION_OVER_3H', COUNT(*)
  FROM citibike_trips_clean
  WHERE duration_minutes > 180
  UNION ALL
  SELECT 'MISSING_STATION', COUNT(*)
  FROM citibike_trips_clean
  WHERE start_station_name IS NULL OR end_station_name IS NULL
     OR start_station_name = '' OR end_station_name = ''
  UNION ALL
  SELECT 'MISSING_COORDS', COUNT(*)
  FROM citibike_trips_clean
  WHERE start_lat IS NULL OR start_lng IS NULL OR end_lat IS NULL OR end_lng IS NULL
) x
WHERE error_count > 0;

INSERT INTO rpt_mr7_station_capacity
SELECT
  CASE
    WHEN capacity < 20 THEN 'SMALL_STATION'
    WHEN capacity < 40 THEN 'MEDIUM_STATION'
    ELSE 'LARGE_STATION'
  END,
  COUNT(*)
FROM citibike_stations_clean
WHERE capacity IS NOT NULL
GROUP BY
  CASE
    WHEN capacity < 20 THEN 'SMALL_STATION'
    WHEN capacity < 40 THEN 'MEDIUM_STATION'
    ELSE 'LARGE_STATION'
  END;

INSERT INTO rpt_mr8_station_status_check
SELECT
  CASE
    WHEN is_installed = 1 AND is_renting = 1 AND is_returning = 1
    THEN 'ACTIVE_STATION'
    ELSE 'MAINTENANCE_OR_LOCKED_STATION'
  END,
  COUNT(*)
FROM citibike_stations_clean
GROUP BY
  CASE
    WHEN is_installed = 1 AND is_renting = 1 AND is_returning = 1
    THEN 'ACTIVE_STATION'
    ELSE 'MAINTENANCE_OR_LOCKED_STATION'
  END;

SELECT 'rpt_mr1_user_behavior' AS table_name, COUNT(*) AS rows_count FROM rpt_mr1_user_behavior
UNION ALL SELECT 'rpt_mr2_top_routes', COUNT(*) FROM rpt_mr2_top_routes
UNION ALL SELECT 'rpt_mr3_hourly_trends', COUNT(*) FROM rpt_mr3_hourly_trends
UNION ALL SELECT 'rpt_mr4_weekly_analysis', COUNT(*) FROM rpt_mr4_weekly_analysis
UNION ALL SELECT 'rpt_mr5_distance_calc', COUNT(*) FROM rpt_mr5_distance_calc
UNION ALL SELECT 'rpt_mr6_anomaly_detection', COUNT(*) FROM rpt_mr6_anomaly_detection
UNION ALL SELECT 'rpt_mr7_station_capacity', COUNT(*) FROM rpt_mr7_station_capacity
UNION ALL SELECT 'rpt_mr8_station_status_check', COUNT(*) FROM rpt_mr8_station_status_check;
"@

Write-Host "Dang nap lai cac bang report cho Dashboard..." -ForegroundColor Cyan
$Sql | docker exec -i citibike-mysql mysql -utestuser -ptestpass -D testdb
Write-Host "Hoan tat. Refresh trang Dashboard de xem du lieu moi." -ForegroundColor Green
