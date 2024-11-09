
from .app import Forms, Drawing

from typing import Optional, Union, List, Tuple
from .style import Color

class Box(Forms.Panel):

    def __init__(
        self,
        size: Tuple[int, int] = (100, 100),
        location: Tuple[int, int] = (0, 0),
        background_color: Optional[Color] = None
    ):
        super().__init__()
        self._size = size
        self._location = location
        self._background_color = background_color
        self._widgets = []
        
        self.Size = Drawing.Size(*self._size)
        self.Location = Drawing.Point(*self._location)
        if self._background_color:
            self.BackColor = self._background_color


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
    def background_color(self) -> Optional[Drawing.Color]:
        return self._background_color

    @background_color.setter
    def background_color(self, value: Optional[Drawing.Color]):
        self._background_color = value
        if value:
            self.BackColor = value

    
    @property
    def widgets(self) -> List[Forms.Control]:
        return self._widgets


    
    def insert(self, controls: Union[Forms.Control, List[Forms.Control]]):
        if isinstance(controls, Forms.Control):
            self.Controls.Add(controls)
            self._widgets.append(controls)
        elif isinstance(controls, list):
            for control in controls:
                if isinstance(control, Forms.Control):
                    self.Controls.Add(control)
                    self._widgets.append(controls)
                else:
                    raise TypeError("All items in the list must be instances of Forms.Control.")
        else:
            raise TypeError("controls must be a Forms.Control or a list of Forms.Control.")
        

    
    def remove(self, controls: Union[Forms.Control, List[Forms.Control]]):
        if isinstance(controls, Forms.Control):
            self.Controls.Remove(controls)
        elif isinstance(controls, list):
            for control in controls:
                if isinstance(control, Forms.Control):
                    self.Controls.Remove(control)
                else:
                    raise TypeError("All items in the list must be instances of Forms.Control.")
        else:
            raise TypeError("controls must be a Forms.Control or a list of Forms.Control.")
