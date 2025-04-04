import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';
import { BranchesListComponent } from './sucursal-list/sucursal-list.component';
import { BranchFormComponent } from './sucursal-form/sucursal-form.component';
import { TablesListComponent } from './tables-list/tables-list.component';
import { TableFormComponent } from './table-form/table-form.component';
import { AuthGuard } from '../../core/guards/auth.guard';
import { RoleGuard } from '../../core/guards/role.guard';

const routes: Routes = [
    {
        path: '',
        component: BranchesListComponent,
        canActivate: [AuthGuard, RoleGuard],
        data: { roles: ['admin'] }
    },
    {
        path: 'new',
        component: BranchFormComponent,
        canActivate: [AuthGuard, RoleGuard],
        data: { roles: ['admin'] }
    },
    {
        path: 'edit/:id',
        component: BranchFormComponent,
        canActivate: [AuthGuard, RoleGuard],
        data: { roles: ['admin'] }
    },
    {
        path: ':id/tables',
        component: TablesListComponent,
        canActivate: [AuthGuard],
        data: { roles: ['admin', 'cajero', 'mesero'] }
    },
    {
        path: ':id/tables/new',
        component: TableFormComponent,
        canActivate: [AuthGuard, RoleGuard],
        data: { roles: ['admin'] }
    },
    {
        path: ':id/tables/edit/:tableId',
        component: TableFormComponent,
        canActivate: [AuthGuard, RoleGuard],
        data: { roles: ['admin'] }
    }
];

@NgModule({
    declarations: [
        BranchesListComponent,
        BranchFormComponent,
        TablesListComponent,
        TableFormComponent
    ],
    imports: [
        CommonModule,
        SharedModule,
        RouterModule.forChild(routes)
    ],
    exports: [RouterModule]
})
export class BranchesModule { }