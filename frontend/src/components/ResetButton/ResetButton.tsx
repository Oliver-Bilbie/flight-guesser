import { FC, useState } from "react";
import "./ResetButton.css";
import { useGameStore } from "../../utils/gameStore";
import PopupMenu from "../PopupMenu/PopupMenu";
import ConfirmDisplay from "../ConfirmDisplay/ConfirmDisplay";

const ResetButton: FC = () => {
  const [confirm, setConfirm] = useState(false);
  const doReset = useGameStore((state) => state.reset);

  return (
    <>
      <button className="reset-button" onClick={() => setConfirm(true)}>
        <svg
          height="1.5rem"
          width="1.5rem"
          viewBox="0 0 1920 1920"
          fill="currentColor"
        >
          <g>
            <path d="M960 0v213.333c411.627 0 746.667 334.934 746.667 746.667S1371.627 1706.667 960 1706.667 213.333 1371.733 213.333 960c0-197.013 78.4-382.507 213.334-520.747v254.08H640V106.667H53.333V320h191.04C88.64 494.08 0 720.96 0 960c0 529.28 430.613 960 960 960s960-430.72 960-960S1489.387 0 960 0" />
          </g>
        </svg>
        <h3>Reset</h3>
      </button>

      {confirm && (
        <PopupMenu>
          <ConfirmDisplay
            title="Confirm reset"
            message="Are you sure that you want to reset your guessed flights?"
            onConfirm={() => {
              doReset();
              setConfirm(false);
            }}
            onReject={() => setConfirm(false)}
          />
        </PopupMenu>
      )}
    </>
  );
};

export default ResetButton;
