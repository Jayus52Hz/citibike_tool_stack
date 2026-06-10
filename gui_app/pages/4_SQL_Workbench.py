"""
SQL Workbench - chạy truy vấn tùy ý và các câu lệnh CRUD có kiểm soát.
"""
import os
import re
import sys

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db_config import run_query, run_write


st.set_page_config(page_title="SQL Workbench", page_icon="🔎", layout="wide")
st.title("SQL Workbench")
st.caption("Chay truy van SELECT va thao tac CRUD truc tiep tren MySQL.")

READ_PREFIXES = ("SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN")
WRITE_PREFIXES = ("INSERT", "UPDATE", "DELETE")


def normalize_sql(sql: str) -> str:
    sql = sql.strip()
    if sql.endswith(";"):
        sql = sql[:-1].strip()
    return sql


def statement_type(sql: str) -> str:
    first = re.split(r"\s+", sql.strip(), maxsplit=1)[0].upper() if sql.strip() else ""
    if first in READ_PREFIXES:
        return "read"
    if first in WRITE_PREFIXES:
        return "write"
    return "blocked"


def is_single_statement(sql: str) -> bool:
    return ";" not in normalize_sql(sql)


with st.sidebar:
    st.header("Bang du lieu")
    try:
        tables = run_query("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
        table_col = tables.columns[0] if not tables.empty else None
        table_names = tables[table_col].tolist() if table_col else []
        selected_table = st.selectbox("Xem nhanh schema", table_names)
        if selected_table:
            st.dataframe(
                run_query(f"DESCRIBE `{selected_table}`"),
                use_container_width=True,
                hide_index=True,
            )
    except Exception as exc:
        st.error(f"Khong doc duoc danh sach bang: {exc}")

examples = {
    "Dem so chuyen di": "SELECT COUNT(*) AS total_trips FROM citibike_trips_clean;",
    "Top tram xuat phat": """
SELECT start_station_name, COUNT(*) AS total_trips
FROM citibike_trips_clean
GROUP BY start_station_name
ORDER BY total_trips DESC
LIMIT 10;
""".strip(),
    "Them dong test": """
INSERT INTO test_data (id, name, value)
VALUES (2, 'manual_insert', 200)
ON DUPLICATE KEY UPDATE name = VALUES(name), value = VALUES(value);
""".strip(),
    "Cap nhat dong test": "UPDATE test_data SET value = value + 1 WHERE id = 2;",
    "Xoa dong test": "DELETE FROM test_data WHERE id = 2;",
}

choice = st.selectbox("Mau truy van", list(examples.keys()))
sql = st.text_area("SQL", value=examples[choice], height=180)
sql_clean = normalize_sql(sql)
kind = statement_type(sql_clean)

execute = st.button("Run", type="primary", use_container_width=False)
confirm_write = False
if kind == "write":
    confirm_write = st.checkbox("Toi xac nhan muon thay doi du lieu")

if execute:
    if not sql_clean:
        st.warning("Nhap cau SQL truoc khi chay.")
    elif not is_single_statement(sql_clean):
        st.error("Chi cho phep chay mot statement moi lan.")
    elif kind == "blocked":
        st.error("Chi ho tro SELECT/SHOW/DESCRIBE/EXPLAIN va INSERT/UPDATE/DELETE.")
    else:
        try:
            if kind == "read":
                df = run_query(sql_clean)
                st.success(f"Query thanh cong: {len(df):,} dong.")
                st.dataframe(df, use_container_width=True, hide_index=True)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Tai ket qua CSV",
                    csv,
                    "query_result.csv",
                    "text/csv",
                    use_container_width=True,
                )
            elif not confirm_write:
                st.warning("Tick xac nhan truoc khi chay INSERT/UPDATE/DELETE.")
            else:
                affected = run_write(sql_clean)
                st.success(f"CRUD thanh cong. So dong anh huong: {affected:,}.")
        except Exception as exc:
            st.error(f"Loi SQL: {exc}")
