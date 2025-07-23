import { FC, ReactElement } from "react";
import "./MessageDisplay.css";

interface MessageDisplayProps {
  title: string;
  message: string;
  continueText: string;
  onContinue: () => void;
}

const MessageDisplay: FC<MessageDisplayProps> = ({
  title,
  message,
  continueText,
  onContinue,
}): ReactElement => {
  return (
    <div className="message-display">
      <h2>{title}</h2>
      <h4>{message}</h4>
      <button onClick={onContinue}>{continueText}</button>
    </div>
  );
};

export default MessageDisplay;
