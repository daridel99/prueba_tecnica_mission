import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { PaisService } from '../../../core/services/pais.service';
import { RiesgoService } from '../../../core/services/riesgo.service';
import { Pais } from '../../../core/models/pais.model';
import { IndicadorEconomico } from '../../../core/models/indicador.model';
import { TipoCambio } from '../../../core/models/tipo-cambio.model';
import { IndiceRiesgo } from '../../../core/models/riesgo.model';

@Component({
  selector: 'app-pais-detail',
  standalone: true,
  imports: [
    CommonModule, RouterLink, MatCardModule, MatChipsModule,
    MatIconModule, MatButtonModule, MatTableModule, MatProgressSpinnerModule,
    NgxChartsModule
  ],
  template: `
    @if (loading) {
      <div class="loading-center"><mat-spinner></mat-spinner></div>
    } @else if (pais) {
      <div class="header">
        <button mat-button routerLink="/paises">
          <mat-icon>arrow_back</mat-icon> Volver
        </button>
        <h2>{{ pais.nombre }}</h2>
      </div>

      <div class="info-grid">
        <mat-card>
          <mat-card-header><mat-card-title>Informacion General</mat-card-title></mat-card-header>
          <mat-card-content>
            <div class="info-row"><span class="label">Codigo ISO:</span><span>{{ pais.codigo_iso }}</span></div>
            <div class="info-row"><span class="label">Region:</span><span>{{ pais.region }}</span></div>
            <div class="info-row"><span class="label">Moneda:</span><span>{{ pais.moneda_codigo }} - {{ pais.moneda_nombre }}</span></div>
            <div class="info-row"><span class="label">Poblacion:</span><span>{{ pais.poblacion | number }}</span></div>
          </mat-card-content>
        </mat-card>

        @if (riesgo) {
          <mat-card>
            <mat-card-header><mat-card-title>Indice de Riesgo</mat-card-title></mat-card-header>
            <mat-card-content>
              <div class="risk-display">
                <div class="risk-value" [style.color]="getNivelColor(riesgo.nivel)">{{ riesgo.indice | number:'1.1-1' }}</div>
                <span class="risk-chip" [style.background]="getNivelColor(riesgo.nivel)">{{ riesgo.nivel }}</span>
              </div>
              <div class="info-row"><span class="label">Fecha:</span><span>{{ riesgo.fecha | date:'shortDate' }}</span></div>
            </mat-card-content>
          </mat-card>
        }
      </div>

      @if (indicadores.length > 0) {
        <mat-card class="section-card">
          <mat-card-header><mat-card-title>Indicadores Economicos</mat-card-title></mat-card-header>
          <mat-card-content>
            <div class="indicators-grid">
              @for (ind of indicadores; track ind.id) {
                <mat-card class="indicator-card">
                  <mat-card-content>
                    <div class="ind-type">{{ ind.tipo }}</div>
                    <div class="ind-value">{{ ind.valor | number:'1.2-2' }} {{ ind.unidad }}</div>
                    <div class="ind-year">{{ ind.anio }}</div>
                  </mat-card-content>
                </mat-card>
              }
            </div>
          </mat-card-content>
        </mat-card>

        @if (indicadorChartData.length) {
          <mat-card class="section-card">
            <mat-card-header><mat-card-title>Historico de Indicadores</mat-card-title></mat-card-header>
            <mat-card-content>
              <ngx-charts-line-chart
                [results]="indicadorChartData"
                [xAxis]="true"
                [yAxis]="true"
                [showXAxisLabel]="true"
                [showYAxisLabel]="true"
                [xAxisLabel]="'Anio'"
                [yAxisLabel]="'Valor'"
                [legend]="true"
                [autoScale]="true"
                [view]="[700, 350]">
              </ngx-charts-line-chart>
            </mat-card-content>
          </mat-card>
        }
      }

      @if (tiposCambio.length > 0) {
        <mat-card class="section-card">
          <mat-card-header><mat-card-title>Tipo de Cambio</mat-card-title></mat-card-header>
          <mat-card-content>
            @if (tipoCambioChartData.length) {
              <ngx-charts-line-chart
                [results]="tipoCambioChartData"
                [xAxis]="true"
                [yAxis]="true"
                [showXAxisLabel]="true"
                [showYAxisLabel]="true"
                [xAxisLabel]="'Fecha'"
                [yAxisLabel]="'Tasa'"
                [autoScale]="true"
                [view]="[700, 300]">
              </ngx-charts-line-chart>
            }
            <table mat-table [dataSource]="tiposCambio" class="full-width">
              <ng-container matColumnDef="fecha">
                <th mat-header-cell *matHeaderCellDef>Fecha</th>
                <td mat-cell *matCellDef="let tc">{{ tc.fecha | date:'shortDate' }}</td>
              </ng-container>
              <ng-container matColumnDef="tasa">
                <th mat-header-cell *matHeaderCellDef>Tasa</th>
                <td mat-cell *matCellDef="let tc">{{ tc.tasa | number:'1.4-4' }}</td>
              </ng-container>
              <ng-container matColumnDef="variacion">
                <th mat-header-cell *matHeaderCellDef>Variacion %</th>
                <td mat-cell *matCellDef="let tc" [class]="tc.variacion_porcentual >= 0 ? 'positive' : 'negative'">
                  {{ tc.variacion_porcentual | number:'1.2-2' }}%
                </td>
              </ng-container>
              <tr mat-header-row *matHeaderRowDef="['fecha', 'tasa', 'variacion']"></tr>
              <tr mat-row *matRowDef="let row; columns: ['fecha', 'tasa', 'variacion']"></tr>
            </table>
          </mat-card-content>
        </mat-card>
      }
    }
  `,
  styles: [`
    .loading-center { display: flex; justify-content: center; padding: 48px; }
    .header { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }
    .header h2 { margin: 0; }
    .info-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 16px;
      margin-bottom: 16px;
    }
    .info-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }
    .label { font-weight: 500; color: #666; }
    .risk-display { text-align: center; padding: 16px 0; }
    .risk-value { font-size: 3rem; font-weight: 700; }
    .risk-chip { padding: 4px 16px; border-radius: 12px; color: white; font-weight: 600; }
    .section-card { margin-bottom: 16px; }
    .indicators-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }
    .indicator-card { background: #f8f9fa; }
    .ind-type { font-weight: 600; color: #1e3a5f; text-transform: uppercase; font-size: 0.8rem; }
    .ind-value { font-size: 1.5rem; font-weight: 700; margin: 8px 0; }
    .ind-year { color: #999; font-size: 0.85rem; }
    .full-width { width: 100%; }
    .positive { color: #22c55e; }
    .negative { color: #ef4444; }
    ngx-charts-line-chart { display: block; margin: 0 auto 16px; }
  `]
})
export class PaisDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private paisService = inject(PaisService);
  private riesgoService = inject(RiesgoService);

  pais: Pais | null = null;
  indicadores: IndicadorEconomico[] = [];
  tiposCambio: TipoCambio[] = [];
  riesgo: IndiceRiesgo | null = null;
  loading = true;
  indicadorChartData: any[] = [];
  tipoCambioChartData: any[] = [];

  ngOnInit(): void {
    const codigo = this.route.snapshot.paramMap.get('codigoIso')!;

    this.paisService.getById(codigo).subscribe(data => {
      this.pais = data;
      this.loading = false;
    });

    this.paisService.getIndicadores(codigo).subscribe(data => {
      this.indicadores = data.results || [];
      this.indicadorChartData = this.buildIndicadorChart(this.indicadores);
    });

    this.paisService.getTipoCambio(codigo).subscribe(data => {
      this.tiposCambio = data.results || [];
      this.tipoCambioChartData = this.buildTipoCambioChart(this.tiposCambio);
    });

    this.riesgoService.getByPais(codigo).subscribe({
      next: data => this.riesgo = data,
      error: () => {}
    });
  }

  private buildIndicadorChart(indicadores: IndicadorEconomico[]): any[] {
    const grouped: Record<string, { name: string; value: number }[]> = {};
    for (const ind of indicadores) {
      if (!grouped[ind.tipo]) grouped[ind.tipo] = [];
      grouped[ind.tipo].push({ name: String(ind.anio), value: ind.valor });
    }
    return Object.entries(grouped).map(([name, series]) => ({
      name,
      series: series.sort((a, b) => +a.name - +b.name)
    }));
  }

  private buildTipoCambioChart(datos: TipoCambio[]): any[] {
    if (!datos.length) return [];
    const series = datos
      .slice()
      .sort((a, b) => a.fecha.localeCompare(b.fecha))
      .map(tc => ({ name: tc.fecha, value: tc.tasa }));
    return [{ name: 'Tasa USD', series }];
  }

  getNivelColor(nivel: string): string {
    const colors: Record<string, string> = {
      'BAJO': '#22c55e', 'MODERADO': '#eab308', 'ALTO': '#f97316', 'CRITICO': '#ef4444'
    };
    return colors[nivel] || '#999';
  }
}
