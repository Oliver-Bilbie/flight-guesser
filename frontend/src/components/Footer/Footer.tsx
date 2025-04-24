import { FC, ReactElement, useState } from "react";
import "./Footer.css";
import PopupMenu from "../PopupMenu/PopupMenu";
import Changelog from "../Changelog/Changelog";

const Footer: FC = (): ReactElement => {
  const [showChanges, setShowChanges] = useState(false);

  return (
    <div className="footer">
      <h4>Version: {APP_VERSION}</h4>
      <span className="text-button" onClick={() => setShowChanges(true)}>
        What's new?
      </span>

      {showChanges && (
        <PopupMenu onClose={() => setShowChanges(false)}>
          <div className="footer-changelog">
            <Changelog />
          </div>
        </PopupMenu>
      )}
    </div>
  );
};

export default Footer;
