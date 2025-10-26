import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import MaterialsDialog from "./materials-dialog";
import QuizDialog from "./quiz-dialog";
import { Target, Clock, CheckCircle, Circle, Brain } from "lucide-react";
import type { IGoal } from "./roadmap.types";

interface GoalsDisplayProps {
  goals: IGoal[];
  sessionId: number;
}

export default function GoalsDisplay({ goals, sessionId }: GoalsDisplayProps) {
  const [selectedGoal, setSelectedGoal] = useState<IGoal | null>(null);
  const [quizDialogOpen, setQuizDialogOpen] = useState(false);

  const handleStartQuiz = (goal: IGoal) => {
    setSelectedGoal(goal);
    setQuizDialogOpen(true);
  };
  const getSkillLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case "beginner":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300";
      case "intermediate":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300";
      case "advanced":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300";
    }
  };

  const getPriorityColor = (priority: number) => {
    if (priority <= 2)
      return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300";
    if (priority <= 4)
      return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300";
    return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300";
  };

  const getPriorityLabel = (priority: number) => {
    if (priority <= 2) return "High";
    if (priority <= 4) return "Medium";
    return "Low";
  };

  if (goals.length === 0) {
    return (
      <div className="text-center py-12">
        <Target className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
        <h3 className="text-lg font-semibold mb-2">No Goals Yet</h3>
        <p className="text-muted-foreground">
          Goals will appear here once your learning roadmap is generated.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-4">
        <Target className="w-5 h-5" />
        <h3 className="text-xl font-semibold">Learning Goals</h3>
        <Badge variant="secondary">{goals.length} goals</Badge>
      </div>

      <div className="grid gap-4">
        {goals
          .sort((a, b) => a.goal_number - b.goal_number)
          .map((goal) => (
            <div key={goal.id} className="border rounded-lg p-6 bg-card">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Badge variant="outline" className="text-xs">
                      Goal {goal.goal_number}
                    </Badge>
                    <Badge
                      className={`text-xs ${getSkillLevelColor(
                        goal.skill_level
                      )}`}
                    >
                      {goal.skill_level}
                    </Badge>
                    <Badge
                      className={`text-xs ${getPriorityColor(goal.priority)}`}
                    >
                      {getPriorityLabel(goal.priority)} Priority
                    </Badge>
                  </div>
                  <h4 className="text-lg font-semibold mb-2">{goal.title}</h4>
                  <p className="text-muted-foreground text-sm mb-4">
                    {goal.description}
                  </p>
                </div>

                <div className="flex items-center ml-4">
                  {goal.completion_percentage >= 100 ? (
                    <CheckCircle className="w-6 h-6 text-green-500" />
                  ) : (
                    <Circle className="w-6 h-6 text-gray-400" />
                  )}
                </div>
              </div>

              {/* Progress */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Progress</span>
                  <span className="text-sm text-muted-foreground">
                    {Math.round(goal.completion_percentage)}%
                  </span>
                </div>
                <Progress value={goal.completion_percentage} className="h-2" />
              </div>

              {/* Time tracking */}
              <div className="flex items-center gap-4 mb-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  <span>Estimated: {goal.estimated_hours}h</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  <span>Spent: {goal.actual_hours_spent}h</span>
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  {/* Materials */}
                  {goal.materials && goal.materials.length > 0 && (
                    <div className="text-sm text-muted-foreground">
                      {goal.materials.length} learning material
                      {goal.materials.length !== 1 ? "s" : ""}
                      {goal.materials.filter((m) => m.is_completed).length >
                        0 && (
                        <span className="ml-2">
                          ({goal.materials.filter((m) => m.is_completed).length}{" "}
                          completed)
                        </span>
                      )}
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {goal.materials && goal.materials.length > 0 && (
                    <MaterialsDialog
                      materials={goal.materials}
                      goalTitle={goal.title}
                    />
                  )}
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleStartQuiz(goal)}
                    className="flex items-center gap-2"
                  >
                    <Brain className="h-4 w-4" />
                    Take Quiz
                  </Button>
                </div>
              </div>
            </div>
          ))}
      </div>

      {selectedGoal && (
        <QuizDialog
          open={quizDialogOpen && !!selectedGoal}
          onOpenChange={(open) => {
            setQuizDialogOpen(open);
            if (!open) {
              setSelectedGoal(null);
            }
          }}
          sessionId={sessionId}
          goal={selectedGoal!}
        />
      )}
    </div>
  );
}
