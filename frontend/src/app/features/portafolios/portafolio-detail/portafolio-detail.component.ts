import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PortafolioService } from '../../../core/services/portafolio.service';
import { AuthService } from '../../../core/services/auth.service';
import { Portafolio, Posicion } from '../../../core/models/portafolio.model';

@Component({
  selector: 'app-portafolio-detail',
  standalone: true,
  imports: [
    CommonModule, RouterLink, ReactiveFormsModule,
    MatCardModule, MatTableModule, MatButtonModule, MatIconModule,
    MatFormFieldModule, MatInputModule, MatSelectModule, MatProgressSpinnerModule
  ],
  template: `
    @if (loading) {
      <div class="loading-center"><mat-spinner></mat-spinner></div>
    } @else if (portafolio) {
      <div class="header">
        <button mat-button routerLink="/portafolios">
          <mat-icon>arrow_back</mat-icon> Volver
        </button>
        <h2>{{ portafolio.nombre }}</h2>
        <span class="spacer"></span>
        <button mat-raised-button color="accent" (click)="downloadPdf()">
          <mat-icon>picture_as_pdf</mat-icon> Exportar PDF
        </button>
      </div>

      <p class="description">{{ portafolio.descripcion }}</p>

      <div class="summary-grid">
        <mat-card>
          <mat-card-content>
            <div class="summary-label">Total Invertido</div>
            <div class="summary-value">\${{ totalInvertido | number:'1.2-2' }} USD</div>
          </mat-card-content>
        </mat-card>
        <mat-card>
          <mat-card-content>
            <div class="summary-label">Posiciones</div>
            <div class="summary-value">{{ portafolio.posiciones.length || 0 }}</div>
          </mat-card-content>
        </mat-card>
        <mat-card>
          <mat-card-content>
            <div class="summary-label">Estado</div>
            <div class="summary-value">{{ portafolio.es_publico ? 'Publico' : 'Privado' }}</div>
          </mat-card-content>
        </mat-card>
      </div>

      <mat-card class="section-card">
        <mat-card-header><mat-card-title>Posiciones</mat-card-title></mat-card-header>
        <mat-card-content>
          @if (portafolio.posiciones.length) {
            <table mat-table [dataSource]="portafolio.posiciones" class="full-width">
              <ng-container matColumnDef="pais">
                <th mat-header-cell *matHeaderCellDef>Pais</th>
                <td mat-cell *matCellDef="let pos">{{ pos.pais }}</td>
              </ng-container>
              <ng-container matColumnDef="tipo_activo">
                <th mat-header-cell *matHeaderCellDef>Tipo Activo</th>
                <td mat-cell *matCellDef="let pos">{{ pos.tipo_activo }}</td>
              </ng-container>
              <ng-container matColumnDef="monto">
                <th mat-header-cell *matHeaderCellDef>Monto USD</th>
                <td mat-cell *matCellDef="let pos">\${{ pos.monto_inversion_usd | number:'1.2-2' }}</td>
              </ng-container>
              <ng-container matColumnDef="fecha_entrada">
                <th mat-header-cell *matHeaderCellDef>Fecha Entrada</th>
                <td mat-cell *matCellDef="let pos">{{ pos.fecha_entrada | date:'shortDate' }}</td>
              </ng-container>
              <ng-container matColumnDef="acciones">
                <th mat-header-cell *matHeaderCellDef></th>
                <td mat-cell *matCellDef="let pos">
                  @if (canEdit) {
                    <button mat-icon-button color="warn" (click)="deletePosicion(pos)">
                      <mat-icon>delete</mat-icon>
                    </button>
                  }
                </td>
              </ng-container>
              <tr mat-header-row *matHeaderRowDef="posColumns"></tr>
              <tr mat-row *matRowDef="let row; columns: posColumns;"></tr>
            </table>
          } @else {
            <p>No hay posiciones</p>
          }
        </mat-card-content>
      </mat-card>

      @if (canEdit) {
        <mat-card class="section-card">
          <mat-card-header><mat-card-title>Agregar Posicion</mat-card-title></mat-card-header>
          <mat-card-content>
            <form [formGroup]="posForm" (ngSubmit)="addPosicion()" class="pos-form">
              <mat-form-field appearance="outline">
                <mat-label>Pais (codigo ISO)</mat-label>
                <input matInput formControlName="pais" placeholder="e.g. CO">
              </mat-form-field>

              <mat-form-field appearance="outline">
                <mat-label>Tipo Activo</mat-label>
                <mat-select formControlName="tipo_activo">
                  <mat-option value="RENTA_FIJA">Renta Fija</mat-option>
                  <mat-option value="RENTA_VARIABLE">Renta Variable</mat-option>
                  <mat-option value="COMMODITIES">Commodities</mat-option>
                  <mat-option value="MONEDA">Moneda</mat-option>
                </mat-select>
              </mat-form-field>

              <mat-form-field appearance="outline">
                <mat-label>Monto USD</mat-label>
                <input matInput formControlName="monto_inversion_usd" type="number">
              </mat-form-field>

              <mat-form-field appearance="outline">
                <mat-label>Fecha Entrada</mat-label>
                <input matInput formControlName="fecha_entrada" type="date">
              </mat-form-field>

              <mat-form-field appearance="outline">
                <mat-label>Notas</mat-label>
                <input matInput formControlName="notas">
              </mat-form-field>

              <button mat-raised-button color="primary" type="submit" [disabled]="posForm.invalid">
                <mat-icon>add</mat-icon> Agregar
              </button>
            </form>
          </mat-card-content>
        </mat-card>
      }
    }
  `,
  styles: [`
    .loading-center { display: flex; justify-content: center; padding: 48px; }
    .header { display: flex; align-items: center; gap: 16px; margin-bottom: 8px; flex-wrap: wrap; }
    .header h2 { margin: 0; }
    .spacer { flex: 1; }
    .description { color: #666; margin-bottom: 16px; }
    .summary-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 16px;
    }
    .summary-label { color: #666; font-size: 0.9rem; }
    .summary-value { font-size: 1.5rem; font-weight: 700; color: #1e3a5f; }
    .section-card { margin-bottom: 16px; }
    .full-width { width: 100%; }
    .pos-form {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: flex-start;
    }
    .pos-form mat-form-field { flex: 1; min-width: 150px; }
  `]
})
export class PortafolioDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private portafolioService = inject(PortafolioService);
  private authService = inject(AuthService);
  private fb = inject(FormBuilder);
  private snackBar = inject(MatSnackBar);

  portafolio: Portafolio | null = null;
  loading = true;
  canEdit = false;
  totalInvertido = 0;
  posColumns = ['pais', 'tipo_activo', 'monto', 'fecha_entrada', 'acciones'];

  posForm = this.fb.group({
    pais: ['', Validators.required],
    tipo_activo: ['RENTA_FIJA', Validators.required],
    monto_inversion_usd: [0, [Validators.required, Validators.min(0.01)]],
    fecha_entrada: ['', Validators.required],
    notas: ['']
  });

  ngOnInit(): void {
    const role = this.authService.getUserRole();
    this.canEdit = role === 'ADMIN' || role === 'ANALISTA';
    this.loadData();
  }

  loadData(): void {
    const id = +this.route.snapshot.paramMap.get('id')!;
    this.portafolioService.getById(id).subscribe(data => {
      this.portafolio = data;
      this.totalInvertido = (data.posiciones || []).reduce((sum, p) => sum + p.monto_inversion_usd, 0);
      this.loading = false;
    });
  }

  addPosicion(): void {
    if (!this.portafolio || this.posForm.invalid) return;
    this.portafolioService.createPosicion(this.portafolio.id, this.posForm.value as any).subscribe({
      next: () => {
        this.snackBar.open('Posicion agregada', 'OK', { duration: 3000 });
        this.posForm.reset({ tipo_activo: 'RENTA_FIJA' });
        this.loadData();
      }
    });
  }

  deletePosicion(pos: Posicion): void {
    if (!this.portafolio || !confirm('Eliminar posicion?')) return;
    this.portafolioService.deletePosicion(this.portafolio.id, pos.id).subscribe(() => {
      this.snackBar.open('Posicion eliminada', 'OK', { duration: 3000 });
      this.loadData();
    });
  }

  downloadPdf(): void {
    if (!this.portafolio) return;
    this.portafolioService.exportPdf(this.portafolio.id).subscribe(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `portafolio_${this.portafolio!.id}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }
}
