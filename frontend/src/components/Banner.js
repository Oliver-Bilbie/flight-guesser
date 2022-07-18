import React from "react";
import { Header, Heading, Box, Anchor, Nav } from "grommet";
import { Github, Linkedin } from "grommet-icons";

const navBarItems = [
  {
    key: "github",
    icon: <Github color="text-strong" />,
    href: "https://github.com/Oliver-Bilbie",
  },
  {
    key: "linkedin",
    icon: <Linkedin color="text-strong" />,
    href: "https://www.linkedin.com/in/oliver-bilbie/",
  },
];

const Banner = () => {
  return (
    <Header
      elevation="small"
      background="brand"
      pad="small"
      height="xsmall"
      animation="fadeIn"
      direction="row"
    >
      <Box direction="row" align="center">
        <Heading level="2" color="text-strong">
          Flight Guesser
        </Heading>
      </Box>
      <Nav direction="row" pad="medium" color="text-strong">
        {navBarItems.map((item) => (
          <Anchor key={item.key} icon={item.icon} href={item.href} />
        ))}
      </Nav>
    </Header>
  );
};

export default Banner;
