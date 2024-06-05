import toga
from toga.style import Pack
from helloworld.app import HelloWorld
import pytest


def test_end_to_end():
    # Initialize the app
    app = HelloWorld("HelloWorld", "1")

    # Create the main window and UI elements
    app.startup()

    # Simulate toggling the "Convert" switch to make starting elements visible
    app.starting_fuel_switch.value = True
    app.toggle_button_visibility(app.starting_fuel_switch)

    # Check that the starting elements are now visible
    assert app.starting_title.style.visibility == toga.style.pack.VISIBLE
    assert app.starting_slider.style.visibility == toga.style.pack.VISIBLE
    assert app.starting_label_lbs.style.visibility == toga.style.pack.VISIBLE

    # Simulate moving the starting slider
    app.starting_slider.value = 8000
    app.on_starting_slider_change(app.starting_slider)

    # Check that the starting label is updated
    assert app.starting_label_lbs.text == "8,000 lbs"

    # Simulate moving the fuel slider
    app.fuel_slider.value = 20000
    app.on_fuel_slider_change(app.fuel_slider)

    # Check that the fuel labels are updated
    fuel_volume = 20000 / app.GALLON_CONVERSION_FACTOR
    delta_volume = (20000 - 8000) / app.GALLON_CONVERSION_FACTOR

    assert app.fuel_label_weight.text == "20,000 lbs"
    assert app.fuel_label_volume.text == f"{fuel_volume:,.0f} gals"
    assert app.delta_volume_label.text == f"{delta_volume:,.0f} gals"

    # Simulate toggling the "Gals" switch to convert to liters
    app.is_liters.value = True
    app.toggle_conversion_factor(app.is_liters)

    # Check that the conversion factor and labels are updated correctly
    fuel_volume_liters = 20000 / app.LITRE_CONVERSION_FACTOR
    delta_volume_liters = (20000 - 8000) / app.LITRE_CONVERSION_FACTOR

    assert app.conversion_factor == app.LITRE_CONVERSION_FACTOR
    assert app.fuel_volume_label == "liters"
    assert app.fuel_label_volume.text == f"{fuel_volume_liters:,.0f} liters"
    assert app.delta_volume_label.text == f"{delta_volume_liters:,.0f} liters"

    # Simulate pressing a preset button
    preset_button = app.create_button_box().children[0]  # Assuming first button is for 10K lbs
    preset_button.on_press(preset_button)

    # Check that the fuel slider is updated to 10K lbs
    assert app.fuel_slider.value == 10000

    # Update the display after setting the preset
    app.update_fuel_display()

    fuel_volume_liters_preset = 10000 / app.LITRE_CONVERSION_FACTOR
    delta_volume_liters_preset = (10000 - 8000) / app.LITRE_CONVERSION_FACTOR

    # Check that the labels are updated accordingly
    assert app.fuel_label_volume.text == f"{fuel_volume_liters_preset:,.0f} liters"
    assert app.delta_volume_label.text == f"{delta_volume_liters_preset:,.0f} liters"


if __name__ == "__main__":
    pytest.main()
