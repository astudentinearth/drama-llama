import { cn } from "@/lib/utils";

export default function Logo(props: { className?: string }) {
  return (
    <span
      className={cn(
        "flex text-center justify-center font-extrabold text-brand text-4xl",
        props.className,
      )}
    >
      GrowthWay
    </span>
  );
}
