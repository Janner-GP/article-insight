import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ChatService } from '../../services/chat.service';
import { ActivatedRoute, NavigationEnd, Router, RouterModule } from '@angular/router';
import { Message, MessageResponse } from '../../interfaces/message.interface';
import { FormsModule } from '@angular/forms';
import { catchError, of } from 'rxjs';

@Component({
  selector: 'app-chat-panel',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
  ],
  templateUrl: './chat_panel.component.html',
  styleUrl: './chat_panel.component.css',
  changeDetection: ChangeDetectionStrategy.Default,
})
export class ChatPanelComponent implements OnInit {

  newChat: boolean = false;
  chatId: string = '';
  messages: Message[] = [];
  isLoading: boolean = false;
  isLoadingMsg: boolean = false;
  progress: number = 0;
  answer: string = '';
  error: boolean = false;
  @ViewChild('chatContainer') chatContainer: ElementRef | undefined;
  scrollPosition: number = 0;

  constructor(
    private chatService: ChatService,
    private activeRoute: ActivatedRoute,
    private router: Router
  ) {
    this.simulateGradualLoad();
  }

  ngOnInit(): void {
    this.handleRouteChange();
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.handleRouteChange();
        this.simulateGradualLoad();
        this.fetchMessages();
      }
    });

    this.fetchMessages();
  }

  private handleRouteChange(): void {
    this.activeRoute.params.subscribe(params => {
      this.chatId = params['id'] || '';
      localStorage.setItem('chatId', this.chatId);
      this.newChat = !this.chatId;
    });
  }

  getSummary(article_url: string): void {
    this.isLoading = true;
    this.chatService.getSummary(article_url).subscribe((response: any) => {
      const message = response['message'];
      this.isLoading = false;
      this.chatService.getAllChats();
      this.router.navigate([`/chat/${message.chat_id}`]);
      this.newChat = false;
    });
  }

  fetchMessages(): void {
    this.isLoadingMsg = true;
    this.messages = [];
    console.log(this.chatId);
    this.chatService.getAllMessages(this.chatId)
      .pipe(
        catchError(err => {
          console.log(err)
          this.isLoadingMsg = false;
          this.error = true
          return of([]);
        })
      )
      .subscribe((response) => {
        console.log(response);
        response.forEach((message: any) => {
          if (message.is_visible) {
            this.messages.push(message);
          }
        });
        this.isLoadingMsg = false;
        this.scrollToBottom();
      });
  }

  sendMessage(){
    const content = this.answer;
    this.answer = '';

    this.messages.push({
      id: '',
      chatId: this.chatId,
      content: content,
      role: 'user',
      createdAt: new Date(),
      isVisible: true
    });
    this.isLoading = true;
    setTimeout(() => this.scrollToBottom(), 1000);
    this.chatService.sendMessage(this.chatId, content).subscribe((response: MessageResponse) => {
      this.messages.push({
        id: response.id,
        chatId: response.chat_id,
        content: response.content,
        role: response.role,
        createdAt: response.created_at,
        isVisible: response.is_visible
      });
      this.isLoading = false;
      setTimeout(() => this.scrollToBottom(), 1000);
    });
  }

  simulateGradualLoad(): void {
    const interval = setInterval(() => {
      this.progress += 10;
      if (this.progress >= 100) {
        this.isLoadingMsg = false;
        clearInterval(interval);
      }
    }, 20);
  }

  scrollToBottom(): void {
    if (this.chatContainer && this.chatContainer.nativeElement) {
      const container = this.chatContainer.nativeElement;
      this.scrollPosition = container.scrollHeight + 150;
    }
  }
}
