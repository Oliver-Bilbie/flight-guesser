import { FC, ReactElement } from "react";
import "./ConfirmDisplay.css";

interface ConfirmDisplayProps {
  title: string;
  message: string;
  onConfirm: () => void;
  onReject: () => void;
}

const ConfirmDisplay: FC<ConfirmDisplayProps> = ({
  title,
  message,
  onConfirm,
  onReject,
}): ReactElement => {
  return (
    <div className="confirm-display">
      <h2>{title}</h2>
      <h4>{message}</h4>
      <div className="confirm-display-buttons">
        <button onClick={onReject}>Back</button>
        <button onClick={onConfirm}>Confirm</button>
      </div>
    </div>
  );
};

export default ConfirmDisplay;
