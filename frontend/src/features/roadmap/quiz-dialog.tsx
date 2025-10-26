import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { Clock, Target, XCircle, Trophy } from "lucide-react";
import {
  useCreateQuizMutation,
  useCreateQuizAttemptMutation,
  useSubmitQuizAttemptMutation,
} from "./roadmap.query";
import type { IGoal, IQuiz, IQuizAttempt, IQuizAnswer } from "./roadmap.types";

interface QuizDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  sessionId: number;
  goal: IGoal;
}

type QuizStep = "setup" | "loading" | "quiz" | "submitting" | "results";

export default function QuizDialog({
  open,
  onOpenChange,
  sessionId,
  goal,
}: QuizDialogProps) {
  const [currentStep, setCurrentStep] = useState<QuizStep>("setup");
  const [quiz, setQuiz] = useState<IQuiz | null>(null);
  const [attempt, setAttempt] = useState<IQuizAttempt | null>(null);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [questionStartTime, setQuestionStartTime] = useState(Date.now());
  const [questionTimes, setQuestionTimes] = useState<Record<number, number>>({});

  const createQuizMutation = useCreateQuizMutation();
  const createAttemptMutation = useCreateQuizAttemptMutation();
  const submitAttemptMutation = useSubmitQuizAttemptMutation();

  // Timer effect
  useEffect(() => {
    if (currentStep === "quiz" && timeRemaining > 0) {
      const timer = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 1) {
            handleSubmitQuiz();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [currentStep]);

  // Reset state when dialog opens/closes
  useEffect(() => {
    if (!open) {
      setCurrentStep("setup");
      setQuiz(null);
      setAttempt(null);
      setAnswers({});
      setCurrentQuestionIndex(0);
      setTimeRemaining(0);
      setQuestionTimes({});
    }
  }, [open]);

  const handleStartQuiz = async () => {
    setCurrentStep("loading");
    
    try {
      // Create quiz with default settings
      const quizResult = await createQuizMutation.mutateAsync({
        sessionId,
        request: {
          goal_id: goal.id,
          time_limit_minutes: 15, // Default 15 minutes
          passing_score_percentage: 70, // Default 70%
          max_attempts: 3, // Default 3 attempts
        },
      });

      setQuiz(quizResult.data);

      // Create attempt
      const attemptResult = await createAttemptMutation.mutateAsync({
        sessionId,
        request: {
          quiz_id: quizResult.data.id,
        },
      });

      setAttempt(attemptResult.data);
      setTimeRemaining(quizResult.data.time_limit_minutes * 60); // Convert to seconds
      setQuestionStartTime(Date.now());
      setCurrentStep("quiz");
    } catch (error) {
      console.error("Failed to start quiz:", error);
      setCurrentStep("setup");
    }
  };

  const handleAnswerChange = (questionId: number, answer: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleNextQuestion = () => {
    if (!quiz) return;

    // Record time spent on current question
    const timeSpent = Math.floor((Date.now() - questionStartTime) / 1000);
    const currentQuestion = quiz.questions[currentQuestionIndex];
    setQuestionTimes(prev => ({ ...prev, [currentQuestion.id]: timeSpent }));

    if (currentQuestionIndex < quiz.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setQuestionStartTime(Date.now());
    } else {
      handleSubmitQuiz();
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
      setQuestionStartTime(Date.now());
    }
  };

  const handleSubmitQuiz = async () => {
    if (!quiz || !attempt) return;

    setCurrentStep("submitting");

    // Record time for last question
    const timeSpent = Math.floor((Date.now() - questionStartTime) / 1000);
    const currentQuestion = quiz.questions[currentQuestionIndex];
    const finalQuestionTimes = { ...questionTimes, [currentQuestion.id]: timeSpent };

    try {
      const quizAnswers: IQuizAnswer[] = quiz.questions.map(question => ({
        question_id: question.id,
        selected_answer: answers[question.id] || "",
        time_spent_seconds: finalQuestionTimes[question.id] || 0,
      }));

      const result = await submitAttemptMutation.mutateAsync({
        sessionId,
        request: {
          attempt_id: attempt.id,
          answers: quizAnswers,
        },
      });

      setAttempt(result.data);
      setCurrentStep("results");
    } catch (error) {
      console.error("Failed to submit quiz:", error);
      setCurrentStep("quiz");
    }
  };

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const currentQuestion = quiz?.questions[currentQuestionIndex];
  const progress = quiz ? ((currentQuestionIndex + 1) / quiz.questions.length) * 100 : 0;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Target className="h-5 w-5" />
            Quiz: {goal.title}
          </DialogTitle>
          <DialogDescription>
            Test your knowledge of this learning goal
          </DialogDescription>
        </DialogHeader>

        {currentStep === "setup" && (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Quiz Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <Label className="font-medium">Time Limit</Label>
                    <p className="text-muted-foreground">15 minutes</p>
                  </div>
                  <div>
                    <Label className="font-medium">Passing Score</Label>
                    <p className="text-muted-foreground">70%</p>
                  </div>
                  <div>
                    <Label className="font-medium">Questions</Label>
                    <p className="text-muted-foreground">~10 questions</p>
                  </div>
                  <div>
                    <Label className="font-medium">Attempts</Label>
                    <p className="text-muted-foreground">3 maximum</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="bg-muted/50 rounded-lg p-4">
              <h4 className="font-medium mb-2">About this goal:</h4>
              <p className="text-sm text-muted-foreground">{goal.description}</p>
            </div>
          </div>
        )}

        {currentStep === "loading" && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-muted-foreground">Generating quiz questions...</p>
            </div>
          </div>
        )}

        {currentStep === "quiz" && currentQuestion && quiz && (
          <div className="space-y-6">
            {/* Quiz Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <Badge variant="outline">
                  Question {currentQuestionIndex + 1} of {quiz.questions.length}
                </Badge>
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  {formatTime(timeRemaining)}
                </div>
              </div>
              <Progress value={progress} className="w-32" />
            </div>

            {/* Question */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">
                  {currentQuestion.question_text}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <RadioGroup
                  value={answers[currentQuestion.id] || ""}
                  onValueChange={(value: string) => handleAnswerChange(currentQuestion.id, value)}
                >
                  {currentQuestion.options.map((option, index) => {
                    const optionLetter = String.fromCharCode(65 + index); // A, B, C, D
                    return (
                      <div key={index} className="flex items-start space-x-3 p-3 rounded-lg border hover:bg-muted/50 cursor-pointer">
                        <RadioGroupItem value={optionLetter} id={`option-${currentQuestion.id}-${index}`} />
                        <Label htmlFor={`option-${currentQuestion.id}-${index}`} className="flex-1 cursor-pointer">
                          <span className="font-medium mr-2">{optionLetter}.</span>
                          {option}
                        </Label>
                      </div>
                    );
                  })}
                </RadioGroup>
              </CardContent>
            </Card>
          </div>
        )}

        {currentStep === "submitting" && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-muted-foreground">Submitting your answers...</p>
            </div>
          </div>
        )}

        {currentStep === "results" && attempt && quiz && (
          <div className="space-y-6">
            <div className="text-center py-6">
              <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 ${
                attempt.passed ? "bg-green-100" : "bg-red-100"
              }`}>
                {attempt.passed ? (
                  <Trophy className="h-8 w-8 text-green-600" />
                ) : (
                  <XCircle className="h-8 w-8 text-red-600" />
                )}
              </div>
              <h3 className="text-lg font-semibold mb-2">
                {attempt.passed ? "Quiz Passed!" : "Quiz Not Passed"}
              </h3>
              <div className="bg-muted/50 rounded-lg p-4 max-w-md mx-auto">
                <div className="text-2xl font-bold text-primary mb-1">
                  {attempt.score_percentage.toFixed(1)}%
                </div>
                <div className="text-sm text-muted-foreground">
                  {attempt.correct_answers} out of {attempt.total_questions} correct
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <Label className="font-medium">Time Spent</Label>
                <p className="text-muted-foreground">{attempt.time_spent_minutes} minutes</p>
              </div>
              <div>
                <Label className="font-medium">Passing Score</Label>
                <p className="text-muted-foreground">{quiz.passing_score_percentage}%</p>
              </div>
              <div>
                <Label className="font-medium">Attempt</Label>
                <p className="text-muted-foreground">{attempt.attempt_number} of {quiz.max_attempts}</p>
              </div>
              <div>
                <Label className="font-medium">Status</Label>
                <p className={attempt.passed ? "text-green-600" : "text-red-600"}>
                  {attempt.passed ? "Passed" : "Failed"}
                </p>
              </div>
            </div>
          </div>
        )}

        <DialogFooter>
          {currentStep === "setup" && (
            <>
              <Button variant="outline" onClick={() => onOpenChange(false)}>
                Cancel
              </Button>
              <Button onClick={handleStartQuiz} disabled={createQuizMutation.isPending}>
                Start Quiz
              </Button>
            </>
          )}
          
          {currentStep === "quiz" && (
            <div className="flex justify-between w-full">
              <Button
                variant="outline"
                onClick={handlePreviousQuestion}
                disabled={currentQuestionIndex === 0}
              >
                Previous
              </Button>
              <Button
                onClick={handleNextQuestion}
                disabled={!currentQuestion || !answers[currentQuestion.id]}
              >
                {currentQuestionIndex === (quiz?.questions.length || 0) - 1 ? "Submit Quiz" : "Next"}
              </Button>
            </div>
          )}

          {currentStep === "results" && (
            <Button onClick={() => onOpenChange(false)}>
              Close
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}