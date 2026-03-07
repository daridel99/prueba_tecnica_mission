export interface TipoCambio {
  id: number;
  pais: string;
  moneda_destino: string;
  tasa: number;
  fecha: string;
  variacion_porcentual: number;
  fuente: string;
}
