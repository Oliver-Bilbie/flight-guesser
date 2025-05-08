import { useEffect } from "react";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import ScoreDisplay from "./components/ScoreDisplay/ScoreDisplay";
import Game from "./components/Game/Game";
import { useThemeStore } from "./utils/themeStore";
import Leaderboard from "./components/Leaderboard/Leaderboard";

function App() {
  const theme = useThemeStore((state) => state.theme);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  return (
    <>
      <Header />

      <main>
        <ScoreDisplay />
        <Leaderboard />
        <Game />
      </main>

      <Footer />
    </>
  );
}

export default App;
