import { Component, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from './service/chat.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'] // Link the new CSS here
})
export class AppComponent {
  userMessage = '';
  chatHistory: { role: string, text: string }[] = [];
  loading = false;

  constructor(private chatService: ChatService) {}

  sendMessage() {
    if (!this.userMessage.trim() || this.loading) return;

    const userText = this.userMessage;
    this.chatHistory.push({ role: 'You', text: userText });
    this.userMessage = '';
    this.loading = true;

    this.chatService.sendToAI(userText).subscribe({
      next: (res) => {
        this.chatHistory.push({ role: 'AI', text: res.reply });
        this.loading = false;
      },
      error: () => {
        this.chatHistory.push({ role: 'Error', text: 'Backend unavailable. Is FastAPI running?' });
        this.loading = false;
      }
    });
  }
}