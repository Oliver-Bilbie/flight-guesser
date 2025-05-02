import { useState, useEffect } from "react";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import ScoreDisplay from "./components/ScoreDisplay/ScoreDisplay";
import MakeGuess from "./components/MakeGuess/MakeGuess";
import SettingsMenu from "./components/SettingsMenu/SettingsMenu";
import SettingsButton from "./components/SettingsButton/SettingsButton";
import { useThemeStore } from "./utils/themeStore";

function App() {
  const [showSettings, setShowSettings] = useState(false);

  const theme = useThemeStore((state) => state.theme);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

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
