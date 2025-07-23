import { Position } from "./types";

export function geodesicMidpoint(pos1: Position, pos2: Position): Position {
  const toRad = (deg: number) => (deg * Math.PI) / 180;
  const toDeg = (rad: number) => (rad * 180) / Math.PI;

  const lat1 = toRad(pos1.lat);
  const lon1 = toRad(pos1.lon);
  const lat2 = toRad(pos2.lat);
  const lon2 = toRad(pos2.lon);

  const dLon = lon2 - lon1;

  const Bx = Math.cos(lat2) * Math.cos(dLon);
  const By = Math.cos(lat2) * Math.sin(dLon);

  const lat3 = Math.atan2(
    Math.sin(lat1) + Math.sin(lat2),
    Math.sqrt((Math.cos(lat1) + Bx) ** 2 + By ** 2),
  );
  const lon3 = lon1 + Math.atan2(By, Math.cos(lat1) + Bx);

  return {
    lat: toDeg(lat3),
    lon: toDeg(lon3),
  };
}
