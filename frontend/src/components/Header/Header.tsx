import { FC, ReactElement } from "react";
import "./Header.css";
import MultiplayerButton from "../MultiplayerButton/MultiplayerButton";
import SettingsButton from "../SettingsButton/SettingsButton";
import Tooltip from "../Tooltip/Tooltip";

interface HeaderProps {
  setShowSettings: (show: boolean) => void;
  setShowMultiplayer: (show: boolean) => void;
}

const Header: FC<HeaderProps> = ({
  setShowSettings,
  setShowMultiplayer,
}): ReactElement => {
  return (
    <header className="header">
      <h1 className="light-text">Flight Guesser</h1>
      <div className="header-buttons">
        <Tooltip message="Multiplayer" position="left">
          <MultiplayerButton onClick={() => setShowMultiplayer(true)} />
        </Tooltip>
        <Tooltip message="Settings" position="left">
          <SettingsButton onClick={() => setShowSettings(true)} />
        </Tooltip>
      </div>
    </header>
  );
};

export default Header;
