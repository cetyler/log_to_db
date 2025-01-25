import json
from typing import Any, Dict


class Encoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, set):
            return tuple(o)
        elif isinstance(o, str):
            return o.encode("unicode_escape").decode("ascii")
        return super().default(o)


class StructuredMessage:
    def __init__(self, message: str, **kwargs: Any):
        self.message: Dict[str, str] = {"message": message}
        self.kwargs: Dict[str, Any] = kwargs

    def __str__(self) -> str:
        self.message.update(self.kwargs)
        s = Encoder().encode(self.message)
        return "%s" % (s)


m = StructuredMessage  # optional, to improve readability
