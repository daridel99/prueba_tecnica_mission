import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PortafolioService } from '../../../core/services/portafolio.service';
import { AuthService } from '../../../core/services/auth.service';
import { Portafolio } from '../../../core/models/portafolio.model';
import { PortafolioDialogComponent } from '../portafolio-dialog/portafolio-dialog.component';

@Component({
  selector: 'app-portafolios-list',
  standalone: true,
  imports: [
    CommonModule, RouterLink, MatTableModule, MatButtonModule,
    MatIconModule, MatChipsModule, MatDialogModule, MatProgressSpinnerModule
  ],
  template: `
    <div class="header">
      <h2>Portafolios</h2>
      @if (canEdit) {
        <button mat-raised-button color="primary" (click)="openDialog()">
          <mat-icon>add</mat-icon> Nuevo Portafolio
        </button>
      }
    </div>

    @if (loading) {
      <div class="loading-center"><mat-spinner></mat-spinner></div>
    } @else {
      <table mat-table [dataSource]="portafolios" class="full-width mat-elevation-z2">
        <ng-container matColumnDef="nombre">
          <th mat-header-cell *matHeaderCellDef>Nombre</th>
          <td mat-cell *matCellDef="let p">
            <a [routerLink]="['/portafolios', p.id]">{{ p.nombre }}</a>
          </td>
        </ng-container>
        <ng-container matColumnDef="descripcion">
          <th mat-header-cell *matHeaderCellDef>Descripcion</th>
          <td mat-cell *matCellDef="let p">{{ p.descripcion | slice:0:80 }}{{ p.descripcion?.length > 80 ? '...' : '' }}</td>
        </ng-container>
        <ng-container matColumnDef="publico">
          <th mat-header-cell *matHeaderCellDef>Publico</th>
          <td mat-cell *matCellDef="let p">
            <mat-icon [style.color]="p.es_publico ? '#22c55e' : '#999'">{{ p.es_publico ? 'visibility' : 'visibility_off' }}</mat-icon>
          </td>
        </ng-container>
        <ng-container matColumnDef="fecha">
          <th mat-header-cell *matHeaderCellDef>Creado</th>
          <td mat-cell *matCellDef="let p">{{ p.fecha_creacion | date:'shortDate' }}</td>
        </ng-container>
        <ng-container matColumnDef="acciones">
          <th mat-header-cell *matHeaderCellDef>Acciones</th>
          <td mat-cell *matCellDef="let p">
            @if (canEdit) {
              <button mat-icon-button (click)="openDialog(p); $event.stopPropagation()">
                <mat-icon>edit</mat-icon>
              </button>
              <button mat-icon-button color="warn" (click)="deletePortafolio(p); $event.stopPropagation()">
                <mat-icon>delete</mat-icon>
              </button>
            }
          </td>
        </ng-container>
        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
      </table>
    }
  `,
  styles: [`
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
    .loading-center { display: flex; justify-content: center; padding: 48px; }
    .full-width { width: 100%; }
    a { color: #1e3a5f; text-decoration: none; font-weight: 500; }
    a:hover { text-decoration: underline; }
  `]
})
export class PortafoliosListComponent implements OnInit {
  private portafolioService = inject(PortafolioService);
  private authService = inject(AuthService);
  private dialog = inject(MatDialog);
  private snackBar = inject(MatSnackBar);

  portafolios: Portafolio[] = [];
  loading = true;
  canEdit = false;
  displayedColumns = ['nombre', 'descripcion', 'publico', 'fecha', 'acciones'];

  ngOnInit(): void {
    const role = this.authService.getUserRole();
    this.canEdit = role === 'ADMIN' || role === 'ANALISTA';
    this.loadData();
  }

  loadData(): void {
    this.loading = true;
    this.portafolioService.getAll().subscribe(data => {
      this.portafolios = data.results;
      this.loading = false;
    });
  }

  openDialog(portafolio?: Portafolio): void {
    const dialogRef = this.dialog.open(PortafolioDialogComponent, {
      width: '500px',
      data: portafolio || null
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) this.loadData();
    });
  }

  deletePortafolio(p: Portafolio): void {
    if (confirm(`Eliminar portafolio "${p.nombre}"?`)) {
      this.portafolioService.delete(p.id).subscribe(() => {
        this.snackBar.open('Portafolio eliminado', 'OK', { duration: 3000 });
        this.loadData();
      });
    }
  }
}
