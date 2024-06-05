import pytest
from helloworld import app

# Mocking the toga.App for the tests
class MockApp:
    def __init__(self):
        self.starting_label_lbs = MockStarLabelLbs()
        self.starting_slider = MockSlider()

    def update_fuel_display(self):
        pass


# Mocking the starting label lbs and slider for the tests
class MockStarLabelLbs:
    def __init__(self):
        self.text = ""


class MockSlider:
    def __init__(self):
        self.value = 0

    def set(self, new_value):
        self.value = new_value

# Complete test case setup

def test_on_starting_slider_change():
    # Arrange
    sut = app.HelloWorld("Hello World", "com.example.helloworld")
    sut.starting_label_lbs = MockStarLabelLbs()
    sut.starting_slider = MockSlider()
    sut.starting_slider.set(3500)

    # Act
    sut.on_starting_slider_change(None)

    # Assert
    assert sut.starting_label_lbs.text == "3,500 lbs"

def test_on_starting_slider_change_zero():
    # Arrange
    sut = app.HelloWorld("Hello World", "com.example.helloworld")
    sut.starting_label_lbs = MockStarLabelLbs()
    sut.starting_slider = MockSlider()
    sut.starting_slider.set(0)

    # Act
    sut.on_starting_slider_change(None)

    # Assert
    assert sut.starting_label_lbs.text == "0 lbs"