export interface Portafolio {
  id: number;
  nombre: string;
  descripcion: string;
  usuario: number;
  fecha_creacion: string;
  fecha_modificacion: string;
  activo: boolean;
  es_publico: boolean;
  posiciones: Posicion[];
}

export interface Posicion {
  id: number;
  portafolio: number;
  pais: string;
  tipo_activo: 'RENTA_FIJA' | 'RENTA_VARIABLE' | 'COMMODITIES' | 'MONEDA';
  monto_inversion_usd: number;
  fecha_entrada: string;
  fecha_salida: string | null;
  notas: string;
}
