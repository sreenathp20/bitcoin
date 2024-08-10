import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  apiUrl = 'http://localhost:4200/api';

  constructor(private http: HttpClient) { }

  getBlocks(): Observable<any[]> {
    const headers = new HttpHeaders()
    return this.http.get<any[]>(`${this.apiUrl}/block/`);
  }
  getOnesCount(): Observable<any[]> {
    const headers = new HttpHeaders()
    return this.http.get<any[]>(`${this.apiUrl}/onescount/`);
  }
  getBlocksByHash(hash_swap:string): Observable<any[]> {
    const headers = new HttpHeaders()
    return this.http.get<any[]>(`${this.apiUrl}/blockbyhash/`+hash_swap);
  }
  

}
