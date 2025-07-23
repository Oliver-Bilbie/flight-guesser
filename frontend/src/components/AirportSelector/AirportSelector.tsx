import { FC, ReactElement, useContext } from "react";
import "./AirportSelector.css";
import Selector from "../Selector/Selector";
import AirportContext from "../AirportProvider/AirportContext";
import { Airport } from "../../utils/types";

interface AirportSelectorProps {
  onSelect: (airport: Airport) => void;
}

const AirportSelector: FC<AirportSelectorProps> = ({
  onSelect,
}): ReactElement => {
  const airports = useContext(AirportContext);

  return (
    <div className="airport-selector">
      <Selector
        items={airports}
        displayItem={(airport) => airport.name}
        onSelect={onSelect}
      />
    </div>
  );
};

export default AirportSelector;
