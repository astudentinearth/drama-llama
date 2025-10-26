import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getSessions, Session, createSession } from "./roadmap.api";

export function useSessionsQuery() {
  return useQuery({
    queryKey: ["roadmap", "sessions"],
    queryFn: getSessions,
  });
}

export function useSessionQuery(sessionId: number) {
  return useQuery({
    queryKey: ["roadmap", "session", sessionId],
    queryFn: () => Session(sessionId).get(),
    enabled: !!sessionId,
  });
}

export function useFullSessionQuery(sessionId: number) {
  return useQuery({
    queryKey: ["roadmap", "session", sessionId, "full"],
    queryFn: () => Session(sessionId).getFull(),
    enabled: !!sessionId,
  });
}

export function useSessionMessagesQuery(sessionId: number) {
  return useQuery({
    queryKey: ["roadmap", "session", sessionId, "messages"],
    queryFn: () => Session(sessionId).getMessages(),
    enabled: !!sessionId,
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
  });
}

export function useCreateSessionMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ sessionName, description }: { sessionName: string; description: string }) =>
      createSession(sessionName, description),
    onSuccess: () => {
      // Invalidate and refetch sessions list
      queryClient.invalidateQueries({ queryKey: ["roadmap", "sessions"] });
    },
  });
}

// Graduation Project Query Hooks
export function useGraduationQuestionsQuery(sessionId: number) {
  return useQuery({
    queryKey: ["roadmap", "graduation-project", sessionId, "questions"],
    queryFn: () => Session(sessionId).getGraduationQuestions(),
    enabled: !!sessionId,
    retry: false, // Don't retry if questions don't exist yet
    throwOnError: false, // Don't throw errors, handle them gracefully
  });
}

export function useGenerateGraduationQuestionsMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (sessionId: number) => Session(sessionId).generateGraduationQuestions(),
    onSuccess: (_, sessionId) => {
      // Invalidate and refetch graduation questions for this session
      queryClient.invalidateQueries({ 
        queryKey: ["roadmap", "graduation-project", sessionId, "questions"] 
      });
    },
  });
}

export function useSubmitGraduationAnswersMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ sessionId, answers }: { sessionId: number; answers: Array<{ question_id: string; text: string }> }) =>
      Session(sessionId).submitGraduationAnswers(answers),
    onSuccess: (_, { sessionId }) => {
      // Optionally invalidate related queries after submission
      queryClient.invalidateQueries({ 
        queryKey: ["roadmap", "graduation-project", sessionId] 
      });
    },
  });
}

// Quiz Query Hooks
export function useCreateQuizMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ sessionId, request }: { sessionId: number; request: { goal_id: number; time_limit_minutes: number; passing_score_percentage: number; max_attempts: number } }) =>
      Session(sessionId).createQuiz(request),
    onSuccess: (_, { sessionId }) => {
      // Invalidate related queries after quiz creation
      queryClient.invalidateQueries({ 
        queryKey: ["roadmap", "session", sessionId] 
      });
    },
  });
}

export function useCreateQuizAttemptMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ sessionId, request }: { sessionId: number; request: { quiz_id: number } }) =>
      Session(sessionId).createQuizAttempt(request),
    onSuccess: (_, { sessionId }) => {
      // Invalidate quiz attempts after creating new attempt
      queryClient.invalidateQueries({ 
        queryKey: ["roadmap", "quiz-attempts", sessionId] 
      });
    },
  });
}

export function useSubmitQuizAttemptMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ sessionId, request }: { sessionId: number; request: { attempt_id: number; answers: Array<{ question_id: number; selected_answer: string; time_spent_seconds: number }> } }) =>
      Session(sessionId).submitQuizAttempt(request),
    onSuccess: (_, { sessionId }) => {
      // Invalidate quiz attempts and session data after submission
      queryClient.invalidateQueries({ 
        queryKey: ["roadmap", "quiz-attempts", sessionId] 
      });
      queryClient.invalidateQueries({ 
        queryKey: ["roadmap", "session", sessionId] 
      });
    },
  });
}