"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Paperclip, Loader2 } from "lucide-react"; // Icone da lucide-react

type Message = {
  role: "user" | "ai";
  content: string;
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", content: "Ciao! Sono il tuo assistente allo studio. Fammi una domanda o carica un documento di testo!" }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isUploading, setIsUploading] = useState(false); // Stato per il caricamento in corso
  
  // useRef ci permette di avere un "telecomando" per cliccare l'input nascosto
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userText = inputValue;

    const newUserMessage: Message = { role: "user", content: userText };
    setMessages((prev) => [...prev, newUserMessage]);
    
    setInputValue("");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText }),
      });

      if (!response.ok) throw new Error("Errore dal server FastAPI");

      const data = await response.json();
      
      const aiMessage: Message = { role: "ai", content: data.reply };
      setMessages((prev) => [...prev, aiMessage]);
      
    } catch (error) {
      console.error("Errore fetch:", error);
      setMessages((prev) => [...prev, { role: "ai", content: "⚠️ Si è verificato un errore di rete." }]);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    
    // Costruiamo i dati come "Multipart Form" (il formato standard per i file)
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Mandiamo il file al backend
      const response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        // ATTENZIONE: Non impostare i Content-Type! 
        // Il browser lo calcola in automatico per FormData aggiungendo il "boundary" corretto
        body: formData, 
      });

      if (!response.ok) throw new Error("Errore durante l'upload");
      
      // Comunichiamo il successo nella chat come se fosse un messaggio dell'AI
      setMessages((prev) => [...prev, { 
        role: "ai", 
        content: `✅ Documento "${file.name}" letto e memorizzato. Ora puoi farmi domande a riguardo!` 
      }]);
    } catch (error) {
      console.error("Errore upload:", error);
      setMessages((prev) => [...prev, { role: "ai", content: `❌ Impossibile caricare il file.` }]);
    } finally {
      setIsUploading(false);
      // Svuotiamo l'input per permettere di ricaricare lo stesso file in futuro
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  return (
    <div className="flex h-screen w-full items-center justify-center bg-zinc-100 p-4">
      <Card className="w-full max-w-3xl h-[85vh] flex flex-col shadow-2xl">
        <CardHeader className="border-b bg-white rounded-t-xl">
          <CardTitle>📚 Study Assistant AI</CardTitle>
        </CardHeader>
        
        <CardContent className="flex flex-col flex-1 overflow-hidden p-4 bg-white rounded-b-xl">
          
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

          {/* AREA INPUT E BOTTONI */}
          <div className="flex gap-2 pt-4 border-t items-center">
            
            {/* Input file Nascosto */}
            <input 
              type="file" 
              accept=".txt" 
              className="hidden" 
              ref={fileInputRef}
              onChange={handleFileUpload}
            />
            
            {/* Bottone Graffetta per Upload */}
            <Button 
              variant="outline" 
              size="icon" 
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading}
              title="Allega un file di testo (.txt)"
            >
              {isUploading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Paperclip className="h-4 w-4" />}
            </Button>

            <Input 
              placeholder="Fai una domanda sul materiale..." 
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
              className="flex-1"
            />
            
            <Button onClick={handleSendMessage} disabled={isUploading}>
              Invia
            </Button>
          </div>

        </CardContent>
      </Card>
    </div>
  );
}
