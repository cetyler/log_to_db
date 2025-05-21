import pytest

from log_to_db.db_log import DBLog


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

@pytest.mark.parametrize(
    "code, code_text",
    [
        (0,"Successful."),
        (-1,"Can't connect to database."),
        (-2,"Can't write to database."),
        (-3,"Invalid log message."),
        (-4,"Invalid timezone."),
        (-5,"Invalid folder path."),
        (-6,"Invalid filename."),
        (-99,"Invalid error code."),
        (9999,"Invalid error code."),
    ]
)
def test_get_error_codes(code,code_text):
    log = DBLog(
        save_level="debug",
        pc_name="test_pc",
        program_name="test_prog",
    )

    assert code_text == log.get_error_codes(code)

@pytest.mark.parametrize(
    "level,message,details,save_level",
    [
        ("debug","test message.",dict(test="test details"),"debug"),
        ("debug","test message.",dict(test="test details"),"info"),
        ("debug","test message.",dict(test="test details"),"warning"),
        ("debug","test message.",dict(test="test details"),"error"),
        ("debug","test message.",dict(test="test details"),"critical"),
        ("info", "test message.", dict(test="test details"), "debug"),
        ("info", "test message.", dict(test="test details"), "info"),
        ("info", "test message.", dict(test="test details"), "warning"),
        ("info", "test message.", dict(test="test details"), "error"),
        ("info", "test message.", dict(test="test details"), "critical"),
        ("warning","test message.",dict(test="test details"),"debug"),
        ("warning","test message.",dict(test="test details"),"info"),
        ("warning","test message.",dict(test="test details"),"warning"),
        ("warning","test message.",dict(test="test details"),"error"),
        ("warning","test message.",dict(test="test details"),"critical"),
        ("error","test message.",dict(test="test details"),"debug"),
        ("error","test message.",dict(test="test details"),"info"),
        ("error","test message.",dict(test="test details"),"warning"),
        ("error","test message.",dict(test="test details"),"error"),
        ("error","test message.",dict(test="test details"),"critical"),
        ("critical","test message.",dict(test="test details"),"debug"),
        ("critical","test message.",dict(test="test details"),"info"),
        ("critical","test message.",dict(test="test details"),"warning"),
        ("critical","test message.",dict(test="test details"),"error"),
        ("critical","test message.",dict(test="test details"),"critical"),
    ]
)
def test_log(level,message,details,save_level):
    log = DBLog(
        save_level=save_level,
        pc_name="test_pc",
        program_name="test_prog",
    )
    log.load_log_levels()
    log.log(level,message,details)

    if log.get_log_level(level) >= log.get_log_level(save_level):
        for log_entry in log.logs.values():
            assert log_entry["pc_name"] == "test_pc"
            assert log_entry["program_name"] == "test_prog"
            assert log_entry["level"] == log.get_log_level(level)
            assert log_entry["message"] == message
            assert log_entry["details"] == details
    else:
        assert log.logs == dict()
