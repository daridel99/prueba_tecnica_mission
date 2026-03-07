import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-not-found',
  standalone: true,
  imports: [RouterLink, MatButtonModule, MatIconModule],
  template: `
    <div class="not-found">
      <mat-icon class="big-icon">search_off</mat-icon>
      <h1>404</h1>
      <p>Pagina no encontrada</p>
      <a mat-raised-button color="primary" routerLink="/dashboard">Volver al Dashboard</a>
    </div>
  `,
  styles: [`
    .not-found {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 60vh;
      text-align: center;
    }
    .big-icon { font-size: 80px; width: 80px; height: 80px; color: #ccc; }
    h1 { font-size: 4rem; color: #1e3a5f; margin: 16px 0 8px; }
    p { color: #666; margin-bottom: 24px; }
  `]
})
export class NotFoundComponent {}
