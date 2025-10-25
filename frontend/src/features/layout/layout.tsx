import { Outlet } from "react-router-dom";
import Nav from "./nav";

export default function Layout() {
  return (
    <div className="absolute w-full h-full left-0 right-0 top-0 bottom-0 flex flex-col items-center">
      <Nav />
      <div className="w-full max-w-300 overflow-x-hidden h-full">
        <Outlet />
      </div>
    </div>
  );
}
