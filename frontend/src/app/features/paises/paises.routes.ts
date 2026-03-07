import { Routes } from '@angular/router';

export const PAISES_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./paises-list/paises-list.component').then(m => m.PaisesListComponent)
  },
  {
    path: ':codigoIso',
    loadComponent: () => import('./pais-detail/pais-detail.component').then(m => m.PaisDetailComponent)
  }
];
