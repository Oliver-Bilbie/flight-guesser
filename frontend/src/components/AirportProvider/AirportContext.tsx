import { createContext } from "react";
import { Airport } from "../../utils/types";

const AirportContext = createContext<Airport[]>([]);

export default AirportContext;
