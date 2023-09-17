import React from "react";
import {
  Box,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CheckBox,
  Heading,
  Button,
  Text,
} from "grommet";
import { CircleInformation, Close, Globe, Launch } from "grommet-icons";

import { LobbyMode, SettingsType } from "../../types";

interface SettingsMenuProps {
  settingsValues: SettingsType;
  locked: boolean;
  setSettingsValues: (values: SettingsType) => void;
  setShowLobbyMenu: (setting: LobbyMode) => void;
  onClose: () => void;
}

const SettingsMenu: React.FC<SettingsMenuProps> = ({
  settingsValues,
  locked,
  setSettingsValues,
  setShowLobbyMenu,
  onClose,
}): React.ReactElement => {
  const settingsItems = [
    {
      label: "Guess Origin",
      key: "useOrigin",
      value: settingsValues.useOrigin,
      locked: locked,
      setValue: (value: boolean): void =>
        setSettingsValues({ ...settingsValues, useOrigin: value }),
    },
    {
      label: "Guess Destination",
      key: "useDestination",
      value: settingsValues.useDestination,
      locked: locked,
      setValue: (value: boolean): void =>
        setSettingsValues({ ...settingsValues, useDestination: value }),
    },
    {
      label: "Data Saver",
      key: "dataSaver",
      value: settingsValues.dataSaver,
      locked: false,
      setValue: (value: boolean): void =>
        setSettingsValues({ ...settingsValues, dataSaver: value }),
    },
  ];

  return (
    <Card>
      <CardHeader
        pad={{ horizontal: "small", vertical: "xxsmall" }}
        background="brand"
      >
        <Heading level="3" color="text-strong">
          Settings
        </Heading>
        <Button icon={<Close color="text-strong" />} onClick={onClose} />
      </CardHeader>
      <CardBody pad="small" background="light-2">
        {locked && (
          <Box
            pad={{ horizontal: "small", vertical: "medium" }}
            direction="column"
            width="medium"
            align="center"
          >
            <CircleInformation size="medium" />
            <Text textAlign="center">
              Some settings have been disabled because you are currently in a
              multiplayer lobby
            </Text>
          </Box>
        )}
        {settingsItems.map((item) => (
          <Box pad="xsmall" direction="row" key={item.key}>
            <CheckBox
              label={item.label}
              checked={item.value}
              onChange={(event): void => item.setValue(event.target.checked)}
              disabled={item.locked}
              toggle
              fill
              reverse
            />
          </Box>
        ))}
      </CardBody>
      <CardFooter pad="small" background="light-2">
        <button
          className="custom-button"
          onClick={(): void => setShowLobbyMenu(LobbyMode.create)}
        >
          <Launch color="text" />
          <div className="pad" />
          <h4>Create Lobby</h4>
        </button>
        <button
          className="custom-button"
          onClick={(): void => setShowLobbyMenu(LobbyMode.join)}
        >
          <Globe color="text" />
          <div className="pad" />
          <h4>Join Lobby</h4>
        </button>
      </CardFooter>
    </Card>
  );
};

export default SettingsMenu;
