import { AfterViewInit, Component, OnInit, } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@reddit/core/services/user/user.service';
import { MatSnackBar } from '@angular/material/snack-bar';


@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss']
})
export class SignInComponent implements OnInit {
  loginForm: FormGroup;
  isLoading: boolean = false;
  hidePassword: boolean = true;

  constructor(
    private userService: UserService,
    private router: Router,
    private snackbar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.loginForm = new FormGroup({
      email: new FormControl('', {
        validators: [Validators.required, Validators.email]
      }),
      password: new FormControl('', { validators: [Validators.required] })
    });
  }

  toggleVisibility() {
    this.hidePassword = !this.hidePassword;
  }

  onSubmit() {
    console.log('Sign-in form submitted');
    console.log('Form valid:', this.loginForm.valid);
    console.log('Form values:', this.loginForm.value);
    
    if (!this.loginForm.valid) {
      console.log('Form is invalid, not submitting');
      this.snackbar.open('Please fill in all required fields', 'Close', { duration: 3000 });
      return;
    }

    const loginData = {
      email: this.loginForm.value.email,
      password: this.loginForm.value.password
    };
    
    console.log('Sending login request with data:', loginData);
    this.isLoading = true;
    
    this.userService.login(loginData).subscribe(
      (result: any) => {
        console.log('Login successful:', result);
        this.isLoading = false;
        
        // Store the auth token if provided
        if (result.key) {
          localStorage.setItem('auth_token', result.key);
          console.log('Auth token stored:', result.key);
        }
        
        // Fetch user profile after successful login
        this.userService.getAuthUser((user) => {
          console.log('User profile fetched after login:', user);
          if (user) {
            this.userService.setUser(user);
          }
        });
        
        this.snackbar.open('Successfully logged in', 'Close', { duration: 3000 });
        this.router.navigate(['']);
      },
      (err) => {
        console.error('Login error:', err);
        this.isLoading = false;
        if (err.error) {
          if (err.error.non_field_errors) {
            this.snackbar.open(err.error.non_field_errors[0], 'Close', { duration: 5000 });
          } else if (err.error.email) {
            this.snackbar.open(err.error.email[0], 'Close', { duration: 5000 });
          } else {
            this.snackbar.open('Login failed. Please try again.', 'Close', { duration: 5000 });
          }
        } else {
          this.snackbar.open('Network error. Please check your connection.', 'Close', { duration: 5000 });
        }
      }
    );
  }

  onGoogleLogin(): void {
    console.log('Google login clicked');
    this.snackbar.open('Google login is not configured yet. Please contact the administrator.', 'Close', {
      duration: 5000
    });
    // TODO: Implement Google OAuth when client credentials are configured
    // window.location.href = `${environment.serverUrl}/accounts/google/login/`;
  }

  onFacebookLogin(): void {
    console.log('Facebook login clicked');
    this.snackbar.open('Facebook login is not configured yet. Please contact the administrator.', 'Close', {
      duration: 5000
    });
    // TODO: Implement Facebook OAuth when app credentials are configured
    // window.location.href = `${environment.serverUrl}/accounts/facebook/login/`;
  }

}
