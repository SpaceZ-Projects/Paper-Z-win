
from pathlib import Path
from typing import Optional
from .app import Forms, Drawing
from .style import Color


class Toolbar(Forms.MenuStrip):
    def __init__(
        self,
        color: Optional[Color] = None,
        background_color: Optional[Color] = None,
    ):
        super().__init__()

        self.commands = []
        
        self._color = color
        self._background_color = background_color

        if self._color:
            self.ForeColor = self._color

        if self._background_color:
            self.BackColor = self._background_color

    def add_command(self, commands: list):
        if not isinstance(commands, list):
            raise ValueError("The 'commands' parameter must be a list of Command objects.")
        
        for command in commands:
            self.commands.append(command)
            self.Items.Add(command)


class Command(Forms.ToolStripMenuItem):
    def __init__(
        self,
        title: str = "",
        action=None,
        sub_commands=None,
        icon: Path = None,
        color: Optional[Color] = None,
        background_color :Optional[Color] = None
    ):
        super().__init__(title)

        self._title = title
        self._action = action
        self._sub_commands = sub_commands
        self._icon = icon
        self._color = color
        self._background_color = background_color

        if self._icon:
            self._set_icon(self._icon)

        if action:
            self.Click += action

        if self._sub_commands:
            for sub_command in self._sub_commands:
                self.DropDownItems.Add(sub_command)
        
        if self._color:
            self.ForeColor = self._color
        
        if self._background_color:
            self.BackColor = self._background_color


    def _set_icon(self, icon_path: Path):
        try:
            image = Drawing.Image.FromFile(str(icon_path))
            self.Image = image
        except Exception as e:
            print(f"Error loading image: {e}")
            self.Image = None