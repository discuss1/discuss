import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '@reddit/env/environment';
import { User } from '@reddit/core/models/user.model';
import { StorageHandlerService } from '../storage/storage-handler.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private serverUrl = `${environment.serverUrl}`;
  user: BehaviorSubject<User>;
  userInitialized = new BehaviorSubject(false);

  constructor(
    public http: HttpClient,
    private storage: StorageHandlerService
  ) {
    console.log('UserService: serverUrl configured as:', this.serverUrl);
    console.log('UserService: environment:', environment);
    
    // Initialize user BehaviorSubject
    this.user = new BehaviorSubject<User>(null);
  }

  setUser(user: User, callback?: (user: User) => any): void {
    console.log('UserService: Setting user:', user);
    this.user.next(user);
    if (user) {
      this.storage.storeItem('user', user);
    }
    this.userInitialized.next(true);
    if (callback) {
      callback(user);
    }
  }

  unsetUser(): void {
    this.user.next(null);
    this.storage.removeItem('user');
  }

  fetchUser(callback: (user: User) => any): void {
    if (this.user?.value) {
      callback(this.user.value);
    }
    const storageUser = this.storage.getItem('user');
    if (storageUser) {
      this.setUser(storageUser, callback);
    } else {
      this.getAuthUser((user) => this.setUser(user, callback));
    }
  }

  getAuthUser(callback: (user: User) => any): void {
    console.log('UserService: Fetching authenticated user from:', this.serverUrl + '/rest-auth/user/');
    this.http.get(this.serverUrl + '/rest-auth/user/').subscribe(
      (response: Object) => {
        console.log('UserService: Auth user response:', response);
        callback(response as User);
      }, (error: any) => {
        console.error('UserService: Auth user error:', error);
        callback(null);
      }
    );
  }

  getUserByUsername(username: string) {
    return this.http.get(this.serverUrl + '/api/v1/users/' + username + '/');
  }

  register(postData) {
    const url = this.serverUrl + '/rest-auth/registration/';
    console.log('UserService: Making registration request to:', url);
    console.log('UserService: Registration data:', postData);
    return this.http.post(url, postData);
  }

  login(postData) {
    const url = this.serverUrl + '/rest-auth/login/';
    console.log('UserService: Making login request to:', url);
    console.log('UserService: Login data:', postData);
    return this.http.post(url, postData);
  }

  logout() {
    return this.http.post(this.serverUrl + '/rest-auth/logout/', {});
  }

  addInterests(username: string) {
    return;
  }

  userInvitations(username: string) {
    return this.http.get(this.serverUrl + '/api/v1/users/' + username + '/invitations/');
  }

  userRequestedGroups(username: string) {
    return this.http.get(this.serverUrl + '/api/v1/users/' + username + '/requested_groups/');
  }

  userInvites(username: string) {
    return this.http.get(this.serverUrl + '/api/v1/users/' + username + '/user_invites/');
  }

  userUpvotes(username: string) {
    return this.http.get(this.serverUrl + '/api/v1/users/' + username + '/user_upvotes/');
  }

  userDownvotes(username: string) {
    return this.http.get(this.serverUrl + '/api/v1/users/' + username + '/user_downvotes/');
  }

  getBookmarks(username: string) {
    return this.http.get(this.serverUrl + '/api/v1/users/' + username + '/bookmarks/');
  }

}
