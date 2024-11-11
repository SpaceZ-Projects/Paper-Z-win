
from typing import Optional, Callable
import asyncio
from .app import Forms


class SaveFile(Forms.SaveFileDialog):
    def __init__(
        self,
        title: str = "Save File",
        initial_directory: str = "",
        file_name: str = "",
        result: Optional[Callable[[str], None]] = None
    ):
        super().__init__()

        self.Title = title
        self.Filter = "JPEG Image (*.jpg)|*.jpg"
        self.InitialDirectory = initial_directory
        self.DefaultExt = ".jpg"
        self.FileName = file_name
        self.result_callback = result
    
    def show(self):
        asyncio.run(self.show_dialog())
    
    async def show_dialog(self):
        loop = asyncio.get_event_loop()
        dialog_result = await loop.run_in_executor(None, self.ShowDialog)

        if dialog_result == Forms.DialogResult.OK:
            selected_file = self.FileName
            if self.result_callback:
                self.result_callback(selected_file)
        else:
            if self.result_callback:
                self.result_callback(None)