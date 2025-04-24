import { FC, ReactElement } from "react";
import "./Header.css";

const Header: FC = (): ReactElement => {
  return (
    <header className="header">
      <h1 className="light-text">Flight Guesser</h1>
    </header>
  );
};

export default Header;
