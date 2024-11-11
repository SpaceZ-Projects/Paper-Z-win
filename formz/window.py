
from .app import Forms, Drawing, Sys

from typing import Callable, Optional, Tuple, Type
from .style import Color
from .app import App


class Window(Forms.Form):
    
    def __init__(
        self,
        title: str = "SpaceZ App",
        size: Tuple[int, int] = (800, 600),
        content: Optional[Type] = None,
        location: Tuple[int, int] = (100, 100),
        center_screen: bool = False,
        background_color: Optional[Color] = None,
        resizable: bool = True,
        minimizable: bool = True,
        maxmizable: bool = True,
        closable: bool = True,
        borderless: bool = True,
        on_close: Optional[Callable[[Type], bool]] = None,
        on_minimize: Optional[Callable[[Type], None]] = None,
        draggable: bool = False
    ):
       
        super().__init__()
        self._title = title
        self._size = Drawing.Size(size[0], size[1])
        self._content = content
        self._location = location
        self._center_screen = center_screen
        self._background_color = background_color
        self._resizable = resizable
        self._minimizable = minimizable
        self._maxmizable = maxmizable
        self._closable = closable
        self._borderless = borderless

        self._on_close = on_close
        self._on_minimize = on_minimize
        self._draggable = draggable

        self._dragging = False
        self._drag_start = Drawing.Point(0, 0)

        self.Text = self._title
        self.Size = self._size

        app_icon = App.get_icon()
        if app_icon:
            self.Icon = app_icon

        if background_color:
            self.BackColor = self._background_color

        self.MinimizeBox = self._minimizable
        self.MaximizeBox = self._maxmizable
        self.ControlBox = self._closable

        if content:
            self.Controls.Add(self._content_panel)

        if center_screen:
            self.StartPosition = Forms.FormStartPosition.CenterScreen
        else:
            self.StartPosition = Forms.FormStartPosition.Manual
            self.Location = Drawing.Point(self._location[0], self._location[1])

        if not self._borderless:
            self.FormBorderStyle = Forms.FormBorderStyle(0)
        elif not self._resizable:
            self.FormBorderStyle = Forms.FormBorderStyle.FixedDialog

        if draggable:
            self._update_draggable()

        self.FormClosing += self._handle_form_closing
        self.Resize += self._handle_minimize_window

    
    @property
    def title(self):
        return self._title
    

    @title.setter
    def title(self, new_title: str):
        self._title = new_title
        self.Text = new_title


    @property
    def size(self):
        return (self.Size.Width, self.Size.Height)
    

    @size.setter
    def size(self, new_size: Tuple[int, int]):
        self._size = Drawing.Size(new_size[0], new_size[1])
        self.Size = self._size


    @property
    def content(self) -> Optional[Type]:
        return self._content
    

    @content.setter
    def content(self, new_content: Optional[Type]):
        if self._content and self._content in self.Controls:
            self.Controls.Remove(self._content)
        self._content = new_content
        if new_content:
            self.Controls.Add(new_content)

    
    @property
    def location(self) -> Tuple[int, int]:
        return (self.Location.X, self.Location.Y)

    @location.setter
    def location(self, new_location: Tuple[int, int]):
        self._set_location(new_location)

    def _set_location(self, location: Tuple[int, int]):
        self._location = location
        if not self._center_screen:
            self.Location = Drawing.Point(location[0], location[1])


    @property
    def background_color(self) -> Optional[Color]:
        return self._background_color

    @background_color.setter
    def background_color(self, color: Optional[Color]):
        
        self._background_color = color
        if color is not None:
            self.BackColor = color
        else:
            self.BackColor = None


    @property
    def resizable(self):
        
        return self.FormBorderStyle == Forms.FormBorderStyle.Sizable

    @resizable.setter
    def resizable(self, value: bool):
        
        if value:
            self.FormBorderStyle = Forms.FormBorderStyle.Sizable
        else:
            self.FormBorderStyle = Forms.FormBorderStyle.FixedDialog
        self._resizable = value


    @property
    def minimizable(self) -> bool:
        
        return self.MinimizeBox

    @minimizable.setter
    def minimizable(self, value: bool):
        
        self.MinimizeBox = value
        self._minimizable = value


    @property
    def maxmizable(self) -> bool:
        
        return self.MaximizeBox

    @maxmizable.setter
    def maxmizable(self, value: bool):
        
        self.MaximizeBox = value
        self._maxmizable = value


    @property
    def closable(self) -> bool:
        
        return self.ControlBox

    @closable.setter
    def closable(self, value: bool):
        
        self.ControlBox = value
        self._closable = value


    
    @property
    def borderless(self) -> bool:
        
        return self._borderless

    @borderless.setter
    def borderless(self, value: bool):
        
        if value:
            self.FormBorderStyle = Forms.FormBorderStyle(1)
            self._borderless = True
        else:
            self.FormBorderStyle = Forms.FormBorderStyle(0)
            self._borderless = False


    
    @property
    def on_close(self) -> Optional[Callable[[Type], bool]]:
        
        return self._on_exit

    @on_close.setter
    def on_close(self, handler: Optional[Callable[[Type], bool]]):
        
        self._on_close = handler

    
    @property
    def on_minimize(self) -> Optional[Callable[[Type], None]]:
        return self._on_minimize
    

    @on_minimize.setter
    def on_minimize(self, handler: Optional[Callable[[Type], None]]):
        self._on_minimize = handler



    def _on_mouse_down(self, sender: object, e: Forms.MouseEventArgs):
        if e.Button == Forms.MouseButtons.Left:
            self._dragging = True
            self._drag_start = e.Location



    def _on_mouse_move(self, sender: object, e: Forms.MouseEventArgs):
        if self._dragging:
            self.Location = Drawing.Point(self.Location.X + e.X - self._drag_start.X,
                                          self.Location.Y + e.Y - self._drag_start.Y)
            
            

    def _on_mouse_up(self, sender: object, e: Forms.MouseEventArgs):
        if e.Button == Forms.MouseButtons.Left:
            self._dragging = False



    def _handle_form_closing(self, sender, e: Forms.FormClosingEventArgs):
        
        if self._on_close:
            result = self._on_close()
            if result is False:
                e.Cancel = True 


    def _handle_minimize_window(self, sender, e: Sys.EventArgs):
        
        if self.WindowState == Forms.FormWindowState.Minimized:
            if callable(self._on_minimize):
                self._on_minimize()


    def activate(self):
        
        self.Activate()


    def hide(self):
        
        self.Hide()

    def show(self):
        
        self.ShowDialog()


    def close(self):
        
        self.Close()