import { FC, ReactElement } from "react";
import "./FlightCard.css";
import { Flight } from "../../utils/types";

interface FlightCardProps {
  flight: Flight;
}

const FlightCard: FC<FlightCardProps> = ({ flight }): ReactElement => {
  return (
    <div className="flight-card">
      {flight.image_src && (
        <img
          src={flight.image_src}
          alt={`${flight.aircraft_type} image`}
          className="flight-image"
        />
      )}
      <div className="flight-content">
        <h2>
          {flight.callsign} ({flight.aircraft_registration})
        </h2>
        <p>
          <strong>Aircraft:</strong> {flight.aircraft_type}
        </p>
        <p>
          <strong>Airline:</strong> {flight.airline}
        </p>
        {flight.origin ? (
          <p>
            <strong>Origin:</strong> {flight.origin.name}, {flight.origin.city}{" "}
            ({flight.origin.iata})
          </p>
        ) : (
          <p className="muted">No origin available</p>
        )}
        {flight.destination ? (
          <p>
            <strong>Destination:</strong> {flight.destination.name},{" "}
            {flight.destination.city} ({flight.destination.iata})
          </p>
        ) : (
          <p className="muted">No destination available</p>
        )}
      </div>
    </div>
  );
};

export default FlightCard;
