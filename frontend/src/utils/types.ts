export type Rules = {
  useOrigin: boolean;
  useDestination: boolean;
};

export type Airport = {
  name: string;
  iata: string;
  lon: number;
  lat: number;
};
