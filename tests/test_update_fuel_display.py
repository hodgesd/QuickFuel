import toga
from toga.style import Pack
from helloworld.app import HelloWorld


def dummy_callback(widget):
    pass


def test_update_fuel_display_with_gallons():
    # Initialize the app
    app = HelloWorld("HelloWorld", "1")

    # Create the sliders with initial values
    app.fuel_slider = toga.Slider(min=5000, max=41500, value=20000, on_change=dummy_callback)
    app.starting_slider = toga.Slider(min=4000, max=15000, value=8000, on_change=dummy_callback)

    # Create the labels
    app.delta_volume_label = toga.Label("0", style=Pack())
    app.fuel_label_weight = toga.Label("0 lbs", style=Pack())
    app.fuel_label_volume = toga.Label("0 gals", style=Pack())

    # Set initial conversion factor and label
    app.conversion_factor = app.GALLON_CONVERSION_FACTOR
    app.fuel_volume_label = "gals"

    # Call the method to be tested
    app.update_fuel_display()

    # Calculate expected values
    fuel_volume = app.fuel_slider.value / app.conversion_factor
    delta_lbs = app.fuel_slider.value - app.starting_slider.value
    delta_volume = delta_lbs / app.conversion_factor

    # Check if the display has been updated correctly
    assert app.delta_volume_label.text == f"{delta_volume:,.0f} gals"
    assert app.fuel_label_weight.text == f"{app.fuel_slider.value:,.0f} lbs"
    assert app.fuel_label_volume.text == f"{fuel_volume:,.0f} gals"


def test_update_fuel_display_with_liters():
    # Initialize the app
    app = HelloWorld("HelloWorld", "1")

    # Create the sliders with initial values
    app.fuel_slider = toga.Slider(min=5000, max=41500, value=20000, on_change=dummy_callback)
    app.starting_slider = toga.Slider(min=4000, max=15000, value=8000, on_change=dummy_callback)

    # Create the labels
    app.delta_volume_label = toga.Label("0", style=Pack())
    app.fuel_label_weight = toga.Label("0 lbs", style=Pack())
    app.fuel_label_volume = toga.Label("0 liters", style=Pack())

    # Set initial conversion factor and label
    app.conversion_factor = app.LITRE_CONVERSION_FACTOR
    app.fuel_volume_label = "liters"

    # Call the method to be tested
    app.update_fuel_display()

    # Calculate expected values
    fuel_volume = app.fuel_slider.value / app.conversion_factor
    delta_lbs = app.fuel_slider.value - app.starting_slider.value
    delta_volume = delta_lbs / app.conversion_factor

    # Check if the display has been updated correctly
    assert app.delta_volume_label.text == f"{delta_volume:,.0f} liters"
    assert app.fuel_label_weight.text == f"{app.fuel_slider.value:,.0f} lbs"
    assert app.fuel_label_volume.text == f"{fuel_volume:,.0f} liters"


def test_update_fuel_display_zero_starting_volume():
    # Initialize the app
    app = HelloWorld("HelloWorld", "1")

    # Create the sliders with initial values
    app.fuel_slider = toga.Slider(min=5000, max=41500, value=20000, on_change=dummy_callback)
    app.starting_slider = toga.Slider(min=4000, max=15000, value=0, on_change=dummy_callback)

    # Create the labels
    app.delta_volume_label = toga.Label("0", style=Pack())
    app.fuel_label_weight = toga.Label("0 lbs", style=Pack())
    app.fuel_label_volume = toga.Label("0 gals", style=Pack())

    # Set initial conversion factor and label
    app.conversion_factor = app.GALLON_CONVERSION_FACTOR
    app.fuel_volume_label = "gals"

    # Call the method to be tested
    app.update_fuel_display()

    # Calculate expected values
    fuel_volume = app.fuel_slider.value / app.conversion_factor
    delta_lbs = app.fuel_slider.value - app.starting_slider.value  # Adjust for the starting value
    delta_volume = delta_lbs / app.conversion_factor

    # Check if the display has been updated correctly
    assert app.delta_volume_label.text == f"{delta_volume:,.0f} gals"
    assert app.fuel_label_weight.text == f"{app.fuel_slider.value:,.0f} lbs"
    assert app.fuel_label_volume.text == f"{fuel_volume:,.0f} gals"
