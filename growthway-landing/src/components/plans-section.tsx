import { useUserMode } from "../contexts/user-mode-context";

type Plan = {
    id: string;
    title: string;
    image: string;
};

const PLANS: Record<string, Plan> = {
    free: { id: "free", title: "Free Plan", image: "/plans/free.png" },
    premium: { id: "premium", title: "Premium Plan", image: "/plans/premium.png" },
    starter: { id: "starter", title: "Starter Plan", image: "/plans/starter.png" },
    enterprise: { id: "enterprise", title: "Enterprise Plan", image: "/plans/enterprise.png" },
};

const cardClasses =
    "";

export default function PlansSection() {
    const { userMode } = useUserMode();

    // For 'individual' show Free + Premium. For 'business' show Starter + Enterprise.
    const visiblePlans =
        userMode === "individual"
            ? [PLANS.free, PLANS.premium]
            : [PLANS.starter, PLANS.enterprise];

    return (
        <section className="max-w-6xl mx-auto px-6">
            <div className="flex flex-col items-center mb-8">
                <h2 className="text-3xl font-semibold">Choose a plan</h2>
                <p className="text-sm text-gray-500 mt-2">Recommended plans for {userMode}</p>
            </div>

            <div className="flex flex-col sm:flex-row justify-center gap-8 items-stretch">
                {visiblePlans.map((p) => (
                    <div key={p.id} className={cardClasses}>
                        <div className="flex-1">
                            <img src={p.image} alt={p.title} className="w-full h-auto block rounded-xl" />
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
}
