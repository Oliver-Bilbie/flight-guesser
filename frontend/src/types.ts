import { ReactElement } from "react";

export type AlertType = {
  message: string;
  show: boolean;
};

export type ResponseType = {
  message?: string;
  body?: string;
};

export type ResultType = {
  score: number;
  ids: string[];
  message: string;
};

export type FlightData = {
  id: string;
  aircraft: string;
  origin: string;
  destination: string;
  score: string;
};

export type PlayerData = {
  name: string;
  player_id: string;
  score: number;
};

export type SettingsType = {
  useOrigin: boolean;
  useDestination: boolean;
  dataSaver: boolean;
};

export type ButtonType = {
  label: string;
  icon: ReactElement;
  onClick: () => void;
};

export enum LobbyMode {
  hidden,
  join,
  create,
}
