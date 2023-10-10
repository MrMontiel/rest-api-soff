# RestAPI/FastAPI - SOFF

Instalar Dependencias
`
pip install -r requirements.txt
`

Correr Aplicación
`
uvicorn main:app --reload
`


#### Migrations

* Para correr las migraciones solo tiene que agregar los modelos al archivo `env.py` de la carpeta `alembic`.

Los comandos son los siguientes:
Para correr las migraciones.
```
alembic revision --autogenerate
```
Para crear las tablas en la base de datos
```
alembic upgrade head
```