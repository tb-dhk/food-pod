import arcade
import arcade.gui
import math
import matplotlib.pyplot as plt
from main import MenuView
from main import MyGame
from main import SettingsView
from main import LiveView
from main import CreditsView
from main import TrendsView
curr_colour = arcade.color.TEAL_GREEN
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image
class TrendsView(arcade.View):
    global data
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
        self.u_box = arcade.gui.UIBoxLayout()
    def on_show_view(self):
        self.manager.enable()
        # logo - UITextureButton
        home_button = arcade.gui.UITextureButton(
            x=0,
            y=0,
            texture=arcade.load_texture("./assets/FoodPodLogo.png"),
            texture_hovered=arcade.load_texture('./assets/FoodPodLogo.png'),
            texture_pressed=arcade.load_texture('./assets/FoodPodLogo.png'),
        )
        self.v_box.add(home_button)
        # trends button - UIFlatButton
        trends_button = arcade.gui.UIFlatButton(
            text="Trends",
            width = 90,
            height = 75,
            style = {"font_name": "utopia",
                     "font_size": 17,
                     "font_color": curr_colour,
                     "border_width": 2,
                     "border_color": arcade.color.BLACK,
                     "bg_color": (250,235,215),
                     "bg_color_pressed": arcade.color.BLACK,
                     "border_color_pressed": arcade.color.ANTIQUE_WHITE,
                     "font_color_pressed": arcade.color.ANTIQUE_WHITE}
        )
        self.v_box.add(trends_button)
        # settings button - UIFlatButton
        settings_button = arcade.gui.UIFlatButton(
            text="Settings",
            width=90,
            height=75,
            style={"font_name": "utopia",
                   "font_size": 17,
                   "font_color": curr_colour,
                   "border_width": 2,
                   "border_color": arcade.color.BLACK,
                   "bg_color": (250,235,215),
                   "bg_color_pressed": arcade.color.BLACK,
                   "border_color_pressed": arcade.color.ANTIQUE_WHITE,
                   "font_color_pressed": arcade.color.ANTIQUE_WHITE}
        )
        self.v_box.add(settings_button)
        # live feed
        live_button = arcade.gui.UIFlatButton(
            text="Live Feed",
            width=90,
            height=75,
            style={"font_name": "utopia",
                   "font_size": 17,
                   "font_color": curr_colour,
                   "border_width": 2,
                   "border_color": arcade.color.BLACK,
                   "bg_color": (250, 235, 215),
                   "bg_color_pressed": arcade.color.BLACK,
                   "border_color_pressed": arcade.color.ANTIQUE_WHITE,
                   "font_color_pressed": arcade.color.ANTIQUE_WHITE}
        )
        self.v_box.add(live_button)
        # credits
        credits_button = arcade.gui.UIFlatButton(
            text="Credits",
            width=90,
            height=75,
            style={"font_name": "utopia",
                   "font_size": 17,
                   "font_color": curr_colour,
                   "border_width": 2,
                   "border_color": arcade.color.BLACK,
                   "bg_color": (250,235,215),
                   "bg_color_pressed": arcade.color.BLACK,
                   "border_color_pressed": arcade.color.ANTIQUE_WHITE,
                   "font_color_pressed": arcade.color.ANTIQUE_WHITE}
        )
        self.v_box.add(credits_button)

        home_button.on_click = self.on_click_home
        trends_button.on_click = self.on_click_trends  # run on_click_trends() method
        settings_button.on_click = self.on_click_settings  # run on_click_settings() method
        live_button.on_click = self.on_click_live
        credits_button.on_click = self.on_click_credits  # run on_click_credits() method

        # centre the widgets using UIAnchorWidget
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="left",
                                                   anchor_y="top",
                                                   child=self.v_box))

        # U_BOX BUTTONS
        for i in data:
            food_button = arcade.gui.UIFlatButton(
                text=i['food'],
                width=105,
                height=50,
                style={"font_name": "utopia",
                        "font_size": 17,
                        "font_color": curr_colour,
                        "border_width": 2,
                        "border_color": arcade.color.BLACK,
                        "bg_color": (250, 235, 215),
                        "bg_color_pressed": arcade.color.BLACK,
                        "border_color_pressed": arcade.color.ANTIQUE_WHITE,
                        "font_color_pressed": arcade.color.ANTIQUE_WHITE}
            )
            if data.index(i) == 0:
                self.u_box.add(food_button.with_space_around(top=200, right=15))
            else:
                self.u_box.add(food_button.with_space_around(right=15))

            def on_click_food(self, event, food):
                print("Food clicked:", food)

                if self.data is None:
                    print("Error: self.data is None")
                    return

                # Filter data for the selected food
                filtered_data = [entry for entry in self.data if entry['food'] == food]
                print("Filtered data:", filtered_data)

                if not filtered_data:
                    print(f"No data found for food: {food}")
                    return

                # Extract times and weights for the selected food
                try:
                    times = [datetime.fromtimestamp(entry['time']) for entry in filtered_data]
                    weights = [entry['weight'] for entry in filtered_data]
                except Exception as e:
                    print(f"Error extracting times or weights: {e}")
                    return

                print("Times:", times)
                print("Weights:", weights)

                if not times or not weights:
                    print(f"Error: No times or weights available for food: {food}")
                    return

                # Create a figure and axis
                fig, ax = plt.subplots()

                # Plot the recent month's data
                ax.plot(times, weights, label='Recent Month')

                # Add logic for the previous month data if needed
                # previous_times = ...
                # previous_weights = ...
                # ax.plot(previous_times, previous_weights, label='Previous Month')

                # Set labels and title
                ax.set(xlabel='Time', ylabel='Weight', title=f'Waste Trends for {food}')
                ax.legend()

                # Format the x-axis to display dates nicely
                fig.autofmt_xdate()

                # Create a canvas and draw the figure onto it
                canvas = FigureCanvasAgg(fig)
                canvas.draw()

                # Convert canvas to an image
                buf = canvas.buffer_rgba()
                buf = bytes(buf)
                img = Image.frombytes('RGBA', canvas.get_width_height(), buf)
                texture = arcade.Texture(name=f"multiline_graph_{food}", image=img)

                # Draw the texture at the specified position
                arcade.draw_texture_rectangle(self.width // 2, self.height // 2 - 100, 175, 200, texture)

                # Close the figure to free up memory
                plt.close(fig)

            food_button.on_click = on_click_food

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center",
                                                   anchor_y="center",
                                                   child=self.u_box.with_space_around()))

        home_button.on_click = self.on_click_home
        trends_button.on_click = self.on_click_trends  # run on_click_trends() method
        settings_button.on_click = self.on_click_settings  # run on_click_settings() method
        live_button.on_click = self.on_click_live
        credits_button.on_click = self.on_click_credits  # run on_click_credits() method

        # centre the widgets using UIAnchorWidget
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="left",
                                                   anchor_y="top",
                                                   child=self.v_box))

    def on_hide_view(self):
        self.manager.disable()

    def draw_table(self):
        arcade.draw_rectangle_filled(220, 186, 210, 325, arcade.color.ANTIQUE_WHITE)
        arcade.draw_line(325, 25, 325, 350, arcade.color.BLACK, 2)
        arcade.draw_line(115, 25, 115, 350, arcade.color.BLACK, 2)
        arcade.draw_line(220, 25, 220, 350, arcade.color.BLACK, 2)
        arcade.draw_line(115, 25, 325, 25, arcade.color.BLACK, 2)
        arcade.draw_line(115, 350, 325, 350, arcade.color.BLACK, 2)
        arcade.draw_line(115, 300, 325, 300, arcade.color.BLACK, 2)
        arcade.draw_text("Not Ready Yet", 95.0, 550.0, arcade.color.ANTIQUE_WHITE, 22, 250, "center", "utopia")
        arcade.draw_text("Food", 143, 317, arcade.color.BLACK, 15, 50, "center", "utopia")
        arcade.draw_text("Amount", 236, 317, arcade.color.BLACK, 15, 50, "center", "utopia")
        countheight = 267
        for i in data:
            arcade.draw_text(i['weight'], 236, countheight, arcade.color.BLACK, 15, 50, "center", "utopia")
            countheight -= 50
    def on_click_home(self, event):
        print("Home:", event)
        home_view = MenuView(MyGame())
        self.window.show_view(home_view)

    def on_click_trends(self, event):
        print("Trends:", event)
        trends_view = TrendsView()
        trends_view.setup()  # call setup() method from main.py
        self.window.show_view(trends_view)

    def on_click_settings(self, event):
        print("Settings:", event)
        settings_view = SettingsView()
        settings_view.setup()  # call setup() method from main.py
        self.window.show_view(settings_view)

    def on_click_live(self, event):
        print("Live:", event)
        live_view = LiveView()
        live_view.setup()
        self.window.show_view(live_view)
    def on_click_credits(self, event):
        print("Credits:", event)
        credits_view = CreditsView()
        credits_view.setup()  # call setup() method from main.py
        self.window.show_view(credits_view)

    def setup(self):
        self.manager.enable()
        arcade.set_background_color(curr_colour)

    def on_draw(self):
        self.window.clear()
        self.draw_table()
        self.manager.draw()