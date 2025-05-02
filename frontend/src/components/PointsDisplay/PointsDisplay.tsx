import { FC, ReactElement } from "react";
import "./PointsDisplay.css";
import { Points, Rules } from "../../utils/types";

interface PointsDisplayProps {
  points: Points;
  isAlreadyGuessed: boolean;
  rules: Rules;
  hasOrigin: boolean;
  hasDestination: boolean;
}

const PointsDisplay: FC<PointsDisplayProps> = ({
  points,
  isAlreadyGuessed,
  rules,
  hasOrigin,
  hasDestination,
}): ReactElement => {
  if (isAlreadyGuessed) {
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

  const noPointsAvailable = !(
    (rules.useOrigin && hasOrigin) ||
    (rules.useDestination && hasDestination)
  );

  if (noPointsAvailable) {
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
