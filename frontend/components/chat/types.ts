export interface Message {
    id: number;
    role: 'user' | 'assistant';
    content: string;
    created_at: string;
}

export interface ChatState {
    messages: Message[];
    isLoading: boolean;
    error: string | null;
}

export interface ChatRequest {
    message: string;
    conversation_id?: number;
}

export interface ChatResponse {
    conversation_id: number;
    response: string;
}
