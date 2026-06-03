CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;

CREATE TABLE IF NOT EXISTS test_data (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  value INT NOT NULL
);

INSERT INTO test_data (id, name, value)
VALUES (1, 'test', 100)
ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  value = VALUES(value);

CREATE TABLE IF NOT EXISTS sqoop_export_test (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  value INT NOT NULL
);
