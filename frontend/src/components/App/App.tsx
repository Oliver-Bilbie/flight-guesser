import React from "react";
import { Grommet, Box } from "grommet";
import Theme from "../../theme";
import Banner from "../Banner/Banner";
import Footer from "../Footer/Footer";
import Game from "../Game/Game";
import "../../styles.css";

const App: React.FC = (): React.ReactElement => {
  return (
    <div className="App">
      <Grommet theme={Theme} full={true}>
        <div className="texture">
          <Banner />
          <Box
            alignContent="center"
            align="center"
            justify="center"
            pad="large"
          >
            <Game />
          </Box>
          <Footer />
        </div>
      </Grommet>
    </div>
  );
};

export default App;
