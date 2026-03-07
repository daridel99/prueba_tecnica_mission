import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { DashboardResumen, MapaPais, Tendencia } from '../models/dashboard.model';

@Injectable({ providedIn: 'root' })
export class DashboardService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/dashboard`;

  getResumen(): Observable<DashboardResumen> {
    return this.http.get<DashboardResumen>(`${this.apiUrl}/resumen/`);
  }

  getMapa(): Observable<MapaPais[]> {
    return this.http.get<MapaPais[]>(`${this.apiUrl}/mapa/`);
  }

  getTendencias(tipo?: string, pais?: string): Observable<Tendencia[]> {
    let params = new HttpParams();
    if (tipo) params = params.set('tipo', tipo);
    if (pais) params = params.set('pais', pais);
    return this.http.get<Tendencia[]>(`${this.apiUrl}/tendencias/`, { params });
  }
}
