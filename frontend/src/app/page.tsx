"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

// Definiamo il tipo TypeScript per i nostri messaggi
type Message = {
  role: "user" | "ai";
  content: string;
};

export default function ChatPage() {
  // Stato: memorizza la lista dei messaggi
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", content: "Ciao! Sono il tuo assistente allo studio. Fammi una domanda o carica un documento!" }
  ]);
  
  // Stato: memorizza il testo che l'utente sta digitando nell'input
  const [inputValue, setInputValue] = useState("");

  const handleSendMessage = () => {
    // Evitiamo di inviare messaggi vuoti
    if (!inputValue.trim()) return;

    // 1. Aggiungiamo il messaggio dell'utente all'interfaccia
    const newUserMessage: Message = { role: "user", content: inputValue };
    setMessages((prev) => [...prev, newUserMessage]);
    
    // 2. Svuotiamo il campo di testo
    setInputValue("");

    // TODO: (Prossimo step) Fare la chiamata al backend FastAPI per avere la risposta dell'AI
  };

  return (
    <div className="flex h-screen w-full items-center justify-center bg-zinc-100 p-4">
      {/* Contenitore principale a forma di Card */}
      <Card className="w-full max-w-3xl h-[85vh] flex flex-col shadow-2xl">
        <CardHeader className="border-b bg-white rounded-t-xl">
          <CardTitle>📚 Study Assistant AI</CardTitle>
        </CardHeader>
        
        <CardContent className="flex flex-col flex-1 overflow-hidden p-4 bg-white rounded-b-xl">
          
          {/* 1. AREA DEI MESSAGGI (Scrollabile) */}
          <ScrollArea className="flex-1 pr-4 mb-4">
            <div className="flex flex-col gap-4">
              {messages.map((msg, index) => (
                <div 
                  key={index} 
                  className={`p-3 rounded-lg max-w-[80%] ${
                    msg.role === "user" 
                      ? "bg-zinc-900 text-white self-end ml-auto" 
                      : "bg-zinc-100 text-black self-start mr-auto"
                  }`}
                >
                  {msg.content}
                </div>
              ))}
            </div>
          </ScrollArea>

          {/* 2. AREA DI INPUT */}
          <div className="flex gap-2 pt-4 border-t">
            <Input 
              placeholder="Fai una domanda sul materiale..." 
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
              className="flex-1"
            />
            <Button onClick={handleSendMessage}>Invia</Button>
          </div>

        </CardContent>
      </Card>
    </div>
  );
}
