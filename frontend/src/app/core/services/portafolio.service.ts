import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Portafolio, Posicion } from '../models/portafolio.model';
import { PaginatedResponse } from '../models/pagination.model';

@Injectable({ providedIn: 'root' })
export class PortafolioService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/portafolios`;

  getAll(): Observable<PaginatedResponse<Portafolio>> {
    return this.http.get<PaginatedResponse<Portafolio>>(`${this.apiUrl}/`);
  }

  getById(id: number): Observable<Portafolio> {
    return this.http.get<Portafolio>(`${this.apiUrl}/${id}/`);
  }

  create(data: Partial<Portafolio>): Observable<Portafolio> {
    return this.http.post<Portafolio>(`${this.apiUrl}/`, data);
  }

  update(id: number, data: Partial<Portafolio>): Observable<Portafolio> {
    return this.http.put<Portafolio>(`${this.apiUrl}/${id}/`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}/`);
  }

  getResumen(id: number): Observable<unknown> {
    return this.http.get(`${this.apiUrl}/${id}/resumen/`);
  }

  exportPdf(id: number): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/${id}/export/pdf/`, { responseType: 'blob' });
  }

  createPosicion(portafolioId: number, data: Partial<Posicion>): Observable<Posicion> {
    return this.http.post<Posicion>(`${this.apiUrl}/${portafolioId}/posiciones/`, data);
  }

  updatePosicion(portafolioId: number, posicionId: number, data: Partial<Posicion>): Observable<Posicion> {
    return this.http.put<Posicion>(`${this.apiUrl}/${portafolioId}/posiciones/${posicionId}/`, data);
  }

  deletePosicion(portafolioId: number, posicionId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${portafolioId}/posiciones/${posicionId}/`);
  }
}
