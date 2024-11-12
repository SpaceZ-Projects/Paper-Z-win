
from typing import Optional, Callable, Type
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




class Dialog(Forms.MessageBox):
    def __init__(
        self,
        message: str = None,
        title: str = None,
        buttons: Type[any] = None,
        icon: Type[any] = None,
        result: Callable = None
    ):
        self.message = message
        self.title = title
        if buttons:
            self.buttons = buttons
        else:
            self.buttons = Forms.MessageBoxButtons.OK
        if icon:
            self.icon = icon
        else:
            self.icon = Forms.MessageBoxIcon(0)
        self.result = result
        
        result = self.Show(self.message, self.title, self.buttons, self.icon)
        if self.result:
            self.result(result)
            return result
    


class MessageButtons:
    """The message box contains Abort, Retry, and Ignore buttons."""
    ABORTRETRYIGNORE = Forms.MessageBoxButtons.AbortRetryIgnore
    """The message box contains an OK button."""
    OK = Forms.MessageBoxButtons.OK
    """The message box contains OK and Cancel buttons."""
    OKCANCEL = Forms.MessageBoxButtons.OKCancel
    """The message box contains Retry and Cancel buttons."""
    RETRYCANCEL = Forms.MessageBoxButtons.RetryCancel
    """Forms.MessageBoxButtons."""
    YESNO = Forms.MessageBoxButtons.YesNo
    """The message box contains Yes, No, and Cancel buttons."""
    YESNOCANCEL = Forms.MessageBoxButtons.YesNoCancel


class MessageIcon:
    """The message box contains a symbol consisting of a lowercase letter i in a circle."""
    ASTERISK = Forms.MessageBoxIcon.Asterisk
    """The message box contains a symbol consisting of white X in a circle with a red background."""
    ERROR = Forms.MessageBoxIcon.Error
    """The message box contains a symbol consisting of an exclamation point in a triangle with a yellow background."""
    EXCLAMATION = Forms.MessageBoxIcon.Exclamation
    """The message box contains a symbol consisting of a white X in a circle with a red background."""
    HAND = Forms.MessageBoxIcon.Hand
    """The message box contains a symbol consisting of a lowercase letter i in a circle."""
    INFORMATION = Forms.MessageBoxIcon.Information
    """The message box contains no symbols."""
    NONE = Forms.MessageBoxIcon(0)
    """The message box contains a symbol consisting of a question mark in a circle."""
    QUESTION = Forms.MessageBoxIcon.Question
    """The message box contains a symbol consisting of white X in a circle with a red background."""
    STOP = Forms.MessageBoxIcon.Stop
    """The message box contains a symbol consisting of an exclamation point in a triangle with a yellow background."""
    WARNING = Forms.MessageBoxIcon.Warning