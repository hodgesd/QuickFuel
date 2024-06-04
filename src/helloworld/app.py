from functools import partial
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, MONOSPACE, BOLD, HIDDEN, VISIBLE


class HelloWorld(toga.App):
    ACCENT_COLOR = "#006db6"
    INITIAL_VOLUME_LABEL = "gals"
    INITIAL_VOLUME_LBS = 5000
    GALLON_CONVERSION_FACTOR = 6.7
    LITRE_CONVERSION_FACTOR = 1.54322
    ALT_LABEL_SIZE = 13

    def __init__(self, formal_name, app_id):
        self.accent_color = self.ACCENT_COLOR
        self.fuel_volume_label = self.INITIAL_VOLUME_LABEL
        self.starting_volume_lbs = self.INITIAL_VOLUME_LBS
        self.conversion_factor = self.GALLON_CONVERSION_FACTOR
        self.alt_label_size = self.ALT_LABEL_SIZE
        super().__init__(formal_name, app_id)
        # self.initialize_ui_elements()

    def initialize_ui_elements(self):
        self.starting_title = self.create_label("Fuel Gauge", hidden=True, accent=True, padding_top=35)
        self.starting_slider = self.create_slider(4000, 15000, self.on_starting_slider_change, hidden=True)
        self.starting_label_lbs = self.create_label(f"{self.starting_slider.value:,.0f} lbs", hidden=True, accent=True, padding=(0, 5))

        self.starting_fuel_switch = self.create_switch("Convert", self.toggle_button_visibility)
        self.starting_alt_label = self.create_label("Uplift", size=self.alt_label_size, padding=10)

        self.is_liters = self.create_switch("Gals", self.toggle_conversion_factor)
        self.is_liters_alt_label = self.create_label("L", size=self.alt_label_size, padding=10)

        self.flex_box = toga.Box(style=Pack(flex=1))

        self.fuel_slider_title = self.create_label("Fuel Conversion")
        self.fuel_slider = self.create_slider(5000, 41500, self.on_fuel_slider_change)
        self.fuel_label_volume = self.create_label(f"{self.fuel_slider.value / self.conversion_factor:,.0f} {self.fuel_volume_label}", padding=(0, 5))
        self.fuel_label_weight = self.create_label(f"{self.fuel_slider.value:,.0f} lbs", padding=(0, 5))

        self.delta_title = self.create_label("Fuel Uplift", hidden=True, accent=True, padding_top=60)
        delta_volume = (self.fuel_slider.value - self.starting_volume_lbs) / self.conversion_factor
        self.delta_volume_label = self.create_label(f"{delta_volume:,.0f} {self.fuel_volume_label}", hidden=True, accent=True, padding=10)

        self.flex_box2 = toga.Box(style=Pack(flex=1))

    def create_label(self, text, hidden=False, accent=False, size=24, weight=BOLD, **style_kwargs):
        visibility = HIDDEN if hidden else VISIBLE
        color = self.accent_color if accent else "#000000"
        style = Pack(text_align=CENTER, color=color, font_family=MONOSPACE, font_size=size, font_weight=weight, visibility=visibility, **style_kwargs)
        return toga.Label(text, style=style)

    def create_slider(self, min_value, max_value, on_change, hidden=False):
        visibility = HIDDEN if hidden else VISIBLE
        tick_count = int((max_value - min_value) / 100) + 1
        style = Pack(color=self.accent_color, flex=1, visibility=visibility)
        return toga.Slider(min=min_value, max=max_value, tick_count=tick_count, on_change=on_change, style=style)

    def create_switch(self, label, on_change):
        return toga.Switch(label, on_change=on_change, style=Pack(font_weight=BOLD, font_family=MONOSPACE, padding=(4, 0)))

    def startup(self):
        self.initialize_ui_elements()
        main_box = self.create_main_box()
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.Box(children=[main_box, self.flex_box2, self.create_switch_box()], style=Pack(direction=COLUMN, padding=(40, 0)))
        self.main_window.show()

    def create_main_box(self):
        return toga.Box(
            style=Pack(direction=COLUMN, alignment=CENTER, padding=20),
            children=[
                self.create_starting_box(),
                self.create_fuel_slider_box()
            ]
        )

    def create_starting_box(self):
        self.box_start_switch = toga.Box(style=Pack(direction=ROW, padding=(0, 15)))
        self.box_start_switch.add(self.starting_fuel_switch)
        self.box_start_switch.add(self.starting_alt_label)

        self.starting_box = toga.Box(style=Pack(direction=COLUMN, padding=(0, 15)), children=[
            self.starting_title,
            self.starting_slider,
            self.starting_label_lbs
        ])
        return self.starting_box

    def create_fuel_slider_box(self):
        return toga.Box(
            style=Pack(direction=COLUMN, padding=(60, 25), alignment=CENTER),
            children=[
                self.fuel_slider_title,
                self.create_button_box(),
                self.fuel_label_weight,
                self.fuel_slider,
                self.fuel_label_volume,
                self.delta_title,
                self.delta_volume_label
            ]
        )

    def create_button_box(self):
        fuel_presets = [10000, 15000, 20000, 30000, 41500]
        buttons = [
            toga.Button(
                "Max" if pounds == 41500 else f"{pounds // 1000}K",
                on_press=partial(self.set_pounds, pounds),
                style=Pack(padding=(5, 15))
            )
            for pounds in fuel_presets
        ]
        return toga.Box(style=Pack(direction=ROW, padding=(0, 15)), children=buttons)

    def create_switch_box(self):
        self.box_is_liters_switch = toga.Box(style=Pack(direction=ROW, padding=(0, 15)))
        self.box_is_liters_switch.add(self.is_liters)
        self.box_is_liters_switch.add(self.is_liters_alt_label)

        return toga.Box(style=Pack(direction=ROW, padding_bottom=20, flex=1), children=[
            self.box_start_switch,
            self.flex_box,
            self.box_is_liters_switch
        ])

    def toggle_conversion_factor(self, _widget):
        self.conversion_factor, self.fuel_volume_label = (
            (self.GALLON_CONVERSION_FACTOR, "gals")
            if not self.is_liters.value else
            (self.LITRE_CONVERSION_FACTOR, "liters")
        )
        self.update_fuel_display()

    def toggle_button_visibility(self, _widget):
        self.change_visibility(VISIBLE if self.starting_fuel_switch.value else HIDDEN)

    def change_visibility(self, visibility):
        for widget in [self.starting_title, self.starting_slider, self.starting_label_lbs, self.delta_title, self.delta_volume_label]:
            widget.style.visibility = visibility

    def on_starting_slider_change(self, _widget):
        self.starting_label_lbs.text = f"{self.starting_slider.value:,.0f} lbs"
        self.update_fuel_display()

    def on_fuel_slider_change(self, _widget):
        self.fuel_volume_label = "gals" if not self.is_liters.value else "liters"
        self.update_fuel_display()

    def update_fuel_display(self):
        fuel_volume = self.fuel_slider.value / self.conversion_factor
        delta_lbs = self.fuel_slider.value - self.starting_slider.value
        delta_volume = delta_lbs / self.conversion_factor

        self.delta_volume_label.text = f"{delta_volume:,.0f} {self.fuel_volume_label}"
        self.fuel_label_weight.text = f"{self.fuel_slider.value:,.0f} lbs"
        self.fuel_label_volume.text = f"{fuel_volume:,.0f} {self.fuel_volume_label}"

    def set_pounds(self, pounds, *args, **kwargs):
        self.fuel_slider.value = pounds

    def get_fuel_unit(self):
        return "gals" if not self.is_liters.value else "liters"


def main():
    return HelloWorld("G-VII Fuel Calculator", "org.example.helloworld")


if __name__ == '__main__':
    app = main()
    app.main_loop()
