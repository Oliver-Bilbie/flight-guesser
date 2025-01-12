import React from "react";
import { Box, Layer } from "grommet";
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
    <Layer>
      <Box
        width="medium"
        pad="small"
        gap="medium"
        align="center"
        justify="center"
      >
        {body}
        <Box direction="row" justify="center" gap="medium">
          {buttons.map((button: ButtonType) => {
            return (
              <button
                className="custom-button"
                onClick={button.onClick}
                key={button.label}
              >
                {button.icon}
                <div className="pad" />
                <h4>{button.label}</h4>
              </button>
            );
          })}
        </Box>
      </Box>
    </Layer>
  );
};

export default PopupMenu;
