from yaml import safe_load


# -----------------------------------------------------


def get_config() -> None:
    """Return the configuration file as a dict."""

    with open('config.yaml', 'r') as file:
        return safe_load(file)
