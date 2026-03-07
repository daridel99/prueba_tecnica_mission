# DataPulse Latam

Plataforma de monitoreo de indicadores economicos y riesgo pais para America Latina.

## Arquitectura

```
prueba_tecnica_mission/
├── backend/                  # Django REST Framework API
│   ├── apps/
│   │   ├── alerts/           # Alertas y notificaciones
│   │   ├── countries/        # Paises y datos geograficos
│   │   ├── dashboard/        # Endpoints agregados del dashboard
│   │   ├── exchange/         # Tipos de cambio
│   │   ├── indicators/       # Indicadores economicos
│   │   ├── logs/             # Middleware de auditoria
│   │   ├── portfolios/       # Portafolios de inversion
│   │   ├── risk/             # Calculo IRPC (Indice de Riesgo Pais Compuesto)
│   │   └── users/            # Autenticacion y roles
│   ├── config/
│   │   └── settings/         # base.py, production.py
│   └── manage.py
├── frontend/                 # Angular 17 (standalone components)
│   └── src/app/
│       ├── core/             # Services, guards, interceptors, models
│       ├── features/         # Auth, Dashboard, Paises, Portafolios, Alertas
│       └── shared/           # Componentes reutilizables
├── docker-compose.yml
└── README.md
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

## IRPC - Indice de Riesgo Pais Compuesto

El IRPC evalua el riesgo de inversion en cada pais usando 3 dimensiones:

| Dimension | Peso | Factores |
|-----------|------|----------|
| Score Economico | 40% | PIB per capita, inflacion, desempleo, deuda/PIB |
| Score Cambiario | 30% | Volatilidad tipo de cambio (30 dias), depreciacion |
| Score Estabilidad | 30% | Balanza comercial, tendencia PIB, concentracion riesgo |

**Formula:** `IRPC = (Score_Economico * 0.40) + (Score_Cambiario * 0.30) + (Score_Estabilidad * 0.30)`

**Clasificacion:**
- **BAJO** (75-100): Favorable para inversion
- **MODERADO** (50-74): Invertir con precaucion
- **ALTO** (25-49): Reducir exposicion
- **CRITICO** (0-24): Evitar nueva inversion

## Decisiones Tecnicas

- **JWT (SimpleJWT)**: Autenticacion stateless con access/refresh tokens
- **Roles**: ADMIN (staff+superuser), ANALISTA (CRUD portafolios), VIEWER (solo lectura)
- **Soft Delete**: Portafolios usan `activo=False` en lugar de eliminacion fisica
- **IRPC por penalizacion**: Parte de 100 y resta segun umbrales (mas intuitivo que suma)
- **N+1 optimizado**: Dashboard usa `Subquery` + `annotate` en lugar de queries por pais
- **Alertas globales**: `usuario=null` para alertas del sistema visibles a todos
- **Angular standalone**: Sin NgModules, lazy loading por rutas

## Instalacion

### Con Docker (recomendado)

```bash
git clone <repo-url>
cd prueba_tecnica_mission
docker-compose up --build
```

- Frontend: http://localhost
- Backend API: http://localhost:8000/api/
- Swagger: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

### Manual

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con SECRET_KEY y DATABASE_URL

python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

**Frontend:**

```bash
cd frontend
npm install
ng serve
```

Abrir http://localhost:4200

## Credenciales de Prueba

| Rol | Email | Password |
|-----|-------|----------|
| Admin | admin@datapulse.com | DataPulse2026! |
| Analista | analista@datapulse.com | DataPulse2026! |
| Viewer | viewer@datapulse.com | DataPulse2026! |

## API Endpoints

| Recurso | Endpoint | Metodos |
|---------|----------|---------|
| Auth Login | `/api/auth/login/` | POST |
| Auth Register | `/api/auth/register/` | POST |
| Auth Me | `/api/auth/me/` | GET |
| Token Refresh | `/api/auth/refresh/` | POST |
| Paises | `/api/paises/` | GET |
| Pais Detalle | `/api/paises/{codigo_iso}/` | GET |
| Pais Indicadores | `/api/paises/{codigo_iso}/indicadores/` | GET |
| Indicadores | `/api/indicators/indicadores/` | GET |
| Tipos Cambio | `/api/indicators/tipos-cambio/` | GET |
| Dashboard Mapa | `/api/dashboard/mapa/` | GET |
| Dashboard Resumen | `/api/dashboard/resumen/` | GET |
| Dashboard Tendencias | `/api/dashboard/tendencias/` | GET |
| Portafolios | `/api/portafolios/` | GET, POST |
| Portafolio Detalle | `/api/portafolios/{id}/` | GET, PUT, DELETE |
| Portafolio Resumen | `/api/portafolios/{id}/resumen/` | GET |
| Posiciones | `/api/portafolios/{id}/posiciones/` | POST |
| Alertas | `/api/alertas/` | GET |
| Alerta Leer | `/api/alertas/{id}/marcar_leida/` | POST |
| Riesgo Pais | `/api/riesgo/{codigo_iso}/` | GET |
| Riesgo Calcular | `/api/riesgo/{codigo_iso}/calcular/` | POST |
| Swagger Docs | `/api/docs/` | GET |

## Tests

```bash
cd backend
python manage.py test --verbosity=2
```

23 tests cubriendo:
- Calculo IRPC (7 tests): scores economico/cambiario, clasificacion, creacion de registros
- Autenticacion (7 tests): login, registro, permisos por rol, endpoint /me
- Portafolios (4 tests): CRUD, permisos VIEWER, soft delete, resumen
- Paises (5 tests): listado, busqueda, filtros, autenticacion

## Datos Seed

El comando `seed_data` carga:
- 10 paises latinoamericanos (CO, BR, MX, AR, CL, PE, EC, UY, PY, PA)
- 180 indicadores economicos (6 tipos x 3 anios x 10 paises)
- 310 registros de tipo de cambio (31 dias x 10 paises)
- 10 indices de riesgo IRPC calculados
- 2 portafolios de ejemplo con 8 posiciones
- 4 alertas de ejemplo
- 3 usuarios (admin, analista, viewer)
