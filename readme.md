## Ejecutables


```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con SECRET_KEY y DATABASE_URL


python manage.py makemigrations 
python manage.py migrate
python manage.py seed_users
python manage.py runserver


## Usuarios de prueba:

| Rol | Email | Password |
|-----|-------|----------|
| Admin | admin@datapulse.com | DataPulse2026! |
| Analista | analista@datapulse.com | DataPulse2026! |
| Viewer | viewer@datapulse.com | DataPulse2026! |


## Estructura del Proyecto

git ls-files > estructura.txt

``` text
.
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
│
├── apps
│   ├── __init__.py
│   │
│   ├── alerts
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   └── migrations
│   │       ├── __init__.py
│   │       └── 0001_initial.py
│   │
│   ├── countries
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── management
│   │   │   └── commands
│   │   │       ├── __init__.py
│   │   │       └── sync_paises.py
│   │   └── migrations
│   │       ├── __init__.py
│   │       ├── 0001_initial.py
│   │       └── 0002_alter_pais_options.py
│   │
│   ├── exchange
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   └── migrations
│   │       ├── __init__.py
│   │       ├── 0001_initial.py
│   │       └── 0002_alter_tipocambio_unique_together_and_more.py
│   │
│   ├── indicators
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── management
│   │   │   └── commands
│   │   │       ├── __init__.py
│   │   │       └── sync_indicadores.py
│   │   └── migrations
│   │       ├── __init__.py
│   │       ├── 0001_initial.py
│   │       └── 0002_rename_fecha_carga_indicadoreconomico_fecha_actualizacion_and_more.py
│   │
│   ├── logs
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   └── migrations
│   │       ├── __init__.py
│   │       └── 0001_initial.py
│   │
│   ├── portfolios
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── migrations
│   │       ├── __init__.py
│   │       └── 0001_initial.py
│   │
│   ├── risk
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── services
│   │   │   └── irpc_service.py
│   │   ├── management
│   │   │   └── commands
│   │   │       ├── __init__.py
│   │   │       └── recalcular_riesgo.py
│   │   └── migrations
│   │       ├── __init__.py
│   │       ├── 0001_initial.py
│   │       └── 0002_indiceriesgo_risk_indice_pais_id_5ba7f4_idx_and_more.py
│   │
│   └── users
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── permissions.py
│       ├── serializers.py
│       ├── urls.py
│       ├── views.py
│       └── migrations
│           ├── __init__.py
│           └── 0001_initial.py
│
└── config
    ├── __init__.py
    ├── asgi.py
    ├── urls.py
    ├── wsgi.py
    └── settings
        ├── __init__.py
        ├── base.py
        ├── local.py
        └── production.py
```

## Diagrama ER

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Usuario   │     │      Pais        │     │  IndiceRiesgo    │
│─────────────│     │──────────────────│     │──────────────────│
│ email       │     │ codigo_iso (PK)  │────>│ pais_id (FK)     │
│ username    │     │ nombre           │     │ score_economico  │
│ rol (ADMIN/ │     │ moneda_codigo    │     │ score_cambiario  │
│  ANALISTA/  │     │ region           │     │ score_estabilidad│
│  VIEWER)    │     │ latitud/longitud │     │ indice_compuesto │
│ is_staff    │     │ poblacion        │     │ clasificacion    │
└──────┬──────┘     │ activo           │     │ fecha_calculo    │
       │            └────────┬─────────┘     └──────────────────┘
       │                     │
       │            ┌────────┴─────────┐
       │            │                  │
       │     ┌──────┴──────┐   ┌──────┴──────────┐
       │     │ Indicador   │   │  TipoCambio     │
       │     │ Economico   │   │─────────────────│
       │     │─────────────│   │ pais_id (FK)    │
       │     │ pais_id(FK) │   │ fecha           │
       │     │ tipo        │   │ tasa            │
       │     │ anio        │   │ variacion_%     │
       │     │ valor       │   └─────────────────┘
       │     └─────────────┘
       │
  ┌────┴────────┐      ┌─────────────┐
  │ Portafolio  │      │  Posicion   │
  │─────────────│      │─────────────│
  │ usuario(FK) │──┐   │ portafolio  │
  │ nombre      │  └──>│ pais (FK)   │
  │ descripcion │      │ tipo_activo │
  │ es_publico  │      │ monto_usd   │
  │ activo      │      │ fecha_entrada│
  └─────────────┘      └─────────────┘

  ┌─────────────┐
  │   Alerta    │
  │─────────────│
  │ usuario(FK) │  (nullable = alerta global)
  │ tipo        │
  │ severidad   │
  │ mensaje     │
  │ leida       │
  └─────────────┘
```
