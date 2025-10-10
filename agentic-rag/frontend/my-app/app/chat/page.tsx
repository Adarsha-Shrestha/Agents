"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Sparkles, Send, Loader2, BookOpen, Plus, MessageSquare, Trash2, Menu, X, MoreVertical } from "lucide-react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

const API_BASE_URL = "http://localhost:8000/api/chat"

interface Message {
  role: "user" | "assistant"
  content: string
  timestamp: string
  sources?: Array<{ page_content: string; metadata: any }>
  isConversational?: boolean
}

interface Session {
  session_id: string
  message_count: number
  created: string | null
  subject?: string
}

interface ChatSession {
  session_id: string
  messages: Message[]
}

export default function ChatPage() {
  const [sessions, setSessions] = useState<Session[]>([])
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [subject, setSubject] = useState<string>("All Subjects")
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [isMounted, setIsMounted] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Fix hydration error
  useEffect(() => {
    setIsMounted(true)
  }, [])

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Load sessions on mount
  useEffect(() => {
    loadSessions()
  }, [])

  const loadSessions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions`)
      const data = await response.json()
      setSessions(data.sessions || [])
    } catch (error) {
      console.error("Error loading sessions:", error)
    }
  }

  const createNewSession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/session`, {
        method: "POST",
      })
      const data = await response.json()
      
      setCurrentSessionId(data.session_id)
      setMessages([])
      await loadSessions()
    } catch (error) {
      console.error("Error creating session:", error)
    }
  }

  const loadSession = async (sessionId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/session/${sessionId}`)
      const data: ChatSession = await response.json()
      
      setCurrentSessionId(sessionId)
      setMessages(data.messages)
    } catch (error) {
      console.error("Error loading session:", error)
    }
  }

  const deleteSession = async (sessionId: string) => {
    try {
      await fetch(`${API_BASE_URL}/session/${sessionId}`, {
        method: "DELETE",
      })
      
      if (currentSessionId === sessionId) {
        setCurrentSessionId(null)
        setMessages([])
      }
      
      await loadSessions()
    } catch (error) {
      console.error("Error deleting session:", error)
    }
  }

  const sendMessage = async () => {
    if (!input.trim()) return

    // Create session if none exists
    if (!currentSessionId) {
      await createNewSession()
      // Wait a bit for session to be created
      await new Promise(resolve => setTimeout(resolve, 100))
      await loadSessions()
      setSessions((prev) =>
        prev.map((s) =>
          s.session_id === currentSessionId ? { ...s, subject } : s
          )
        )

    }

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    }
    
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const endpoint = currentSessionId
        ? `${API_BASE_URL}/session/${currentSessionId}/message`
        : `${API_BASE_URL}/message`

      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: input,
          subject: subject === "All Subjects" ? undefined : subject,
        }),
      })

      const data = await response.json()

      const assistantMessage: Message = {
        role: "assistant",
        content: data.generation,
        timestamp: new Date().toISOString(),
        sources: data.sources,
        isConversational: data.is_conversational,
      }

      setMessages((prev) => [...prev, assistantMessage])
      await loadSessions()
    } catch (error) {
      console.error("Error sending message:", error)
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please make sure the backend is running on localhost:8000.",
        timestamp: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  // const getSessionPreview = (session: Session) => {
  //   if (!session.created) return "New Chat"
  //   const date = new Date(session.created)
  //   // return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
  //   return subject === "All Subjects" ? "All Subjects" : subject
  // }

  const getSessionPreview = (session: Session) => {
    if (session.subject) return session.subject
    if (!session.created) return "New Chat"
    return "All Subjects"
  }
  

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <div
        className={`${
          sidebarOpen ? "w-64" : "w-0"
        } transition-all duration-300 border-r border-border bg-card flex flex-col overflow-hidden`}
      >
        <div className="p-4 border-b border-border">
          <Button onClick={createNewSession} className="w-full" size="sm">
            <Plus className="w-4 h-4 mr-2" />
            New Chat
          </Button>
        </div>

        <div className="flex-1 overflow-y-auto p-2">
          {sessions.map((session) => (
            <div
              key={session.session_id}
              className={`group flex items-center gap-2 p-3 rounded-lg mb-1 cursor-pointer hover:bg-accent ${
                currentSessionId === session.session_id ? "bg-accent" : ""
              }`}
              onClick={() => loadSession(session.session_id)}
            >
              <MessageSquare className="w-4 h-4 text-muted-foreground flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">
                  {getSessionPreview(session)}
                </p>
                <p className="text-xs text-muted-foreground">
                  {session.message_count} messages
                </p>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild onClick={(e) => e.stopPropagation()}>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="opacity-0 group-hover:opacity-100 h-8 w-8"
                  >
                    <MoreVertical className="w-4 h-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem
                    onClick={(e) => {
                      e.stopPropagation()
                      deleteSession(session.session_id)
                    }}
                    className="text-destructive"
                  >
                    <Trash2 className="w-4 h-4 mr-2" />
                    Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="border-b border-border bg-card">
          <div className="px-4 py-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </Button>
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-primary-foreground" />
                </div>
                <span className="text-xl font-bold text-foreground">AI Chat</span>
              </div>
            </div>
            <Select value={subject} onValueChange={setSubject}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="All Subjects" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="All Subjects">All Subjects</SelectItem>
                <SelectItem value="DataMining">Data Mining</SelectItem>
                <SelectItem value="Network">Network Systems</SelectItem>
                <SelectItem value="Distributed">Distributed Computing</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-6">
          <div className="max-w-4xl mx-auto">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center max-w-md">
                  <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Sparkles className="w-8 h-8 text-primary" />
                  </div>
                  <h2 className="text-2xl font-bold text-foreground mb-2">Ask me anything</h2>
                  <p className="text-muted-foreground leading-relaxed">
                    I can help you understand concepts from your course materials using advanced retrieval-augmented
                    generation.
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message, index) => (
                  <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                    <Card
                      className={`max-w-[80%] p-4 ${
                        message.role === "user" ? "bg-primary text-primary-foreground" : "bg-card"
                      }`}
                    >
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                      {message.sources && message.sources.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-border">
                          <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
                            <BookOpen className="w-3 h-3" />
                            <span>Sources ({message.sources.length})</span>
                          </div>
                          <div className="space-y-2">
                            {message.sources.slice(0, 2).map((source, idx) => (
                              <div key={idx} className="text-xs bg-muted/50 p-2 rounded">
                                <p className="line-clamp-2">{source.page_content}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </Card>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <Card className="p-4 bg-card">
                      <Loader2 className="w-5 h-5 animate-spin text-primary" />
                    </Card>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-border bg-card p-4">
          <div className="max-w-4xl mx-auto flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !isLoading && sendMessage()}
              placeholder="Ask a question about your course materials..."
              className="flex-1"
              disabled={isLoading}
            />
            <Button onClick={sendMessage} disabled={isLoading || !input.trim()}>
              {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}