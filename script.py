import requests
import os
import time
import csv
from dotenv import load_dotenv

load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") 

LIMIT = 1000
URL = f"https://api.polygon.io/v3/reference/tickers?market=indices&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

OUTFILE = "tickers.csv"
FIELDNAMES = ["ticker", "name", "market", "locale", "active", "source_feed"]

# Si el archivo no existe, escribir encabezado; si existe, se agrega
write_header = not os.path.exists(OUTFILE)
csvfile = open(OUTFILE, "a", newline="", encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
if write_header:
    writer.writeheader()

# contador simple para rate limit: 5 requests -> sleep 60s
requests_made = 0
MAX_PER_MINUTE = 5
SLEEP_SECONDS = 60

def write_ticker_row(item):
    row = {
        "ticker": item.get("ticker"),
        "name": item.get("name"),
        "market": item.get("market"),
        "locale": item.get("locale"),
        "active": item.get("active"),
        "source_feed": item.get("source_feed"),
    }
    writer.writerow(row)
    csvfile.flush()  # asegura que se escriba al disco

# primera petición
resp = requests.get(URL)
print(resp.json())
requests_made += 1
data = resp.json()
for it in data.get("results", []):
    write_ticker_row(it)
print("Guardados:", os.path.getsize(OUTFILE), "bytes (archivo)")

# paginación simple con espera cada 5 requests
while data.get("next_url"):
    next_url = data["next_url"] + f"&apiKey={POLYGON_API_KEY}"
    if requests_made >= MAX_PER_MINUTE:
        print(f"Alcanzado {MAX_PER_MINUTE} requests. Durmiendo {SLEEP_SECONDS}s...")
        time.sleep(SLEEP_SECONDS)
        requests_made = 0

    resp = requests.get(next_url)
    requests_made += 1
    data = resp.json()
    results = data.get("results", [])
    print(results)
    if not results:
        print("Sin 'results' en la respuesta. Terminando.")
        break
    for it in results:
        write_ticker_row(it)

csvfile.close()
print("Terminado. CSV guardado en", OUTFILE)