import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { MainLayoutComponent } from './layouts/main-layout/main-layout.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';
import { AccessDeniedComponent } from './pages/access-denied/access-denied.component';
import { AuthGuard } from './core/guards/auth.guard';

const routes: Routes = [
    {
        path: 'login',
        component: LoginComponent
    },
    {
        path: 'access-denied',
        component: AccessDeniedComponent
    },
    {
        path: '',
        component: MainLayoutComponent,
        canActivate: [AuthGuard],
        children: [
            {
                path: '',
                redirectTo: 'dashboard',
                pathMatch: 'full'
            },
            {
                path: 'dashboard',
                loadChildren: () => import('./modules/dashboard/dashboard.module').then(m => m.DashboardModule)
            },
            {
                path: 'users',
                loadChildren: () => import('./modules/users/users.module').then(m => m.UsersModule),
                data: { roles: ['admin'] }
            },
            {
                path: 'inventory',
                loadChildren: () => import('./modules/inventory/inventory.module').then(m => m.InventoryModule),
                data: { roles: ['admin', 'cajero'] }
            },
            {
                path: 'orders',
                loadChildren: () => import('./modules/orders/orders.module').then(m => m.OrdersModule),
                data: { roles: ['admin', 'cajero', 'mesero'] }
            },
            {
                path: 'tables',
                loadChildren: () => import('./modules/tables/tables.module').then(m => m.TablesModule),
                data: { roles: ['admin', 'cajero', 'mesero'] }
            },
            {
                path: 'payments',
                loadChildren: () => import('./modules/payments/payments.module').then(m => m.PaymentsModule),
                data: { roles: ['admin', 'cajero'] }
            },
            {
                path: 'reports',
                loadChildren: () => import('./modules/reports/reports.module').then(m => m.ReportsModule),
                data: { roles: ['admin', 'cajero'] }
            },
            {
                path: 'branches',
                loadChildren: () => import('./modules/branches/branches.module').then(m => m.BranchesModule),
                data: { roles: ['admin'] }
            }
        ]
    },
    {
        path: '**',
        component: NotFoundComponent
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }