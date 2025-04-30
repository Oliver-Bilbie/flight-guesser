import { FC, ReactElement } from "react";
import "./PointsDisplay.css";
import { Points } from "../../utils/types";
import { useGameStore } from "../../utils/gameStore";

interface PointsDisplayProps {
  points: Points;
}

const PointsDisplay: FC<PointsDisplayProps> = ({ points }): ReactElement => {
  const rules = useGameStore((state) => state.rules);

  return (
    <div className="points-display">
      <h2>You scored {points.total} points</h2>
      {rules.useOrigin && <h4>Origin guess: {points.origin}/100</h4>}
      {rules.useDestination && <h4>Destination guess: {points.destination}/100</h4>}
    </div>
  );
};

export default PointsDisplay;
