import yaml

config_rules = {
    'max_read_calendars': {'types': [int, type(None)]},
    'max_read_events': {'types': [int, type(None)]},

    'search_events': {'types': [int, float], 'min': 1},
    'refresh_events': {'types': [int, float], 'min': 300},

    'rule_market': {'types': [str]}
}


def load_config(path='config.yaml'):
    with open(path) as f:
        yml = yaml.safe_load(f)

        for key, rule in config_rules.items():
            # Membership check
            if not key in yml:
                raise KeyError(f'Key "{key}" in cfg.yaml not found.')

            v = yml[key]

            # Type check
            if (ty := type(v)) not in rule['types']:
                raise TypeError(f'Key "{key}" is {ty}, expected any of {rule["types"]}')

            # Interval check
            if ty in (int, float) and not (mi := rule.get('min', 0)) < v < (ma := rule.get('max', float('inf'))):
                raise ValueError(f'Key "{key} with value {v} must be higher than {mi} and lower than {ma}.')
        else:
            return yml


