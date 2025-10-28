import { FC, ReactElement, ReactNode, useEffect, useState } from "react";
import AirportContext from "./AirportContext";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner";
import { AIRPORTS_ENDPOINT } from "../../utils/endpoints";
import { Airport } from "../../utils/types";
import "./AirportProvider.css";

interface AirportProviderProps {
  children?: ReactNode;
}

const AirportProvider: FC<AirportProviderProps> = ({
  children,
}): ReactElement => {
  const [isLoading, setLoading] = useState<boolean>(true);
  const [isError, setIsError] = useState<boolean>(false);
  const [airports, setAirports] = useState<Airport[]>([]);

  useEffect(() => {
    fetch(AIRPORTS_ENDPOINT)
      .then((response) => {
        if (!response.ok) {
          throw new Error("The server was unable to process the request");
        }
        return response.json();
      })
      .then((response) => {
        setAirports(response);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Unexpected response from server", error);
        setIsError(true);
      });
  }, []);

  if (isError) {
    return (
      <div className="error-text-container">
        <h2>It was not possible to fetch airport data at this time.</h2>
        <h2>Please try again later.</h2>
      </div>
    );
  }

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <AirportContext.Provider value={airports}>
      {children}
    </AirportContext.Provider>
  );
};

export default AirportProvider;
