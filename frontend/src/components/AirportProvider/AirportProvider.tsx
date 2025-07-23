import { FC, ReactElement, ReactNode } from "react";
import AirportContext from "./AirportContext";
import { Airport, AirportApiResponse } from "../../utils/types";
import airportData from "../../../public/airports.json";

interface AirportProviderProps {
  children?: ReactNode;
}

const AirportProvider: FC<AirportProviderProps> = ({
  children,
}): ReactElement => {
  const airports: Airport[] = airportData.map((airport: AirportApiResponse) => {
    return {
      name: airport.name,
      iata: airport.iata,
      position: {
        lat: airport.lat,
        lon: airport.lon,
      },
      icao: airport.icao,
      country: airport.country,
      city: null,
    };
  });

  return (
    <AirportContext.Provider value={airports}>
      {children}
    </AirportContext.Provider>
  );
};

export default AirportProvider;
