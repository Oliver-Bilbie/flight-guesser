import React, { useState, useEffect } from "react";
import { Box, Select, Text, Spinner } from "grommet";

interface AirportSelectProps {
  label: string;
  value: string;
  airports: string[];
  setSelection: (selection: string) => void;
}

const AirportSelect: React.FC<AirportSelectProps> = ({
  label,
  value,
  airports,
  setSelection,
}): React.ReactElement => {
  const [filteredOptions, setFilteredOptions] = useState(airports);

  useEffect(() => {
    setFilteredOptions(airports);
  }, [airports]);

  const handleSearch = (text): void => {
    const exp = new RegExp(text, "i");
    setFilteredOptions(airports.filter((o) => exp.test(o)));
  };

  return (
    <Box gap="small">
      <Text>{label}</Text>
      <Box align="center">
        {airports.length > 1 ? (
          <Select
            value={value}
            options={filteredOptions}
            onChange={(event): void => setSelection(event.value)}
            onSearch={(text): void => handleSearch(text)}
            placeholder="Select"
            searchPlaceholder="Search..."
          />
        ) : airports.length === 0 ? (
          <Spinner a11yTitle="loading" />
        ) : (
          <Text>{airports[0]}</Text>
        )}
      </Box>
    </Box>
  );
};

export default AirportSelect;
