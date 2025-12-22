#  Adquisición de Datos para Predicción de Inundaciones

Proyecto centrado en la **obtención, preparación y transformación de datos** para la **predicción de inundaciones en zonas urbanas**, con el objetivo de facilitar el desarrollo de modelos predictivos precisos y sistemas de alerta temprana.

##  Integrantes
- Jose Francisco Pérez Mompeán  
- Gabriel Niculescu Ruso 
- Jorge Soto Tripiana  

##  Objetivo del Proyecto
El objetivo principal es **adquirir y preparar datos medioambientales** que permitan entrenar un modelo capaz de **anticipar inundaciones con al menos un 90% de detección**, reduciendo así:
- Pérdidas humanas  
- Daños a infraestructuras  
- Impacto económico y social  

Este tipo de modelo podría ser utilizado por **gobiernos y organismos de protección civil**, integrándose en sistemas de alerta temprana o en la planificación urbana.

---

## Análisis y Necesidades de Datos

### Variables Utilizadas
- **Hidrológicas**: precipitación, escorrentía, caudal del río, evaporación  
- **Suelo**: humedad y agua volumétrica del suelo  
- **Atmosféricas**: presión, temperatura, humedad relativa, viento  
- **Geográficas y temporales**: elevación, fecha y hora  

Todas las variables son **numéricas**, ya que permiten medir acumulaciones y anomalías relevantes para la detección de inundaciones.

### Fuentes de Datos
- **OpenMeteo**: datos de estaciones meteorológicas  
- **ERA5 Land**: datos satelitales  

Ambas fuentes se complementan y proporcionan datos en formato **CSV**, facilitando su procesamiento con herramientas ETL y Python.

---

##  Diseño del Almacén de Datos

Se diseñó un **Data Warehouse con esquema estrella**, optimizado para consultas analíticas:

- **Tabla de Hechos (Hidrología)**: métricas ambientales clave  
- **Dimensión Geografía**: ciudad, latitud y longitud  
- **Dimensión Tiempo**: año, mes, día y hora  

Se añadió la variable **`inundado` (0/1)** como etiqueta (*label*) para el entrenamiento de modelos predictivos.

El diseño:
- Conceptual: draw.io  
- Lógico y físico: MySQL Workbench  
- Implementación automática mediante *forward engineering*

---

##  Limpieza, Transformación y Normalización

El proceso ETL se realizó con **Pentaho (.ktr)**:

1. **Unificación de CSVs**  
   - 8 archivos combinados  
   - Añadida columna de ciudad (Valencia, Bangkok, Houston, Mumbai)  

2. **Normalización de unidades**  
   - Ajuste de unidades inconsistentes en ERA5  

3. **Normalización estructural**  
   - Conversión de OpenMeteo a formato horario (similar a ERA5)  

4. **JOIN de datasets**  
   - RIGHT OUTER JOIN usando ERA5 como base  
   - Evita pérdida de datos históricos  

5. **Ajustes finales**  
   - Promedio de variables duplicadas  
   - Eliminación de columnas redundantes  

---

## 🔄 Transformación Semántica de los Datos

Los datos se transformaron a **RDF** usando:
- Tripletas **Sujeto–Predicado–Objeto**
- Vocabularios **Schema.org**
- Enriquecimiento con **Wikidata** mediante consultas SPARQL  

### Entidades Principales
- **Place**: ciudades (URI propia + enlace a Wikidata)  
- **Event**: eventos climáticos asociados a una fecha y lugar  

Se estableció una relación bidireccional entre eventos y lugares para facilitar la interoperabilidad en la Web Semántica.

---

## 📈 Visualización de Datos

Se realizaron visualizaciones exploratorias para identificar relaciones clave:

- **Precipitación vs. absorción del suelo**  
  - Relación no lineal (exponencial)  
  - Alta acumulación → mayor riesgo de inundación  

- **Presión atmosférica vs. precipitación**  
  - Inundaciones asociadas a **baja presión**  

Se utilizaron **regresores lineales** para el análisis inicial, detectando posteriormente dependencias no lineales relevantes.

> Las visualizaciones pueden consultarse en el repositorio.

---

## 💻 Repositorio de Código

📎 **GitHub**:  
https://github.com/jfpm10-ua/Inundaciones_APD.git

Incluye:
- Procesos ETL (Pentaho)
- Scripts de transformación RDF
- Diseños del Data Warehouse
- Visualizaciones
- Scripts para obtener datos

---

