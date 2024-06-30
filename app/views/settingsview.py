import arcade
import arcade.gui
import math
import matplotlib.pyplot as plt
curr_colour = arcade.color.TEAL_GREEN
from main import MenuView
from main import MyGame
from main import SettingsView
from main import LiveView
from main import CreditsView
from main import TrendsView
class SettingsView(arcade.View):
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
    def setup(self):
        self.manager.enable()
        arcade.set_background_color(curr_colour)
        # trends button - UIFlatButton
        colour_button = arcade.gui.UIFlatButton(
            text="Change Colour",
            width = 150,
            height = 75,
            style = {"font_name": "utopia",
                     "font_size": 20,
                     "font_color": curr_colour,
                     "border_width": 2,
                     "border_color": arcade.color.BLACK,
                     "bg_color": (250,235,215),
                     "bg_color_pressed": arcade.color.BLACK,
                     "border_color_pressed": arcade.color.ANTIQUE_WHITE,
                     "font_color_pressed": arcade.color.ANTIQUE_WHITE}
        )
        self.u_box.add(colour_button.with_space_around(bottom=200, right=60))

        colour_button.on_click = self.on_click_colour  # run on_click_colour() method

        # centre the widgets using UIAnchorWidget
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="right",
                                                   anchor_y="center",
                                                   child=self.u_box))

    def on_hide_view(self):
        self.manager.disable()

    def on_click_colour(self, event):
        global curr_colour
        print("Colour:", event)
        colours_list = [arcade.color.TEAL_GREEN, arcade.color.ALABAMA_CRIMSON, arcade.color.AIR_FORCE_BLUE, arcade.color.AMETHYST, arcade.color.ANTIQUE_BRASS, arcade.color.ARYLIDE_YELLOW, arcade.color.BLACK, arcade.color.BRIGHT_PINK, arcade.color.ORANGE, arcade.color.BRIGHT_TURQUOISE]
        hold_number = colours_list.index(curr_colour)
        try:
            curr_colour = colours_list[hold_number+1]
        except:
            curr_colour = colours_list[0]
        arcade.set_background_color(curr_colour)

    def on_draw(self):
        self.window.clear()
        self.manager.draw()
        arcade.draw_text("Settings:", 95.0, 550.0, arcade.color.ANTIQUE_WHITE, 22, 250, "center", "utopia")