import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { ChatService } from '../../../services/chat.service';
import { NavigationEnd, Router, RouterModule } from '@angular/router';
import { SidebarItem } from '../../../interfaces/items_sidebar.interface';
import { filter } from 'rxjs';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule
  ],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css',
  changeDetection: ChangeDetectionStrategy.Default,
})
export class SidebarComponent implements OnInit{

  isCollapsed = false;
  items: SidebarItem[] = []

  constructor( private chatService: ChatService, private router: Router ) {}

  ngOnInit() {
    // Obtener todos los chats
    this.getAllchats();
    this.router.events
    .pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      this.getAllchats();
    });
  }

  getAllchats() {
    this.chatService.getAllChats().subscribe((chats: any) => {
      this.items = chats
    });
  }
}
