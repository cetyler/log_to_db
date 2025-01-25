import pytest
from db_logging.db_log import DBLog


@pytest.mark.parametrize(
        "level_name, level_value",
        [
            ("debug",10),
            ("info",20),
            ("warning",30),
            ("error",40),
            ("critical",50),
        ]
)
def test_log_levels(level_name, level_value):
    log = DBLog(
        save_level="debug",
        pc_name="test_pc",
        program_name="test_prog",
    )
    log.load_log_levels()

    assert level_value == log.get_log_level(level_name)
