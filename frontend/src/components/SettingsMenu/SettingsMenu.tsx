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
} from "grommet";
import { Close, Globe, Launch } from "grommet-icons";
import { SettingsType } from "../../types";
import PopupMenu from "../PopupMenu/PopupMenu";

interface SettingsMenuProps {
  settingsValues: SettingsType;
  setSettingsValues: (values: SettingsType) => void;
  onClose: () => void;
}

const SettingsMenu: React.FC<SettingsMenuProps> = ({
  settingsValues,
  setSettingsValues,
  onClose,
}): React.ReactElement => {
  const settingsItems = [
    {
      label: "Guess Origin",
      key: "useOrigin",
      value: settingsValues.useOrigin,
      setValue: (value: boolean): void =>
        setSettingsValues({ ...settingsValues, useOrigin: value }),
    },
    {
      label: "Guess Destination",
      key: "useDestination",
      value: settingsValues.useDestination,
      setValue: (value: boolean): void =>
        setSettingsValues({ ...settingsValues, useDestination: value }),
    },
    {
      label: "Data Saver",
      key: "dataSaver",
      value: settingsValues.dataSaver,
      setValue: (value: boolean): void =>
        setSettingsValues({ ...settingsValues, dataSaver: value }),
    },
  ];

  const [showAlert, setShowAlert] = React.useState(false);

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
        {settingsItems.map((item) => (
          <Box pad="xsmall" direction="row" key={item.key}>
            <CheckBox
              label={item.label}
              checked={item.value}
              onChange={(event): void => item.setValue(event.target.checked)}
              toggle
              fill
              reverse
            />
          </Box>
        ))}
      </CardBody>
      <CardFooter pad="small" background="light-2">
        <Button
          label="Create Lobby"
          icon={<Launch />}
          onClick={(): void => setShowAlert(true)}
        />
        <Button
          label="Join Lobby"
          icon={<Globe />}
          onClick={(): void => setShowAlert(true)}
        />
      </CardFooter>
      {showAlert && (
        <PopupMenu
          message="Coming soon"
          onClose={(): void => setShowAlert(false)}
        />
      )}
    </Card>
  );
};

export default SettingsMenu;
