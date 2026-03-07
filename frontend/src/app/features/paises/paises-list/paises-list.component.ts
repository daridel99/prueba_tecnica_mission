import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { HttpParams } from '@angular/common/http';
import { PaisService } from '../../../core/services/pais.service';
import { Pais } from '../../../core/models/pais.model';

@Component({
  selector: 'app-paises-list',
  standalone: true,
  imports: [
    CommonModule, RouterLink, FormsModule,
    MatTableModule, MatPaginatorModule, MatFormFieldModule,
    MatInputModule, MatSelectModule, MatButtonModule,
    MatIconModule, MatProgressSpinnerModule
  ],
  template: `
    <h2>Paises</h2>

    <div class="filters">
      <mat-form-field appearance="outline">
        <mat-label>Buscar</mat-label>
        <input matInput [(ngModel)]="search" (keyup.enter)="loadData()" placeholder="Nombre del pais">
        <mat-icon matSuffix>search</mat-icon>
      </mat-form-field>

      <mat-form-field appearance="outline">
        <mat-label>Region</mat-label>
        <mat-select [(ngModel)]="regionFilter" (selectionChange)="loadData()">
          <mat-option value="">Todas</mat-option>
          <mat-option value="ANDINA">Andina</mat-option>
          <mat-option value="CONO_SUR">Cono Sur</mat-option>
          <mat-option value="CENTROAMERICA">Centroamerica</mat-option>
        </mat-select>
      </mat-form-field>
    </div>

    @if (loading) {
      <div class="loading-center"><mat-spinner></mat-spinner></div>
    } @else {
      <table mat-table [dataSource]="paises" class="full-width mat-elevation-z2">
        <ng-container matColumnDef="nombre">
          <th mat-header-cell *matHeaderCellDef>Nombre</th>
          <td mat-cell *matCellDef="let p">
            <a [routerLink]="['/paises', p.codigo_iso]">{{ p.nombre }}</a>
          </td>
        </ng-container>
        <ng-container matColumnDef="region">
          <th mat-header-cell *matHeaderCellDef>Region</th>
          <td mat-cell *matCellDef="let p">{{ p.region }}</td>
        </ng-container>
        <ng-container matColumnDef="moneda">
          <th mat-header-cell *matHeaderCellDef>Moneda</th>
          <td mat-cell *matCellDef="let p">{{ p.moneda_codigo }} - {{ p.moneda_nombre }}</td>
        </ng-container>
        <ng-container matColumnDef="poblacion">
          <th mat-header-cell *matHeaderCellDef>Poblacion</th>
          <td mat-cell *matCellDef="let p">{{ p.poblacion | number }}</td>
        </ng-container>
        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
      </table>

      <mat-paginator [length]="totalCount" [pageSize]="pageSize" [pageSizeOptions]="[10, 25, 50]" (page)="onPage($event)"></mat-paginator>
    }
  `,
  styles: [`
    .filters { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; }
    .loading-center { display: flex; justify-content: center; padding: 48px; }
    .full-width { width: 100%; }
    a { color: #1e3a5f; text-decoration: none; font-weight: 500; }
    a:hover { text-decoration: underline; }
  `]
})
export class PaisesListComponent implements OnInit {
  private paisService = inject(PaisService);

  paises: Pais[] = [];
  loading = true;
  search = '';
  regionFilter = '';
  totalCount = 0;
  pageSize = 10;
  currentPage = 0;
  displayedColumns = ['nombre', 'region', 'moneda', 'poblacion'];

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;
    let params = new HttpParams()
      .set('page', (this.currentPage + 1).toString())
      .set('page_size', this.pageSize.toString());

    if (this.search) params = params.set('search', this.search);
    if (this.regionFilter) params = params.set('region', this.regionFilter);

    this.paisService.getAll(params).subscribe(data => {
      this.paises = data.results;
      this.totalCount = data.count;
      this.loading = false;
    });
  }

  onPage(event: PageEvent): void {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
    this.loadData();
  }
}
