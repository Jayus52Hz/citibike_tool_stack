CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;

CREATE TABLE IF NOT EXISTS citibike_trips_clean (
  ride_id VARCHAR(100) PRIMARY KEY,
  rideable_type VARCHAR(50),
  started_at DATETIME,
  ended_at DATETIME,
  duration_minutes DOUBLE,
  start_station_id VARCHAR(100),
  start_station_name VARCHAR(255),
  end_station_id VARCHAR(100),
  end_station_name VARCHAR(255),
  start_lat DOUBLE,
  start_lng DOUBLE,
  end_lat DOUBLE,
  end_lng DOUBLE,
  member_casual VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS citibike_stations_clean (
  station_id VARCHAR(100) PRIMARY KEY,
  name VARCHAR(255),
  short_name VARCHAR(100),
  lat DOUBLE,
  lon DOUBLE,
  capacity INT,
  num_bikes_available INT,
  num_docks_available INT,
  is_installed INT,
  is_renting INT,
  is_returning INT,
  last_reported DATETIME
);
