import requests
from django.core.management.base import BaseCommand
from apps.countries.models import Pais
from apps.logs.services.log_service import registrar_log


PAISES = ["CO", "BR", "MX", "AR", "CL", "PE", "EC", "UY", "PY", "PA"]

API_URL = "https://restcountries.com/v3.1/alpha/"


REGION_MAP = {
    "CO": "ANDINA",
    "EC": "ANDINA",
    "PE": "ANDINA",
    "CL": "CONO_SUR",
    "AR": "CONO_SUR",
    "UY": "CONO_SUR",
    "PY": "CONO_SUR",
    "BR": "CONO_SUR",
    "MX": "CENTROAMERICA",
    "PA": "CENTROAMERICA"
}


class Command(BaseCommand):

    help = "Sincroniza países desde REST Countries API"

    def handle(self, *args, **kwargs):

        for codigo in PAISES:

            try:

                url = f"{API_URL}{codigo}"
                response = requests.get(url)

                if response.status_code != 200:

                    self.stdout.write(f"Error consultando {codigo}")

                    registrar_log(
                        accion="ERROR",
                        entidad="Pais",
                        entidad_id=codigo,
                        detalle={
                            "mensaje": "Error consultando API REST Countries"
                        }
                    )

                    continue

                data = response.json()[0]

                nombre = data["name"]["common"]
                poblacion = data.get("population", 0)

                latlng = data.get("latlng", [0, 0])
                lat = latlng[0]
                lon = latlng[1]

                currency_data = data.get("currencies", {})

                moneda_codigo = None
                moneda_nombre = None

                if currency_data:
                    moneda_codigo = list(currency_data.keys())[0]
                    moneda_nombre = currency_data[moneda_codigo]["name"]

                region = REGION_MAP.get(codigo)

                pais, created = Pais.objects.update_or_create(
                    codigo_iso=codigo,
                    defaults={
                        "nombre": nombre,
                        "moneda_codigo": moneda_codigo,
                        "moneda_nombre": moneda_nombre,
                        "region": region,
                        "latitud": lat,
                        "longitud": lon,
                        "poblacion": poblacion,
                        "activo": True
                    }
                )

                accion = "CREAR" if created else "EDITAR"

                registrar_log(
                    accion=accion,
                    entidad="Pais",
                    entidad_id=pais.codigo_iso,
                    detalle={
                        "nombre": nombre,
                        "region": region
                    }
                )

                self.stdout.write(f"✔ Pais sincronizado: {nombre}")

            except Exception as e:

                self.stdout.write(f"X Pais NO sincronizado: {codigo}")

                registrar_log(
                    accion="ERROR",
                    entidad="Pais",
                    entidad_id=codigo,
                    detalle={
                        "error": str(e)
                    }
                )

        self.stdout.write(self.style.SUCCESS("Países sincronizados correctamente"))