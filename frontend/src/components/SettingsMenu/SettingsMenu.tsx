import { FC } from "react";
import "./SettingsMenu.css";
import PopupMenu from "../PopupMenu/PopupMenu";
import ResetButton from "../ResetButton/ResetButton";
import ToggleSwitch from "../ToggleSwitch/ToggleSwitch";
import { useGameStore } from "../../utils/gameStore";
import { useLobbyStore } from "../../utils/lobbyStore";
import { useThemeStore } from "../../utils/themeStore";

interface SettingsMenuProps {
  onClose: () => void;
}

const SettingsMenu: FC<SettingsMenuProps> = ({ onClose }) => {
  const singleRules = useGameStore((state) => state.rules);
  const singleSetRules = useGameStore((state) => state.setRules);

  const isSingleplayer =
    useLobbyStore((state) => state.lobbyResponse.status) === "NotInLobby";
  const multiRules = useLobbyStore((state) => state.rules);

  const rules = isSingleplayer
    ? singleRules
    : multiRules !== null
      ? multiRules
      : { useOrigin: false, useDestination: false };

  const setRules = isSingleplayer ? singleSetRules : () => null;

  const theme = useThemeStore((state) => state.theme);
  const toggleTheme = useThemeStore((state) => state.toggleTheme);

  return (
    <PopupMenu>
      <div className="settings-menu">
        <h1>Settings</h1>
        <>
          {!isSingleplayer && (
            <h4>
              Some settings have been locked to match the other players in the
              multiplayer lobby
            </h4>
          )}

          <div className="settings-menu-container">
            <div className="settings-menu-option">
              <ToggleSwitch
                checked={rules.useOrigin}
                disabled={!isSingleplayer}
                onChange={(isChecked) =>
                  setRules({ ...rules, useOrigin: isChecked })
                }
              />
              <h3>Enable origin guesses</h3>
            </div>

            <div className="settings-menu-option">
              <ToggleSwitch
                checked={rules.useDestination}
                disabled={!isSingleplayer}
                onChange={(isChecked) =>
                  setRules({ ...rules, useDestination: isChecked })
                }
              />
              <h3>Enable destination guesses</h3>
            </div>

            <div className="settings-menu-option">
              <ToggleSwitch
                checked={theme === "dark"}
                onChange={() => toggleTheme()}
              />
              <h3>Dark mode</h3>
            </div>

            <div className="settings-menu-option">
              <ResetButton />
            </div>
          </div>
        </>
        <button onClick={() => onClose()}>Done</button>
      </div>
    </PopupMenu>
  );
};

export default SettingsMenu;
