import clsx from "clsx";
import React from "react";

interface ClickableTextProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

const ClickableText: React.FC<ClickableTextProps> = ({
  children,
  className,
  onClick,
}) => {
  return (
    <span
      className={clsx(className, "underline cursor-pointer")}
      onClick={onClick}
    >
      {children}
    </span>
  );
};

export default ClickableText;
