# api-buda
Tarea 1 de buda. Construir una api.

## Ejecución

Para ejecutar el programa es posible usar Docker:

```docker build -t api-buda .```

```docker run -d --name api-buda -p 8000:8000 api-buda```

O bien ejecutar los pasos por separado:

Para instalar las dependencias se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:

```pip install -r requirements.txt```

Para ejecutar el programa se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:

```uvicorn app.main:app```

Para ejecutar los tests se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:

```pytest```

## Documentación
La documentación de la api se encuentra en la siguiente dirección al ejecutar la api:
```http://localhost:8000/docs```

## Consideraciones
- Se utilizó la librería FastAPI para la construcción de la api.
- Se utilizó la librería Pytest para la construcción de los tests.
- Se asumio conocimiento de los mercados o capacidad para consultarlos a Buda.
- Para el polling se asumio una forma de entregar el dato mayor o menor conveniente para el usuario (un parametro booleano indicando si el spread actual es mayor que la alerta), se entrego un endpoint GET para este punto.