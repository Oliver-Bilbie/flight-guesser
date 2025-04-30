import { FC, ReactElement, ReactNode } from "react";
import "./PopupMenu.css";

interface PopupMenuProps {
  title?: string;
  onClose?: () => void;
  children?: ReactNode;
}

const PopupMenu: FC<PopupMenuProps> = ({
  title,
  onClose,
  children,
}): ReactElement => {
  return (
    <div className="popup-overlay">
      <div className="popup-container">
        {title != null && <h2 className="popup-title">{title}</h2>}
        <div className="popup-content">{children}</div>
        {onClose && (
          <button className="popup-button" onClick={onClose}>
            Close
          </button>
        )}
      </div>
    </div>
  );
};

export default PopupMenu;
