import { Icon } from "leaflet";
import { ReactElement } from "react";

export type Position = {
  lon: number;
  lat: number;
};

export type Rules = {
  useOrigin: boolean;
  useDestination: boolean;
};

export type Airport = {
  name: string;
  city: string | null;
  iata: string | null;
  icao: string | null;
  position: Position | null;
};

export type AirportApiResponse = {
  name: string;
  country: string;
  iata: string;
  icao: string;
  lon: number;
  lat: number;
};

export type Points = {
  origin: number;
  destination: number;
  total: number;
};

export type Flight = {
  id: string;
  flight_number: string | null;
  callsign: string | null;
  airline: string | null;
  aircraft_type: string | null;
  aircraft_registration: string | null;
  image_src: string | null;
  origin: Airport | null;
  destination: Airport | null;
  position: Position | null;
};

export type FlightApiResponse = {
  points: Points;
  flight: Flight;
};

export type FlightApiError = {
  message: string;
};

export type MapMarker = {
  label: ReactElement;
  position: Position;
  icon: Icon;
};

export type ErrorData = {
  show: boolean;
  title: string;
  message: string;
  continueText: string;
  onContinue: () => void;
};
