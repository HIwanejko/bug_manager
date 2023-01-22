import os


def get_env(var, default=None) -> str:
    if default is None:
        try:
            return os.environ[var]
        except KeyError:
            raise KeyError(f"Env var: '{var}' is not set")
    return os.environ.get(var, default)
