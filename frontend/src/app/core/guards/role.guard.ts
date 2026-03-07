import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { map, take, filter } from 'rxjs';

export const roleGuard: CanActivateFn = (route) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const allowedRoles = route.data?.['roles'] as string[];

  if (!allowedRoles) return true;

  return authService.user$.pipe(
    filter(user => user !== null),
    take(1),
    map(user => {
      if (user && allowedRoles.includes(user.rol)) {
        return true;
      }
      return router.createUrlTree(['/dashboard']);
    })
  );
};
