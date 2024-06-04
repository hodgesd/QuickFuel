import sys
from functools import partial

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, MONOSPACE, BOLD, HIDDEN, VISIBLE

print("executable:", sys.executable)


class HelloWorld(toga.App):
    def __init__(self, formal_name, app_id):
        super().__init__(formal_name, app_id)
        self.accent_color = "#006db6"
        self.fuel_volume_label = "gals"
        self.starting_volume_lbs = 5000
        self.CONVERSION_FACTOR = 6.7
        self.alt_label_size = 13
        self.starting_title = None
        self.starting_slider = None
        self.starting_label_lbs = None
        self.starting_box = None
        self.starting_fuel_switch = None
        self.starting_alt_label = None
        self.box_start_switch = None
        self.is_liters = None
        self.is_liters_alt_label = None
        self.box_is_liters_switch = None
        self.flex_box = None
        self.fuel_slider_title = None
        self.fuel_slider = None
        self.fuel_label_volume = None
        self.fuel_label_weight = None
        self.delta_title = None
        self.delta_volume_label = None
        self.flex_box2 = None

    def create_label(self, text, hidden=False, accent=False, size=24, weight=BOLD, **style_kwargs):
        visibility = HIDDEN if hidden else VISIBLE
        color = self.accent_color if accent else "#000000"
        style = Pack(text_align=CENTER, color=color, font_family=MONOSPACE, font_size=size, font_weight=weight,
                     visibility=visibility, **style_kwargs)
        return toga.Label(text, style=style)

    def create_slider(self, min_value, max_value, on_change, hidden=False):
        visibility = HIDDEN if hidden else VISIBLE
        tick_count = int((max_value - min_value) / 100) + 1
        print(tick_count)
        style = Pack(color=self.accent_color, flex=1, visibility=visibility)
        return toga.Slider(min=min_value, max=max_value, tick_count=tick_count, on_change=on_change, style=style)

    def startup(self):
        fuel_presets = [10000, 15000, 20000, 30000, 41500]

        main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=20))

        self.starting_title = self.create_label("Fuel Gauge", hidden=True, accent=True, padding_top=35)
        self.starting_slider = self.create_slider(4000, 15000, on_change=self.on_starting_slider_change, hidden=True)
        self.starting_label_lbs = self.create_label(f"{self.starting_slider.value:,.0f} lbs", hidden=True, accent=True,
                                                    padding=(0, 5))

        self.starting_box = toga.Box(style=Pack(direction=COLUMN, padding=(0, 15)))
        self.starting_box.add(self.starting_title)
        self.starting_box.add(self.starting_slider)
        self.starting_box.add(self.starting_label_lbs)

        self.starting_fuel_switch = toga.Switch("Convert", on_change=self.toggle_button_visibility,
                                                style=Pack(font_weight=BOLD, font_family=MONOSPACE, padding=(4, 0)))
        self.starting_alt_label = self.create_label("Uplift", size=self.alt_label_size, padding=10)
        self.box_start_switch = toga.Box(style=Pack(direction=ROW, padding=(0, 15)))
        self.box_start_switch.add(self.starting_fuel_switch)
        self.box_start_switch.add(self.starting_alt_label)

        self.is_liters = toga.Switch("Gals", on_change=self.toggle_conversion_factor,
                                     style=Pack(font_weight=BOLD, font_family=MONOSPACE, padding=(4, 0)))
        self.is_liters_alt_label = self.create_label("L", size=self.alt_label_size, padding=10)
        self.box_is_liters_switch = toga.Box(style=Pack(direction=ROW, padding=(0, 15)))
        self.box_is_liters_switch.add(self.is_liters)
        self.box_is_liters_switch.add(self.is_liters_alt_label)

        self.flex_box = toga.Box(style=Pack(flex=1))

        self.fuel_slider_title = self.create_label("Fuel Conversion")
        self.fuel_slider = self.create_slider(5000, 41500, on_change=self.on_fuel_slider_change)
        self.fuel_label_volume = self.create_label(
            f"{self.fuel_slider.value / self.CONVERSION_FACTOR:,.0f} {self.fuel_volume_label}", padding=(0, 5))
        self.fuel_label_weight = self.create_label(f"{self.fuel_slider.value:,.0f} lbs", padding=(0, 5))

        fuel_slider_box = toga.Box(style=Pack(direction=COLUMN, padding=(60, 25), alignment=CENTER))

        button_box = toga.Box(style=Pack(direction=ROW, padding=(0, 15)))
        for pounds in fuel_presets:
            label = "Max" if pounds == 41500 else f"{pounds // 1000}K"
            button = toga.Button(label, on_press=partial(self.set_pounds, pounds), style=Pack(padding=(5, 15)))
            button_box.add(button)

        fuel_slider_box.add(self.fuel_slider_title)
        fuel_slider_box.add(button_box)
        fuel_slider_box.add(self.fuel_label_weight)
        fuel_slider_box.add(self.fuel_slider)
        fuel_slider_box.add(self.fuel_label_volume)

        self.delta_title = self.create_label("Fuel Uplift", hidden=True, accent=True, padding_top=60)
        delta_volume = (self.fuel_slider.value - self.starting_volume_lbs) / self.CONVERSION_FACTOR
        self.delta_volume_label = self.create_label(f"{delta_volume:,.0f} {self.fuel_volume_label}", hidden=True,
                                                    accent=True, padding=10)
        fuel_slider_box.add(self.delta_title)
        fuel_slider_box.add(self.delta_volume_label)

        switch_box = toga.Box(style=Pack(direction=ROW, padding_bottom=20, flex=1))
        switch_box.add(self.box_start_switch)
        switch_box.add(self.flex_box)
        switch_box.add(self.box_is_liters_switch)

        main_box.add(self.starting_box)
        main_box.add(fuel_slider_box)

        self.flex_box2 = toga.Box(style=Pack(flex=1))

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.Box(children=[main_box, self.flex_box2, switch_box],
                                            style=Pack(direction=COLUMN, padding=(40, 0)))

        self.main_window.show()

    def toggle_conversion_factor(self, _widget):
        self.CONVERSION_FACTOR, self.fuel_volume_label = (6.7, "gals") if not self.is_liters.value else (
                                                          1.54322, "liters")
        fuel_volume = self.fuel_slider.value / self.CONVERSION_FACTOR
        delta_lbs = self.fuel_slider.value - self.starting_volume_lbs
        delta_volume = delta_lbs / self.CONVERSION_FACTOR
        self.fuel_label_volume.text = f"{fuel_volume:,.0f} {self.fuel_volume_label}"
        self.delta_volume_label.text = f"{delta_volume:,.0f} {self.fuel_volume_label}"

    def toggle_button_visibility(self, _widget):
        visibility = VISIBLE if self.starting_fuel_switch.value else HIDDEN
        self.change_visibility(visibility)

    def change_visibility(self, visibility):
        self.starting_title.style.visibility = visibility
        self.starting_slider.style.visibility = visibility
        self.starting_label_lbs.style.visibility = visibility
        self.delta_title.style.visibility = visibility
        self.delta_volume_label.style.visibility = visibility

    def on_fuel_slider_release(self, _widget):
        self.fuel_slider.value = round(self.fuel_slider.value / 100) * 100

    def on_starting_slider_change(self, _widget):
        self.starting_label_lbs.text = f"{self.starting_slider.value:,.0f} lbs"
        delta_lbs = self.fuel_slider.value - self.starting_slider.value
        delta_volume = delta_lbs / self.CONVERSION_FACTOR
        self.delta_volume_label.text = f"{delta_volume:,.0f} {self.fuel_volume_label}"

    def on_fuel_slider_change(self, _widget):
        self.fuel_volume_label = "gals" if not self.is_liters.value else "liters"
        fuel_volume = self.fuel_slider.value / self.CONVERSION_FACTOR
        delta_lbs = self.fuel_slider.value - self.starting_slider.value
        delta_volume = delta_lbs / self.CONVERSION_FACTOR
        self.delta_volume_label.text = f"{delta_volume:,.0f} {self.fuel_volume_label}"
        self.fuel_label_weight.text = f"{self.fuel_slider.value:,.0f} lbs"
        self.fuel_label_volume.text = f"{fuel_volume:,.0f} {self.fuel_volume_label}"

    def set_pounds(self, pounds, *args, **kwargs):
        if self.fuel_slider:
            self.fuel_slider.value = pounds

    def get_fuel_unit(self):
        return "gals" if not self.is_liters.value else "liters"


def main():
    return HelloWorld("G-VII Fuel Calculator", "org.example.helloworld")


if __name__ == '__main__':
    app = main()
    app.main_loop()
