import React, { ReactElement } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./MapDisplay.css";
import { destinationIcon, flightIcon, originIcon } from "../../utils/icons";
import { Airport, MapMarker, Flight } from "../../utils/types";

interface MapDisplayProps {
  flight: Flight;
}

const formatAirportLabel = (airport: Airport): string => {
  const code = airport.iata ?? airport.icao ?? "unknown code";
  return `${airport.name} (${code})`;
};

const getLabelElement = (title: string, body: string): ReactElement => {
  return (
    <div className="map-label-body">
      <h3>{title}</h3>
      <p>{body}</p>
    </div>
  );
};

const MapDisplay: React.FC<MapDisplayProps> = ({ flight }): ReactElement => {
  const markers: MapMarker[] = [];

  if (flight.position?.lon && flight.position?.lon) {
    markers.push({
      label: getLabelElement(
        "Aircraft",
        `${flight.aircraft_type} (${flight.callsign})`,
      ),
      position: flight.position,
      icon: flightIcon,
    });
  }

  if (flight.origin?.position?.lon && flight.origin?.position?.lat) {
    markers.push({
      label: getLabelElement("Origin", formatAirportLabel(flight.origin)),
      position: flight.origin.position,
      icon: originIcon,
    });
  }

  if (flight.destination?.position?.lon && flight.destination?.position?.lat) {
    markers.push({
      label: getLabelElement(
        "Destination",
        formatAirportLabel(flight.destination),
      ),
      position: flight.destination.position,
      icon: destinationIcon,
    });
  }

  if (markers.length === 0) {
    return (
      <div className="map-placeholder">
        <h4>Map data is unavailable for this flight</h4>
      </div>
    );
  }

  return (
    <MapContainer
      className="map-display"
      bounds={markers.map(
        ({ position }) => [position.lat, position.lon] as [number, number],
      )}
      boundsOptions={{
        padding: [40, 40],
        maxZoom: 12,
      }}
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {markers.map((marker, idx) => (
        <Marker
          key={idx}
          position={[marker.position.lat, marker.position.lon]}
          icon={marker.icon}
        >
          <Popup>
            <h4 className="map-label-text">{marker.label}</h4>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapDisplay;
