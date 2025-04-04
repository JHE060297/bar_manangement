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
export class AuthGuard {

    constructor(
        private authService: AuthService,
        private router: Router
    ) { }

    canActivate(
        route: ActivatedRouteSnapshot,
        state: RouterStateSnapshot
    ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {

        // Verificar si el usuario está autenticado
        if (this.authService.isAuthenticated()) {
            // Si tiene roles requeridos, verificar
            const requiredRoles = route.data['roles'] as string[];

            if (requiredRoles && requiredRoles.length > 0) {
                // Verificar si el usuario tiene al menos uno de los roles requeridos
                const hasRequiredRole = requiredRoles.some(role => {
                    if (role === 'admin') return this.authService.isAdmin();
                    if (role === 'cajero') return this.authService.isCajero();
                    if (role === 'mesero') return this.authService.isMesero();
                    return false;
                });

                if (hasRequiredRole) {
                    return true;
                } else {
                    // Si no tiene los roles requeridos, redirigir a página de acceso denegado
                    return this.router.createUrlTree(['/access-denied']);
                }
            }

            // Si no hay roles requeridos, permitir acceso
            return true;
        }

        // Si no está autenticado, redirigir a login
        return this.router.createUrlTree(['/login'], { queryParams: { returnUrl: state.url } });
    }
}


