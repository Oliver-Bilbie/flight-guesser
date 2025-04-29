import { FC, ReactElement, ReactNode, useEffect, useState } from "react";
import AirportContext from "./AirportContext";
import { Airport } from "./types";
import { AIRPORTS_ENDPOINT } from "../../utils/endpoints";

interface AirportProviderProps {
  children?: ReactNode;
}

const AirportProvider: FC<AirportProviderProps> = ({
  children,
}): ReactElement => {
  const [airports, setAirports] = useState<Airport[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  async function getAirports() {
    try {
      const response = await fetch(AIRPORTS_ENDPOINT);
      const body = await response.json();
      const airports = body.map((airport: Airport) => {
        return {
          name: airport.name,
          iata: airport.iata,
          lat: airport.lat,
          lon: airport.lon,
        };
      });
      setAirports(airports);
    } catch (error) {
      setErrorMessage(String(error));
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    getAirports();
  }, []);

  if (isLoading) {
    return <h1>Loading airports...</h1>;
  } else if (errorMessage.length > 0) {
    return <h1>{errorMessage}</h1>;
  } else {
    return (
      <AirportContext.Provider value={airports}>
        {children}
      </AirportContext.Provider>
    );
  }
};

export default AirportProvider;
