import React from "react";
import { Box, Button, Layer } from "grommet";
import { ButtonType } from "../../types";

interface PopupMenuProps {
  body: React.ReactElement;
  buttons: ButtonType[];
}

const Game: React.FC<PopupMenuProps> = ({
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
              <Button
                label={button.label}
                icon={button.icon}
                onClick={button.onClick}
                key={button.label}
              />
            );
          })}
        </Box>
      </Box>
    </Layer>
  );
};

export default Game;
