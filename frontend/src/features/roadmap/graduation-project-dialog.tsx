import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Clock, Target, BookOpen } from "lucide-react";
import {
  useGraduationQuestionsQuery,
  useGenerateGraduationQuestionsMutation,
  useSubmitGraduationAnswersMutation,
} from "./roadmap.query";
import type { IAnswer, IQuestion, IEvaluation, SubmitAnswersResponse } from "./roadmap.types";

interface GraduationProjectDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  sessionId: number;
}

export default function GraduationProjectDialog({
  open,
  onOpenChange,
  sessionId,
}: GraduationProjectDialogProps) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [currentStep, setCurrentStep] = useState<"loading" | "questions" | "submitting" | "success">("loading");
  const [hasTriedGeneration, setHasTriedGeneration] = useState(false);
  const [submissionResult, setSubmissionResult] = useState<SubmitAnswersResponse | null>(null);

  const { data: questionsData, isLoading: questionsLoading, refetch } = useGraduationQuestionsQuery(sessionId);
  const generateQuestionsMutation = useGenerateGraduationQuestionsMutation();
  const submitAnswersMutation = useSubmitGraduationAnswersMutation();

  const questions = questionsData?.data?.questions || [];
  const graduationProject = questionsData?.data?.graduation_project;



  // Generate questions if not available
  const handleGenerateQuestions = async () => {
    try {
      setHasTriedGeneration(true);
      await generateQuestionsMutation.mutateAsync(sessionId);
      // After generation, refetch the questions
      await refetch();
      setCurrentStep("questions");
    } catch (error) {
      console.error("Failed to generate questions:", error);
      setCurrentStep("loading");
    }
  };

  // Handle answer changes
  const handleAnswerChange = (questionId: string, value: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  // Submit all answers
  const handleSubmit = async () => {
    setCurrentStep("submitting");
    
    const answersArray: IAnswer[] = questions.map(q => ({
      question_id: q.question_id,
      text: answers[q.question_id] || "",
    }));

    try {
      const result = await submitAnswersMutation.mutateAsync({
        sessionId,
        answers: answersArray,
      });
      setSubmissionResult(result);
      setCurrentStep("success");
    } catch (error) {
      console.error("Failed to submit answers:", error);
      setCurrentStep("questions");
    }
  };

  // Check if we need to generate questions
  const needsGeneration = !questionsLoading && questions.length === 0 && !hasTriedGeneration;

  // Auto-generate questions when dialog opens
  if (open && needsGeneration && currentStep === "loading" && !generateQuestionsMutation.isPending) {
    handleGenerateQuestions();
  }

  // Set step to questions when questions are loaded
  if (questions.length > 0 && currentStep === "loading") {
    setCurrentStep("questions");
  }

  // Reset state when dialog closes
  if (!open && hasTriedGeneration) {
    setHasTriedGeneration(false);
    setCurrentStep("loading");
    setAnswers({});
    setSubmissionResult(null);
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "beginner": return "bg-green-100 text-green-800";
      case "intermediate": return "bg-yellow-100 text-yellow-800";
      case "advanced": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const isAnswerValid = (question: IQuestion) => {
    const answer = answers[question.question_id] || "";
    return answer.length >= question.answer_min_chars && answer.length <= question.answer_max_chars;
  };



  const allAnswersValid = questions.every(isAnswerValid);

  // Calculate average score from submission result
  const calculateAverageScore = () => {
    if (!submissionResult?.data?.evaluations) return 0;
    
    const evaluations = submissionResult.data.evaluations;
    const validEvaluations = evaluations.filter((evaluation: IEvaluation) => evaluation.error === null);
    
    if (validEvaluations.length === 0) return 0;
    
    const totalScore = validEvaluations.reduce((sum: number, evaluation: IEvaluation) => sum + evaluation.score, 0);
    return (totalScore / validEvaluations.length) * 100; // Convert to percentage
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Graduation Project Assessment</DialogTitle>
          <DialogDescription>
            Complete your learning journey by answering questions about your graduation project.
          </DialogDescription>
        </DialogHeader>

        {currentStep === "loading" && (
          <div className="flex items-center justify-center py-8">
            <div className="text-center">
              {!generateQuestionsMutation.isError && (
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
              )}
              <p className="text-muted-foreground">
                {generateQuestionsMutation.isPending ? "Generating questions..." : "Loading questions..."}
              </p>
              {generateQuestionsMutation.isError && (
                <div className="mt-4">
                  <p className="text-red-500 text-sm mb-3">
                    Failed to generate questions. Please try again.
                  </p>
                  <Button 
                    onClick={() => {
                      setHasTriedGeneration(false);
                      handleGenerateQuestions();
                    }}
                    disabled={generateQuestionsMutation.isPending}
                  >
                    Retry Generation
                  </Button>
                </div>
              )}
            </div>
          </div>
        )}

        {currentStep === "questions" && graduationProject && (
          <div className="space-y-6">
            {/* Project Overview */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5" />
                  {graduationProject.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">{graduationProject.description}</p>
              </CardContent>
            </Card>

            {/* Questions */}
            <div className="space-y-6">
              {questions.map((question, index) => (
                <Card key={question.question_id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <CardTitle className="text-lg">
                        Question {index + 1}
                      </CardTitle>
                      <div className="flex items-center gap-2">
                        <Badge className={getDifficultyColor(question.difficulty)}>
                          {question.difficulty}
                        </Badge>
                        <Badge variant="outline" className="flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {question.estimated_time_minutes}m
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm">{question.prompt}</p>
                    
                    {question.expected_competencies.length > 0 && (
                      <div>
                        <Label className="text-xs text-muted-foreground flex items-center gap-1">
                          <BookOpen className="h-3 w-3" />
                          Expected Competencies
                        </Label>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {question.expected_competencies.map((comp, i) => (
                            <Badge key={i} variant="secondary" className="text-xs">
                              {comp}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="space-y-2">
                      <Label htmlFor={`answer-${question.question_id}`}>
                        Your Answer ({question.answer_min_chars}-{question.answer_max_chars} characters)
                      </Label>
                      <Textarea
                        id={`answer-${question.question_id}`}
                        placeholder="Type your answer here..."
                        value={answers[question.question_id] || ""}
                        onChange={(e) => handleAnswerChange(question.question_id, e.target.value)}
                        className="min-h-[120px]"
                      />
                      <div className="flex justify-between text-xs text-muted-foreground">
                        <span>
                          {(answers[question.question_id] || "").length} / {question.answer_max_chars} characters
                        </span>
                        <span className={isAnswerValid(question) ? "text-green-600" : "text-red-600"}>
                          {isAnswerValid(question) ? "✓ Valid length" : "✗ Invalid length"}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {currentStep === "submitting" && (
          <div className="flex items-center justify-center py-8">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-muted-foreground">Submitting your answers...</p>
            </div>
          </div>
        )}

        {currentStep === "success" && (
          <div className="space-y-6">
            <div className="text-center py-6">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Target className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Assessment Complete!</h3>
              <p className="text-muted-foreground mb-4">
                Your graduation project assessment has been submitted successfully.
              </p>
              
              {submissionResult && (
                <div className="bg-muted/50 rounded-lg p-4 max-w-md mx-auto">
                  <div className="text-2xl font-bold text-primary mb-1">
                    {calculateAverageScore().toFixed(1)}%
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Average Score
                  </div>
                </div>
              )}
            </div>

            {submissionResult?.data?.evaluations && (
              <div className="space-y-4">
                <h4 className="font-semibold">Question Results:</h4>
                <div className="space-y-3">
                  {submissionResult.data.evaluations.map((evaluation: IEvaluation, index: number) => (
                    <Card key={evaluation.submission_id} className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">Question {index + 1}</span>
                        <Badge 
                          variant={evaluation.score >= 0.7 ? "default" : evaluation.score >= 0.4 ? "secondary" : "destructive"}
                        >
                          {(evaluation.score * 100).toFixed(1)}%
                        </Badge>
                      </div>
                      {evaluation.feedback && (
                        <p className="text-sm text-muted-foreground">
                          {evaluation.feedback}
                        </p>
                      )}
                      {evaluation.error && (
                        <p className="text-sm text-red-500">
                          Error: {evaluation.error}
                        </p>
                      )}
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        <DialogFooter>
          {currentStep === "questions" && (
            <>
              <Button variant="outline" onClick={() => onOpenChange(false)}>
                Cancel
              </Button>
              <Button 
                onClick={handleSubmit}
                disabled={!allAnswersValid || submitAnswersMutation.isPending}
              >
                Submit Assessment
              </Button>
            </>
          )}
          {currentStep === "success" && (
            <Button onClick={() => onOpenChange(false)}>
              Close
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}