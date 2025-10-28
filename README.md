# 📈 Stock Trading Python App

Aplicación desarrollada en **Python** para la **extracción, procesamiento y carga de datos financieros** provenientes de la **API de Polygon.io**, con almacenamiento en **Snowflake** y opción de automatización mediante tareas programadas.

---

## 🚀 Descripción del proyecto

El proyecto **Stock Trading Python App** permite automatizar la descarga y carga de información de tickers de acciones (stocks) desde la API pública de [Polygon.io](https://polygon.io/), procesarla y almacenarla en una base de datos **Snowflake** para su posterior análisis o integración.

El flujo principal del proyecto es:

1. **Extracción de datos** → se obtienen tickers y su información general desde Polygon.io.  
2. **Procesamiento y limpieza** → se agregan campos adicionales (como el date stamp `ds`).  
3. **Carga (ETL)** → los datos se insertan en una tabla Snowflake.  
4. **Automatización opcional** → se puede programar la ejecución automática mediante cron (Linux/macOS) o Task Scheduler (Windows).

---

## 🧩 Estructura del proyecto

📦 stock-trading-python-app
│
├── script.py # Extrae datos desde Polygon y los guarda en un CSV
├── scriptSnow.py # Extrae datos desde Polygon, agrega ds y los carga en Snowflake
├── schedule.py # Automatiza la ejecución de los scripts anteriores
├── ticker.csv # Archivo de salida local (datos extraídos)
├── .env # Variables de entorno (credenciales y configuración)
└── requirements.txt # Dependencias necesarias



---

## ⚙️ Configuración del entorno

### 1. Clonar el repositorio
```bash
git clone https://github.com/JuancruzHarguindeguy/stock-trading-python-app.git
cd stock-trading-python-app
2. Crear entorno virtual

python -m venv pythonenv
# En Windows (PowerShell)
pythonenv\\Scripts\\activate
# En Linux/Mac
source pythonenv/bin/activate
3. Instalar dependencias

pip install -r requirements.txt
Si no tienes requirements.txt, instala lo necesario:


pip install requests python-dotenv snowflake-connector-python schedule
4. Configurar el archivo .env
Crea un archivo .env en la raíz con tus credenciales y configuración (no lo subas a GitHub). Ejemplo:


POLYGON_API_KEY=tu_api_key_de_polygon

SNOWFLAKE_USER=tu_usuario
SNOWFLAKE_PASSWORD=tu_contraseña
SNOWFLAKE_ACCOUNT=tu_cuenta
SNOWFLAKE_WAREHOUSE=Snowflake_Learning_Warehouse
SNOWFLAKE_DATABASE=tu_database
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_TABLE=stock_tickers
🧠 Uso
▶️ Ejecutar el script que descarga datos y genera el CSV

python script.py
▶️ Ejecutar el script que carga datos en Snowflake

python scriptSnow.py
🕒 Automatizar la ejecución (cron o scheduler)
En Linux / macOS (cron)
Editar el crontab:


crontab -e
Agregar una línea como:


0 7 * * * /usr/bin/python3 /ruta/a/stock-trading-python-app/scriptSnow.py
En Windows (Task Scheduler)
Usar el Programador de tareas o el comando schtasks:


schtasks /create /tn "PipelineSnowflake" /tr "C:\\ruta\\a\\pythonenv\\Scripts\\python.exe C:\\ruta\\a\\stock-trading-python-app\\scriptSnow.py" /sc daily /st 07:00
🧱 Estructura de la tabla en Snowflake

CREATE TABLE stock_tickers (
  ticker VARCHAR,
  name VARCHAR,
  market VARCHAR,
  locale VARCHAR,
  active BOOLEAN,
  source_feed VARCHAR,
  ds VARCHAR
);
Nota: si tu pipeline escribe active como texto, considera convertirlo a booleano antes de insertar o ajustar la columna a VARCHAR. Si cambias tipos, revisa la DDL y/o usa CREATE OR REPLACE TABLE con cuidado.

📊 API utilizada: Polygon.io
Se utiliza el endpoint público:


https://api.polygon.io/v3/reference/tickers
Campos obtenidos:
ticker

name

market

locale

active

source_feed

ds (fecha de extracción agregada por el script)

🔒 Limitaciones (plan gratuito)
El plan básico de Polygon impone las siguientes restricciones (tenlo en cuenta; el script ya contempla esto):

Máximo 5 requests por minuto.

Máximo 1.000 resultados por request.

Los datos de algunos mercados o fuentes pueden estar parcialmente disponibles.

No se incluyen precios ni métricas en tiempo real.

El script implementa una espera automática (p. ej. 60s) después de cada bloque de 5 requests para respetar el límite.

🧰 Dependencias principales
requests — para consumir la API de Polygon.

python-dotenv — para manejar credenciales desde .env.

snowflake-connector-python — para conectar y escribir en Snowflake.

schedule (opcional) — para automatizar ejecuciones desde Python.

📅 Automatización
El archivo schedule.py proporciona lógica para automatizar la ejecución del script deseado.
En sistemas Linux/macOS se recomienda usar cron; en Windows usar Task Scheduler.

🔐 Buenas prácticas
No subas tu .env con credenciales al repositorio.

Añade .env a .gitignore.

Usa un entorno virtual por proyecto (venv).

Revisa los límites de la API de Polygon para no exceder tu plan.

🧠 Autor
Juan Cruz Harguindeguy
Desarrollador Python / Data Engineering

🧾 Licencia
Este proyecto se distribuye bajo la licencia MIT.


