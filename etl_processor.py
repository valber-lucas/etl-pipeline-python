import csv
import time
import logging
import sqlite3
from pathlib import Path
from typing import Iterator, Dict, Tuple, Optional, Any # <--- Importando tipos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("etl_process.log"),
        logging.StreamHandler()
    ]
)

INPUT_FILE = "sales_data.csv"
DB_FILE = "warehouse.db"
BATCH_SIZE = 5000

def setup_database() -> None:
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY,
                produto TEXT,
                total REAL,
                status TEXT,
                data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("DELETE FROM vendas")
        conn.commit()
        conn.close()
    except Exception as e:
        logging.critical(f"Database setup failed: {e}")

def get_data_stream(file_path: str) -> Iterator[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        logging.error(f"File not found: {file_path}")
        return

    with path.open(mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row

def transform_data(row: Dict[str, Any]) -> Optional[Tuple[int, str, float, str]]:
    try:
        return (
            int(row["transaction_id"]),
            row["product"].upper(),
            float(row["price"]) * int(row["quantity"]),
            row["status"]
        )
    except ValueError:
        return None

def run_pipeline() -> None:
    setup_database()
    
    start_time = time.time()
    logging.info("Starting ETL Pipeline with DB Insertion...")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    processed_count = 0
    batch_buffer = []

    data_stream = get_data_stream(INPUT_FILE)

    for raw_row in data_stream:
        processed_count += 1
        
        clean_data_tuple = transform_data(raw_row)

        if clean_data_tuple and clean_data_tuple[3] == "Aprovado" and raw_row["region"] == "Sudeste":
            batch_buffer.append(clean_data_tuple)

        if len(batch_buffer) >= BATCH_SIZE:
            cursor.executemany("INSERT INTO vendas (id, produto, total, status) VALUES (?, ?, ?, ?)", batch_buffer)
            batch_buffer = []
            logging.info(f"Persisted batch. Rows scanned: {processed_count}")

    if batch_buffer:
        cursor.executemany("INSERT INTO vendas (id, produto, total, status) VALUES (?, ?, ?, ?)", batch_buffer)

    conn.commit()
    conn.close()

    elapsed_time = time.time() - start_time
    
    logging.info("=" * 30)
    logging.info("ETL COMPLETED")
    logging.info(f"Rows Scanned: {processed_count}")
    logging.info(f"Execution Time: {elapsed_time:.2f} seconds")
    logging.info("=" * 30)

if __name__ == "__main__":
    run_pipeline()