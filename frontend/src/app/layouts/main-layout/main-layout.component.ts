import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthService } from '../../core/authentication/auth.service';
import { Usuario } from '../../core/models/user.model';
import { Router } from '@angular/router';

interface MenuOption {
    name: string;
    route: string;
    icon: string;
    roles: string[];
}

@Component({
    selector: 'app-main-layout',
    templateUrl: './main-layout.component.html',
    styleUrls: ['./main-layout.component.scss']
})
export class MainLayoutComponent implements OnInit {
    currentUser$: Observable<Usuario | null>;
    isSidenavOpen = true;

    menuOptions: MenuOption[] = [
        { name: 'Dashboard', route: '/dashboard', icon: 'dashboard', roles: ['admin', 'cajero', 'mesero'] },
        { name: 'Mesas', route: '/tables', icon: 'table_restaurant', roles: ['admin', 'cajero', 'mesero'] },
        { name: 'Pedidos', route: '/orders', icon: 'receipt_long', roles: ['admin', 'cajero', 'mesero'] },
        { name: 'Inventario', route: '/inventory', icon: 'inventory', roles: ['admin', 'cajero'] },
        { name: 'Pagos', route: '/payments', icon: 'payments', roles: ['admin', 'cajero'] },
        { name: 'Reportes', route: '/reports', icon: 'assessment', roles: ['admin', 'cajero'] },
        { name: 'Usuarios', route: '/users', icon: 'people', roles: ['admin'] },
        { name: 'Sucursales', route: '/branches', icon: 'store', roles: ['admin'] }
    ];

    constructor(
        private authService: AuthService,
        private router: Router
    ) {
        this.currentUser$ = this.authService.currentUser$;
    }

    ngOnInit(): void {
    }

    toggleSidenav(): void {
        this.isSidenavOpen = !this.isSidenavOpen;
    }

    logout(): void {
        this.authService.logout();
    }

    hasRoleForOption(option: MenuOption): boolean {
        const hasRole = option.roles.some(role => {
            if (role === 'admin') return this.authService.isAdmin();
            if (role === 'cajero') return this.authService.isCajero();
            if (role === 'mesero') return this.authService.isMesero();
            return false;
        });

        return hasRole;
    }
}