import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/auth.routes').then(m => m.AUTH_ROUTES)
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard]
  },
  {
    path: 'paises',
    loadChildren: () => import('./features/paises/paises.routes').then(m => m.PAISES_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: 'portafolios',
    loadChildren: () => import('./features/portafolios/portafolios.routes').then(m => m.PORTAFOLIOS_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: 'alertas',
    loadComponent: () => import('./features/alertas/alertas.component').then(m => m.AlertasComponent),
    canActivate: [authGuard]
  },
  {
    path: '**',
    loadComponent: () => import('./shared/components/not-found/not-found.component').then(m => m.NotFoundComponent)
  }
];
