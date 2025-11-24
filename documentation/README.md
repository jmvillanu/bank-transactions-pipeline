# bank-transactions-pipeline

Este pipeline se encarga de transacciones de un archivo JSONL de una ubicación local en la carpeta data/input y crear una vista agregada para analítica y reportería.

El script fue desarrollado usando Python 3.11.

## Paso 1. Crear un ambiente virtual

```
python3.11 -m venv .venv
```

## Paso 2. Activar el ambiente.

Mac: ```source .venv/bin/activate```

Windows: ```source .venv/Scripts/activate``` desde Git Bash o ```source .venv/Scripts/activate.bat``` desde el Command Prompt

## Paso 3. Instalar las dependencias

Posicionarse en la carpeta src: ```cd src```

Instalar dependencias: ```pip install -r requirements.txt```

## Paso 4. Poner el archivo de transacciones JSONL en la carpeta data/input/

Llevar el archivo de transacciones a la carpeta data/input

## Paso 5. Desde src, correr el script

```python3 main.py --input-filename <nombre-del-archivo>``` 

En nuestro caso, como el archivo se llama **transactions_50k.jsonl**, el comando queda:

```python3 main.py --input-filename transactions_50k.jsonl```

## Paso 6. Revisar la carpeta data/output/

Allí se habrán generado dos archivos:

- view_approved_trxs.parquet --> output
- view_approved_trxs.meta.json --> metadata

## Opcional:

Si lo que se quiere es la vista de las transacciones declinadas o que marcaron error, puede agregarse el flag --trx-status al comando, así:

```python3 main.py --input-filename <nombre-del-archivo> --trx-status declined```

o

```python3 main.py --input-filename <nombre-del-archivo> --trx-status error```

Lo cual generará la vista agregara para cada caso respectivo en la carpeta data/output.

