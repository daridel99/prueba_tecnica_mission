import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { catchError, throwError } from 'rxjs';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const snackBar = inject(MatSnackBar);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 0) {
        snackBar.open('Error de conexion con el servidor', 'Cerrar', { duration: 5000 });
      } else if (error.status === 403) {
        snackBar.open('No tienes permisos para esta accion', 'Cerrar', { duration: 5000 });
      } else if (error.status === 500) {
        snackBar.open('Error interno del servidor', 'Cerrar', { duration: 5000 });
      } else if (error.status !== 401) {
        const msg = error.error?.detail || error.error?.message || 'Ha ocurrido un error';
        snackBar.open(msg, 'Cerrar', { duration: 5000 });
      }
      return throwError(() => error);
    })
  );
};
