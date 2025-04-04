import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../../shared/shared.module';
import { TablesViewComponent } from './tables-view/tables-view.component';
import { TableDetailComponent } from './table-detail/table-detail.component';
import { AuthGuard } from '../../core/guards/auth.guard';
import { RoleGuard } from '../../core/guards/role.guard';

const routes: Routes = [
  {
    path: '',
    component: TablesViewComponent,
    canActivate: [AuthGuard],
    data: { roles: ['admin', 'cajero', 'mesero'] }
  },
  {
    path: ':id',
    component: TableDetailComponent,
    canActivate: [AuthGuard],
    data: { roles: ['admin', 'cajero', 'mesero'] }
  }
];

@NgModule({
  declarations: [
    TablesViewComponent,
    TableDetailComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class TablesModule { }