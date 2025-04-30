import { FC, ReactElement } from "react";
import "./ScoreDisplay.css";
import { useGameStore } from "../../utils/gameStore";

const ScoreDisplay: FC = (): ReactElement => {
  const score = useGameStore((state) => state.score);
  return <h1 className="scoreText">Score: {score}</h1>;
};

export default ScoreDisplay;
