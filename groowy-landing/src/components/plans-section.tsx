import { useUserMode } from "../contexts/user-mode-context";
import { Check } from "lucide-react";
import { BackgroundGradient } from "./ui/background-gradient";

type Plan = {
    id: string;
    title: string;
    subtitle: string;
    price: number | string;
    features: string[];
    gradient: string;
    borderGradient: string;
};

const PLANS: Record<string, Plan> = {
    free: {
        id: "free",
        title: "Free Plan",
        subtitle: "Best for casual users or trial purposes",
        price: "Free",
        features: [
            "Access to three personalized learning roadmap",
            "Project submission allowed but not visible to employers"
        ],
        gradient: "from-[#d4d4d8] via-[#e4e4e7] to-[#d4d4d8]",
        borderGradient: "from-blue-500 via-purple-500 to-blue-500"
    },
    premium: {
        id: "premium",
        title: "Premium Plan",
        subtitle: "Best for active users who want full success",
        price: 20,
        features: [
            "Full access to all courses",
            "Personalized tests and performance tracking",
            "Project visibility for employers",
            "Smart Portfolio and CV updater",
            "Chat-based 24/7 AI mentor"
        ],
        gradient: "from-[#93c5fd] via-[#dbeafe] to-[#bfdbfe]",
        borderGradient: "from-blue-600 via-blue-400 to-blue-600"
    },
    starter: {
        id: "starter",
        title: "Starter Plan",
        subtitle: "Best for startup and small teams",
        price: 150,
        features: [
            "Up to 10 job postings a month",
            "Access to 50 applicant database access",
            "AI-assisted job post creation",
            "Candidate-job matching scores"
        ],
        gradient: "from-[#d8b4fe] via-[#f3e8ff] to-[#e9d5ff]",
        borderGradient: "from-purple-600 via-blue-500 to-purple-600"
    },
    enterprise: {
        id: "enterprise",
        title: "Enterprise Plan",
        subtitle: "Best for growing and large-scale HR teams",
        price: 450,
        features: [
            "Unlimited job listings",
            "Full candidate database access",
            "AI-assisted job post creation",
            "Candidate-job matching scores",
            "Talent Pool analytics and reporting",
            "Hiring performance analytics and reporting"
        ],
        gradient: "from-[#a5f3fc] via-[#f5d0fe] to-[#d8b4fe]",
        borderGradient: "from-cyan-500 via-purple-400 to-purple-500"
    }
};

function PlanCard({ plan }: { plan: Plan }) {
    return (
        <div className="h-full">
            <BackgroundGradient
                containerClassName="h-full"
                className="h-full"
            >
                <div className={`h-full rounded-[2rem] bg-gradient-to-br ${plan.gradient} p-8 flex flex-col min-h-[600px]`}>
                    {/* Header */}
                    <div className="mb-6">
                        <h3 className="text-2xl font-bold text-gray-900 mb-1">{plan.title}</h3>
                        <p className="text-sm text-gray-600">{plan.subtitle}</p>
                    </div>

                    {/* Price */}
                    <div className="mb-6">
                        <div className="flex items-baseline gap-1">
                            <span className="text-5xl font-bold text-gray-900">
                                ${typeof plan.price === "number" ? plan.price : "0"}
                            </span>
                            {typeof plan.price === "number" && (
                                <span className="text-lg text-gray-700">/mo</span>
                            )}
                        </div>
                        {typeof plan.price === "number" && (
                            <p className="text-sm text-gray-600 mt-1">Cancel or pause any time</p>
                        )}
                    </div>

                    {/* CTA Button */}
                    <a href="/app" className="w-full block mb-8">
                        <button className="w-full bg-gray-900 hover:bg-gray-800 text-white font-semibold py-4 px-6 rounded-2xl transition-all cursor-pointer hover:shadow-2xl">
                            Get started
                        </button>
                    </a>

                    {/* Features */}
                    <div className="space-y-4 flex-grow">
                        {plan.features.map((feature, idx) => (
                            <div key={idx} className="flex gap-3 items-start">
                                <Check className="w-5 h-5 text-gray-900 flex-shrink-0 mt-0.5" strokeWidth={3} />
                                <span className="text-sm text-gray-900 leading-relaxed">{feature}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </BackgroundGradient>
        </div>
    );
}

export default function PlansSection() {
    const { userMode } = useUserMode();

    // For 'individual' show Free + Premium. For 'business' show Starter + Enterprise.
    const visiblePlans =
        userMode === "individual"
            ? [PLANS.free, PLANS.premium]
            : [PLANS.starter, PLANS.enterprise];

    return (
        <section className="max-w-6xl mx-auto px-6 py-12">
            <div className="flex flex-col items-center mb-12">
                <h2 className="text-4xl font-bold text-gray-900">Choose a plan</h2>
                <p className="text-lg text-gray-600 mt-3">Recommended plans for {userMode}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto items-stretch">
                {visiblePlans.map((p) => (
                    <PlanCard key={p.id} plan={p} />
                ))}
            </div>
        </section>
    );
}
