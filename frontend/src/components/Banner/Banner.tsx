import React from "react";
import { Box } from "grommet";

const Banner: React.FC = (): React.ReactElement => {
  return (
    <Box
      align="center"
      as="header"
      direction="row"
      flex={false}
      gap="medium"
      justify="between"
      elevation="small"
      background="brand"
      pad="small"
      height="xsmall"
      animation="fadeIn"
    >
      <h1 className="light-text">Flight Guesser</h1>
    </Box>
  );
};

export default Banner;
