import { FC, ReactElement, ReactNode } from "react";
import "./HideMenu.css";

interface HideMenuProps {
  isHidden: boolean;
  children: ReactNode;
}

const HideMenu: FC<HideMenuProps> = ({ isHidden, children }): ReactElement => {
  return (
    <div className={`hide-menu ${isHidden ? "hidden" : "visible"}`}>
      {children}
    </div>
  );
};

export default HideMenu;
