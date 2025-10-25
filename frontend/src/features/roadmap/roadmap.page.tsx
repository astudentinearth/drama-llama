import SessionsSidebar from "./sessions-sidebar";
import SessionDetail from "./session-detail";

export default function RoadmapPage() {
  return (
    <div className="page-transition flex h-full">
      <SessionsSidebar />
      <SessionDetail />
    </div>
  );
}
