import { Injectable } from '@angular/core';
import {
    HttpRequest,
    HttpHandler,
    HttpEvent,
    HttpInterceptor,
    HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError, BehaviorSubject } from 'rxjs';
import { catchError, filter, switchMap, take, finalize } from 'rxjs/operators';
import { AuthService } from '../authentication/auth.service';
import { environment } from '../../../environments/environment';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    private refreshTokenInProgress = false;
    private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

    constructor(private authService: AuthService) { }

    intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
        // No interceptar solicitudes de autenticación
        if (this.isAuthRequest(request)) {
            return next.handle(request);
        }

        // Agregar token a la solicitud si existe
        request = this.addToken(request, this.authService.getToken());

        // Manejar la solicitud con la lógica de refresh token
        return next.handle(request).pipe(
            catchError((error: HttpErrorResponse) => {
                // Si el error es 401 (Unauthorized), intentar refrescar el token
                if (error.status === 401) {
                    if (this.refreshTokenInProgress) {
                        // Si ya hay un refresh en progreso, esperar a que termine y reintentar
                        return this.refreshTokenSubject.pipe(
                            filter(token => token !== null),
                            take(1),
                            switchMap(token => {
                                return next.handle(this.addToken(request, token));
                            })
                        );
                    } else {
                        // Iniciar proceso de refresh
                        this.refreshTokenInProgress = true;
                        this.refreshTokenSubject.next(null);

                        return this.authService.refreshToken().pipe(
                            switchMap(token => {
                                this.refreshTokenInProgress = false;
                                this.refreshTokenSubject.next(token);

                                if (!token) {
                                    // Si no se pudo refrescar el token, cerrar sesión
                                    this.authService.logout();
                                    return throwError(() => new Error('Sesión expirada'));
                                }

                                // Reintentar con el nuevo token
                                return next.handle(this.addToken(request, token));
                            }),
                            catchError(err => {
                                this.refreshTokenInProgress = false;
                                this.authService.logout();
                                return throwError(() => new Error('Error al refrescar token'));
                            }),
                            finalize(() => {
                                this.refreshTokenInProgress = false;
                            })
                        );
                    }
                }

                // Para otros errores, simplemente reenviarlos
                return throwError(() => error);
            })
        );
    }

    private addToken(request: HttpRequest<any>, token: string | null): HttpRequest<any> {
        if (token) {
            return request.clone({
                setHeaders: {
                    Authorization: `${environment.tokenPrefix} ${token}`
                }
            });
        }
        return request;
    }

    private isAuthRequest(request: HttpRequest<any>): boolean {
        const authUrls = [
            `${environment.apiUrl}token/`,
            `${environment.apiUrl}token/refresh/`
        ];

        return authUrls.some(url => request.url.includes(url));
    }
}