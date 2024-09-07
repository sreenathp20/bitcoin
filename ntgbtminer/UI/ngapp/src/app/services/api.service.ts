import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class ApiService {
    constructor(private http: HttpClient) { }
    apiUrl = 'http://127.0.0.1:5000/'

    getConfig() {
        return this.http.get(this.apiUrl+'sha256');
    }
}