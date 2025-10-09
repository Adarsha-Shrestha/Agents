"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Brain, ArrowLeft, Loader2, CheckCircle2, XCircle, Trophy, Camera, Shield } from "lucide-react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface QuizQuestion {
  question: string
  options: string[]
  correct_answer: string
  explanation: string
  difficulty: string
}

type QuizState = "setup" | "taking" | "results"

export default function QuizPage() {
  const [state, setState] = useState<QuizState>("setup")
  const [topic, setTopic] = useState("")
  const [subject, setSubject] = useState("")
  const [numQuestions, setNumQuestions] = useState("5")
  const [isLoading, setIsLoading] = useState(false)

  const [quizId, setQuizId] = useState("")
  const [questions, setQuestions] = useState<QuizQuestion[]>([])
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState("")
  const [answers, setAnswers] = useState<Array<{ correct: boolean; explanation: string }>>([])

  const [score, setScore] = useState(0)

  const generateQuiz = async () => {
    if (!topic.trim()) return

    setIsLoading(true)
    try {
      const response = await fetch("http://localhost:8000/api/quiz/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic,
          subject: subject || undefined,
          num_questions: Number.parseInt(numQuestions),
        }),
      })

      const data = await response.json()

      if (data.success) {
        setQuizId(data.quiz_id)
        setQuestions(data.quiz_data)
        setState("taking")
        setCurrentQuestion(0)
        setAnswers([])
        setScore(0)
      }
    } catch (error) {
      console.error("[v0] Error generating quiz:", error)
      alert("Failed to generate quiz. Make sure the backend is running.")
    } finally {
      setIsLoading(false)
    }
  }

  const submitAnswer = () => {
    if (!selectedAnswer) return

    const current = questions[currentQuestion]
    const isCorrect = selectedAnswer === current.correct_answer

    setAnswers([...answers, { correct: isCorrect, explanation: current.explanation }])

    if (isCorrect) {
      setScore(score + 1)
    }

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
      setSelectedAnswer("")
    } else {
      setState("results")
    }
  }

  const resetQuiz = () => {
    setState("setup")
    setTopic("")
    setQuestions([])
    setCurrentQuestion(0)
    setSelectedAnswer("")
    setAnswers([])
    setScore(0)
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
              <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-accent-foreground" />
              </div>
              <span className="text-xl font-bold text-foreground">Quiz Generator</span>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-3xl">
        {state === "setup" && (
          <>
            <Alert className="mb-6 border-destructive/50 bg-destructive/5">
              <Shield className="w-4 h-4 text-destructive" />
              <AlertDescription className="text-foreground">
                <div className="flex items-center justify-between">
                  <span>Need a proctored exam with AI monitoring?</span>
                  <Button asChild variant="destructive" size="sm" className="ml-4">
                    <Link href="/quiz/proctored">
                      <Camera className="w-4 h-4 mr-2" />
                      Start Proctored Quiz
                    </Link>
                  </Button>
                </div>
              </AlertDescription>
            </Alert>

            <Card className="p-8">
              <h2 className="text-2xl font-bold text-foreground mb-6">Create Your Quiz</h2>

              <div className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="topic">Topic</Label>
                  <Input
                    id="topic"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="e.g., Decision Trees, TCP/IP, MapReduce"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="subject">Subject (Optional)</Label>
                  <Select value={subject} onValueChange={setSubject}>
                    <SelectTrigger id="subject">
                      <SelectValue placeholder="All Subjects" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Subjects</SelectItem>
                      <SelectItem value="DataMining">Data Mining</SelectItem>
                      <SelectItem value="Network">Network Systems</SelectItem>
                      <SelectItem value="Distributed">Distributed Computing</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="numQuestions">Number of Questions</Label>
                  <Select value={numQuestions} onValueChange={setNumQuestions}>
                    <SelectTrigger id="numQuestions">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="3">3 Questions</SelectItem>
                      <SelectItem value="5">5 Questions</SelectItem>
                      <SelectItem value="10">10 Questions</SelectItem>
                      <SelectItem value="15">15 Questions</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <Button onClick={generateQuiz} disabled={isLoading || !topic.trim()} className="w-full" size="lg">
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Generating Quiz...
                    </>
                  ) : (
                    "Generate Quiz"
                  )}
                </Button>
              </div>
            </Card>
          </>
        )}

        {state === "taking" && questions.length > 0 && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="text-sm text-muted-foreground">
                Question {currentQuestion + 1} of {questions.length}
              </div>
              <div className="text-sm font-medium text-foreground">
                Score: {score}/{currentQuestion}
              </div>
            </div>

            <Card className="p-8">
              <div className="mb-2">
                <span className="inline-block px-2 py-1 bg-accent/10 text-accent text-xs font-medium rounded">
                  {questions[currentQuestion].difficulty}
                </span>
              </div>

              <h3 className="text-xl font-semibold text-foreground mb-6 leading-relaxed">
                {questions[currentQuestion].question}
              </h3>

              <RadioGroup value={selectedAnswer} onValueChange={setSelectedAnswer}>
                <div className="space-y-3">
                  {questions[currentQuestion].options.map((option, index) => (
                    <div
                      key={index}
                      className="flex items-center space-x-3 p-4 rounded-lg border border-border hover:bg-muted/50 transition-colors"
                    >
                      <RadioGroupItem value={String.fromCharCode(65 + index)} id={`option-${index}`} />
                      <Label htmlFor={`option-${index}`} className="flex-1 cursor-pointer">
                        <span className="font-medium mr-2">{String.fromCharCode(65 + index)}.</span>
                        {option}
                      </Label>
                    </div>
                  ))}
                </div>
              </RadioGroup>

              <Button onClick={submitAnswer} disabled={!selectedAnswer} className="w-full mt-6" size="lg">
                {currentQuestion < questions.length - 1 ? "Next Question" : "Finish Quiz"}
              </Button>
            </Card>
          </div>
        )}

        {state === "results" && (
          <div className="space-y-6">
            <Card className="p-8 text-center">
              <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Trophy className="w-10 h-10 text-primary" />
              </div>

              <h2 className="text-3xl font-bold text-foreground mb-2">Quiz Complete!</h2>

              <div className="text-5xl font-bold text-primary my-6">
                {score}/{questions.length}
              </div>

              <p className="text-lg text-muted-foreground mb-6">
                {score / questions.length >= 0.9
                  ? "Excellent! Outstanding knowledge!"
                  : score / questions.length >= 0.7
                    ? "Great job! Very good understanding!"
                    : score / questions.length >= 0.5
                      ? "Good work! Keep studying!"
                      : "Keep practicing! You'll improve!"}
              </p>

              <div className="flex gap-3">
                <Button onClick={resetQuiz} variant="outline" className="flex-1 bg-transparent">
                  Create New Quiz
                </Button>
                <Button onClick={() => setState("setup")} className="flex-1">
                  Try Again
                </Button>
              </div>
            </Card>

            <Card className="p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Review</h3>
              <div className="space-y-3">
                {answers.map((answer, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-muted/50">
                    {answer.correct ? (
                      <CheckCircle2 className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
                    ) : (
                      <XCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
                    )}
                    <div className="flex-1">
                      <div className="text-sm font-medium text-foreground mb-1">Question {index + 1}</div>
                      <p className="text-sm text-muted-foreground">{answer.explanation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}
