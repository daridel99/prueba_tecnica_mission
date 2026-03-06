from apps.logs.models import LogActividad


def registrar_log(usuario=None, accion=None, entidad=None, entidad_id=None, detalle=None, request=None):

    ip = None

    if request:
        ip = request.META.get("REMOTE_ADDR")

    LogActividad.objects.create(
        usuario=usuario,
        accion=accion,
        entidad_afectada=entidad,
        entidad_id=entidad_id,
        detalle=detalle or {},
        ip_address=ip
    )