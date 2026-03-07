import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpParams } from '@angular/common/http';
import { AlertaService } from '../../core/services/alerta.service';
import { Alerta } from '../../core/models/alerta.model';

@Component({
  selector: 'app-alertas',
  standalone: true,
  imports: [
    CommonModule, FormsModule, MatTableModule, MatButtonModule,
    MatIconModule, MatFormFieldModule, MatSelectModule,
    MatChipsModule, MatPaginatorModule, MatProgressSpinnerModule
  ],
  template: `
    <div class="header">
      <h2>Alertas</h2>
      <button mat-raised-button color="primary" (click)="markAllRead()">
        <mat-icon>done_all</mat-icon> Marcar todas leidas
      </button>
    </div>

    <div class="filters">
      <mat-form-field appearance="outline">
        <mat-label>Tipo</mat-label>
        <mat-select [(ngModel)]="tipoFilter" (selectionChange)="loadData()">
          <mat-option value="">Todos</mat-option>
          <mat-option value="RIESGO">Riesgo</mat-option>
          <mat-option value="TIPO_CAMBIO">Tipo Cambio</mat-option>
          <mat-option value="INDICADOR">Indicador</mat-option>
        </mat-select>
      </mat-form-field>

      <mat-form-field appearance="outline">
        <mat-label>Severidad</mat-label>
        <mat-select [(ngModel)]="severidadFilter" (selectionChange)="loadData()">
          <mat-option value="">Todas</mat-option>
          <mat-option value="INFO">Info</mat-option>
          <mat-option value="WARNING">Warning</mat-option>
          <mat-option value="CRITICAL">Critical</mat-option>
        </mat-select>
      </mat-form-field>

      <mat-form-field appearance="outline">
        <mat-label>Estado</mat-label>
        <mat-select [(ngModel)]="leidaFilter" (selectionChange)="loadData()">
          <mat-option value="">Todas</mat-option>
          <mat-option value="false">No leidas</mat-option>
          <mat-option value="true">Leidas</mat-option>
        </mat-select>
      </mat-form-field>
    </div>

    @if (loading) {
      <div class="loading-center"><mat-spinner></mat-spinner></div>
    } @else {
      <table mat-table [dataSource]="alertas" class="full-width mat-elevation-z2">
        <ng-container matColumnDef="severidad">
          <th mat-header-cell *matHeaderCellDef>Sev.</th>
          <td mat-cell *matCellDef="let a">
            <mat-icon [style.color]="getSeveridadColor(a.severidad)">
              {{ getSeveridadIcon(a.severidad) }}
            </mat-icon>
          </td>
        </ng-container>
        <ng-container matColumnDef="titulo">
          <th mat-header-cell *matHeaderCellDef>Titulo</th>
          <td mat-cell *matCellDef="let a" [style.font-weight]="a.leida ? 'normal' : 'bold'">{{ a.titulo }}</td>
        </ng-container>
        <ng-container matColumnDef="tipo_alerta">
          <th mat-header-cell *matHeaderCellDef>Tipo</th>
          <td mat-cell *matCellDef="let a">{{ a.tipo_alerta }}</td>
        </ng-container>
        <ng-container matColumnDef="pais">
          <th mat-header-cell *matHeaderCellDef>Pais</th>
          <td mat-cell *matCellDef="let a">{{ a.pais }}</td>
        </ng-container>
        <ng-container matColumnDef="fecha">
          <th mat-header-cell *matHeaderCellDef>Fecha</th>
          <td mat-cell *matCellDef="let a">{{ a.fecha_creacion | date:'short' }}</td>
        </ng-container>
        <ng-container matColumnDef="acciones">
          <th mat-header-cell *matHeaderCellDef></th>
          <td mat-cell *matCellDef="let a">
            @if (!a.leida) {
              <button mat-icon-button (click)="markRead(a)">
                <mat-icon>check</mat-icon>
              </button>
            }
          </td>
        </ng-container>
        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns;" [class.unread]="!row.leida"></tr>
      </table>

      <mat-paginator [length]="totalCount" [pageSize]="pageSize" [pageSizeOptions]="[10, 25, 50]" (page)="onPage($event)"></mat-paginator>
    }
  `,
  styles: [`
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
    .filters { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; }
    .loading-center { display: flex; justify-content: center; padding: 48px; }
    .full-width { width: 100%; }
    .unread { background: #f0f7ff; }
  `]
})
export class AlertasComponent implements OnInit {
  private alertaService = inject(AlertaService);
  private snackBar = inject(MatSnackBar);

  alertas: Alerta[] = [];
  loading = true;
  totalCount = 0;
  pageSize = 10;
  currentPage = 0;
  tipoFilter = '';
  severidadFilter = '';
  leidaFilter = '';
  displayedColumns = ['severidad', 'titulo', 'tipo_alerta', 'pais', 'fecha', 'acciones'];

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;
    let params = new HttpParams()
      .set('page', (this.currentPage + 1).toString())
      .set('page_size', this.pageSize.toString());

    if (this.tipoFilter) params = params.set('tipo_alerta', this.tipoFilter);
    if (this.severidadFilter) params = params.set('severidad', this.severidadFilter);
    if (this.leidaFilter) params = params.set('leida', this.leidaFilter);

    this.alertaService.getAll(params).subscribe(data => {
      this.alertas = data.results;
      this.totalCount = data.count;
      this.loading = false;
    });
  }

  markRead(alerta: Alerta): void {
    this.alertaService.markRead(alerta.id).subscribe(() => {
      alerta.leida = true;
    });
  }

  markAllRead(): void {
    this.alertaService.markAllRead().subscribe(() => {
      this.snackBar.open('Todas las alertas marcadas como leidas', 'OK', { duration: 3000 });
      this.loadData();
    });
  }

  onPage(event: PageEvent): void {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    this.loadData();
  }

  getSeveridadColor(severidad: string): string {
    const colors: Record<string, string> = {
      'INFO': '#2196f3', 'WARNING': '#ff9800', 'CRITICAL': '#ef4444'
    };
    return colors[severidad] || '#999';
  }

  getSeveridadIcon(severidad: string): string {
    const icons: Record<string, string> = {
      'INFO': 'info', 'WARNING': 'warning', 'CRITICAL': 'error'
    };
    return icons[severidad] || 'info';
  }
}
