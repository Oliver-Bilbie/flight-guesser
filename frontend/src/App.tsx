import { useState, useEffect } from "react";
import Footer from "./components/Footer/Footer";
import Game from "./components/Game/Game";
import Header from "./components/Header/Header";
import Leaderboard from "./components/Leaderboard/Leaderboard";
import SettingsMenu from "./components/SettingsMenu/SettingsMenu";
import SettingsMultiplayer from "./components/SettingsMultiplayer/SettingsMultiplayer";
import ScoreDisplay from "./components/ScoreDisplay/ScoreDisplay";
import { useLobbyStore } from "./utils/lobbyStore";
import { useThemeStore } from "./utils/themeStore";

function App() {
  const [showMultiplayer, setShowMultiplayer] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const theme = useThemeStore((state) => state.theme);
  const isSingleplayer =
    useLobbyStore((state) => state.lobbyResponse.status) === "NotInLobby";

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  return (
    <>
      <Header
        setShowSettings={setShowSettings}
        setShowMultiplayer={setShowMultiplayer}
      />

      <main>
        {isSingleplayer ? <ScoreDisplay /> : <Leaderboard />}
        <Game />
      </main>

      <Footer />

      {showMultiplayer && (
        <SettingsMultiplayer onClose={() => setShowMultiplayer(false)} />
      )}
      {showSettings && <SettingsMenu onClose={() => setShowSettings(false)} />}
    </>
  );
}

export default App;
