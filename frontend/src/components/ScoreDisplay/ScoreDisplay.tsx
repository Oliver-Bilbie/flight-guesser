import { FC, ReactElement } from "react";
import "./ScoreDisplay.css";
import { useGameStore } from "../../utils/gameStore";
import { useLobbyStore } from "../../utils/lobbyStore";

const ScoreDisplay: FC = (): ReactElement => {
  const singleScore = useGameStore((state) => state.score);

  const isSingleplayer =
    useLobbyStore((state) => state.lobbyResponse.status) === "NotInLobby";
  const multiScore = useLobbyStore((state) => state.score);

  return (
    <h1 className="scoreText">
      Score: {isSingleplayer ? singleScore : multiScore}
    </h1>
  );
};

export default ScoreDisplay;
