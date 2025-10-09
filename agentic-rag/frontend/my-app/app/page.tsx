import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { MessageSquare, Brain, BookOpen, Sparkles, ArrowRight } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold text-foreground">EduRAG</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/chat" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Chat
            </Link>
            <Link href="/quiz" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Quiz
            </Link>
            <Link href="/flashcards" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Flashcards
            </Link>
          </nav>
          <Button asChild>
            <Link href="/chat">Get Started</Link>
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:py-32">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block mb-4 px-3 py-1 bg-primary/10 text-primary text-sm font-medium rounded-full">
            AI-Powered Learning
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 text-balance">
            Master Your Studies with <span className="text-primary">Intelligent Learning</span>
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground mb-8 text-pretty leading-relaxed">
            Leverage advanced RAG technology to chat with your course materials, generate personalized quizzes, and
            create smart flashcards for effective learning.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild className="text-base">
              <Link href="/chat">
                Start Learning <ArrowRight className="ml-2 w-4 h-4" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild className="text-base bg-transparent">
              <Link href="/quiz">Explore Features</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">Three Powerful Learning Tools</h2>
            <p className="text-lg text-muted-foreground">Everything you need to excel in your studies</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {/* Chat Feature */}
            <Card className="p-6 bg-card border-border hover:border-primary/50 transition-colors">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <MessageSquare className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-2">AI Chat Assistant</h3>
              <p className="text-muted-foreground mb-4 leading-relaxed">
                Ask questions and get instant answers from your course materials using advanced retrieval-augmented
                generation.
              </p>
              <Button variant="ghost" asChild className="w-full justify-start px-0">
                <Link href="/chat">
                  Try Chat <ArrowRight className="ml-2 w-4 h-4" />
                </Link>
              </Button>
            </Card>

            {/* Quiz Feature */}
            <Card className="p-6 bg-card border-border hover:border-primary/50 transition-colors">
              <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
                <Brain className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-2">Smart Quiz Generator</h3>
              <p className="text-muted-foreground mb-4 leading-relaxed">
                Generate custom quizzes on any topic with multiple difficulty levels and instant feedback on your
                answers.
              </p>
              <Button variant="ghost" asChild className="w-full justify-start px-0">
                <Link href="/quiz">
                  Create Quiz <ArrowRight className="ml-2 w-4 h-4" />
                </Link>
              </Button>
            </Card>

            {/* Flashcard Feature */}
            <Card className="p-6 bg-card border-border hover:border-primary/50 transition-colors">
              <div className="w-12 h-12 bg-success/10 rounded-lg flex items-center justify-center mb-4">
                <BookOpen className="w-6 h-6 text-success" />
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-2">Flashcard Studio</h3>
              <p className="text-muted-foreground mb-4 leading-relaxed">
                Create intelligent flashcards automatically and study with spaced repetition for better retention.
              </p>
              <Button variant="ghost" asChild className="w-full justify-start px-0">
                <Link href="/flashcards">
                  Make Flashcards <ArrowRight className="ml-2 w-4 h-4" />
                </Link>
              </Button>
            </Card>
          </div>
        </div>
      </section>

      {/* Subjects Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto">
          <Card className="p-8 md:p-12 bg-card border-border text-center">
            <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-4">Specialized for Your Courses</h2>
            <p className="text-muted-foreground mb-6 leading-relaxed">
              Currently supporting Data Mining, Network Systems, and Distributed Computing
            </p>
            <div className="flex flex-wrap justify-center gap-3">
              <div className="px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-medium">Data Mining</div>
              <div className="px-4 py-2 bg-accent/10 text-accent rounded-full text-sm font-medium">Network Systems</div>
              <div className="px-4 py-2 bg-success/10 text-success rounded-full text-sm font-medium">
                Distributed Computing
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border mt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-primary rounded flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="text-sm text-muted-foreground">© 2025 EduRAG. Powered by AI.</span>
            </div>
            <div className="flex gap-6">
              <Link href="/chat" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Chat
              </Link>
              <Link href="/quiz" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Quiz
              </Link>
              <Link
                href="/flashcards"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                Flashcards
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
