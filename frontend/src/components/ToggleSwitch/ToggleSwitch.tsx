import { FC } from "react";
import "./ToggleSwitch.css";

interface ToggleSwitchProps {
  checked: boolean;
  disabled?: boolean;
  onChange: (checked: boolean) => void;
}

const ToggleSwitch: FC<ToggleSwitchProps> = ({
  checked,
  disabled = false,
  onChange,
}) => {
  return (
    <label className="toggle-switch">
      <input
        type="checkbox"
        checked={checked}
        disabled={disabled}
        onChange={(e) => onChange(e.target.checked)}
      />
      <span className={disabled ? "slider-disabled" : "slider"} />
    </label>
  );
};

export default ToggleSwitch;
