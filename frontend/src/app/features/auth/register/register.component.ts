import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { RouterLink, Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule, ReactiveFormsModule, RouterLink,
    MatCardModule, MatFormFieldModule, MatInputModule,
    MatButtonModule, MatSelectModule, MatProgressSpinnerModule
  ],
  template: `
    <div class="auth-container">
      <mat-card class="auth-card">
        <mat-card-header>
          <mat-card-title>DataPulse Latam</mat-card-title>
          <mat-card-subtitle>Crear Cuenta</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content>
          <form [formGroup]="form" (ngSubmit)="onSubmit()">
            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Nombre Completo</mat-label>
              <input matInput formControlName="nombre_completo">
              @if (form.get('nombre_completo')?.hasError('required') && form.get('nombre_completo')?.touched) {
                <mat-error>Nombre es requerido</mat-error>
              }
            </mat-form-field>

            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Username</mat-label>
              <input matInput formControlName="username">
              @if (form.get('username')?.hasError('required') && form.get('username')?.touched) {
                <mat-error>Username es requerido</mat-error>
              }
            </mat-form-field>

            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Email</mat-label>
              <input matInput formControlName="email" type="email">
              @if (form.get('email')?.hasError('required') && form.get('email')?.touched) {
                <mat-error>Email es requerido</mat-error>
              }
            </mat-form-field>

            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Password</mat-label>
              <input matInput formControlName="password" type="password">
              @if (form.get('password')?.hasError('required') && form.get('password')?.touched) {
                <mat-error>Password es requerido</mat-error>
              }
              @if (form.get('password')?.hasError('minlength') && form.get('password')?.touched) {
                <mat-error>Minimo 8 caracteres</mat-error>
              }
            </mat-form-field>

            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Rol</mat-label>
              <mat-select formControlName="rol">
                <mat-option value="VIEWER">Viewer</mat-option>
                <mat-option value="ANALISTA">Analista</mat-option>
                <mat-option value="ADMIN">Admin</mat-option>
              </mat-select>
            </mat-form-field>

            @if (errorMsg) {
              <p class="error-msg">{{ errorMsg }}</p>
            }

            <button mat-raised-button color="primary" type="submit" class="full-width submit-btn" [disabled]="loading">
              @if (loading) {
                <mat-spinner diameter="20"></mat-spinner>
              } @else {
                Crear Cuenta
              }
            </button>
          </form>
        </mat-card-content>
        <mat-card-actions align="end">
          <a mat-button routerLink="/auth/login">Ya tengo cuenta</a>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
  styles: [`
    .auth-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: #f5f5f5;
    }
    .auth-card {
      width: 100%;
      max-width: 420px;
      padding: 24px;
    }
    .full-width { width: 100%; }
    .submit-btn { height: 48px; margin-top: 8px; }
    .error-msg { color: #ef4444; font-size: 14px; margin: 8px 0; }
    mat-card-header { justify-content: center; margin-bottom: 24px; }
  `]
})
export class RegisterComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);
  private snackBar = inject(MatSnackBar);

  loading = false;
  errorMsg = '';

  form = this.fb.group({
    nombre_completo: ['', [Validators.required]],
    username: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
    rol: ['VIEWER', [Validators.required]]
  });

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.loading = true;
    this.errorMsg = '';
    this.authService.register(this.form.value as any).subscribe({
      next: () => {
        this.snackBar.open('Cuenta creada exitosamente', 'OK', { duration: 3000 });
        this.router.navigate(['/auth/login']);
      },
      error: (err) => {
        this.loading = false;
        this.errorMsg = err.error?.detail || err.error?.email?.[0] || 'Error al crear cuenta';
      }
    });
  }
}
