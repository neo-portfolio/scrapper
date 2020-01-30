import os
from typing import List
from exceptions import InvalidEnvError


def check_env(variables: List[str]) -> None:
    for v in variables:
        if os.getenv(v) is None:
            raise InvalidEnvError(v)
