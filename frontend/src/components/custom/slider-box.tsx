import { InputNumeric } from "@/components/custom/input-numeric";
import { Slider } from "@/components/ui/slider";

interface SliderBoxProps {
  min: number;
  max: number;
  value: number;
  onChange: (value: number) => void;
}

export function SliderBox(props: SliderBoxProps) {
  const { min, max, value, onChange } = props;

  return (
    <div className="flex items-center gap-2 ml-auto">
      <span>{min}</span>

      <Slider
        className="w-32"
        value={[value]}
        min={min}
        max={max}
        onValueChange={(newValues) => onChange(newValues[0])}
      />

      <span>{max}</span>

      <InputNumeric
        className="w-16"
        value={value}
        min={min}
        max={max}
        onChange={onChange}
        type="number"
      />
    </div>
  );
}
