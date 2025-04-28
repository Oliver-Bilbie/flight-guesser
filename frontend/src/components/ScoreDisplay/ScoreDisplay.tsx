import { FC, ReactElement } from "react";
import "./ScoreDisplay.css";
import { useSingleplayerStore } from "../../utils/singleplayerStore";

const ScoreDisplay: FC = (): ReactElement => {
  const score = useSingleplayerStore((state) => state.score);
  return <h1 className="scoreText">Score: {score}</h1>;
};

export default ScoreDisplay;
