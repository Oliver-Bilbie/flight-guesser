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
  country: string | null;
  iata: string | null;
  icao: string | null;
  position: Position | null;
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

export type FlightMessageResponse = {
  points: Points;
  flight: Flight;
  status: SuccessStatus;
  score: number;
};

export type FlightApiError = {
  message: string;
};

export type MapMarker = {
  label: ReactElement;
  position: Position;
  icon: Icon;
};

export type Message = {
  title: string;
  message: string;
};

const successStatusValues = ["Success", "AlreadyGuessed", "PointsUnavailable"];

export type SuccessStatus =
  (typeof successStatusValues)[keyof typeof successStatusValues];

export function isSuccessStatus<T>(status: T) {
  if (typeof status !== "string") {
    return false;
  }
  return Object.values(successStatusValues).includes(status);
}

const errorStatusValues = [
  "ValidationError",
  "LocationError",
  "ClientError",
  "ApiError",
  "ServerError",
];

export type ErrorStatus =
  (typeof errorStatusValues)[keyof typeof errorStatusValues];

export function isErrorStatus<T>(status: T) {
  if (typeof status !== "string") {
    return false;
  }
  return Object.values(errorStatusValues).includes(status);
}

export type GuessResponse = {
  status: "Ready" | "Loading" | SuccessStatus | ErrorStatus;
  value: FlightApiResponse | null;
  error: Message | null;
};

export type LobbyStatus = "Ready" | "NotInLobby" | "Loading" | "Error";

export type LobbyResponse = {
  status: LobbyStatus;
  error: Message | null;
};

export const defaultRules: Rules = { useOrigin: true, useDestination: true };

export const zeroPoints: Points = {
  origin: 0,
  destination: 0,
  total: 0,
};

export type PlayerData = {
  player_name: string;
  score: number;
  guess_count: number;
};

export type LobbyApiResponse = {
  event: "lobby_joined";
  lobby: string;
  rules: { use_origin: boolean; use_destination: boolean };
  player_name: string;
  score: number;
  players: PlayerData[];
};
