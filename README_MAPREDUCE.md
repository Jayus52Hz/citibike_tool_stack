# MapReduce va GUI Guide

File nay tap trung vao phan MapReduce, export report ve MySQL va GUI quan ly/visualization. De chay toan bo pipeline tu dau, doc `CITIBIKE_PIPELINE_GUIDE.md`.

## 1. Dieu kien truoc khi chay

Can co stack Docker dang chay va du lieu clean trong MySQL/HDFS:

```powershell
cd "D:\Bigdata\New game\projects\citibike_tool_stack"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-citibike-pipeline.ps1
```

Neu build moi, chay dependency prep truoc:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\prepare-build-deps.ps1
docker compose up -d --build
```

## 2. Chay tat ca MapReduce jobs

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-jobs.ps1 -JobId "ALL"
```

Script se chay 8 job Hadoop Streaming bang Python mapper/reducer:

| JobId khi chay rieng | Report table | Noi dung |
| --- | --- | --- |
| `mr1_user_behavior` | `rpt_mr1_user_behavior` | User behavior theo member/casual va loai xe |
| `mr2_top_routes` | `rpt_mr2_top_routes` | Top route pho bien |
| `mr3_hourly_trends` | `rpt_mr3_hourly_trends` | Xu huong theo gio |
| `mr4_weekly_analysis` | `rpt_mr4_weekly_analysis` | Phan tich theo ngay trong tuan |
| `mr5_distance_calc` | `rpt_mr5_distance_calc` | Khoang cach trung binh theo route |
| `mr6_anomaly_detection` | `rpt_mr6_anomaly_detection` | Phat hien anomaly |
| `mr7_station_capacity` | `rpt_mr7_station_capacity` | Phan loai capacity tram |
| `mr8_station_status_check` | `rpt_mr8_station_status_check` | Kiem tra trang thai tram |

Chay rieng mot job de debug:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-jobs.ps1 -JobId "mr1_user_behavior"
```

Log moi nhat:

```text
logs/citibike_mapreduce_latest.md
```

## 3. Export ket qua MapReduce ve MySQL

Export tat ca report tables:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export_all_to_mysql.ps1 -JobId "ALL"
```

Export rieng mot job:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export_all_to_mysql.ps1 -JobId "mr1_user_behavior"
```

Kiem tra MySQL:

```powershell
docker exec citibike-mysql mysql -utestuser -ptestpass testdb -e "SHOW TABLES LIKE 'rpt_mr%';"
```

Log moi nhat:

```text
logs/citibike_sqoop_export_latest.md
```

## 4. GUI Streamlit

Start GUI:

```powershell
docker compose up -d --build gui-app
```

Mo:

```text
http://127.0.0.1:8501
```

Trang chinh:

- `Dashboard`: xem bang report va bieu do MapReduce.
- `Manage Trips`: CRUD bang `citibike_trips_clean`.
- `Manage Stations`: CRUD bang `citibike_stations_clean`.
- `SQL Workbench`: query va thao tac SQL co xac nhan.
- `Backup / Restore`: backup/restore MySQL bang ZIP chua CSV.

## 5. Visualizations

Dashboard dung cac bang `rpt_mr*` va co nhieu loai chart:

- Bar chart cho user behavior, top route, weekly analysis.
- Line/area chart cho hourly trends.
- Pie/donut chart cho station capacity va station status.
- Data table mode de xem/export CSV.
- Station map nam trong `Manage Stations`.

Neu dashboard chua co du lieu, chay:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-jobs.ps1 -JobId "ALL"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export_all_to_mysql.ps1 -JobId "ALL"
```

Hoac tao nhanh report tu MySQL clean data:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\refresh-dashboard-reports.ps1
```

## 6. Evidence de nop

- Screenshot lenh MapReduce success.
- Screenshot `logs/citibike_mapreduce_latest.md`.
- Screenshot `logs/citibike_sqoop_export_latest.md`.
- Screenshot `Dashboard`.
- Screenshot `SQL Workbench`.
- Screenshot `Manage Trips` va `Manage Stations`.
- Screenshot `Backup / Restore`.

