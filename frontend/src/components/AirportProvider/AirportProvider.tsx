import { FC, ReactElement, ReactNode, useEffect, useState } from "react";
import AirportContext from "./AirportContext";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner";
import {
  Airport,
  AirportApiResponse,
  emptyError,
  ErrorData,
} from "../../utils/types";
import { AIRPORTS_ENDPOINT } from "../../utils/endpoints";
import MessageDisplay from "../MessageDisplay/MessageDisplay";

interface AirportProviderProps {
  children?: ReactNode;
}

const AirportProvider: FC<AirportProviderProps> = ({
  children,
}): ReactElement => {
  const [airports, setAirports] = useState<Airport[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<ErrorData>(emptyError);

  async function getAirports() {
    try {
      const response = await fetch(AIRPORTS_ENDPOINT);

      if (response.ok) {
        const body: AirportApiResponse[] = await response.json();
        const airports: Airport[] = body.map((airport) => {
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
        setAirports(airports);
      } else {
        throw "API request was unsuccessful";
      }
    } catch (error) {
      setError({
        show: true,
        title: "Unable to load airports",
        message:
          "Something went wrong when trying to contact the server. Please try again later.",
        continueText: "Retry",
        onContinue: () => {
          setError(emptyError);
          getAirports();
        },
      });
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    getAirports();
  }, []);

  if (isLoading) {
    return <LoadingSpinner />;
  } else if (error.show) {
    return (
      <MessageDisplay
        title={error.title}
        message={error.message}
        continueText={error.continueText}
        onContinue={error.onContinue}
      />
    );
  } else {
    return (
      <AirportContext.Provider value={airports}>
        {children}
      </AirportContext.Provider>
    );
  }
};

export default AirportProvider;
