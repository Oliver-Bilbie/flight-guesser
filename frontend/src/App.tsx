import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import ScoreDisplay from "./components/ScoreDisplay/ScoreDisplay";
import MakeGuess from "./components/MakeGuess/MakeGuess";
import SettingsMenu from "./components/SettingsMenu/SettingsMenu";
import { useState } from "react";
import SettingsButton from "./components/SettingsButton/SettingsButton";

function App() {
  const [showSettings, setShowSettings] = useState(false);

  return (
    <>
      <Header />
      <ScoreDisplay />

      {showSettings ? (
        <SettingsMenu onClose={() => setShowSettings(false)} />
      ) : (
        <MakeGuess />
      )}

      <SettingsButton onClick={() => setShowSettings(true)} />

      <Footer />
    </>
  );
}

export default App;
