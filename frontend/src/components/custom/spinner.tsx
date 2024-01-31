import { cn } from "@/lib/utils";
import { Loader, LucideProps } from "lucide-react";

export function Spinner(props: LucideProps) {
  return <Loader {...props} className={cn("animate-spin", props.className)} />;
}
