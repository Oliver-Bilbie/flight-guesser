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
