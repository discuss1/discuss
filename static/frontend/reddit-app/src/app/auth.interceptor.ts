import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor() {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Get auth token from localStorage
    const authToken = localStorage.getItem('auth_token');
    
    // Clone request with credentials and auth token if available
    let clonedRequest = request.clone({
      withCredentials: true
    });
    
    if (authToken) {
      clonedRequest = clonedRequest.clone({
        setHeaders: {
          'Authorization': `Token ${authToken}`
        }
      });
    }
    
    return next.handle(clonedRequest);
  }
}
