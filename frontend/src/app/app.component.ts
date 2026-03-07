import { Component, inject, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterOutlet, RouterLink, RouterLinkActive, NavigationEnd } from '@angular/router';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatBadgeModule } from '@angular/material/badge';
import { MatMenuModule } from '@angular/material/menu';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Subject, interval, filter, takeUntil, startWith } from 'rxjs';
import { AuthService } from './core/services/auth.service';
import { AlertaService } from './core/services/alerta.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule, RouterOutlet, RouterLink, RouterLinkActive,
    MatSidenavModule, MatToolbarModule, MatIconModule, MatButtonModule,
    MatListModule, MatBadgeModule, MatMenuModule
  ],
  template: `
    @if (isAuthRoute) {
      <router-outlet />
    } @else {
      <mat-sidenav-container class="app-container">
        <mat-sidenav #sidenav [mode]="isMobile ? 'over' : 'side'" [opened]="!isMobile && isLoggedIn" class="app-sidenav">
          <div class="sidenav-header">
            <h2>DataPulse Latam</h2>
          </div>
          <mat-nav-list>
            <a mat-list-item routerLink="/dashboard" routerLinkActive="active" (click)="isMobile && sidenav.close()">
              <mat-icon matListItemIcon>dashboard</mat-icon>
              <span matListItemTitle>Dashboard</span>
            </a>
            <a mat-list-item routerLink="/paises" routerLinkActive="active" (click)="isMobile && sidenav.close()">
              <mat-icon matListItemIcon>public</mat-icon>
              <span matListItemTitle>Paises</span>
            </a>
            <a mat-list-item routerLink="/portafolios" routerLinkActive="active" (click)="isMobile && sidenav.close()">
              <mat-icon matListItemIcon>account_balance_wallet</mat-icon>
              <span matListItemTitle>Portafolios</span>
            </a>
            <a mat-list-item routerLink="/alertas" routerLinkActive="active" (click)="isMobile && sidenav.close()">
              <mat-icon matListItemIcon>notifications</mat-icon>
              <span matListItemTitle>Alertas</span>
            </a>
          </mat-nav-list>
        </mat-sidenav>

        <mat-sidenav-content>
          <mat-toolbar color="primary" class="app-toolbar">
            <button mat-icon-button (click)="sidenav.toggle()">
              <mat-icon>menu</mat-icon>
            </button>
            <span class="toolbar-title">DataPulse Latam</span>
            <span class="spacer"></span>

            @if (isLoggedIn) {
              <button mat-icon-button routerLink="/alertas" [matBadge]="alertCount > 0 ? alertCount : null" matBadgeColor="warn" matBadgeSize="small">
                <mat-icon>notifications</mat-icon>
              </button>

              <button mat-icon-button [matMenuTriggerFor]="userMenu">
                <mat-icon>account_circle</mat-icon>
              </button>
              <mat-menu #userMenu="matMenu">
                <div mat-menu-item disabled>
                  <mat-icon>person</mat-icon>
                  <span>{{ (authService.user$ | async)?.nombre_completo }}</span>
                </div>
                <button mat-menu-item (click)="logout()">
                  <mat-icon>logout</mat-icon>
                  <span>Cerrar Sesion</span>
                </button>
              </mat-menu>
            }
          </mat-toolbar>

          <main class="app-content">
            <router-outlet />
          </main>
        </mat-sidenav-content>
      </mat-sidenav-container>
    }
  `,
  styles: [`
    .app-container {
      height: 100vh;
    }
    .app-sidenav {
      width: 250px;
      background: #1e3a5f;
    }
    .sidenav-header {
      padding: 16px;
      text-align: center;
      h2 {
        color: white;
        margin: 0;
        font-size: 1.3rem;
      }
    }
    .app-sidenav ::ng-deep .mat-mdc-list-item {
      color: rgba(255,255,255,0.8) !important;
      &.active {
        color: white !important;
        background: rgba(255,255,255,0.1);
      }
    }
    .app-sidenav ::ng-deep .mat-icon {
      color: rgba(255,255,255,0.8) !important;
    }
    .app-toolbar {
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .toolbar-title {
      margin-left: 8px;
      font-size: 1.1rem;
    }
    .spacer {
      flex: 1;
    }
    .app-content {
      padding: 24px;
      max-width: 1400px;
      margin: 0 auto;
    }
    @media (max-width: 768px) {
      .app-content {
        padding: 12px;
      }
    }
  `]
})
export class AppComponent implements OnInit, OnDestroy {
  authService = inject(AuthService);
  private alertaService = inject(AlertaService);
  private router = inject(Router);
  private breakpointObserver = inject(BreakpointObserver);
  private destroy$ = new Subject<void>();

  isAuthRoute = false;
  isLoggedIn = false;
  isMobile = false;
  alertCount = 0;

  ngOnInit(): void {
    this.breakpointObserver.observe([Breakpoints.Handset]).pipe(
      takeUntil(this.destroy$)
    ).subscribe(result => this.isMobile = result.matches);

    this.router.events.pipe(
      filter(e => e instanceof NavigationEnd),
      takeUntil(this.destroy$)
    ).subscribe((e) => {
      const nav = e as NavigationEnd;
      this.isAuthRoute = nav.urlAfterRedirects.startsWith('/auth');
    });

    this.authService.user$.pipe(takeUntil(this.destroy$)).subscribe(user => {
      this.isLoggedIn = !!user;
      if (user) {
        this.startAlertPolling();
      }
    });
  }

  private startAlertPolling(): void {
    interval(30000).pipe(
      startWith(0),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      if (this.authService.isLoggedIn()) {
        this.alertaService.getResumen().subscribe(res => {
          this.alertCount = res.no_leidas;
        });
      }
    });
  }

  logout(): void {
    this.authService.logout();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
