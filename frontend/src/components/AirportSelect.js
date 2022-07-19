import React, { useEffect, useState } from "react";
import { Box, Select } from "grommet";

// eslint-disable-next-line react/prop-types
const AirportSelect = ({ setAirport }) => {
  const [options, setOptions] = useState([]);
  const [filteredOptions, setFilteredOptions] = useState([]);
  const [search, setSearch] = useState(false);

  useEffect(() => {
    let request = new XMLHttpRequest();
    const path = "https://nhqos29571.execute-api.eu-west-1.amazonaws.com";

    request.onerror = function () {
      setOptions(["Failed to load"]);
    };
    request.ontimeout = function () {
      setOptions(["Failed to load"]);
    };
    request.onload = function () {
      if (request.status === 200) {
        if (request.response.status === 200) {
          setOptions(request.response.response);
        } else {
          setOptions(["Failed to load"]);
        }
      } else {
        setOptions(["Failed to load"]);
      }
    };

    request.timeout = 10000;
    request.responseType = "json";
    request.open("GET", path);
    request.send();
  }, []);

  const handleSearch = (text) => {
    setFilteredOptions([]);
    if (text.length < 3) {
      setSearch(false);
    } else {
      const exp = new RegExp(text, "i");
      setFilteredOptions(options.filter((o) => exp.test(o)));
      setSearch(true);
    }
  };

  const handleChange = (value) => {
    setAirport(value);
    setFilteredOptions([]);
    setSearch(false);
  };

  return (
    <Box direction="row" align="center">
      <Select
        options={search ? filteredOptions : []}
        onChange={(event) => handleChange(event.value)}
        onSearch={(text) => handleSearch(text)}
        placeholder="Search..."
      />
    </Box>
  );
};

export default AirportSelect;
