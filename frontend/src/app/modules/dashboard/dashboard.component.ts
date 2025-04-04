import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../core/authentication/auth.service';
import { Usuario } from '../../core/models/user.model';

@Component({
    standalone: false,
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
    currentUser: Usuario | null = null;
    isAdmin = false;
    isCajero = false;
    isMesero = false;

    // Datos de muestra para las tarjetas
    dashboardCards = {
        pendingOrders: 0,
        dailySales: 0,
        availableTables: 0,
        lowStockItems: 0
    };

    constructor(private authService: AuthService) { }

    ngOnInit(): void {
        // Suscripción al usuario actual
        this.authService.currentUser$.subscribe(user => {
            this.currentUser = user;

            // Verificar roles
            this.isAdmin = this.authService.isAdmin();
            this.isCajero = this.authService.isCajero();
            this.isMesero = this.authService.isMesero();

            // Cargar datos según el rol
            this.loadDashboardData();
        });
    }

    loadDashboardData(): void {
        // Aquí cargaríamos datos reales del backend
        // Por ahora usamos datos de muestra
        this.dashboardCards = {
            pendingOrders: 5,
            dailySales: 152000,
            availableTables: 8,
            lowStockItems: 3
        };
    }
}