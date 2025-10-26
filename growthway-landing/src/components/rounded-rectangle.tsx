"use client";
import { AnimatedTooltip } from "./ui/animated-tooltip";
import { useUserMode } from "../contexts/user-mode-context";

const individuals = [
    {
        id: 1,
        name: "Emma Wilson",
        designation: "Computer Science Student",
        image:
            "https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YXZhdGFyfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60",
    },
    {
        id: 2,
        name: "Alex Chen",
        designation: "Marketing Intern",
        image:
            "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3540&q=80",
    },
    {
        id: 3,
        name: "Sofia Garcia",
        designation: "Design Student",
        image:
            "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60",
    },
    {
        id: 4,
        name: "Marcus Johnson",
        designation: "Software Engineering Intern",
        image:
            "https://images.unsplash.com/photo-1599566150163-29194dcaad36?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3387&q=80",
    },
    {
        id: 5,
        name: "Lily Park",
        designation: "Business Administration Student",
        image:
            "https://images.unsplash.com/photo-1544725176-7c40e5a71c5e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3534&q=80",
    },
];

const companies = [
    {
        id: 1,
        name: "Sarah Mitchell",
        designation: "HR Director",
        image:
            "https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YXZhdGFyfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60",
    },
    {
        id: 2,
        name: "Michael Chen",
        designation: "Talent Acquisition Manager",
        image:
            "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3540&q=80",
    },
    {
        id: 3,
        name: "Jessica Rodriguez",
        designation: "Recruitment Specialist",
        image:
            "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGF2YXRhcnxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60",
    },
    {
        id: 4,
        name: "David Thompson",
        designation: "Head of Recruiting",
        image:
            "https://images.unsplash.com/photo-1599566150163-29194dcaad36?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3387&q=80",
    },
    {
        id: 5,
        name: "Amanda Parker",
        designation: "Talent Scout",
        image:
            "https://images.unsplash.com/photo-1544725176-7c40e5a71c5e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3534&q=80",
    },
];

export default function RoadmapCTA() {
    const { userMode } = useUserMode();
    const people = userMode === "individual" ? individuals : companies;

    return (
        <div className="w-full bg-black rounded-3xl shadow-2xl overflow-hidden">
            <div className="flex flex-row items-center justify-between gap-6 px-8 py-6">
                {/* Left Section */}
                <div className="shrink-0 space-y-4 max-w-[280px]">
                    {userMode === "individual" ? (
                        <h2 className="text-3xl font-bold text-white leading-tight">
                            Get <span className="text-blue-400">your Roadmap</span>
                            <br />
                            <span className="text-blue-400">Today!</span>
                        </h2>
                    ) : (
                        <h2 className="text-3xl font-bold text-white leading-tight">
                            Discover the <span className="text-blue-400">Talent Pool</span>
                        </h2>
                    )}
                    <a href="/app">
                        <button className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg border-2 border-blue-500 transition-all duration-300">
                            Get started
                        </button>
                    </a>
                </div>

                {/* Center Section - Graph */}
                <div className="shrink-0">
                    <div className="relative w-[320px] h-80 bg-gray-300 rounded-xl p-6">
                        {/* Grid pattern */}
                        <div className="absolute inset-6 grid grid-cols-4 grid-rows-4 gap-0">
                            {Array.from({ length: 16 }).map((_, i) => (
                                <div key={i} className="border-r border-b border-gray-400/30 last:border-r-0 [&:nth-child(4n)]:border-r-0" />
                            ))}
                        </div>

                        {/* Graph line and nodes */}
                        <img src="/graph.png" alt="Graph" className="absolute inset-0 w-full h-full object-cover opacity-20" />
                    </div>
                </div>

                {/* Right Section */}
                <div className="shrink-0 space-y-4 max-w-[280px]">
                    {userMode === "individual" ? (
                        <p className="text-base text-white leading-relaxed">
                            Our users have already learn with their personalized roadmap.{" "}
                            <span className="text-blue-400 font-semibold">Try it too!</span>
                        </p>
                    ) : (
                        <p className="text-base text-white leading-relaxed">
                            Our partners have already started grow their businesses.{" "}
                            <span className="text-blue-400 font-semibold">Join us!</span>
                        </p>
                    )}

                    {/* Avatar stack with AnimatedTooltip */}
                    <div className="flex items-center gap-2">
                        <AnimatedTooltip items={people} />
                        <div className="w-10 h-10 rounded-full bg-white border-2 border-black flex items-center justify-center">
                            <span className="text-xs font-bold text-black">+2m</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
