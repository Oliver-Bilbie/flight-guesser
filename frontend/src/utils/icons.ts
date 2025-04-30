import L from "leaflet";
import flightIconUrl from "../assets/flight_icon.webp";
import originIconUrl from "../assets/origin_icon.webp";
import destinationIconUrl from "../assets/destination_icon.webp";

export const flightIcon = new L.Icon({
  iconUrl: flightIconUrl,
  iconSize: [50, 50],
  iconAnchor: [25, 25],
  popupAnchor: [0, -32],
});

export const originIcon = new L.Icon({
  iconUrl: originIconUrl,
  iconSize: [50, 50],
  iconAnchor: [25, 25],
  popupAnchor: [0, -32],
});

export const destinationIcon = new L.Icon({
  iconUrl: destinationIconUrl,
  iconSize: [50, 50],
  iconAnchor: [25, 25],
  popupAnchor: [0, -32],
});
