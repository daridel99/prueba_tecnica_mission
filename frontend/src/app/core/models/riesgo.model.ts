export interface IndiceRiesgo {
  pais: string;
  codigo_iso: string;
  indice: number;
  nivel: 'BAJO' | 'MODERADO' | 'ALTO' | 'CRITICO';
  fecha: string;
}
