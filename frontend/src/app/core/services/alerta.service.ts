import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Alerta } from '../models/alerta.model';
import { PaginatedResponse } from '../models/pagination.model';

@Injectable({ providedIn: 'root' })
export class AlertaService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/alertas`;

  getAll(params?: HttpParams): Observable<PaginatedResponse<Alerta>> {
    return this.http.get<PaginatedResponse<Alerta>>(`${this.apiUrl}/`, { params });
  }

  markRead(id: number): Observable<Alerta> {
    return this.http.put<Alerta>(`${this.apiUrl}/${id}/leer/`, {});
  }

  markAllRead(): Observable<unknown> {
    return this.http.put(`${this.apiUrl}/leer-todas/`, {});
  }

  getResumen(): Observable<{ no_leidas: number; total: number }> {
    return this.http.get<{ no_leidas: number; total: number }>(`${this.apiUrl}/resumen/`);
  }
}
