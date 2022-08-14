import React from "react";
import { Box, Button, Layer, Text } from "grommet";

interface PopupMenuProps {
  message: string;
  onClose: () => void;
}

const Game: React.FC<PopupMenuProps> = ({
  message,
  onClose,
}): React.ReactElement => {
  return (
    <Layer onEsc={onClose} onClickOutside={onClose}>
      <Box
        width="medium"
        pad="small"
        gap="medium"
        align="center"
        justify="center"
      >
        <Text>{message}</Text>
        <Box width="xsmall">
          <Button label="Close" onClick={onClose} />
        </Box>
      </Box>
    </Layer>
  );
};

export default Game;
