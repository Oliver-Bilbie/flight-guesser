import { FC, useState } from "react";
import "./SettingsMenu.css";
import MultiplayerButton from "../MultiplayerButton/MultiplayerButton";
import SettingsGeneral from "../SettingsGeneral/SettingsGeneral";
import SettingsMultiplayer from "../SettingsMultiplayer/SettingsMultiplayer";

interface SettingsMenuProps {
  onClose: () => void;
}

const SettingsMenu: FC<SettingsMenuProps> = ({ onClose }) => {
  const [showMulti, setShowMulti] = useState(false);

  return (
    <div className="settings-menu">
      {showMulti ? (
        <>
          <h1>Multiplayer</h1>
          <SettingsMultiplayer />
        </>
      ) : (
        <>
          <h1>Settings</h1>
          <MultiplayerButton onClick={() => setShowMulti(true)} />
          <SettingsGeneral />
        </>
      )}
      <div className="settings-menu-option">
        {showMulti && (
          <button onClick={() => setShowMulti(false)}>Settings</button>
        )}
        <button onClick={() => onClose()}>{"Done"}</button>
      </div>
    </div>
  );
};

export default SettingsMenu;
