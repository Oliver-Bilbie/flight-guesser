import { FC } from "react";
import "./TextInput.css";

interface TextInputProps {
  value: string;
  setValue: (value: string) => void;
}

const TextInput: FC<TextInputProps> = ({ value, setValue }) => {
  return (
    <input
      className="text-input"
      type="text"
      value={value}
      onChange={(event) => setValue(event.target.value)}
    />
  );
};

export default TextInput;
