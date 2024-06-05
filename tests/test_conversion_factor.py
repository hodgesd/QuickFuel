import toga
from toga.style import Pack

from helloworld.app import HelloWorld


def dummy_callback(widget):
    pass


def test_toggle_conversion_factor_to_liters():
    # Initialize the app
    app = HelloWorld("HelloWorld", "1")

    # Create the switch
    app.is_liters = toga.Switch("Gals", on_change=app.toggle_conversion_factor)

    # Set the switch to True (simulate toggling to liters)
    app.is_liters.value = True

    # Call the method to be tested
    app.toggle_conversion_factor(app.is_liters)

    # Assert that the conversion factor and fuel volume label have been updated correctly
    assert app.conversion_factor == app.LITRE_CONVERSION_FACTOR
    assert app.fuel_volume_label == "liters"


def test_toggle_conversion_factor_to_gals():
    # Initialize the app
    app = HelloWorld("HelloWorld", "1")

    # Create the switch
    app.is_liters = toga.Switch("Gals", on_change=app.toggle_conversion_factor)

    # Set the switch to False (simulate toggling to gals)
    app.is_liters.value = False

    # Call the method to be tested
    app.toggle_conversion_factor(app.is_liters)

    # Assert that the conversion factor and fuel volume label have been updated correctly
    assert app.conversion_factor == app.GALLON_CONVERSION_FACTOR
    assert app.fuel_volume_label == "gals"


def test_toggle_conversion_factor_updates_display():
    # Initialize the app
    app = HelloWorld("HelloWorld", "1")

    # Create the switch and slider
    app.is_liters = toga.Switch("Gals", on_change=app.toggle_conversion_factor)
    app.fuel_slider = toga.Slider(min=5000, max=41500, value=10000, on_change=dummy_callback)
    app.starting_slider = toga.Slider(min=4000, max=15000, value=5000, on_change=dummy_callback)
    app.delta_volume_label = toga.Label("0", style=Pack())
    app.fuel_label_weight = toga.Label("0 lbs", style=Pack())
    app.fuel_label_volume = toga.Label("0 gals", style=Pack())

    # Set the switch to True (simulate toggling to liters)
    app.is_liters.value = True

    # Call the method to be tested
    app.toggle_conversion_factor(app.is_liters)

    # Assert that the conversion factor and fuel volume label have been updated correctly
    assert app.conversion_factor == app.LITRE_CONVERSION_FACTOR
    assert app.fuel_volume_label == "liters"

    # Check if the display has been updated
    assert app.delta_volume_label.text == f"{(app.fuel_slider.value - app.starting_slider.value) / app.conversion_factor:,.0f} liters"
    assert app.fuel_label_weight.text == f"{app.fuel_slider.value:,.0f} lbs"
    assert app.fuel_label_volume.text == f"{app.fuel_slider.value / app.conversion_factor:,.0f} liters"


if __name__ == '__main__':
    test_toggle_conversion_factor_to_liters()
    test_toggle_conversion_factor_to_gals()
    test_toggle_conversion_factor_updates_display()
    print("All tests passed!")
