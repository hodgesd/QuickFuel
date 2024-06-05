from toga.style.pack import HIDDEN, ITALIC

from helloworld.app import HelloWorld


def test_create_label_with_defaults():
    helloworld = HelloWorld("HelloWorld", "1")
    label = helloworld.create_label("Test text")
    assert label.text == "Test text"
    assert label.style.font_size == 24


def test_create_label_with_size_change():
    helloworld = HelloWorld("HelloWorld", "1")
    label = helloworld.create_label("Test text", size=12)
    assert label.text == "Test text"
    assert label.style.font_size == 12


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return f"rgb({int(hex_color[0:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:6], 16)})"


def test_create_label_accent_text():
    helloworld = HelloWorld("HelloWorld", "1")
    label = helloworld.create_label("Test text", accent=True)
    assert label.text == "Test text"
    assert str(label.style.color) == hex_to_rgb(HelloWorld.ACCENT_COLOR)


def test_create_label_hidden_text():
    helloworld = HelloWorld("HelloWorld", "1")
    label = helloworld.create_label("Test text", hidden=True)
    assert label.text == "Test text"
    assert label.style.visibility == HIDDEN


def test_create_label_additional_style_kwargs():
    helloworld = HelloWorld("HelloWorld", "1")
    label = helloworld.create_label("Test text", font_style=ITALIC)
    assert label.text == "Test text"
    assert label.style.font_style == ITALIC
