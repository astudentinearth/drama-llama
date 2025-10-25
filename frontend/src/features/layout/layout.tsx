import { Outlet } from "react-router-dom";
import Nav from "./nav";

export default function Layout() {
  return (
    <div className="absolute w-full h-full flex flex-col items-center">
      <Nav />
        <div className="h-full w-full max-w-300 overflow-x-hidden overflow-y-auto">
          <Outlet />
        </div>
    </div>
  );
}
