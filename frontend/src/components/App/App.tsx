import React from "react";
import { Grommet, Box } from "grommet";
import Theme from "../../theme";
import Banner from "../Banner/Banner";
import Game from "../Game/Game";

const App: React.FC = (): React.ReactElement => {
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
};

export default App;
