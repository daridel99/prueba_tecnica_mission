export interface DashboardResumen {
  total_paises: number;
  alertas_activas: number;
  portafolios: number;
  riesgo_promedio: number;
}

export interface MapaPais {
  pais: string;
  codigo: string;
  lat: number;
  lng: number;
  riesgo: number | null;
}

export interface Tendencia {
  pais: string;
  codigo_iso: string;
  datos: { anio: number; valor: number }[];
}
