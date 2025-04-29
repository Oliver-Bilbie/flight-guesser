import { FC, ReactElement, useContext } from "react";
import "./AirportSelector.css";
import Selector from "../Selector/Selector";
import AirportContext from "../AirportProvider/AirportContext";
import { Airport } from "../../utils/types";

interface AirportSelectorProps {
  onSelect: (airportName: string) => void;
}

const AirportSelector: FC<AirportSelectorProps> = ({
  onSelect,
}): ReactElement => {
  const airports = useContext(AirportContext);
  const airportNames = airports.map((airport) => airport.name);

  return (
    <div className="airport-selector">
      <Selector items={airportNames} onSelect={onSelect} />
    </div>
  );
};

export default AirportSelector;
