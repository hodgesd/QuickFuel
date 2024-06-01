"""
My first Toga application
"""

import httpx
import numpy as np
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, MONOSPACE, BOLD, HIDDEN


class HelloWorld(toga.App):

    def startup(self):
        # Create main layout container
        main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=20))
        self.fuel_volume_label = "gals"
        self.starting_volume_lbs = 5000

        self.CONVERSION_FACTOR = 6.7
        self.name_label = toga.Label("Starting Fuel: ", style=Pack(visibility=HIDDEN,padding=(0, 5)))
        self.name_input = toga.NumberInput(style=Pack(visibility=HIDDEN,flex=1))
        self.name_input.on_confirm = self.say_hello

        # Create a box to hold the name label and input
        self.name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.name_box.add(self.name_label)
        self.name_box.add(self.name_input)

        self.starting_fuel_switch = toga.Switch("Start Fuel", on_change=self.toggle_button_visibility,
                                                style=Pack(padding=25))
        self.is_liters = toga.Switch("Liters", on_change=self.toggle_conversion_factor,
                                     style=Pack(padding=25))
        self.flex_box = toga.Box(style=Pack(flex=1))
        self.hello_button = toga.Button("Say Hello!", on_press=self.say_hello,
                                        style=Pack(visibility=HIDDEN,padding=5))

        # Fuel slider and label
        self.fuel_slider = toga.Slider(min=5000, max=41500, tick_count=366, on_change=self.on_fuel_slider_change,
                                       on_release=self.on_fuel_slider_release, style=Pack(flex=1))
        self.fuel_label_volume = toga.Label(f"{self.fuel_slider.value / self.CONVERSION_FACTOR:,.0f} {self.fuel_volume_label}",
                                            style=Pack(padding=(0, 5), text_align=CENTER, font_family=MONOSPACE,
                                                     font_size=24, font_weight=BOLD))
        self.fuel_label_weight = toga.Label(f"{self.fuel_slider.value:,.0f} lbs",
                                         style=Pack(padding=(0, 5), text_align=CENTER, font_family=MONOSPACE,
                                                    font_size=24, font_weight=BOLD))
        fuel_slider_box = toga.Box(style=Pack(direction=COLUMN, padding=25, alignment=CENTER))
        fuel_slider_box.add(self.fuel_label_weight)
        fuel_slider_box.add(self.fuel_slider)
        fuel_slider_box.add(self.fuel_label_volume)

        self.delta_title = toga.Label("Uplift",style=Pack(visibility=HIDDEN, padding_top=(25), text_align=CENTER, font_family=MONOSPACE,
                                                    font_size=24, font_weight=BOLD))
        self.delta_volume_label = toga.Label(f"{(self.fuel_slider.value - self.starting_volume_lbs ) / self.CONVERSION_FACTOR:,.0f} {self.fuel_volume_label}", style=Pack(visibility=HIDDEN,padding=(0, 5), text_align=CENTER, font_family=MONOSPACE,
                                                    font_size=24, font_weight=BOLD))
        fuel_slider_box.add(self.delta_title)
        fuel_slider_box.add(self.delta_volume_label)

        # Define fuel amounts
        fuel_amounts = [10000, 15000, 20000, 30000, 41500]

        # Create buttons using a loop
        button_box = toga.Box(style=Pack(direction=ROW, padding=15))
        for pounds in fuel_amounts:
            label = "Max" if pounds == 41500 else f"{pounds // 1000}K"
            button = toga.Button(label, on_press=lambda widget, p=pounds: self.set_pounds(widget, p),
                                 style=Pack(padding=5))
            button_box.add(button)


        switch_box = toga.Box(style=Pack(direction=ROW, padding=5, flex=1))
        switch_box.add(self.starting_fuel_switch)
        switch_box.add(self.flex_box)
        switch_box.add(self.is_liters)

        main_box.add(self.name_box)
        main_box.add(self.hello_button)
        main_box.add(button_box)
        main_box.add(fuel_slider_box)

        self.flex_box2 = toga.Box(style=Pack(flex=1))

        # Set the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.Box(children=[main_box, self.flex_box2, switch_box],
                                            style=Pack(direction=COLUMN, padding=0, )
                                            )

        self.main_window.show()

    def toggle_conversion_factor(self, widget):
        self.CONVERSION_FACTOR, self.fuel_volume_label = (6.7, "gals") if not self.is_liters.value else (1.54322, "liters")
        fuel_volume = self.fuel_slider.value / self.CONVERSION_FACTOR
        delta_lbs = self.fuel_slider.value - self.starting_volume_lbs
        delta_volume = delta_lbs / self.CONVERSION_FACTOR
        self.fuel_label_volume.text = f"{fuel_volume:,.0f} {self.fuel_volume_label}"
        self.delta_volume_label.text = f"{delta_volume:,.0f} {self.fuel_volume_label}"

    def toggle_button_visibility(self, widget):
        start_fuel_visible = self.starting_fuel_switch.value
        # self.hello_button.enabled = start_fuel_visible
        if start_fuel_visible:
            self.name_input.style.visibility = 'visible'
            self.name_label.style.visibility = 'visible'
            self.hello_button.style.visibility = 'visible'
            self.delta_title.style.visibility = 'visible'
            self.delta_volume_label.style.visibility = 'visible'
        else:
            self.name_input.style.visibility = 'hidden'
            self.name_label.style.visibility = 'hidden'
            self.hello_button.style.visibility = 'hidden'
            self.delta_title.style.visibility = 'hidden'
            self.delta_volume_label.style.visibility = 'hidden'


    def on_fuel_slider_release(self, widget):
        # round to nearst 25
        self.fuel_slider.value = round(self.fuel_slider.value / 100) * 100

    def on_fuel_slider_change(self, widget):
        """Update fuel label based on slider value"""
        self.fuel_volume_label = "gals" if not self.is_liters.value else "liters"
        fuel_volume = self.fuel_slider.value / self.CONVERSION_FACTOR
        delta_lbs = self.fuel_slider.value - self.starting_volume_lbs
        delta_volume = delta_lbs / self.CONVERSION_FACTOR
        self.fuel_label_weight.text = f"{self.fuel_slider.value:,.0f} lbs"
        self.fuel_label_volume.text = f"{fuel_volume:,.0f} {self.fuel_volume_label}"
        self.delta_volume_label.text = f"{delta_volume:,.0f} {self.fuel_volume_label}"

    def set_pounds(self, widget, lbs_preset: int):
        self.fuel_slider.value = lbs_preset

    async def say_hello(self, widget=None):
        # Fetch data from an API and show it in a dialog
        async with httpx.AsyncClient() as client:
            response = await client.get("https://jsonplaceholder.typicode.com/posts/42")
        payload = response.json()

        self.main_window.info_dialog(greeting(self.name_input.value), payload["body"])

    def get_fuel_unit(self):
        return "gals" if not self.is_liters.value else "litres"


def greeting(name):
    # Generate a greeting message with a random number
    value = np.random.randint(100)
    if name:
        return f"Hello, {name} - {value}"
    else:
        return f"Hello, stranger - {value}"


def main():
    return HelloWorld()


if __name__ == '__main__':
    app = main()
    app.main_loop()
