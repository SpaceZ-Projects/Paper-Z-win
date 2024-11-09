
import clr

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

import System.IO as Os
import System.Drawing as Drawing
import System.Windows.Forms as Forms

from typing import Optional, Type, Tuple
from pathlib import Path
from .style import Color


class App:
    _icon = None
    _app_path = None
    _app_data = None

    @classmethod
    def _initialize_app_path(cls):
        if cls._app_path is None:
            try:
                script_path = Os.Path.GetDirectoryName(__file__)
                cls._app_path = Os.Path.GetDirectoryName(script_path)
            except Exception as e:
                print(f"Error initializing app path: {e}")


    @classmethod
    def set_icon(cls, icon_path: Optional[Path]):
        if icon_path:
            try:
                cls._icon = Drawing.Icon(str(icon_path))
            except Exception as e:
                print(f"Error setting icon: {e}")
        else:
            cls._icon = None

    @classmethod
    def get_icon(cls) -> Optional[Drawing.Icon]:
        return cls._icon
    

    @property
    def app_path(cls) -> Optional[str]:
        if cls._app_path is None:
            cls._initialize_app_path()
        return cls._app_path
    
    @property
    def app_data(cls) -> Path:
        if cls._app_data is None:
            cls._app_data = Path.home() / 'AppData' / 'Local' / 'BTCZCommunity' / 'PaperZ'
            if not Os.Directory.Exists(str(cls._app_data)):
                Os.Directory.CreateDirectory(str(cls._app_data))
        return cls._app_data

    @classmethod
    def __getattr__(cls, item):
        if item == 'app_path':
            if cls._app_path is None:
                cls._initialize_app_path()
            return cls._app_path
        raise AttributeError(f"'{cls.__name__}' object has no attribute '{item}'")



class MainWindow(Forms.Form):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            print("Warning: An instance of MainWindow already exists")
            return cls._instance
        cls._instance = super(MainWindow, cls).__new__(cls)
        return cls._instance
    

    def __init__(
        self,
        title: str = "Paper-Z",
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
        icon: Optional[Path] = None,
    ):
        if hasattr(self, '_initialized') and self._initialized:
            return
    
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
        self._icon = icon

        self.SetStyle(
            Forms.ControlStyles.AllPaintingInWmPaint | 
            Forms.ControlStyles.UserPaint | 
            Forms.ControlStyles.DoubleBuffer, True
        )

        self.Text = self._title
        self.Size = self._size

        if self._icon:
            App.set_icon(self._icon)
            self.Icon = App.get_icon()

        if background_color:
            self.BackColor = self._background_color

        self.MinimizeBox = self._minimizable
        self.MaximizeBox = self._maxmizable

        if content:
            self.Controls.Add(self._content)

        if center_screen:
            self.StartPosition = Forms.FormStartPosition.CenterScreen
        else:
            self.StartPosition = Forms.FormStartPosition.Manual
            self.Location = Drawing.Point(self._location[0], self._location[1])

        if not self._borderless:
            self.FormBorderStyle = Forms.FormBorderStyle(0)
        elif not self._resizable:
            self.FormBorderStyle = Forms.FormBorderStyle.FixedDialog

        self._initialized = True

    
    @property
    def title(self):
        return self._title
    

    @title.setter
    def title(self, new_title: str):
        self._title = new_title
        self.Text = new_title


    @property
    def size(self) -> Tuple[int, int]:
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
    def center_screen(self) -> bool:
        return self.StartPosition == Forms.FormStartPosition.CenterScreen
    


    @center_screen.setter
    def center_screen(self, value: bool):
        if value:
            self.StartPosition = Forms.FormStartPosition.CenterScreen
        else:
            self.StartPosition = Forms.FormStartPosition.Manual
            self.Location = Drawing.Point(self._location[0], self._location[1])


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
    def maxmizable(self) -> bool:
        return self.MaximizeBox

    @maxmizable.setter
    def maxmizable(self, value: bool):
        self.MaximizeBox = value
        self._maxmizable = value


    
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
    def icon(self) -> Optional[Path]:
        return self._icon
    


    @icon.setter
    def icon(self, value: Optional[Drawing.Icon]):
        self._icon = value
        App.set_icon(value)
        self.Icon = App.get_icon()


    def run(self):
        Forms.Application.EnableVisualStyles()
        Forms.Application.Run(self)