#tree /f > estructura.txt

#git ls-files > estructura.txt

## Estructura del Proyecto

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