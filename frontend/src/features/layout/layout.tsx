import { Outlet } from "react-router-dom";
import Nav from "./nav";

export default function Layout() {
  return (
    <div className="absolute w-full h-full flex flex-col">
      <Nav />
      <div className="flex">
        <div className="w-120">Sidebar</div>
        <div className="h-full w-full overflow-x-hidden overflow-y-auto">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
