import React from "react";
import { Grommet, Box } from "grommet";
import Theme from "./theme";
import Banner from "./components/Banner";
import Game from "./components/Game";

function App() {
  return (
    <div className="App">
      <Grommet theme={Theme} full={true}>
        <Banner />
        <Box alignContent="center" align="center" justify="center" pad="large">
          <Game />
        </Box>
      </Grommet>
    </div>
  );
}

export default App;
