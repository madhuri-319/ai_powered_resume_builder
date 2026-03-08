import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from './service/chat.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styles: [`.chat-box { height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; }`]
})
export class AppComponent {
  userMessage = '';
  chatHistory: { role: string, text: string }[] = [];
  loading = false;

  constructor(private chatService: ChatService) {}

  async sendMessage() {
    if (!this.userMessage.trim()) return;

    this.chatHistory.push({ role: 'You', text: this.userMessage });
    const currentPrompt = this.userMessage;
    this.userMessage = '';
    this.loading = true;

    this.chatService.sendToAI(currentPrompt).subscribe({
      next: (res) => {
        this.chatHistory.push({ role: 'AI', text: res.reply });
        this.loading = false;
      },
      error: () => {
        this.chatHistory.push({ role: 'Error', text: 'Failed to reach backend.' });
        this.loading = false;
      }
    });
  }
}