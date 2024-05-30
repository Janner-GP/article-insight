import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { SidebarItem } from './../interfaces/items_sidebar.interface';
import { Chat } from '../interfaces/chat.interface';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  apiUrl = environment.apiUrl;

  constructor(private _http: HttpClient) { }

  getSummary(article_url: string): Observable<any> {
    return this._http.post(`${this.apiUrl}/summary`, { "url": article_url });
  }

  getAllChats(): Observable<SidebarItem[]>{
    return this._http.get<Chat[]>(`${this.apiUrl}/chats`).pipe(
      map((chats: Chat[]) => {
        return chats.map((chat: Chat) => {
          return {
            name: chat.name,
            icon: 'fa-solid fa-comments',
            path: `/chat/${chat.id}`
          };
        });
      })
    );
  }

  getAllMessages(chatId: string): Observable<any> {
    return this._http.get(`${this.apiUrl}/chat/${chatId}/messages`);
  }

  sendMessage(chatId: string, message: string): Observable<any> {
    return this._http.post(`${this.apiUrl}/chat/${chatId}/messages`, { "content": message });
  }

}
