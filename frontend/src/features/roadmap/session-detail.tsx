import { useParams } from "react-router-dom";
import { useSessionQuery } from "./roadmap.query";

export default function SessionDetail() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const sessionIdNum = sessionId ? parseInt(sessionId, 10) : 0;
  
  const { data: session, isLoading, error } = useSessionQuery(sessionIdNum);

  if (!sessionId) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-semibold mb-2">Welcome to Roadmaps</h2>
          <p className="text-muted-foreground">
            Select a learning session from the sidebar to get started
          </p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-muted-foreground">Loading session...</div>
      </div>
    );
  }

  if (error || !session) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2 text-red-500">
            Session Not Found
          </h2>
          <p className="text-muted-foreground">
            The requested session could not be loaded
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2">{session.session_name}</h1>
          <p className="text-muted-foreground text-lg">{session.description}</p>
        </div>
        
        <div className="bg-card rounded-lg p-6 border">
          <div className="flex items-center gap-4 mb-4">
            <div className="flex items-center gap-2">
              <div
                className={`w-3 h-3 rounded-full ${
                  session.status === "completed"
                    ? "bg-green-500"
                    : session.status === "active"
                    ? "bg-blue-500"
                    : "bg-gray-400"
                }`}
              />
              <span className="text-sm font-medium capitalize">{session.status}</span>
            </div>
            <div className="text-sm text-muted-foreground">
              Created: {new Date(session.created_at).toLocaleDateString()}
            </div>
            {session.completed_at && (
              <div className="text-sm text-muted-foreground">
                Completed: {new Date(session.completed_at).toLocaleDateString()}
              </div>
            )}
          </div>
          
          <div className="text-center py-12 text-muted-foreground">
            Session content will be loaded here...
          </div>
        </div>
      </div>
    </div>
  );
}