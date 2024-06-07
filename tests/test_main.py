import pytest
from src.helloworld import app


def test_main():
    result = app.main()
    assert result.formal_name == "AeroFuel", "The title of the main function should be 'G-VII Fuel Calculator'"
    assert result.app_id == "org.hdgs.helloworld", "The org_id of the main function should be 'org.hdgs.helloworld'"