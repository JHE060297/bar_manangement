import { Injectable } from '@angular/core';
import {
    ActivatedRouteSnapshot,
    Router,
    RouterStateSnapshot,
    UrlTree
} from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '../authentication/auth.service';

@Injectable({
    providedIn: 'root'
})
export class RoleGuard {

    constructor(
        private authService: AuthService,
        private router: Router
    ) { }

    canActivate(
        route: ActivatedRouteSnapshot,
        state: RouterStateSnapshot
    ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

        // Si el usuario es admin, siempre permitir acceso
        if (this.authService.isAdmin()) {
            return true;
        }

        // Verificar roles específicos
        const requiredRoles = route.data['roles'] as string[];

        if (!requiredRoles || requiredRoles.length === 0) {
            return true; // Si no hay roles específicos, permitir acceso
        }

        // Verificar si el usuario tiene al menos uno de los roles requeridos
        const hasRequiredRole = requiredRoles.some(role => {
            if (role === 'cajero') return this.authService.isCajero();
            if (role === 'mesero') return this.authService.isMesero();
            return false;
        });

        if (hasRequiredRole) {
            return true;
        }

        // Redirigir a página de acceso denegado
        return this.router.createUrlTree(['/access-denied']);
    }
}