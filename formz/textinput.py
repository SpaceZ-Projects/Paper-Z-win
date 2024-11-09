
from .app import Forms, Drawing

from typing import Optional, Tuple, Callable, Type
from .style import Font, FontStyle, Color, AlignForm

class TextInput(Forms.TextBox):
    def __init__(
        self,
        value: str = "",
        size: Tuple[int, int] = (100,30),
        font: Optional[Font] = Font.SERIF,
        style: Optional[FontStyle] = FontStyle.REGULAR,
        aligne: Optional[AlignForm] = AlignForm.LEFT,
        text_color: Optional[Color] = Color.BLACK,
        background_color: Optional[Color] = Color.WHITE,
        location: Tuple[int, int] = (0, 0),
        text_size: Optional[int] = 12,
        multiline: bool = False,
        read_only: bool = False,
    ):
        super().__init__()

        self._value = value
        self._size = size
        self._font = font
        self._style = style
        self._aligne = aligne
        self._text_color = text_color
        self._background_color = background_color
        self._location = location
        self._text_size = text_size
        self._multiline = multiline
        self._read_only = read_only

        self._font_object = Drawing.Font(self._font, self._text_size, self._style)

        self.Text = self._value
        self.TextAlign = self._aligne
        self.ForeColor = self._text_color
        self.BackColor = self._background_color
        self.Location = Drawing.Point(self._location[0], self._location[1])
        self.Font = self._font_object
        self.Multiline = self._multiline
        self.BorderStyle = Forms.BorderStyle(1)
        self.ReadOnly = self._read_only

        self.Size = Drawing.Size(self._size[0], self._size[1])



    @property
    def value(self) -> str:
        return self._value
    

    @value.setter
    def value(self, value: Optional[str]):
        if value is None:
            value = ""
        self._value = value

        if '\n' in value:
            self.Text = value.replace('\n', '\r\n')
        else:
            self.Text = value


    @property
    def size(self) -> Tuple[int, int]:
        return (self.Width, self.Height)


    @size.setter
    def size(self, value: Tuple[int, int]):
        if value[0] > 0:
            self.Width = value[0]
        if value[1] > 0:
            self.Height = value[1]



    @property
    def font(self) -> Font:
        return self._font
    


    @font.setter
    def font(self, value: Font):
        self._font = value
        self._update_font()



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
    def text_size(self) -> int:
        return self._text_size
    


    @text_size.setter
    def size(self, value: int):
        if value <= 0:
            raise ValueError("Font size must be a positive integer.")
        self._text_size = value
        self._update_font()



    @property
    def multiline(self) -> bool:
        return self._multiline
    


    @multiline.setter
    def multiline(self, value: bool):
        self._multiline = value
        self.Multiline = value



    def _update_font(self):
        self._font_object = Drawing.Font(self._font, self._text_size, self._style)
        self.Font = self._font_object
