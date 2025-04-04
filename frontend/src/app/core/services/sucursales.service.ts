import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Sucursal, Mesa } from '../models/user.model';

@Injectable({
    providedIn: 'root'
})
export class BranchesService {
    private apiUrl = `${environment.apiUrl}branches/`;

    constructor(private http: HttpClient) { }

    // Sucursales
    getBranches(): Observable<Sucursal[]> {
        return this.http.get<Sucursal[]>(`${this.apiUrl}branches/`);
    }

    getBranchById(id: number): Observable<Sucursal> {
        return this.http.get<Sucursal>(`${this.apiUrl}branches/${id}/`);
    }

    createBranch(branch: Sucursal): Observable<Sucursal> {
        return this.http.post<Sucursal>(`${this.apiUrl}branches/`, branch);
    }

    updateBranch(id: number, branch: Partial<Sucursal>): Observable<Sucursal> {
        return this.http.patch<Sucursal>(`${this.apiUrl}branches/${id}/`, branch);
    }

    deleteBranch(id: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}branches/${id}/`);
    }

    // Mesas
    getTables(filters?: any): Observable<Mesa[]> {
        let url = `${this.apiUrl}tables/`;
        if (filters) {
            const params = new URLSearchParams();
            Object.keys(filters).forEach(key => {
                if (filters[key] !== null && filters[key] !== undefined) {
                    params.set(key, filters[key]);
                }
            });
            if (params.toString()) {
                url += `?${params.toString()}`;
            }
        }
        return this.http.get<Mesa[]>(url);
    }

    getTableById(id: number): Observable<Mesa> {
        return this.http.get<Mesa>(`${this.apiUrl}tables/${id}/`);
    }

    createTable(table: Mesa): Observable<Mesa> {
        return this.http.post<Mesa>(`${this.apiUrl}tables/`, table);
    }

    updateTable(id: number, table: Partial<Mesa>): Observable<Mesa> {
        return this.http.patch<Mesa>(`${this.apiUrl}tables/${id}/`, table);
    }

    deleteTable(id: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}tables/${id}/`);
    }

    changeTableStatus(id: number, estado: string): Observable<any> {
        return this.http.post(`${this.apiUrl}tables/${id}/cambiar_estado/`, { estado });
    }

    freeTable(id: number): Observable<any> {
        return this.http.post(`${this.apiUrl}tables/${id}/liberar_mesa/`, {});
    }

    getTablesByBranch(branchId: number): Observable<Mesa[]> {
        return this.getTables({ id_sucursal: branchId });
    }
}