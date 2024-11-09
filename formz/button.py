

from .app import Forms, Drawing

from typing import Optional, Callable, Tuple
from pathlib import Path
from .style import Font, FontStyle, Color

class Button(Forms.Button):
    def __init__(
        self,
        text: str = None,
        size: Tuple[int, int] = (100, 50),
        location: Tuple[int, int] = (0, 0),
        background_color: Optional[Color] = Color.TRANSPARENT,
        text_color: Optional[Color] = None,
        text_size: Optional[int] = None,
        text_font: Optional[Font] = None,
        text_style: Optional[FontStyle] = None,
        icon: Optional[Path] = None,
        on_click: Optional[Callable[[], None]] = None
    ):
        super().__init__()
        self._text = text
        self._size = size
        self._location = location
        self._background_color = background_color
        self._text_color = text_color
        self._text_size = text_size
        self._text_font = text_font
        self._text_style = text_style
        self._icon = icon
        self._on_click = on_click

        self._tooltip = Forms.ToolTip()
        
        if self._text:
            self.Text = self._text

        self.Size = Drawing.Size(*self._size)
        self.Location = Drawing.Point(*self._location)
        self.BackColor = self._background_color

        if self._text_color:
            self.ForeColor = self._text_color

        if self._icon:
            self.Image = Drawing.Image.FromFile(self._icon)

        self._set_font()

        if self._on_click:
            self.Click += self._handle_click


    def _set_font(self):
        font_family = self._text_font or Font.SERIF
        font_size = self._text_size or 10
        font_style = self._text_style or FontStyle.REGULAR
        
        self.Font = Drawing.Font(font_family, font_size, font_style)

            

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.Text = value

    @property
    def size(self) -> Tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: Tuple[int, int]):
        self._size = value
        self.Size = Drawing.Size(*value)

    @property
    def location(self) -> Tuple[int, int]:
        return self._location

    @location.setter
    def location(self, value: Tuple[int, int]):
        self._location = value
        self.Location = Drawing.Point(*value)

    @property
    def background_color(self) -> Optional[any]:
        return self._background_color

    @background_color.setter
    def background_color(self, value: Optional[any]):
        self._background_color = value
        if value:
            self.BackColor = value

    @property
    def text_color(self) -> Optional[any]:
        return self._text_color

    @text_color.setter
    def text_color(self, value: Optional[any]):
        self._text_color = value
        if value:
            self.ForeColor = value


    @property
    def text_size(self) -> Optional[int]:

        return self._text_size
    


    @text_size.setter
    def text_size(self, value: Optional[int]):
        self._text_size = value
        if value:
            self.Font = Drawing.Font(self.Font.FontFamily, value)
        else:
            self.Font = Drawing.Font(self.Font.FontFamily, 10)


    @property
    def icon(self) -> Optional[str]:
        return self._icon

    @icon.setter
    def icon(self, value: Optional[str]):
        self._icon = value
        if value:
            self.Image = Drawing.Image.FromFile(value)
        else:
            self.Image = None
    

    @property
    def on_click(self) -> Optional[Callable[[], None]]:
        return self._on_click

    @on_click.setter
    def on_click(self, value: Optional[Callable[[], None]]):
        self._on_click = value
        if value:
            self.Click += self._handle_click
        else:
            self.Click -= self._handle_click

    def _handle_click(self, sender, event_args):
        if self._on_click:
            self._on_click()
