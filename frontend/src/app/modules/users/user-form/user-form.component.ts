import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { UserService } from '../../../core/services/user.service';
import { BranchesService } from '../../../core/services/branches.service';
import { Usuario, Rol, Sucursal } from '../../../core/models/user.model';
import { forkJoin, of } from 'rxjs';
import { catchError, finalize } from 'rxjs/operators';

@Component({
    standalone: false,
    selector: 'app-user-form',
    templateUrl: './user-form.component.html',
    styleUrls: ['./user-form.component.scss']
})
export class UserFormComponent implements OnInit {
    userForm: FormGroup;
    isNewUser: boolean = true;
    userId: number | null = null;
    isLoading: boolean = false;
    isSubmitting: boolean = false;
    hidePassword: boolean = true;
    roles: Rol[] = [];
    branches: Sucursal[] = [];
    error: string = '';

    constructor(
        private fb: FormBuilder,
        private userService: UserService,
        private branchesService: BranchesService,
        private route: ActivatedRoute,
        private router: Router,
        private snackBar: MatSnackBar
    ) {
        this.userForm = this.createForm();
    }

    ngOnInit(): void {
        // Determinar si es nuevo o edición basado en el URL
        const idParam = this.route.snapshot.paramMap.get('id');
        this.userId = idParam ? +idParam : null;
        this.isNewUser = !this.userId;

        // Inicializar los datos
        this.loadInitialData();
    }

    createForm(): FormGroup {
        return this.fb.group({
            nombre: ['', [Validators.required]],
            apellido: ['', [Validators.required]],
            usuario: ['', [Validators.required]],
            password: ['', this.isNewUser ? [Validators.required, Validators.minLength(6)] : []],
            id_rol: ['', [Validators.required]],
            id_sucursal: ['', [Validators.required]],
            is_active: [true]
        });
    }

    loadInitialData(): void {
        this.isLoading = true;

        // Cargar roles y sucursales en paralelo
        forkJoin({
            roles: this.userService.getRoles().pipe(catchError(() => of([]))),
            branches: this.branchesService.getBranches().pipe(catchError(() => of([]))),
            user: this.isNewUser ? of(null) : this.userService.getUserById(this.userId as number).pipe(catchError(() => of(null)))
        })
            .pipe(
                finalize(() => this.isLoading = false)
            )
            .subscribe(
                result => {
                    this.roles = result.roles;
                    this.branches = result.branches;

                    // Si es edición, llenar el formulario con los datos del usuario
                    if (!this.isNewUser && result.user) {
                        this.populateForm(result.user);
                    }
                },
                error => {
                    this.error = 'Error al cargar datos iniciales';
                    console.error('Error loading initial data', error);
                }
            );
    }

    populateForm(user: Usuario): void {
        this.userForm.patchValue({
            nombre: user.nombre,
            apellido: user.apellido,
            usuario: user.usuario,
            id_rol: user.id_rol,
            id_sucursal: user.id_sucursal,
            is_active: user.is_active
        });

        // Eliminar la validación requerida del password en modo edición
        const passwordControl = this.userForm.get('password');
        if (passwordControl) {
            passwordControl.setValidators([]);
            passwordControl.updateValueAndValidity();
        }
    }

    onSubmit(): void {
        if (this.userForm.invalid) {
            return;
        }

        this.isSubmitting = true;
        const userData = this.userForm.value;

        // Si el campo password está vacío en modo edición, eliminarlo del objeto
        if (!this.isNewUser && !userData.password) {
            delete userData.password;
        }

        // Crear o actualizar usuario según corresponda
        const operation = this.isNewUser
            ? this.userService.createUser(userData)
            : this.userService.updateUser(this.userId as number, userData);

        operation.pipe(
            finalize(() => this.isSubmitting = false)
        ).subscribe(
            (response) => {
                this.snackBar.open(
                    this.isNewUser
                        ? 'Usuario creado exitosamente'
                        : 'Usuario actualizado exitosamente',
                    'Cerrar',
                    { duration: 3000 }
                );
                this.router.navigate(['/users']);
            },
            (error) => {
                const errorMessage = this.isNewUser
                    ? 'Error al crear usuario'
                    : 'Error al actualizar usuario';
                this.snackBar.open(errorMessage, 'Cerrar', { duration: 5000 });
                console.error('Error with user operation', error);
            }
        );
    }

    onCancel(): void {
        this.router.navigate(['/users']);
    }
}