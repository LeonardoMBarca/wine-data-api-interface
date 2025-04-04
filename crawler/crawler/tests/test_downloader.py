import os
from crawler import config

def test_check_link_exist():
    """Verifies that the link dictionary exists and contains URLs"""
    assert isinstance(config.CSV_LINKS, dict)
    assert len(config.CSV_LINKS) > 0

def test_check_link_config():
    """Check that all links start with http"""
    for nome, url in config.CSV_LINKS.items():
        assert url.startswith("http"), f"Invalid link to {nome}: {url}"

def test_check_path_download():
    """Ensures that the download directory is set correctly"""
    assert isinstance(config.DOWNLOAD_DIR, str)
    assert config.DOWNLOAD_DIR != ""

def test_check_log_config():
    """Checks that the log file is configured correctly"""
    assert isinstance(config.LOG_FILE, str)
    assert config.LOG_FILE.endswith(".log")
