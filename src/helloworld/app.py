"""
My first Toga application
"""

import httpx
import numpy as np
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, MONOSPACE, BOLD


class HelloWorld(toga.App):
    def startup(self):
        # Create main layout container
        main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=20))

        # Name input field
        name_label = toga.Label("Your name: ", style=Pack(padding=(0, 5)))
        self.name_input = toga.TextInput(style=Pack(flex=1))
        self.name_input.on_confirm = self.say_hello

        # Create a box to hold the name label and input
        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        # Fuel slider and label
        self.fuel_slider = toga.Slider(min=5000, max=41500, tick_count=366, on_change=self.on_fuel_slider_change,
                                       on_release=self.on_fuel_slider_release, style=Pack(flex=1))
        self.fuel_label_gals = toga.Label(f"{self.fuel_slider.value / 6.7:,.0f} gals",
                                          style=Pack(padding=(0, 5), text_align=CENTER, font_family=MONOSPACE,
                                                     font_size=24, font_weight=BOLD))
        self.fuel_label_lbs = toga.Label(f"{self.fuel_slider.value:,.0f} lbs",
                                         style=Pack(padding=(0, 5), text_align=CENTER, font_family=MONOSPACE,
                                                    font_size=24, font_weight=BOLD))
        fuel_slider_box = toga.Box(style=Pack(direction=COLUMN, padding=25, alignment=CENTER))
        fuel_slider_box.add(self.fuel_label_lbs)
        fuel_slider_box.add(self.fuel_slider)
        fuel_slider_box.add(self.fuel_label_gals)

        # Define fuel amounts
        fuel_amounts = [10000, 15000, 20000, 30000, 41500]

        # Create buttons using a loop
        button_box = toga.Box(style=Pack(direction=ROW, padding=15))
        for pounds in fuel_amounts:
            label = "Max" if pounds == 41500 else f"{pounds // 1000}K"
            button = toga.Button(label, on_press=lambda widget, p=pounds: self.set_pounds(widget, p),
                                 style=Pack(padding=5))
            button_box.add(button)

        # Button to say hello

        self.starting_fuel_switch = toga.Switch("Start Fuel", on_change=self.toggle_button_visibility,
                                           style=Pack(padding=5))
        self.starting_fuel_switch.value = True
        fuel_in_lbs_switch = toga.Switch("Liters", value=False)

        self.hello_button = toga.Button("Say Hello!", on_press=self.say_hello,
                                   style=Pack(padding=5))

        switch_box = toga.Box(style=Pack(direction=ROW, padding=5))
        switch_box.add(self.starting_fuel_switch)
        switch_box.add(fuel_in_lbs_switch)

        # Add all widgets to the main box
        main_box.add(name_box)
        main_box.add(self.hello_button)
        main_box.add(button_box)
        main_box.add(fuel_slider_box)
        main_box.add(switch_box)

        # Set the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def toggle_button_visibility(self, widget):
        self.hello_button.enabled = self.starting_fuel_switch.value

    def on_fuel_slider_release(self, widget):
        # round to nearst 25
        self.fuel_slider.value = round(self.fuel_slider.value / 100) * 100

    def on_fuel_slider_change(self, widget):
        # Update fuel label based on slider value
        fuel_gals = self.fuel_slider.value / 6.7
        self.fuel_label_gals.text = f"{fuel_gals:,.0f} gals"
        self.fuel_label_lbs.text = f"{self.fuel_slider.value:,.0f} lbs"

    def set_pounds(self, widget, lbs: int):
        self.fuel_slider.value = lbs

    async def say_hello(self, widget=None):
        # Fetch data from an API and show it in a dialog
        async with httpx.AsyncClient() as client:
            response = await client.get("https://jsonplaceholder.typicode.com/posts/42")
        payload = response.json()

        self.main_window.info_dialog(greeting(self.name_input.value), payload["body"])


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
