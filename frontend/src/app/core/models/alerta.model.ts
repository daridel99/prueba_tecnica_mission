export interface Alerta {
  id: number;
  usuario: number | null;
  pais: string;
  tipo_alerta: 'RIESGO' | 'TIPO_CAMBIO' | 'INDICADOR';
  severidad: 'INFO' | 'WARNING' | 'CRITICAL';
  titulo: string;
  mensaje: string;
  leida: boolean;
  fecha_creacion: string;
}
