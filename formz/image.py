
from .app import Forms, Drawing

from typing import Optional, Tuple
from pathlib import Path
from .style import Color

class ImageBox(Forms.PictureBox):
    def __init__(
        self,
        image: Path = None,
        size: Tuple[int, int] = None,
        background_color: Optional[Color] = Color.TRANSPARENT,
        location: Optional[Tuple[int, int]] = (0, 0)
    ):
        super().__init__()
        self._image_path = image
        self._size = size
        self._background_color = background_color
        self._location = location

        self.BackColor = self._background_color

        if self._location:
            self.Location = Drawing.Point(*self._location)

        if self._image_path:
            self._set_image(self._image_path)


    def _set_image(self, image_path: Path):
        try:
            image = Drawing.Image.FromFile(str(image_path))
            self.Image = image
            
            if self._size is None:
                self._size = (image.Width, image.Height)
                self.Size = Drawing.Size(*self._size)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.Image = None



    @property
    def image_path(self) -> Path:
        return self._image_path
    


    @image_path.setter
    def image_path(self, value: Path):
        self._image_path = value
        if value:
            self._set_image(value)
        else:
            self.Image = None



    @property
    def size(self) -> Tuple[int, int]:
        return self._size
    


    @size.setter
    def size(self, value: Optional[Tuple[int, int]]):
        if value:
            self._size = value
            self.Size = Drawing.Size(*value)
        else:
            if self.Image:
                self._size = (self.Image.Width, self.Image.Height)
                self.Size = Drawing.Size(*self._size)



    @property
    def background_color(self) -> Optional[Color]:
        return self._background_color
    


    @background_color.setter
    def background_color(self, value: Optional[Color]):
        self._background_color = value
        if value:
            self.BackColor = value


    
    @property
    def location(self) -> Tuple[int, int]:
        return self._location
    

    @location.setter
    def location(self, value: Tuple[int, int]):
        self._location = value
        self.Location = Drawing.Point(*value)
