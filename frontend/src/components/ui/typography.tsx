import { cn } from "@/lib/utils";

export function TypographyH1(props: { children: React.ReactNode }) {
  return (
    <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
      {props.children}
    </h1>
  );
}

export function TypographyH2(props: { children: React.ReactNode }) {
  return (
    <h2 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0">
      {props.children}
    </h2>
  );
}

export function TypographyH3(props: { children: React.ReactNode }) {
  return (
    <h3 className="scroll-m-20 text-2xl font-semibold tracking-tight">
      {props.children}
    </h3>
  );
}

export function TypographyH4(props: { children: React.ReactNode }) {
  return (
    <h4 className="scroll-m-20 text-xl font-semibold tracking-tight">
      {props.children}
    </h4>
  );
}

export function TypographyP(props: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <p className={cn("leading-7 [&:not(:first-child)]:mt-6", props.className)}>
      {props.children}
    </p>
  );
}

export function TypographyLead(props: { children: React.ReactNode }) {
  return <p className="text-xl text-muted-foreground">{props.children}</p>;
}

export function TypographyLarge(props: { children: React.ReactNode }) {
  return <div className="text-lg font-semibold"> {props.children}</div>;
}

export function TypographySmall(props: { children: React.ReactNode }) {
  return (
    <small className="text-sm font-medium leading-none">{props.children}</small>
  );
}

export function TypographyMuted(props: { children: React.ReactNode }) {
  return <p className="text-sm text-muted-foreground"> {props.children}</p>;
}
