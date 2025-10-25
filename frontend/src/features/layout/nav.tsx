import { Link } from "react-router-dom";
import { useAuth } from "../auth/auth.query";
import type { ReactNode } from "react";
import Logo from "@/components/logo";
import { useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

export default function Nav() {
  const user = useAuth().data;
  return (
    <nav className="bg-card border-b  items-center w-full h-fit px-8 py-3 shrink-0 flex gap-2">
      <Logo className="text-2xl" />
      <div className="w-5"></div>
      <NavLink to="/roadmaps">Roadmaps</NavLink>
      <NavLink to="/jobs">Jobs</NavLink>
      <NavLink to="/profile">Profile</NavLink>
    </nav>
  );
}

function NavLink(props: { to: string; children: ReactNode }) {
  const loc = useLocation();
  const active = loc.pathname.startsWith(props.to);
  return (
    <Link
      to={props.to}
      className={cn(
        "py-3 px-4 hover:bg-primary/10 rounded-lg cursor-pointer transition-colors duration-75",
        active && "text-primary",
      )}
    >
      {props.children}
    </Link>
  );
}
