import SessionsSidebar from "./sessions-sidebar";
import SessionDetail from "./session-detail";
import { useParams } from "react-router-dom";
import ChatPane from "./chat-pane";

export default function RoadmapPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const sessionIdNum = sessionId ? parseInt(sessionId, 10) : 0;
  return (
    <div className="page-transition flex h-full w-full py-4 px-4">
      <SessionsSidebar />
      <SessionDetail />
      {sessionIdNum > 1 && (
        <ChatPane key={sessionIdNum} sessionId={sessionIdNum} />
      )}
    </div>
  );
}
