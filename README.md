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

	git clone https://github.com/JuancruzHarguindeguy/stock-trading-python-app.git
	cd stock-trading-python-app
###2. Crear entorno virtual
	python -m venv pythonenv
---
	 En Windows (PowerShell)
	pythonenv\\Scripts\\activate
---
	En Linux/Mac
	source pythonenv/bin/activate

###3. Instalar dependencias
	pip install -r requirements.txt


