export const settingsToRules = (
  useOrigin: boolean,
  useDestination: boolean
): number => {
  const origin_value = useOrigin ? 1 : 0;
  const desintation_value = useDestination ? 2 : 0;

  const rules_value = origin_value + desintation_value;

  return rules_value;
};

export const rulesToSettings = (
  rules: number
): { useOrigin: boolean; useDestination: boolean } => {
  const origin = rules % 2 === 1;
  const destination = Math.floor(rules / 2) === 1;

  const settings_values = {
    useOrigin: origin,
    useDestination: destination,
  };

  return settings_values;
};
