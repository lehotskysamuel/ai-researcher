import * as React from "react";
import * as ProgressPrimitive from "@radix-ui/react-progress";

import { cn } from "@/lib/utils";

const Progress = React.forwardRef<
  React.ElementRef<typeof ProgressPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root>
>(({ className, value, ...props }, ref) => (
  <ProgressPrimitive.Root
    ref={ref}
    className={cn(
      "relative h-4 w-full overflow-hidden rounded-full bg-secondary",
      className
    )}
    {...props}
  >
    <ProgressPrimitive.Indicator
      className="h-full w-full flex-1 bg-primary transition-all"
      style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
    />
  </ProgressPrimitive.Root>
));
Progress.displayName = ProgressPrimitive.Root.displayName;

interface ProgressWithPercentageProps
  extends React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root> {
  finished: number;
  total: number;
}

function ProgressWithPercentage({
  finished,
  total,
  ...progressProps
}: ProgressWithPercentageProps) {
  return (
    <span className="flex items-center gap-2">
      <Progress
        className="flex-1"
        value={(finished / total) * 100}
        {...progressProps}
      />
      <span>
        {finished} / {total}
      </span>
    </span>
  );
}

export { Progress, ProgressWithPercentage };
