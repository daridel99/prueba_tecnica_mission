import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Pais } from '../models/pais.model';
import { IndicadorEconomico } from '../models/indicador.model';
import { TipoCambio } from '../models/tipo-cambio.model';
import { PaginatedResponse } from '../models/pagination.model';

@Injectable({ providedIn: 'root' })
export class PaisService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/paises`;

  getAll(params?: HttpParams): Observable<PaginatedResponse<Pais>> {
    return this.http.get<PaginatedResponse<Pais>>(`${this.apiUrl}/`, { params });
  }

  getById(codigoIso: string): Observable<Pais> {
    return this.http.get<Pais>(`${this.apiUrl}/${codigoIso}/`);
  }

  getIndicadores(codigoIso: string): Observable<PaginatedResponse<IndicadorEconomico>> {
    return this.http.get<PaginatedResponse<IndicadorEconomico>>(`${this.apiUrl}/${codigoIso}/indicadores/`);
  }

  getTipoCambio(codigoIso: string): Observable<PaginatedResponse<TipoCambio>> {
    return this.http.get<PaginatedResponse<TipoCambio>>(`${this.apiUrl}/${codigoIso}/tipo-cambio/`);
  }
}
