import { ReactElement, FC } from "react";
import "./SettingsMenu.css";
import PopupMenu from "../PopupMenu/PopupMenu";
import ToggleSwitch from "../ToggleSwitch/ToggleSwitch";
import { useGameStore } from "../../utils/gameStore";
import { useThemeStore } from "../../utils/themeStore";

interface SettingsMenuProps {
  onClose: () => void;
}

const SettingsMenu: FC<SettingsMenuProps> = ({ onClose }): ReactElement => {
  const rules = useGameStore((state) => state.rules);
  const setRules = useGameStore((state) => state.setRules);

  const theme = useThemeStore((state) => state.theme);
  const toggleTheme = useThemeStore((state) => state.toggleTheme);

  return (
    <PopupMenu>
      <div className="settings-menu">
        <h1>Settings</h1>
        <div className="settings-menu-container">
          <div className="settings-menu-option">
            <ToggleSwitch
              checked={rules.useOrigin}
              onChange={(isChecked) =>
                setRules({ ...rules, useOrigin: isChecked })
              }
            />
            <h3>Enable origin guesses</h3>
          </div>

          <div className="settings-menu-option">
            <ToggleSwitch
              checked={rules.useDestination}
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
        </div>
        <button onClick={() => onClose()}>{"Done"}</button>
      </div>
    </PopupMenu>
  );
};

export default SettingsMenu;
