import { FC, ReactElement } from "react";
import "./Changelog.css";
import changelog_file from "../../assets/CHANGELOG.md?raw";
import ReactMarkdown from "react-markdown";

const Changelog: FC = (): ReactElement => {
  return (
    <div className="changelog-container">
      <ReactMarkdown children={changelog_file} />
    </div>
  );
};

export default Changelog;
