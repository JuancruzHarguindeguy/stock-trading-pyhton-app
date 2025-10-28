import requests
import os
import time
from dotenv import load_dotenv
import snowflake.connector
from datetime import datetime

load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

LIMIT = 1000
# Rate limit: 5 requests por minuto
MAX_PER_MINUTE = 5
SLEEP_SECONDS = 60

def safe_get(url, retries=3, wait=10):
    """GET con retries sencillos para errores transitorios (5xx, timeouts, etc.)."""
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            print(f"[safe_get] Intento {attempt}/{retries} falló: {e}")
            if attempt < retries:
                time.sleep(wait)
                print(f"[safe_get] Reintentando en {wait}s...")
            else:
                print("[safe_get] Demasiados intentos fallidos.")
                raise

def run_stock_job():
    DS = datetime.now().strftime('%Y-%m-%d')
    base_url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'

    # contenedor de tickers
    tickers = []

    # contador local de requests para aplicar pausa cada MAX_PER_MINUTE
    requests_made = 0

    print("Solicitando primera página...")
    response = requests.get(base_url)
    requests_made += 1

    data = response.json()
    for ticker in data.get('results', []):
        ticker['ds'] = DS
        tickers.append(ticker)

    # paginación con control de rate limit y safe_get
    while data.get('next_url'):
        # respetar límite local
        if requests_made >= MAX_PER_MINUTE:
            print(f"Alcanzado {MAX_PER_MINUTE} requests. Durmiendo {SLEEP_SECONDS}s...")
            time.sleep(SLEEP_SECONDS)
            requests_made = 0

        next_url = data['next_url'] + f'&apiKey={POLYGON_API_KEY}'
        print('Requesting next page ')

        response = requests.get(next_url)
        requests_made += 1

        data = response.json()
        results = data.get('results', [])
        if not results:
            print("Sin 'results' en la respuesta. Terminando paginación.")
            break

        for ticker in results:
            ticker['ds'] = DS
            tickers.append(ticker)

    print(f"Fetch completo. Total tickers: {len(tickers)}")
    
    # ahora cargamos a Snowflake

    example_ticker =  {        
        'ticker': 'A1BSC', 
        'name': 'Dow Jones Americas Basic Materials Index', 
        'market': 'indices', 
        'locale': 'us', 
        'active': True, 
        'source_feed': 'CMEMarketDataPlatformDowJones',
        'ds': '2025-10-27'
        }
        
    fieldnames = list(example_ticker.keys())

    load_to_snowflake(tickers, fieldnames)

    print(f'Loaded {len(tickers)} rows to Snowflake')




def load_to_snowflake(rows,fieldnames):
    
    import snowflake.connector

    # Configuración Snowflake desde .env
    user = os.getenv('SNOWFLAKE_USER')
    pwd = os.getenv('SNOWFLAKE_PASSWORD')
    account = os.getenv('SNOWFLAKE_ACCOUNT')
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    database = os.getenv('SNOWFLAKE_DATABASE')
    schema = os.getenv('SNOWFLAKE_SCHEMA')
    role = os.getenv('SNOWFLAKE_ROLE')
    table_name = os.getenv('SNOWFLAKE_TABLE', 'stock_tickers')

    # Validar credenciales mínimas
    if not (user and pwd and account and database):
        raise RuntimeError("Credenciales de Snowflake incompletas en .env")

    # Conectar
    conn = snowflake.connector.connect(
        user=user,
        password=pwd,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role,
        session_parameters={"CLIENT_TELEMETRY_ENABLED": False},
    )

    # Estructura fija de columnas (todas VARCHAR)
    fieldnames = ["ticker", "name", "market", "locale", "active", "source_feed", "ds"]

    try:
        cs = conn.cursor()
        try:
            table_name = os.getenv('SNOWFLAKE_TABLE', 'stock_tickers')

            # Define typed schema based on example_ticker
            type_overrides = {
                'ticker': 'VARCHAR',
                'name': 'VARCHAR',
                'market': 'VARCHAR',
                'locale': 'VARCHAR',
                'active': 'BOOLEAN',
                'source_feed': 'VARCHAR',
                'ds': 'VARCHAR'
            }
            columns_sql_parts = []
            for col in fieldnames:
                col_type = type_overrides.get(col, 'VARCHAR')
                columns_sql_parts.append(f'"{col.upper()}" {col_type}')

            create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ( ' + ', '.join(columns_sql_parts) + ' )'
            cs.execute(create_table_sql)

            column_list = ', '.join([f'"{c.upper()}"' for c in fieldnames])
            placeholders = ', '.join([f'%({c})s' for c in fieldnames])
            insert_sql = f'INSERT INTO {table_name} ( {column_list} ) VALUES ( {placeholders} )'

            # Conform rows to fieldnames
            transformed = []
            for t in rows:
                row = {}
                for k in fieldnames:
                    row[k] = t.get(k, None)
                    
                transformed.append(row)

            if transformed:
                cs.executemany(insert_sql, transformed)
        finally:
            cs.close()
    finally:
        conn.close()


if __name__ == '__main__':
    run_stock_job()
