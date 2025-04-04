import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../core/authentication/auth.service';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
    loginForm: FormGroup;
    isLoading = false;
    hidePassword = true;
    returnUrl: string = '/';

    constructor(
        private formBuilder: FormBuilder,
        private router: Router,
        private route: ActivatedRoute,
        private authService: AuthService,
        private snackBar: MatSnackBar
    ) {
        // Crear formulario de login
        this.loginForm = this.formBuilder.group({
            usuario: ['', [Validators.required]],
            password: ['', [Validators.required]]
        });

        // Verificar si ya está autenticado
        if (this.authService.isAuthenticated()) {
            this.router.navigate(['/']);
        }
    }

    ngOnInit(): void {
        // Obtener la URL de retorno de los query params o usar la raíz por defecto
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    onSubmit(): void {
        if (this.loginForm.invalid) {
            return;
        }

        this.isLoading = true;
        const credentials = this.loginForm.value;

        this.authService.login(credentials).subscribe(
            success => {
                if (success) {
                    this.router.navigateByUrl(this.returnUrl);
                } else {
                    this.snackBar.open('Credenciales incorrectas', 'Cerrar', {
                        duration: 3000,
                        horizontalPosition: 'center',
                        verticalPosition: 'bottom'
                    });
                }
                this.isLoading = false;
            },
            error => {
                console.error('Error de login', error);
                this.snackBar.open('Error al iniciar sesión', 'Cerrar', {
                    duration: 3000,
                    horizontalPosition: 'center',
                    verticalPosition: 'bottom'
                });
                this.isLoading = false;
            }
        );
    }
}