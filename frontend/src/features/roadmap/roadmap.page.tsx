import SessionsSidebar from "./sessions-sidebar";
import SessionDetail from "./session-detail";

export default function RoadmapPage() {
  return (
    <div className="page-transition flex h-full w-full py-4 px-4">
      <SessionsSidebar />
      <SessionDetail />
    </div>
  );
}
