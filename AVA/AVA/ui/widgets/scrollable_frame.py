from customtkinter import CTkCanvas
from customtkinter import ThemeManager
from customtkinter import DrawEngine
from customtkinter import CTkBaseClass

# we need to know all width and height
# for every element inside frame so we have
# a way to know the needed height and width
# to calculate how and where to cut regions
# and parts of every widget when draging
# the scrollbar


class ScrollableFrame(CTkBaseClass):
    def __init__(
        self,
        *args,
        bg_color="transparent",
        fg_color="default_theme",
        border_color="default_theme",
        border_width="default_theme",
        corner_radius="default_theme",
        width=200,
        height=200,
        vscroll=False,
        hscroll=False,
        overwrite_preferred_drawing_method: str = None,
        **kwargs
    ):
        # transfer basic functionality (bg_color, size, _appearance_mode, scaling) to CTkBaseClass
        super().__init__(*args, bg_color=bg_color, width=width, height=height, **kwargs)

        # color
        self.border_color = (
            ThemeManager.theme["frame_border"]["color"]
            if border_color == "default_theme"
            else border_color
        )

        # determine fg_color of frame
        if fg_color == "default_theme":
            if isinstance(self.master, ScrollableFrame):
                if self.master.fg_color == ThemeManager.theme["color"]["frame_low"]:
                    self.fg_color = ThemeManager.theme["color"]["frame_high"]
                else:
                    self.fg_color = ThemeManager.theme["color"]["frame_low"]
            else:
                self.fg_color = ThemeManager.theme["color"]["frame_low"]
        else:
            self.fg_color = fg_color

        # shape
        self.corner_radius = (
            ThemeManager.theme["shape"]["frame_corner_radius"]
            if corner_radius == "default_theme"
            else corner_radius
        )
        self.border_width = (
            ThemeManager.theme["shape"]["frame_border_width"]
            if border_width == "default_theme"
            else border_width
        )

        self.hscroll = hscroll
        self.vscroll = vscroll

        if self.vscroll == True:
            # remove area from width
            # self._current_width need a new value simple subtraction
            pass

        if self.hscroll == True:
            # remove area from height
            # self._current_height need a new value simple subtraction
            pass

        self.canvas = CTkCanvas(
            master=self,
            highlightthickness=0,
            width=self.apply_widget_scaling(self._current_width),
            height=self.apply_widget_scaling(self._current_height),
        )
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas.configure(
            bg=ThemeManager.single_color(self.bg_color, self._appearance_mode)
        )
        self.draw_engine = DrawEngine(self.canvas)
        self._overwrite_preferred_drawing_method = overwrite_preferred_drawing_method

        # create a vcanvas for  vscroll if self.vscroll == True

        # create a hcanvas for  vscroll self.hscroll == True

        self.bind("<Configure>", self.update_dimensions_event)

        self.draw()

    def winfo_children(self):
        """winfo_children of CTkFrame without self.canvas widget,
        because it's not a child but part of the CTkFrame itself"""

        child_widgets = super().winfo_children()
        try:
            child_widgets.remove(self.canvas)
            return child_widgets
        except ValueError:
            return child_widgets

    def set_scaling(self, *args, **kwargs):
        super().set_scaling(*args, **kwargs)

        self.canvas.configure(
            width=self.apply_widget_scaling(self._desired_width),
            height=self.apply_widget_scaling(self._desired_height),
        )
        self.draw()

    def set_dimensions(self, width=None, height=None):
        super().set_dimensions(width, height)

        self.canvas.configure(
            width=self.apply_widget_scaling(self._desired_width),
            height=self.apply_widget_scaling(self._desired_height),
        )
        self.draw()

    def draw(self, no_color_updates=False):
        # modify draw for every widget
        # access to all children
        # try to read only once the total width and height needed
        # perhaps use set theory?
        # only draw the widgets between the drawable region
        # or since we know all widgets width i.e. we create a table or a dict ?

        requires_recoloring = self.draw_engine.draw_rounded_rect_with_border(
            self.apply_widget_scaling(self._current_width),
            self.apply_widget_scaling(self._current_height),
            self.apply_widget_scaling(self.corner_radius),
            self.apply_widget_scaling(self.border_width),
            overwrite_preferred_drawing_method=self._overwrite_preferred_drawing_method,
        )

        if no_color_updates is False or requires_recoloring:
            if self.fg_color is None:
                self.canvas.itemconfig(
                    "inner_parts",
                    fill=ThemeManager.single_color(
                        self.bg_color, self._appearance_mode
                    ),
                    outline=ThemeManager.single_color(
                        self.bg_color, self._appearance_mode
                    ),
                )
            else:
                self.canvas.itemconfig(
                    "inner_parts",
                    fill=ThemeManager.single_color(
                        self.fg_color, self._appearance_mode
                    ),
                    outline=ThemeManager.single_color(
                        self.fg_color, self._appearance_mode
                    ),
                )

            self.canvas.itemconfig(
                "border_parts",
                fill=ThemeManager.single_color(
                    self.border_color, self._appearance_mode
                ),
                outline=ThemeManager.single_color(
                    self.border_color, self._appearance_mode
                ),
            )
            self.canvas.configure(
                bg=ThemeManager.single_color(self.bg_color, self._appearance_mode)
            )

        self.canvas.tag_lower("inner_parts")
        self.canvas.tag_lower("border_parts")

    def configure(self, require_redraw=False, **kwargs):
        # new methods
        if "vscroll" in kwargs:
            self.vscroll = kwargs.pop("vscroll")
            require_redraw = True

        if "hscroll" in kwargs:
            self.hscroll = kwargs.pop("hscroll")
            require_redraw = True

        if "fg_color" in kwargs:
            self.fg_color = kwargs.pop("fg_color")
            require_redraw = True

            # check if CTk widgets are children of the frame and change their bg_color to new frame fg_color
            for child in self.winfo_children():
                if isinstance(child, CTkBaseClass):
                    child.configure(bg_color=self.fg_color)

        if "border_color" in kwargs:
            self.border_color = kwargs.pop("border_color")
            require_redraw = True

        if "corner_radius" in kwargs:
            self.corner_radius = kwargs.pop("corner_radius")
            require_redraw = True

        if "border_width" in kwargs:
            self.border_width = kwargs.pop("border_width")
            require_redraw = True

        if "width" in kwargs:
            self.set_dimensions(width=kwargs.pop("width"))

        if "height" in kwargs:
            self.set_dimensions(height=kwargs.pop("height"))

        super().configure(require_redraw=require_redraw, **kwargs)
