from .app import Forms, Drawing

from typing import Optional, Tuple
from .style import Font, FontStyle, Color, AlignLabel

class Label(Forms.Label):
    
    def __init__(
        self,
        text: str = "Hello, World!",
        font: Optional[Font] = Font.SERIF,
        style: Optional[FontStyle] = FontStyle.REGULAR,
        text_color: Optional[Color] = Color.BLACK,
        background_color: Optional[Color] = Color.TRANSPARENT,
        location: Tuple[int, int] = (0, 0),
        size: Optional[int] = 12
    ):
        super().__init__()

        self._text = text
        self._font = font
        self._style = style
        self._text_color = text_color
        self._background_color = background_color
        self._location = location
        self._size = size

        self._font_object = Drawing.Font(self._font, self._size, self._style)
        self.Text = self._text
        self.ForeColor = self._text_color
        self.BackColor = self._background_color
        self.Location = Drawing.Point(self._location[0], self._location[1])
        self.TextAlign = AlignLabel.CENTER
        self.Font = self._font_object

        self._adjust_size()


    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.Text = value

    @property
    def font(self) -> Font:
        return self._font

    @font.setter
    def font(self, value: Font):
        self._font = value
        self.Font = value

    @property
    def style(self) -> FontStyle:
        return self._style

    @style.setter
    def style(self, value: FontStyle):
        self._style = value
        self._update_font()



    @property
    def text_color(self) -> Color:
        return self._text_color
    


    @text_color.setter
    def text_color(self, value: Color):
        self._text_color = value
        self.ForeColor = value


    @property
    def background_color(self) -> Color:
        return self._background_color
    


    @background_color.setter
    def background_color(self, value: Color):
        self._background_color = value
        self.BackColor = value


    @property
    def location(self) -> Tuple[int, int]:
        return (self.Location.X, self.Location.Y)
    


    @location.setter
    def location(self, value: Tuple[int, int]):

        self._location = value
        self.Location = Drawing.Point(value[0], value[1])


    
    @property
    def size(self) -> int:
        return self._size
    

    @size.setter
    def size(self, value: int):
        if value <= 0:
            raise ValueError("Font size must be a positive integer.")
        self._size = value
        self._update_font()
        

    def _update_font(self):

        self._font_object = Drawing.Font(self._font, self._size, self._style)
        self.Font = self._font_object
        self._adjust_size()


    def _adjust_size(self):

        graphics = self.CreateGraphics()
        text_size = graphics.MeasureString(self.Text, self.Font)

        padding = 5
        self.Size = Drawing.Size(
            int(text_size.Width) + padding,
            int(text_size.Height) + padding
        )

        graphics.Dispose()