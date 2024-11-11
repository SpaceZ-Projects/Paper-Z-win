
from .app import Forms, Drawing, Os

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
            if self._size:
                resized_image = Drawing.Bitmap(self._size[0], self._size[1])
                graphics = Drawing.Graphics.FromImage(resized_image)
                graphics.DrawImage(image, 0, 0, self._size[0], self._size[1])
                self.Image = resized_image
            else:
                self.Image = image
            if not self._size:
                self._size = (image.Width, image.Height)
                self.Size = Drawing.Size(*self._size)
            else:
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






class ImageEditor:
    def __init__(self, jpg_path: str = None):
        self._jpg_path = jpg_path
        self._base_image = None

        if self._jpg_path and Os.File.Exists(self._jpg_path):
            self._base_image = Drawing.Bitmap(self._jpg_path)
        else:
            raise ValueError(f"Invalid JPG file path: {self._jpg_path}")
    
    def add_overlay(self, png_path: str, position=(0, 0)):
        if not Os.File.Exists(png_path):
            raise ValueError(f"Invalid PNG file path: {png_path}")
        
        overlay_image = Drawing.Bitmap(png_path)

        graphics = Drawing.Graphics.FromImage(self._base_image)
        graphics.DrawImage(overlay_image, position[0], position[1])
        graphics.Dispose()



    def add_text(self, text: str, position=(0, 0), font_size=12, color: Color = None):
        graphics = Drawing.Graphics.FromImage(self._base_image)

        font = Drawing.Font("Arial", font_size, Drawing.FontStyle.Bold)
        brush = Drawing.SolidBrush(color)
        
        graphics.DrawString(text, font, brush, position[0], position[1])
        graphics.Dispose()



    def add_multiple_overlays(self, png_files: list, positions: list):
        if len(png_files) != len(positions):
            raise ValueError("The number of PNG files must match the number of positions.")
        
        for png_file, position in zip(png_files, positions):
            self.add_overlay(png_file, position)



    def save(self, output_path: str):
        self._base_image.Save(output_path, Drawing.Imaging.ImageFormat.Jpeg)
