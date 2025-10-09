"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { BookOpen, ArrowLeft, Loader2, RotateCw, ChevronLeft, ChevronRight } from "lucide-react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface Flashcard {
  front: string
  back: string
  category: string
  difficulty: string
  tags: string[]
}

type FlashcardState = "setup" | "studying"

export default function FlashcardsPage() {
  const [state, setState] = useState<FlashcardState>("setup")
  const [topic, setTopic] = useState("")
  const [subject, setSubject] = useState("All Subjects")
  const [numCards, setNumCards] = useState("10")
  const [isLoading, setIsLoading] = useState(false)

  const [flashcards, setFlashcards] = useState<Flashcard[]>([])
  const [currentCard, setCurrentCard] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)

  const generateFlashcards = async () => {
    if (!topic.trim()) return

    setIsLoading(true)
    try {
      const response = await fetch("http://localhost:8000/api/flashcard/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic,
          subject: subject || undefined,
          num_cards: Number.parseInt(numCards),
        }),
      })

      const data = await response.json()

      if (data.success) {
        setFlashcards(data.flashcard_data)
        setState("studying")
        setCurrentCard(0)
        setIsFlipped(false)
      }
    } catch (error) {
      console.error("[v0] Error generating flashcards:", error)
      alert("Failed to generate flashcards. Make sure the backend is running.")
    } finally {
      setIsLoading(false)
    }
  }

  const nextCard = () => {
    if (currentCard < flashcards.length - 1) {
      setCurrentCard(currentCard + 1)
      setIsFlipped(false)
    }
  }

  const prevCard = () => {
    if (currentCard > 0) {
      setCurrentCard(currentCard - 1)
      setIsFlipped(false)
    }
  }

  const resetFlashcards = () => {
    setState("setup")
    setTopic("")
    setFlashcards([])
    setCurrentCard(0)
    setIsFlipped(false)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" asChild>
              <Link href="/">
                <ArrowLeft className="w-5 h-5" />
              </Link>
            </Button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-success rounded-lg flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-foreground">Flashcard Studio</span>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-3xl">
        {state === "setup" && (
          <Card className="p-8">
            <h2 className="text-2xl font-bold text-foreground mb-6">Create Flashcards</h2>

            <div className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="topic">Topic</Label>
                <Input
                  id="topic"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g., Classification Algorithms, Routing Protocols"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="subject">Subject (Optional)</Label>
                <Select value={subject} onValueChange={setSubject}>
                  <SelectTrigger id="subject">
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

              <div className="space-y-2">
                <Label htmlFor="numCards">Number of Cards</Label>
                <Select value={numCards} onValueChange={setNumCards}>
                  <SelectTrigger id="numCards">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="5">5 Cards</SelectItem>
                    <SelectItem value="10">10 Cards</SelectItem>
                    <SelectItem value="15">15 Cards</SelectItem>
                    <SelectItem value="20">20 Cards</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button onClick={generateFlashcards} disabled={isLoading || !topic.trim()} className="w-full" size="lg">
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Generating Flashcards...
                  </>
                ) : (
                  "Generate Flashcards"
                )}
              </Button>
            </div>
          </Card>
        )}

        {state === "studying" && flashcards.length > 0 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="text-sm text-muted-foreground">
                Card {currentCard + 1} of {flashcards.length}
              </div>
              <Button onClick={resetFlashcards} variant="outline" size="sm">
                New Set
              </Button>
            </div>

            <div
              className="relative h-[400px] cursor-pointer perspective-1000"
              onClick={() => setIsFlipped(!isFlipped)}
            >
              <Card
                className={`absolute inset-0 p-8 flex flex-col justify-center items-center transition-all duration-500 transform-style-3d ${
                  isFlipped ? "rotate-y-180 opacity-0" : "rotate-y-0 opacity-100"
                }`}
              >
                <div className="mb-4 flex gap-2">
                  <span className="px-2 py-1 bg-success/10 text-success text-xs font-medium rounded">
                    {flashcards[currentCard].difficulty}
                  </span>
                  <span className="px-2 py-1 bg-primary/10 text-primary text-xs font-medium rounded">
                    {flashcards[currentCard].category}
                  </span>
                </div>

                <div className="text-center">
                  <p className="text-2xl font-semibold text-foreground mb-4 text-balance">
                    {flashcards[currentCard].front}
                  </p>
                  <p className="text-sm text-muted-foreground">Click to reveal answer</p>
                </div>
              </Card>

              <Card
                className={`absolute inset-0 p-8 flex flex-col justify-center items-center transition-all duration-500 transform-style-3d ${
                  isFlipped ? "rotate-y-0 opacity-100" : "rotate-y-180 opacity-0"
                }`}
              >
                <div className="mb-4">
                  <span className="px-2 py-1 bg-accent/10 text-accent text-xs font-medium rounded">Answer</span>
                </div>

                <div className="text-center">
                  <p className="text-lg text-foreground leading-relaxed text-balance">{flashcards[currentCard].back}</p>

                  {flashcards[currentCard].tags.length > 0 && (
                    <div className="flex flex-wrap gap-2 justify-center mt-6">
                      {flashcards[currentCard].tags.map((tag, index) => (
                        <span key={index} className="px-2 py-1 bg-muted text-muted-foreground text-xs rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </Card>
            </div>

            <div className="flex items-center justify-between gap-4">
              <Button onClick={prevCard} disabled={currentCard === 0} variant="outline" size="lg">
                <ChevronLeft className="w-5 h-5 mr-2" />
                Previous
              </Button>

              <Button onClick={() => setIsFlipped(!isFlipped)} variant="outline" size="icon">
                <RotateCw className="w-5 h-5" />
              </Button>

              <Button onClick={nextCard} disabled={currentCard === flashcards.length - 1} size="lg">
                Next
                <ChevronRight className="w-5 h-5 ml-2" />
              </Button>
            </div>

            <div className="w-full bg-muted rounded-full h-2">
              <div
                className="bg-success h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentCard + 1) / flashcards.length) * 100}%` }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
