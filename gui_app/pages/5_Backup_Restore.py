"""
Sao lưu và phục hồi các bảng MySQL bằng file ZIP chứa CSV.
"""
import io
import json
import os
import sys
import zipfile
from datetime import datetime

import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db_config import run_many, run_query, run_write


st.set_page_config(page_title="Backup Restore", page_icon="💾", layout="wide")
st.title("Backup / Restore")
st.caption("Sao luu cac bang MySQL thanh file ZIP va phuc hoi lai du lieu khi can.")


def list_tables():
    df = run_query("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
    if df.empty:
        return []
    return df[df.columns[0]].tolist()


def table_columns(table_name: str):
    desc = run_query(f"DESCRIBE `{table_name}`")
    return desc["Field"].tolist()


def build_backup_zip(table_names):
    buffer = io.BytesIO()
    manifest = {
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "database": "testdb",
        "tables": {},
    }
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for table in table_names:
            df = run_query(f"SELECT * FROM `{table}`")
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            zf.writestr(f"tables/{table}.csv", csv_bytes)
            manifest["tables"][table] = {
                "rows": int(len(df)),
                "columns": list(df.columns),
            }
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))
    buffer.seek(0)
    return buffer.getvalue(), manifest


def restore_table(table_name: str, df: pd.DataFrame, replace_existing: bool):
    existing_cols = table_columns(table_name)
    cols = [col for col in df.columns if col in existing_cols]
    if not cols:
        raise ValueError(f"Khong co cot hop le cho bang {table_name}")

    clean_df = df[cols].where(pd.notna(df[cols]), None)
    rows = [tuple(row) for row in clean_df.itertuples(index=False, name=None)]

    if replace_existing:
        run_write(f"DELETE FROM `{table_name}`")
    if not rows:
        return 0

    col_sql = ", ".join(f"`{col}`" for col in cols)
    placeholders = ", ".join(["%s"] * len(cols))
    update_sql = ", ".join(f"`{col}` = VALUES(`{col}`)" for col in cols)
    sql = (
        f"INSERT INTO `{table_name}` ({col_sql}) VALUES ({placeholders}) "
        f"ON DUPLICATE KEY UPDATE {update_sql}"
    )
    return run_many(sql, rows)


try:
    tables = list_tables()
except Exception as exc:
    st.error(f"Khong ket noi duoc MySQL: {exc}")
    st.stop()

tab_backup, tab_restore = st.tabs(["Sao luu", "Phuc hoi"])

with tab_backup:
    selected_tables = st.multiselect(
        "Chon bang can sao luu",
        tables,
        default=[
            table
            for table in tables
            if table.startswith("citibike_") or table.startswith("rpt_")
        ],
    )
    if st.button("Tao backup", type="primary", disabled=not selected_tables):
        backup_bytes, manifest = build_backup_zip(selected_tables)
        total_rows = sum(item["rows"] for item in manifest["tables"].values())
        st.success(f"Da tao backup: {len(selected_tables)} bang, {total_rows:,} dong.")
        st.json(manifest)
        filename = "citibike_mysql_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".zip"
        st.download_button(
            "Tai file backup ZIP",
            backup_bytes,
            filename,
            "application/zip",
            use_container_width=True,
        )

with tab_restore:
    uploaded = st.file_uploader("Chon file backup ZIP", type=["zip"])
    replace_existing = st.checkbox("Xoa du lieu hien tai truoc khi phuc hoi")

    if uploaded:
        try:
            raw = uploaded.getvalue()
            with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                manifest = json.loads(zf.read("manifest.json").decode("utf-8"))
                backup_tables = list(manifest.get("tables", {}).keys())
                st.json(manifest)
                restore_tables = st.multiselect(
                    "Chon bang can phuc hoi",
                    backup_tables,
                    default=backup_tables,
                )
                if st.button("Phuc hoi du lieu", type="primary", disabled=not restore_tables):
                    restored = {}
                    for table in restore_tables:
                        if table not in tables:
                            st.warning(f"Bo qua {table}: bang chua ton tai trong database.")
                            continue
                        with zf.open(f"tables/{table}.csv") as f:
                            df = pd.read_csv(f)
                        restored[table] = restore_table(table, df, replace_existing)
                    st.success("Phuc hoi hoan tat.")
                    st.dataframe(
                        pd.DataFrame(
                            [{"table": table, "affected_rows": rows} for table, rows in restored.items()]
                        ),
                        use_container_width=True,
                        hide_index=True,
                    )
        except Exception as exc:
            st.error(f"File backup khong hop le hoac phuc hoi that bai: {exc}")
