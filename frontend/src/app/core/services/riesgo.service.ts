import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { IndiceRiesgo } from '../models/riesgo.model';
import { PaginatedResponse } from '../models/pagination.model';

@Injectable({ providedIn: 'root' })
export class RiesgoService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/riesgo`;

  getAll(): Observable<IndiceRiesgo[] | PaginatedResponse<IndiceRiesgo>> {
    return this.http.get<IndiceRiesgo[] | PaginatedResponse<IndiceRiesgo>>(`${this.apiUrl}/`);
  }

  getByPais(codigoIso: string): Observable<IndiceRiesgo> {
    return this.http.get<IndiceRiesgo>(`${this.apiUrl}/${codigoIso}/`);
  }

  getHistorico(codigoIso: string): Observable<IndiceRiesgo[]> {
    return this.http.get<IndiceRiesgo[]>(`${this.apiUrl}/${codigoIso}/historico/`);
  }

  calcular(): Observable<unknown> {
    return this.http.post(`${this.apiUrl}/calcular/`, {});
  }
}
