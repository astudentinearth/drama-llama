import { Link, useParams } from "react-router-dom";
import { useSessionsQuery } from "./roadmap.query";
import CreateSessionDialog from "./create-session-dialog";
import { BookOpen } from "lucide-react";

export default function SessionsSidebar() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const { data: sessions, isLoading, error } = useSessionsQuery();

  if (isLoading) {
    return (
      <div className="w-64 border bg-card p-4">
        <div className="flex items-center gap-2 mb-4">
          <BookOpen className="w-5 h-5" />
          <h2 className="font-semibold">Learning Sessions</h2>
        </div>
        <div className="space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-12 bg-muted animate-pulse rounded-md" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="w-64 border rounded-2xl drop-shadow-sm bg-card p-4">
        <div className="flex items-center gap-2 mb-4">
          <BookOpen className="w-5 h-5" />
          <h2 className="font-semibold">Learning Sessions</h2>
        </div>
        <div className="text-sm text-red-500">
          Failed to load sessions
        </div>
      </div>
    );
  }

  return (
    <div className="w-64 border rounded-2xl drop-shadow-sm drop-shadow-black/5 bg-card p-2">
      <div className="flex items-center justify-between mb-4 px-2 pt-2">
        <div className="flex items-center gap-2">
          <BookOpen className="w-5 h-5" />
          <h2 className="font-semibold">Learning Sessions</h2>
        </div>
        <CreateSessionDialog variant="icon" size="icon-sm" />
      </div>

      <div className="space-y-1">
        {sessions?.map((session) => (
          <Link
            key={session.id}
            to={`/roadmaps/${session.id}`}
            className={`block p-3 rounded-lg border text-sm transition-colors hover:bg-secondary/50 hover:border-primary ${
              sessionId === session.id.toString()
                ? "bg-secondary border-primary text-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <div className="font-medium truncate">{session.session_name}</div>
            <div className="flex items-center gap-2 mt-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  session.status === "completed"
                    ? "bg-green-500"
                    : session.status === "active"
                    ? "bg-blue-500"
                    : "bg-gray-400"
                }`}
              />
              <span className="text-xs capitalize">{session.status}</span>
            </div>
          </Link>
        ))}
      </div>

      {sessions?.length === 0 && (
        <div className="text-center py-8">
          <div className="text-muted-foreground text-sm mb-2">
            No learning sessions yet
          </div>
          <CreateSessionDialog size="sm" />
        </div>
      )}
    </div>
  );
}