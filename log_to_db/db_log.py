"""Save logs to Database."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass
class DBLog:
    save_level: str
    pc_name: str
    program_name: str
    logs: dict = field(default_factory=lambda: dict())
    program_timezone = "America/Chicago"

    def load_log_levels(self) -> None:

        self.log_levels: Dict[str, int] = {
            "debug": 10,
            "info": 20,
            "warning": 30,
            "error": 40,
            "critical": 50,
        }

    def get_log_level(self, level_name) -> int:

        return self.log_levels.get(level_name, 20)

    def get_error_codes(self, code) -> str:
        error_codes = {
            0: "Successful.",
            -1: "Can't connect to database.",
            -2: "Can't write to database.",
            -3: "Invalid log message.",
            -4: "Invalid timezone.",
            -5: "Invalid folder path.",
            -6: "Invalid filename.",
            -99: "Invalid error code.",
        }

        return error_codes.get(code, "Invalid error code.")

    def log(self, level: str, message: str, details: Dict[str, Any]) -> None:
        """Log to file"""

        try:
            log_entry = datetime.now(ZoneInfo(self.program_timezone))
        except Exception as err:
            raise ZoneInfoNotFoundError(err)

        if self.get_log_level(level) >= self.get_log_level(self.save_level):
            self.logs.update(
                {
                    log_entry: {
                        "pc_name": self.pc_name,
                        "program_name": self.program_name,
                        "level": self.get_log_level(level),
                        "message": message,
                        "details": details,
                    }
                }
            )

    def debug(self, message: str, details: Dict[str, Any]) -> None:
        """Log debug to file"""

        self.log(
            level="debug",
            message=message,
            details=details,
        )

    def info(self, message: str, details: Dict[str, Any]) -> None:
        """Log info to file"""

        self.log(
            level="info",
            message=message,
            details=details,
        )

    def warning(self, message: str, details: Dict[str, Any]) -> None:
        """Log warning to file"""

        self.log(
            level="warning",
            message=message,
            details=details,
        )

    def error(self, message: str, details: Dict[str, Any]) -> None:
        """Log error to file"""

        self.log(
            level="error",
            message=message,
            details=details,
        )

    def critical(self, message: str, details: Dict[str, Any]) -> None:
        """Log critical to file"""

        self.log(
            level="critical",
            message=message,
            details=details,
        )
