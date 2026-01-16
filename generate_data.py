import csv
import random
import time
from pathlib import Path

OUTPUT_FILE = "sales_data.csv"
TOTAL_ROWS = 1_000_000
BATCH_SIZE = 100_000

PRODUCTS = [
    "Notebook Gamer",
    "Mouse Wireless",
    "Teclado Mecanico",
    "Monitor 144Hz",
    "Cadeira Ergonomica"
]

REGIONS = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
STATUS_OPTIONS = ["Aprovado", "Pendente", "Cancelado"]

def generate_dataset():
    start_time = time.time()
    print(f"Starting generation of {TOTAL_ROWS} rows...")

    file_path = Path(OUTPUT_FILE)
    
    with file_path.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["transaction_id", "product", "quantity", "price", "region", "status"])

        for i in range(1, TOTAL_ROWS + 1):
            writer.writerow([
                i,
                random.choice(PRODUCTS),
                random.randint(1, 10),
                round(random.uniform(50.0, 5000.0), 2),
                random.choice(REGIONS),
                random.choice(STATUS_OPTIONS)
            ])

            if i % BATCH_SIZE == 0:
                print(f"Progress: {i} rows processed.")

    elapsed_time = time.time() - start_time
    print(f"Process completed. File '{OUTPUT_FILE}' generated in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    generate_dataset()