
# Hướng dẫn chạy Mapreduce &  Giao diện Citi Bike

Nhiệm vụ bao gồm luồng phân tích dữ liệu bằng MapReduce, tiến trình đồng bộ kho dữ liệu bằng Sqoop, và bảng điều khiển tương tác (Dashboard) bằng Streamlit.

## 1. Vận hành Pipeline (MapReduce & Sqoop)

> ** LƯU Ý DÀNH CHO NGƯỜI CHẠY:**
> Để khởi động toàn bộ hệ thống phân tích mới nhất, bạn **CHỈ CẦN** chạy 2 lệnh trong mục "CHẠY TOÀN BỘ". Các lệnh ở mục "CHẠY TỪNG JOB" chỉ được dùng khi hệ thống báo lỗi và cần debug thủ công.

### CHẠY TOÀN BỘ

**Bước 1: Chạy TẤT CẢ các job MapReduce để tính toán và xử lý dữ liệu trên HDFS:**


```powershell
cd D:\Bigdata\citibike_tool_stack>
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-jobs.ps1 -JobId "ALL"

```

**Bước 2: Export TẤT CẢ kết quả phân tích từ HDFS sang cơ sở dữ liệu MySQL thông qua Sqoop:**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export_all_to_mysql.ps1 -JobId "ALL"

```

---

### CHẠY TỪNG JOB (Chỉ sử dụng để Debug/Kiểm tra lỗi)

Chỉ chạy một job MapReduce cụ thể (ví dụ: `mr1_user_behavior`):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-all-jobs.ps1 -JobId "mr1_user_behavior"

```

Chỉ Export một bảng kết quả cụ thể sang MySQL (ví dụ: `mr1_user_behavior`):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\export_all_to_mysql.ps1 -JobId "mr1_user_behavior"

```

## 2. Khởi chạy Giao diện (Streamlit GUI)

Cài đặt các thư viện Python cần thiết và tiến hành mở bảng điều khiển tương tác:

```powershell
py -m pip install -r requirements.txt
cd gui_app
py -m streamlit run app.py

```

Sau khi chạy lệnh trên, hãy mở trình duyệt web và truy cập vào địa chỉ: `http://localhost:8501`

## 3. Kết quả Đầu ra (Outputs)

* **Kết quả MapReduce trên HDFS:** Được xuất ra tại các thư mục từ `/data/citibike/mapreduce/mr1_...` đến `mr8_...`
* **Các bảng Báo cáo trong CSDL MySQL (thuộc database `testdb`):**
* `rpt_mr1_user_behavior`
* `rpt_mr2_top_routes`
* `rpt_mr3_hourly_trends`
* `rpt_mr4_weekly_analysis`
* `rpt_mr5_distance_calc`
* `rpt_mr6_anomaly_detection`
* `rpt_mr7_station_capacity`
* `rpt_mr8_station_status_check`


* **File nhật ký (Log) thực thi MapReduce gần nhất:** `logs/citibike_mapreduce_latest.md`
* **File nhật ký (Log) xuất Sqoop gần nhất:** `logs/citibike_sqoop_export_latest.md`

## 4. Luồng Hoạt động (Architecture Workflow)

Sơ đồ thể hiện luồng luân chuyển của dữ liệu Phân tích và Vận hành (Analytical & Operations flow) trong hệ thống:

```text
HDFS Cleaned TSV -> Hadoop Streaming (Python MR) -> HDFS Result Parts -> Apache Sqoop -> MySQL Report Tables -> Streamlit Dashboard (Read-only) & CRUD

```

