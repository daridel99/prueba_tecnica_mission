import time
import logging
from apps.logs.services.log_service import registrar_log

logger = logging.getLogger(__name__)


class RequestLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        response = self.get_response(request)

        duration = round(time.time() - start_time, 3)

        user = None

        if request.user.is_authenticated:
            user = request.user

        try:

            registrar_log(
                usuario=user,
                accion="CONSULTAR",
                entidad=request.path,
                entidad_id=None,
                detalle={
                    "metodo": request.method,
                    "duracion": duration,
                    "status": response.status_code
                },
                request=request
            )

        except Exception as e:

            logger.error(f"Error registrando log request: {str(e)}")

        logger.info(
            f"{request.method} {request.path} "
            f"{response.status_code} "
            f"{duration}s"
        )

        return response