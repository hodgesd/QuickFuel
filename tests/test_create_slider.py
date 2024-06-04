import toga
from toga.style.pack import VISIBLE, HIDDEN

from helloworld.app import HelloWorld


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return f"rgb({int(hex_color[0:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:6], 16)})"


def dummy_callback(widget):
    pass

def test_create_slider_default_visibility():
    app = HelloWorld("HelloWorld", "1")
    slider = app.create_slider(0, 100, dummy_callback)
    assert isinstance(slider, toga.Slider)
    assert slider.min == 0
    assert slider.max == 100
    assert slider.style.visibility == VISIBLE
    assert str(slider.style.color) == hex_to_rgb(app.accent_color)
    assert slider.style.flex == 1
    assert slider.tick_count == 2

def test_create_slider_hidden_visibility():
    app = HelloWorld("HelloWorld", "1")
    slider = app.create_slider(0, 100, dummy_callback, hidden=True)
    assert isinstance(slider, toga.Slider)
    assert slider.min == 0
    assert slider.max == 100
    assert slider.style.visibility == HIDDEN
    assert str(slider.style.color) == hex_to_rgb(app.accent_color)
    assert slider.style.flex == 1
    assert slider.tick_count == 2

def test_create_slider_tick_count():
    app = HelloWorld("HelloWorld", "1")
    slider = app.create_slider(0, 300, dummy_callback)
    assert isinstance(slider, toga.Slider)
    assert slider.min == 0
    assert slider.max == 300
    assert slider.tick_count == 4

def test_create_slider_color():
    app = HelloWorld("HelloWorld", "1")
    slider = app.create_slider(0, 100, dummy_callback)
    assert str(slider.style.color) == hex_to_rgb(app.accent_color)