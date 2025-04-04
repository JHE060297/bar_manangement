import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Rol, Usuario } from '../models/user.model';

@Injectable({
    providedIn: 'root'
})
export class UserService {
    private apiUrl = `${environment.apiUrl}users/`;

    constructor(private http: HttpClient) { }

    // Obtener listado de usuarios
    getUsers(): Observable<Usuario[]> {
        return this.http.get<Usuario[]>(this.apiUrl);
    }

    // Obtener un usuario específico
    getUserById(id: number): Observable<Usuario> {
        return this.http.get<Usuario>(`${this.apiUrl}${id}/`);
    }

    // Crear un nuevo usuario
    createUser(user: Usuario): Observable<Usuario> {
        return this.http.post<Usuario>(this.apiUrl, user);
    }

    // Actualizar un usuario existente
    updateUser(id: number, user: Partial<Usuario>): Observable<Usuario> {
        return this.http.patch<Usuario>(`${this.apiUrl}${id}/`, user);
    }

    // Eliminar un usuario
    deleteUser(id: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}${id}/`);
    }

    // Activar un usuario
    activateUser(id: number): Observable<any> {
        return this.http.post(`${this.apiUrl}${id}/activate/`, {});
    }

    // Desactivar un usuario
    deactivateUser(id: number): Observable<any> {
        return this.http.post(`${this.apiUrl}${id}/deactivate/`, {});
    }

    // Cambiar el rol de un usuario
    changeRole(id: number, rolId: number): Observable<any> {
        return this.http.post(`${this.apiUrl}${id}/change_role/`, { id_rol: rolId });
    }

    // Cambiar la sucursal de un usuario
    changeBranch(id: number, sucursalId: number): Observable<any> {
        return this.http.post(`${this.apiUrl}${id}/change_branch/`, { id_sucursal: sucursalId });
    }

    // Obtener roles
    getRoles(): Observable<Rol[]> {
        return this.http.get<Rol[]>(`${this.apiUrl}roles/`);
    }
}