# CHANGELOG

Todos los cambios notables a este proyecto serán documentados en este archivo.

El formato es basado en: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Por favor, mantener los últimos cambios de primero (ejemplo: de lo más nuevo a lo más viejo).

### Fixed
### Added
### Changed
### Removed

---
## To do

- Agregar al README.md los supuestos hechos
- Separar funciones del archivo main.py y hacer el script más modular
- Agregar la funcionalidad para que el script procese las transacciones con Polars o PySpark (según la necesidad y volumen de los datos).

---
# 2025-11-24

### Description:
Cambio en el nombre del output del script para reflejar que la vista agregada es parte de la capa gold, con el prefijo **gld_** y adición del CHANGELOG.md.

### Changed
- ```main.py```: El output del script se cambió para que tuviera la siguiente estructura: ```f"gld_trxs_{trx_status}_view"``` donde trx_status es el estado de la transacción sobre la que se hace la agregación: approved, declined o error.

### Added

- ```README.md```: Se agregaron las instrucciones para correr el script y generar la vista requerida.
- Carpeta ```documentation/``` en la raíz del proyecto.
- Los archivos README.md y CHANGELOG.md se movieron a la carpeta -> documentation
- ```CHANGELOG.md```: CHANGELOG del proyecto. Conserva el historial de cambios.

# 2025-11-23

### Description:
Se agregó el script de Python que procesa las transacciones y genera la vista requerida, usando Pandas. Ver [PR #2](https://github.com/jmvillanu/bank-transactions-pipeline/pull/2).

### Added
- ```main.py```: Script principal en el directorio src/ . Procesa las transacciones y genera el archivo de salida. Tiene como opcion generar las vistas para transacciones aprobadas, declinadas o con estado "error".

- ```requirements.txt```: Dentro del directorio src/ . Archivo de dependencias.

- ```.gitignore```: Archivo que le dice a git lo que debe omitir. No se sube al repositorio el archivo de transacciones .jsonl.

- ```.gitkeep```: Archivo dentro de la carpeta **data/input/** para que git haga el seguimiento de la carpeta así esté vacía.

- ```README.md```: README del proyecto.