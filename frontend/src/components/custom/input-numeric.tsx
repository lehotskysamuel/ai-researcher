import { Input, InputProps } from "../ui/input";

export interface InputNumericProps extends Omit<InputProps, "onChange"> {
  onChange(newValue: number): void;
  min?: number;
  max?: number;
}

const InputNumeric = (props: InputNumericProps) => {
  const { onChange, min, max, ...rest } = props;
  return (
    <Input
      onChange={(e) => {
        let newValue = parseInt(e.target.value);
        if (min !== undefined && newValue < min) newValue = min;
        if (max !== undefined && newValue > max) newValue = max;

        if (onChange) onChange(newValue);
      }}
      {...rest}
    />
  );
};
InputNumeric.displayName = "InputNumeric";

export { InputNumeric };
