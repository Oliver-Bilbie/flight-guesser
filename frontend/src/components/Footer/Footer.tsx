import { FC, ReactElement, useState } from "react";
import "./Footer.css";
import PopupMenu from "../PopupMenu/PopupMenu";
import Changelog from "../Changelog/Changelog";
import SettingsButton from "../SettingsButton/SettingsButton";
import SettingsMenu from "../SettingsMenu/SettingsMenu";

const Footer: FC = (): ReactElement => {
  const [showChanges, setShowChanges] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div className="footer">
      <div className="footer-text">
        <h4>Version: {APP_VERSION}</h4>
        <span className="text-button" onClick={() => setShowChanges(true)}>
          What's new?
        </span>
      </div>

      <div className="footer-settings-button">
        <SettingsButton onClick={() => setShowSettings(true)} />
      </div>

      {showChanges && (
        <PopupMenu onClose={() => setShowChanges(false)}>
          <div className="footer-changelog">
            <Changelog />
          </div>
        </PopupMenu>
      )}

      {showSettings && (
        <PopupMenu>
          <div className="footer-settings-menu">
            <SettingsMenu onClose={() => setShowSettings(false)} />
          </div>
        </PopupMenu>
      )}
    </div>
  );
};

export default Footer;
