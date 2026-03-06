from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Portafolio, Posicion
from .serializers import PortafolioSerializer, PosicionSerializer
from apps.users.permissions import IsAdminOrOwnerOrReadOnly
from apps.logs.services.log_service import registrar_log

class PortafolioViewSet(viewsets.ModelViewSet):

    serializer_class = PortafolioSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        return Portafolio.objects.filter(
            Q(usuario=user) | Q(es_publico=True),
            activo=True
        )

    def perform_create(self, serializer):

        portafolio = serializer.save(usuario=self.request.user)

        registrar_log(
            usuario=self.request.user,
            accion="CREAR",
            entidad="Portafolio",
            entidad_id=portafolio.id,
            detalle={"nombre": portafolio.nombre},
            request=self.request
        )

    @action(detail=True, methods=["get"])
    def resumen(self, request, pk=None):

        portafolio = self.get_object()

        posiciones = portafolio.posiciones.filter(fecha_salida__isnull=True)

        total = posiciones.count()

        por_pais = {}
        por_activo = {}

        for p in posiciones:

            pais = p.pais.nombre
            activo = p.tipo_activo

            por_pais[pais] = por_pais.get(pais, 0) + p.monto
            por_activo[activo] = por_activo.get(activo, 0) + p.monto

        data = {
            "total_posiciones": total,
            "distribucion_pais": por_pais,
            "distribucion_tipo_activo": por_activo
        }

        return Response(data)

    @action(detail=True, methods=["post"])
    def posiciones(self, request, pk=None):

        portafolio = self.get_object()

        serializer = PosicionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(portafolio=portafolio)

            registrar_log(
                usuario=request.user,
                accion="CREAR",
                entidad="Posicion",
                entidad_id=serializer.instance.id,
                detalle={"portafolio": portafolio.id},
                request=request
            )

            return Response({
                "mensaje": "Posición creada",
                "posicion": serializer.data
            })

        return Response(serializer.errors, status=400)

    @action( detail=True, methods=["put", "delete"], url_path=r"posiciones/(?P<posicion_id>[^/.]+)" )
    def posiciones_detalle(self, request, pk=None, posicion_id=None):

        portafolio = self.get_object()

        posicion = Posicion.objects.get(
            id=posicion_id,
            portafolio=portafolio
        )

        if request.method == "PUT":

            serializer = PosicionSerializer(posicion, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=400)

        if request.method == "DELETE":

            print(posicion.fecha_entrada)
            posicion.fecha_salida = timezone.now()
            print(posicion.fecha_salida)
            posicion.save()

            return Response({
                "mensaje": "Posición cerrada"
            })
        
    @action(detail=True, methods=["get"], url_path="export/pdf")
    def export_pdf(self, request, pk=None):

        portafolio = self.get_object()

        posiciones = portafolio.posiciones.filter(fecha_salida__isnull=True)
        posiciones_ = portafolio.posiciones.filter(fecha_salida__isnull=False)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="portafolio_{portafolio.id}.pdf"'

        pdf = canvas.Canvas(response, pagesize=letter)

        y = 750

        # -------------------------
        # TITULO
        # -------------------------

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, f"Reporte Portafolio: {portafolio.nombre}")

        y -= 40

        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y, f"Usuario: {portafolio.usuario.email}")

        y -= 20
        pdf.drawString(50, y, f"Fecha creación: {portafolio.fecha_creacion.strftime('%d/%m/%Y')}")

        y -= 40

        # -------------------------
        # POSICIONES ACTIVAS
        # -------------------------

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Posiciones activas")

        y -= 30

        pdf.setFont("Helvetica", 11)

        total = 0

        for p in posiciones:

            linea = f"{p.pais.nombre} | {p.tipo_activo} | USD {p.monto_inversion_usd}"

            pdf.drawString(50, y, linea)

            total += float(p.monto_inversion_usd)

            y -= 20

            if y < 100:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = 750

        y -= 10

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, f"Total invertido (activo): USD {total}")

        y -= 40

        # -------------------------
        # POSICIONES INACTIVAS
        # -------------------------

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Posiciones inactivas")

        y -= 30

        pdf.setFont("Helvetica", 11)

        total = 0

        for p in posiciones_:

            linea = f"{p.pais.nombre} | {p.tipo_activo} | USD {p.monto_inversion_usd}"

            pdf.drawString(50, y, linea)

            total += float(p.monto_inversion_usd)

            y -= 20

            if y < 100:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = 750

        y -= 10

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, f"Total invertido (cerrado): USD {total}")

        pdf.save()

        return response