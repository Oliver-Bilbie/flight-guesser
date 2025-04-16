import React from "react";
import { ButtonType } from "../../types";

interface PopupMenuProps {
  body: React.ReactElement;
  buttons: ButtonType[];
}

const PopupMenu: React.FC<PopupMenuProps> = ({
  body,
  buttons,
}): React.ReactElement => {
  return (
    <div className="popup-overlay">
      <div className="popup-container">
        {body}
        <div className="popup-buttons">
          {buttons.map((button: ButtonType) => (
            <button
              className="custom-button"
              onClick={button.onClick}
              key={button.label}
            >
              {button.icon}
              <div className="pad" />
              <h4>{button.label}</h4>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PopupMenu;
