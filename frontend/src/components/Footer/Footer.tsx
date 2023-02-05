import React from "react";
import { Anchor, Box, Text } from "grommet";

const Footer: React.FC = (): React.ReactElement => {
  return (
    <Box align="center" pad="small">
      <Text>Version: {process.env.REACT_APP_VERSION}</Text>
      <Anchor
        label="What's new?"
        onClick={(): void => {
          window.open(
            "https://github.com/Oliver-Bilbie/flight-guesser/blob/main/CHANGELOG.md",
            "_blank"
          );
        }}
        a11yTitle={"changelog"}
      />
    </Box>
  );
};

export default Footer;
