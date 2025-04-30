import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import ScoreDisplay from "./components/ScoreDisplay/ScoreDisplay";
import MakeGuess from "./components/MakeGuess/MakeGuess";

function App() {
  return (
    <>
      <Header />
      <ScoreDisplay />
      <MakeGuess />
      <Footer />
    </>
  );
}

export default App;
