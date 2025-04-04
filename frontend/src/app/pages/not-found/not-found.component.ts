import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-not-found',
    template: `
    <div class="not-found-container">
      <mat-card>
        <mat-card-header>
          <mat-card-title>Página no encontrada</mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div class="icon-container">
            <mat-icon class="error-icon">search_off</mat-icon>
          </div>
          <h2>404</h2>
          <p>La página que buscas no existe o no está disponible.</p>
        </mat-card-content>
        <mat-card-actions>
          <button mat-raised-button color="primary" (click)="goToHome()">Ir al inicio</button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
    styles: [`
    .not-found-container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f5f5f5;
    }
    
    mat-card {
      max-width: 400px;
      text-align: center;
      padding: 30px;
    }
    
    .icon-container {
      margin: 20px 0;
    }
    
    .error-icon {
      font-size: 60px;
      height: 60px;
      width: 60px;
      color: #ff9800;
    }
    
    h2 {
      font-size: 36px;
      margin: 0;
      color: #ff9800;
    }
    
    mat-card-actions {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }
  `]
})
export class NotFoundComponent {
    constructor(private router: Router) { }

    goToHome(): void {
        this.router.navigate(['/']);
    }
}