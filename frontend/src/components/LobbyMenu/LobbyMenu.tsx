import React from "react";
import { Box, FormField, TextInput } from "grommet";
import { LobbyMode, ResponseType } from "../../types";
import PopupMenu from "../PopupMenu/PopupMenu";
import { callApi } from "../../helpers/callApi";
import { LOBBY_ENDPOINT } from "../../config";
import { Group, LinkPrevious } from "grommet-icons";

interface LobbyMenuProps {
  mode: LobbyMode;
  score: number;
  rules: number;
  guessedFlights: string[];
  setLobbyId: (id: string) => void;
  onJoinLobby: (response: ResponseType) => void;
  onCreateLobby: (response: ResponseType) => void;
  lockSettings: () => void;
  onClose: () => void;
}

const LobbyMenu: React.FC<LobbyMenuProps> = ({
  mode,
  score,
  rules,
  guessedFlights,
  setLobbyId,
  onJoinLobby,
  onCreateLobby,
  lockSettings,
  onClose,
}): React.ReactElement => {
  const [inputs, setInputs] = React.useState({
    name: { value: "", validationMsg: "" },
    lobbyId: { value: "", validationMsg: "" },
  });

  const handleSubmit = (): void => {
    const nameValidation = validateName(inputs.name.value);
    const idValidation = validateId(inputs.lobbyId.value, mode);
    setInputs({
      name: { ...inputs.name, validationMsg: nameValidation },
      lobbyId: { ...inputs.lobbyId, validationMsg: idValidation },
    });

    if (nameValidation === "" && idValidation === "") {
      lockSettings();
      setLobbyId(inputs.lobbyId.value);
      callApi(
        LOBBY_ENDPOINT,
        mode === LobbyMode.join ? "POST" : "PUT",
        `{` +
          `"name": "${inputs.name.value}",` +
          `"score": ${score},` +
          `"guessed_flights": "${guessedFlights}"` +
          `${
            mode === LobbyMode.join
              ? `,"lobby_id": "${inputs.lobbyId.value}"`
              : `,"rules": ${rules}`
          }` +
          `}`,
        mode === LobbyMode.join ? onJoinLobby : onCreateLobby
      );
      onClose();
    }
  };

  const validateName = (name: string): string => {
    let message = "";
    if (name.length === 0) {
      message = "Required";
    } else if (name.length > 16) {
      message = "Too long";
    }

    return message;
  };

  const validateId = (lobbyId: string, mode: LobbyMode): string => {
    let message = "";
    if (lobbyId.length !== 4 && mode === LobbyMode.join) {
      message = "Must be four characters";
    }

    return message;
  };

  return (
    <PopupMenu
      body={
        <Box>
          <FormField label="Name" error={inputs.name.validationMsg}>
            <TextInput
              name="name-input"
              placeholder="Appears to other players"
              value={inputs.name.value}
              onChange={(event): void =>
                setInputs({
                  ...inputs,
                  name: {
                    ...inputs.name,
                    value: event.target.value,
                  },
                })
              }
            />
          </FormField>
          {mode === LobbyMode.join && (
            <FormField label="Lobby ID" error={inputs.lobbyId.validationMsg}>
              <TextInput
                name="lobby-input"
                placeholder="Lobby to join"
                value={inputs.lobbyId.value}
                onChange={(event): void =>
                  setInputs({
                    ...inputs,
                    lobbyId: {
                      ...inputs.lobbyId,
                      value: event.target.value.toUpperCase(),
                    },
                  })
                }
              />
            </FormField>
          )}
        </Box>
      }
      buttons={[
        {
          label: mode === LobbyMode.join ? "Join" : "Create",
          icon: <Group color="text" />,
          onClick: handleSubmit,
        },
        {
          label: "Back",
          icon: <LinkPrevious color="text" />,
          onClick: onClose,
        },
      ]}
    />
  );
};

export default LobbyMenu;
