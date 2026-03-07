import { Routes } from '@angular/router';

export const PORTAFOLIOS_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./portafolios-list/portafolios-list.component').then(m => m.PortafoliosListComponent)
  },
  {
    path: ':id',
    loadComponent: () => import('./portafolio-detail/portafolio-detail.component').then(m => m.PortafolioDetailComponent)
  }
];
