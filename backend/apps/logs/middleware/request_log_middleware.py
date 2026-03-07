import time
import logging
from apps.logs.services.log_service import registrar_log

logger = logging.getLogger(__name__)

EXCLUDED_PATHS = ["/admin/", "/api/docs/", "/api/schema/", "/static/"]
METHOD_ACTION_MAP = {
    "GET": "CONSULTAR", "POST": "CREAR",
    "PUT": "EDITAR", "PATCH": "EDITAR", "DELETE": "ELIMINAR",
}


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = round(time.time() - start_time, 3)

        if any(request.path.startswith(p) for p in EXCLUDED_PATHS):
            return response
        if not request.user.is_authenticated:
            return response

        user = request.user
        accion = METHOD_ACTION_MAP.get(request.method, "CONSULTAR")
        try:
            registrar_log(
                usuario=user, accion=accion, entidad=request.path,
                entidad_id=str(user.id),
                detalle={"metodo": request.method, "duracion": duration, "status": response.status_code},
                request=request
            )
        except Exception as e:
            logger.error(f"Error registrando log request: {str(e)}")

        logger.info(f"{request.method} {request.path} {response.status_code} {duration}s")
        return response
