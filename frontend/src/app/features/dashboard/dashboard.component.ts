import { Component, inject, OnInit, AfterViewInit, OnDestroy, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { DashboardService } from '../../core/services/dashboard.service';
import { RiesgoService } from '../../core/services/riesgo.service';
import { DashboardResumen, MapaPais } from '../../core/models/dashboard.model';
import { IndiceRiesgo } from '../../core/models/riesgo.model';
import * as L from 'leaflet';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule, RouterLink, ReactiveFormsModule,
    MatCardModule, MatTableModule, MatChipsModule, MatIconModule,
    MatProgressSpinnerModule, MatFormFieldModule, MatSelectModule,
    NgxChartsModule
  ],
  template: `
    <h2>Dashboard</h2>

    @if (loading) {
      <div class="loading-center"><mat-spinner></mat-spinner></div>
    } @else {
      <div class="kpi-grid">
        <mat-card class="kpi-card">
          <mat-card-content>
            <mat-icon color="primary">public</mat-icon>
            <div class="kpi-value">{{ resumen?.total_paises || 0 }}</div>
            <div class="kpi-label">Total Paises</div>
          </mat-card-content>
        </mat-card>
        <mat-card class="kpi-card">
          <mat-card-content>
            <mat-icon class="warn-icon">warning</mat-icon>
            <div class="kpi-value">{{ resumen?.alertas_activas || 0 }}</div>
            <div class="kpi-label">Alertas Activas</div>
          </mat-card-content>
        </mat-card>
        <mat-card class="kpi-card">
          <mat-card-content>
            <mat-icon color="accent">account_balance_wallet</mat-icon>
            <div class="kpi-value">{{ resumen?.portafolios || 0 }}</div>
            <div class="kpi-label">Portafolios</div>
          </mat-card-content>
        </mat-card>
        <mat-card class="kpi-card">
          <mat-card-content>
            <mat-icon [style.color]="getRiesgoColor(resumen?.riesgo_promedio || 0)">speed</mat-icon>
            <div class="kpi-value">{{ (resumen?.riesgo_promedio || 0) | number:'1.1-1' }}</div>
            <div class="kpi-label">Riesgo Promedio</div>
          </mat-card-content>
        </mat-card>
      </div>

      <div class="dashboard-grid">
        <mat-card class="map-card">
          <mat-card-header><mat-card-title>Mapa de Riesgo</mat-card-title></mat-card-header>
          <mat-card-content>
            <div #mapContainer class="map-container"></div>
          </mat-card-content>
        </mat-card>

        <mat-card class="ranking-card">
          <mat-card-header><mat-card-title>Ranking de Riesgo</mat-card-title></mat-card-header>
          <mat-card-content>
            <table mat-table [dataSource]="riesgos" class="full-width">
              <ng-container matColumnDef="pais">
                <th mat-header-cell *matHeaderCellDef>Pais</th>
                <td mat-cell *matCellDef="let r">
                  <a [routerLink]="['/paises', r.codigo_iso]">{{ r.pais }}</a>
                </td>
              </ng-container>
              <ng-container matColumnDef="indice">
                <th mat-header-cell *matHeaderCellDef>Indice</th>
                <td mat-cell *matCellDef="let r">{{ r.indice | number:'1.1-1' }}</td>
              </ng-container>
              <ng-container matColumnDef="nivel">
                <th mat-header-cell *matHeaderCellDef>Nivel</th>
                <td mat-cell *matCellDef="let r">
                  <span class="risk-chip" [style.background]="getNivelColor(r.nivel)">{{ r.nivel }}</span>
                </td>
              </ng-container>
              <tr mat-header-row *matHeaderRowDef="['pais', 'indice', 'nivel']"></tr>
              <tr mat-row *matRowDef="let row; columns: ['pais', 'indice', 'nivel']"></tr>
            </table>
          </mat-card-content>
        </mat-card>
      </div>

      <mat-card class="chart-card">
        <mat-card-header>
          <mat-card-title>Tendencias de Indicadores</mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div class="chart-filters">
            <mat-form-field appearance="outline">
              <mat-label>Indicador</mat-label>
              <mat-select [formControl]="tipoControl" (selectionChange)="loadTendencias()">
                <mat-option value="PIB">PIB</mat-option>
                <mat-option value="INFLACION">Inflacion</mat-option>
                <mat-option value="DESEMPLEO">Desempleo</mat-option>
                <mat-option value="PIB_PERCAPITA">PIB Per Capita</mat-option>
                <mat-option value="DEUDA_PIB">Deuda/PIB</mat-option>
                <mat-option value="BALANZA_COMERCIAL">Balanza Comercial</mat-option>
              </mat-select>
            </mat-form-field>
          </div>
          @if (chartData.length) {
            <ngx-charts-line-chart
              [results]="chartData"
              [xAxis]="true"
              [yAxis]="true"
              [showXAxisLabel]="true"
              [showYAxisLabel]="true"
              [xAxisLabel]="'Anio'"
              [yAxisLabel]="tipoControl.value || 'Valor'"
              [legend]="true"
              [autoScale]="true"
              [view]="[700, 350]">
            </ngx-charts-line-chart>
          } @else {
            <p class="no-data">No hay datos de tendencias disponibles</p>
          }
        </mat-card-content>
      </mat-card>
    }
  `,
  styles: [`
    .loading-center { display: flex; justify-content: center; padding: 48px; }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .kpi-card mat-card-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; margin: 8px 0 4px; }
    .kpi-label { color: #666; font-size: 0.9rem; }
    .warn-icon { color: #f97316; }
    .dashboard-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
    }
    @media (max-width: 960px) {
      .dashboard-grid { grid-template-columns: 1fr; }
    }
    .map-container { height: 400px; border-radius: 8px; }
    .full-width { width: 100%; }
    .risk-chip {
      padding: 4px 12px;
      border-radius: 12px;
      color: white;
      font-size: 0.75rem;
      font-weight: 600;
    }
    a { color: #1e3a5f; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .chart-card { margin-bottom: 16px; }
    .chart-filters { margin-bottom: 16px; }
    .no-data { text-align: center; color: #999; padding: 24px; }
    ngx-charts-line-chart { display: block; margin: 0 auto; }
  `]
})
export class DashboardComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('mapContainer') mapContainer!: ElementRef;

  private dashboardService = inject(DashboardService);
  private riesgoService = inject(RiesgoService);

  resumen: DashboardResumen | null = null;
  mapData: MapaPais[] = [];
  riesgos: IndiceRiesgo[] = [];
  loading = true;
  chartData: any[] = [];
  tipoControl = new FormControl('INFLACION');
  private map: L.Map | null = null;

  ngOnInit(): void {
    this.dashboardService.getResumen().subscribe(data => {
      this.resumen = data;
    });

    this.dashboardService.getMapa().subscribe(data => {
      this.mapData = data;
      this.initMap();
    });

    this.riesgoService.getAll().subscribe(data => {
      this.riesgos = (Array.isArray(data) ? data : data.results || []).sort((a, b) => b.indice - a.indice);
      this.loading = false;
    });

    this.loadTendencias();
  }

  loadTendencias(): void {
    this.dashboardService.getTendencias(this.tipoControl.value || 'INFLACION').subscribe(data => {
      this.chartData = this.transformTendencias(data);
    });
  }

  private transformTendencias(data: any[]): any[] {
    const grouped: Record<string, { name: string; value: number }[]> = {};
    for (const item of data) {
      const key = item.pais;
      if (!grouped[key]) grouped[key] = [];
      grouped[key].push({ name: String(item.anio), value: item.valor });
    }
    return Object.entries(grouped).map(([name, series]) => ({ name, series }));
  }

  ngAfterViewInit(): void {
    setTimeout(() => this.initMap(), 500);
  }

  private initMap(): void {
    if (!this.mapContainer?.nativeElement || this.map) return;

    this.map = L.map(this.mapContainer.nativeElement).setView([-15, -60], 3);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap'
    }).addTo(this.map);

    this.mapData.forEach(p => {
      if (p.lat && p.lng) {
        const color = this.getRiesgoColor(p.riesgo || 0);
        L.circleMarker([p.lat, p.lng], {
          radius: 10,
          fillColor: color,
          color: '#333',
          weight: 1,
          fillOpacity: 0.8
        }).bindPopup(`<strong>${p.pais}</strong><br>Riesgo: ${p.riesgo ?? 'N/A'}`)
          .addTo(this.map!);
      }
    });
  }

  getRiesgoColor(value: number): string {
    if (value >= 75) return '#22c55e';
    if (value >= 50) return '#eab308';
    if (value >= 25) return '#f97316';
    return '#ef4444';
  }

  getNivelColor(nivel: string): string {
    const colors: Record<string, string> = {
      'BAJO': '#22c55e',
      'MODERADO': '#eab308',
      'ALTO': '#f97316',
      'CRITICO': '#ef4444'
    };
    return colors[nivel] || '#999';
  }

  ngOnDestroy(): void {
    this.map?.remove();
  }
}
