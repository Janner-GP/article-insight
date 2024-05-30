import { Routes } from '@angular/router';
import { ChatPanelComponent } from './components/chat_panel/chat_panel.component';

export const routes: Routes = [
    { path: 'chat/new', component: ChatPanelComponent },
    { path: 'chat/:id', component: ChatPanelComponent },
    { path: '**', redirectTo: 'chat/new' },
    { path: '', redirectTo: 'chat/new', pathMatch: 'full'}
];
