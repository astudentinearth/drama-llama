import { Link } from "react-router-dom";
import { useAuth } from "../auth/auth.query";
import { useLogoutMutation } from "../auth/auth.mutation";
import type { ReactNode } from "react";
import Logo from "@/components/logo";
import { useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { useMyCompanyQuery } from "../company/company.query";
import { UserRound } from "lucide-react";

export default function Nav() {
  const user = useAuth().data;
  const logoutMutation = useLogoutMutation();
  const myCompany = useMyCompanyQuery();

  return (
    <nav className="bg-card border rounded-xl drop-shadow-xl drop-shadow-black/2 items-center w-[calc(100%-32px)] mt-4 h-fit pl-8 pr-3 py-3 shrink-0 flex gap-2">
      <Logo className="text-2xl" />
      <div className="w-5"></div>
      <NavLink to="/roadmaps">Roadmaps</NavLink>
      <NavLink to="/jobs">Jobs</NavLink>
      <NavLink to="/profile">Profile</NavLink>
      {user?.roles.includes("RECRUITER") && (
        <NavLink to={"/company/" + myCompany.data?.id}>My company</NavLink>
      )}
      <div className="flex-1"></div>
      {user && (
        <>
          <span className="flex items-center gap-2"><UserRound /> {user.username}</span>
          &nbsp;
          <Button
            onClick={() => logoutMutation.mutate()}
            disabled={logoutMutation.isPending}
            className="rounded-2xl px-8 py-6 hover:brightness-125"
            style={{
              background:
                "linear-gradient(90deg, #0F1A2C 36%, #33363A 68%, #000000 100%)",
            }}
          >
            Sign Out
          </Button>
        </>
      )}
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
        active && "text-primary"
      )}
    >
      {props.children}
    </Link>
  );
}
