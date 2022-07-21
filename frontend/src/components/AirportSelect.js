import React, { useState } from "react";
import { Box, Select, Text, Spinner } from "grommet";

// eslint-disable-next-line react/prop-types
const AirportSelect = ({ airports, setSelection }) => {
  const [filteredOptions, setFilteredOptions] = useState(airports);

  const handleSearch = (text) => {
    const exp = new RegExp(text, "i");
    // eslint-disable-next-line react/prop-types
    setFilteredOptions(airports.filter((o) => exp.test(o)));
  };

  return (
    <Box gap="small">
      <Text>Destination:</Text>
      <Box align="center">
        {
          // eslint-disable-next-line react/prop-types
          airports.length > 1 ? (
            <Select
              options={filteredOptions}
              onChange={(event) => setSelection(event.value)}
              onSearch={(text) => handleSearch(text)}
              placeholder="Search..."
            />
          ) : // eslint-disable-next-line react/prop-types
          airports.length === 0 ? (
            <Spinner />
          ) : (
            <Text>{airports[0]}</Text>
          )
        }
      </Box>
    </Box>
  );
};

export default AirportSelect;
