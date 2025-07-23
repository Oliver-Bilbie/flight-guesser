import { FC, ReactElement } from "react";
import "./PointsDisplay.css";
import { Points, Rules, SuccessStatus } from "../../utils/types";

interface PointsDisplayProps {
  points: Points;
  status: SuccessStatus;
  rules: Rules;
}

const PointsDisplay: FC<PointsDisplayProps> = ({
  points,
  status,
  rules,
}): ReactElement => {
  if (status === "AlreadyGuessed") {
    return (
      <div className="points-display">
        <h2>You have already made a guess for this flight</h2>
        <h4>
          No additional points have been awarded, however you can still view the
          flight details
        </h4>
      </div>
    );
  }

  if (status === "PointsUnavailable") {
    return (
      <div className="points-display">
        <h2>No points are available for this flight</h2>
        <h4>
          Route data is missing for this flight so no points have been awarded
        </h4>
      </div>
    );
  }

  return (
    <div className="points-display">
      <h2>You scored {points.total} points</h2>
      {rules.useOrigin && <h4>Origin guess: {points.origin}/100</h4>}
      {rules.useDestination && (
        <h4>Destination guess: {points.destination}/100</h4>
      )}
    </div>
  );
};

export default PointsDisplay;
