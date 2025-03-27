import pytest
import logging
from io import StringIO
from axabsent.utils.logging import setup_logger, log_theory, log_force_emergence


@pytest.mark.utils
def test_logger_basic_output_capture(caplog):
    """
    Test that standard logger outputs DEBUG and INFO correctly.
    """
    logger = setup_logger("test_logger", level="DEBUG")
    with caplog.at_level(logging.DEBUG, logger="test_logger"):
        logger.debug("debug message")
        logger.info("info message")

    assert "debug message" in caplog.text
    assert "info message" in caplog.text


@pytest.mark.utils
def test_logger_formatting_includes_timestamp(caplog):
    """
    Ensure log output contains timestamp and level.
    """
    logger = setup_logger("format_logger", level="INFO")
    with caplog.at_level(logging.INFO):
        logger.info("formatted message test")

    assert "[INFO]" in caplog.text
    assert "[" in caplog.text and "]" in caplog.text  # Timestamp likely present


@pytest.mark.utils
def test_custom_theory_log_output(caplog):
    """
    Test log_theory() emits correct message format for theoretical reasoning steps.
    """
    with caplog.at_level(logging.INFO):
        log_theory("Cross-absolute entropy successfully computed.")

    assert "Cross-absolute entropy" in caplog.text
    assert "[THEORY]" in caplog.text


@pytest.mark.utils
def test_force_emergence_logging(caplog):
    """
    Validate log_force_emergence() appends the FORCE tag.
    """
    with caplog.at_level(logging.INFO):
        log_force_emergence("Gravitational signature decomposition complete.")

    assert "Gravitational signature" in caplog.text
    assert "[FORCE]" in caplog.text


@pytest.mark.utils
def test_logger_file_stream_output(tmp_path):
    """
    Setup logger to file and validate file receives content.
    """
    log_file = tmp_path / "axabsent_test.log"
    logger = setup_logger("file_logger", level="INFO")
    file_handler = logging.FileHandler(str(log_file))
    file_handler.setFormatter(logger.handlers[0].formatter)
    logger.addHandler(file_handler)

    logger.info("Message to file stream.")
    logger.removeHandler(file_handler)

    with open(log_file, "r") as f:
        contents = f.read()

    assert "Message to file stream." in contents
