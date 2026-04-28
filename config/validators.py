import os

def validate_env_vars(*var_names: str) -> None:
    """
    Checks that all provided environment variable names are set and non-empty.
    Collects ALL failures and raises a single ValueError listing every missing
    or empty variable, so you can fix them all in one pass.
    """
    missing = [
        name for name in var_names
        if not os.getenv(name, "").strip()
    ]

    if missing:
        formatted = "\n  - ".join(missing)
        raise ValueError(
            f"The following environment variables are missing or empty:\n  - {formatted}"
        )