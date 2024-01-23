import clsx from "clsx";
import React from "react";

interface ClickableTextProps {
  children: React.ReactNode;
  className?: string;
}

const ClickableText: React.FC<ClickableTextProps> = ({
  children,
  className,
}) => {
  return <span className={clsx(className, "underline")}>{children}</span>;
};

export default ClickableText;
