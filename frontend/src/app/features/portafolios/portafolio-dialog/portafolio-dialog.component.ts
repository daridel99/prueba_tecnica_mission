import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PortafolioService } from '../../../core/services/portafolio.service';
import { Portafolio } from '../../../core/models/portafolio.model';

@Component({
  selector: 'app-portafolio-dialog',
  standalone: true,
  imports: [
    CommonModule, ReactiveFormsModule, MatDialogModule,
    MatFormFieldModule, MatInputModule, MatButtonModule, MatSlideToggleModule
  ],
  template: `
    <h2 mat-dialog-title>{{ data ? 'Editar' : 'Nuevo' }} Portafolio</h2>
    <mat-dialog-content>
      <form [formGroup]="form">
        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Nombre</mat-label>
          <input matInput formControlName="nombre">
          @if (form.get('nombre')?.hasError('required') && form.get('nombre')?.touched) {
            <mat-error>Nombre es requerido</mat-error>
          }
          @if (form.get('nombre')?.hasError('minlength')) {
            <mat-error>Minimo 3 caracteres</mat-error>
          }
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Descripcion</mat-label>
          <textarea matInput formControlName="descripcion" rows="3" maxlength="500"></textarea>
          <mat-hint align="end">{{ form.get('descripcion')?.value?.length || 0 }} / 500</mat-hint>
        </mat-form-field>

        <mat-slide-toggle formControlName="es_publico">Portafolio publico</mat-slide-toggle>
      </form>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close>Cancelar</button>
      <button mat-raised-button color="primary" (click)="save()" [disabled]="form.invalid || saving">
        {{ saving ? 'Guardando...' : 'Guardar' }}
      </button>
    </mat-dialog-actions>
  `,
  styles: [`.full-width { width: 100%; margin-bottom: 16px; }`]
})
export class PortafolioDialogComponent {
  private fb = inject(FormBuilder);
  private portafolioService = inject(PortafolioService);
  private dialogRef = inject(MatDialogRef<PortafolioDialogComponent>);
  private snackBar = inject(MatSnackBar);
  data = inject<Portafolio | null>(MAT_DIALOG_DATA);

  saving = false;

  form = this.fb.group({
    nombre: [this.data?.nombre || '', [Validators.required, Validators.minLength(3), Validators.maxLength(100)]],
    descripcion: [this.data?.descripcion || '', [Validators.maxLength(500)]],
    es_publico: [this.data?.es_publico || false]
  });

  save(): void {
    if (this.form.invalid) return;
    this.saving = true;
    const payload = this.form.value as Record<string, unknown>;

    const obs = this.data
      ? this.portafolioService.update(this.data.id, payload as any)
      : this.portafolioService.create(payload as any);

    obs.subscribe({
      next: () => {
        this.snackBar.open('Portafolio guardado', 'OK', { duration: 3000 });
        this.dialogRef.close(true);
      },
      error: () => {
        this.saving = false;
      }
    });
  }
}
