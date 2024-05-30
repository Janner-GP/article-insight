export interface MessageResponse {
    id: string;
    chat_id: string;
    content: string;
    role: string;
    created_at: Date;
    is_visible: boolean;
}

export interface Message {
    id: string;
    chatId: string;
    content: string;
    role: string;
    createdAt: Date;
    isVisible: boolean;
}
