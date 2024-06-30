import arcade
import arcade.gui
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image
from main import SettingsView
from main import LiveView
from main import CreditsView
from main import TrendsView

curr_colour = arcade.color.TEAL_GREEN
import time

class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("assets/FoodPodLogo.png")

    def setup(self):
        """Set up the app here. """
        pass

    def on_draw(self):
        #Render the screen
        arcade.start_render()
        self.clear()
        # set bg color
        arcade.set_background_color(curr_colour)
        arcade.draw_texture_rectangle(85.0, 500, 100,
                                      200, self.background)
        arcade.finish_render()
class MenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

    def on_show_view(self):
        self.manager.enable()
        # logo - UITextureButton
        home_button = arcade.gui.UITextureButton(
            x=0,
            y=0,
            texture=arcade.load_texture("./assets/FoodPodLogo.png"),
            texture_hovered = arcade.load_texture('./assets/FoodPodLogo.png'),
            texture_pressed = arcade.load_texture('./assets/FoodPodLogo.png'),
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

    def on_hide_view(self):
        self.manager.disable()

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

    def on_draw(self):
        self.window.clear()
        arcade.set_background_color(curr_colour)
        arcade.draw_text("The FoPod App", 95.0, 550.0, arcade.color.ANTIQUE_WHITE, 22, 250, "center", "utopia")
        self.manager.draw()