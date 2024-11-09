

from formz import (
    App, MainWindow, Box, Button, Color, Label,
    ImageBox, FontStyle, Selection, TextInput, Os
)

from utils import (
    generate_taddress, qr_generate,
    language_selection_items, words_selection_items)


class AddressResult(Box):
    def __init__(self):
        super(AddressResult, self).__init__()

        self.size = (660, 280)
        self.location = (10, 10)
        self.background_color = Color.rgb(35,35,35)

        self.qr_code = ImageBox(
            location=(480, 20)
        )

        self.qr_code_box = Box(
            size=(155,155),
            location=(480, 20),
            background_color=Color.rgb(25,25,25)
        )

        self.address_label = Label(
            text="Address :",
            text_color=Color.GRAY,
            style=FontStyle.BOLD,
            location=(15, 30)
        )

        self.address_output = TextInput(
            size=(300, 0),
            text_size=11,
            location=(140, 30),
            read_only=True,
            text_color=Color.WHITE,
            background_color=Color.rgb(35,35,35)
        )

        self.public_key_label = Label(
            text="Public Key :",
            text_color=Color.GRAY,
            style=FontStyle.BOLD,
            location=(15, 85)
        )

        self.public_key_output = TextInput(
            size=(300,0),
            text_size=11,
            location=(140, 85),
            read_only=True,
            text_color=Color.WHITE,
            background_color=Color.rgb(35,35,35)
        )

        self.private_key_label = Label(
            text="Private Key :",
            text_color=Color.GRAY,
            style=FontStyle.BOLD,
            location=(15, 140)
        )

        self.private_key_output = TextInput(
            size=(300,0),
            text_size=11,
            location=(140, 140),
            read_only=True,
            text_color=Color.WHITE,
            background_color=Color.rgb(35,35,35)
        )

        self.passphrase_label = Label(
            text="Passphrase :",
            text_color=Color.GRAY,
            style=FontStyle.BOLD,
            location=(15, 200)
        )

        self.passphrase_output = TextInput(
            read_only=True,
            multiline=True,
            size=(400, 60),
            text_color=Color.WHITE,
            background_color=Color.rgb(35,35,35),
            location=(140, 200)
        )


class PaperZ(MainWindow):
    def __init__(self):
        super(PaperZ, self).__init__()

        icon = Os.Path.Combine(str(App().app_path), 'paperz_logo.ico')
        self.lock_file = Os.Path.Combine(str(App().app_data), ".lock")
        self.lock_file_stream = None

        self.title = "Paper-Z"
        self.size = (700, 400)
        self.maxmizable = False
        self.resizable = False
        self.center_screen = True
        self.icon = icon

        self.outputs = AddressResult()


        self.main_box = Box(
            size=(700, 400),
            background_color=Color.rgb(30,30,30)
        )

        self.divider = Box(
            size=(700,1),
            location=(0,300),
            background_color=Color.rgb(35,35,35)
        )

        self.words_label = Label(
            text="Words :",
            location=(20, 322),
            text_color=Color.GRAY
        )

        self.words_selection = Selection(
            size=(60,0),
            location=(90, 322),
            text_size=11,
            background_color=Color.rgb(35,35,35),
            color=Color.YELLOW,
            items=words_selection_items,
            on_change=self.change_words
        )

        self.language_label = Label(
            text="Language :",
            location=(170, 322),
            text_color=Color.GRAY
        )

        self.passphrase_language = Selection(
            size=(140,0),
            location=(260, 322),
            text_size=11,
            background_color=Color.rgb(35,35,35),
            color=Color.YELLOW,
            items=language_selection_items,
            on_change=self.change_language
        )

        self.generate_button = Button(
            text="Generate",
            location=(550, 320),
            size=(100, 30),
            background_color=Color.rgb(50,50,50),
            text_color=Color.YELLOW,
            on_click=self.generate_address
        )

        self.clear_button = Button(
            text="Clear",
            location=(430, 320),
            size=(100, 30),
            background_color=Color.rgb(50,50,50),
            text_color=Color.YELLOW,
            on_click=self.clear_outputs
        )
        self.clear_button.Enabled = False
        
        self.main_box.insert(
            [
                self.outputs,
                self.words_label,
                self.words_selection,
                self.language_label,
                self.passphrase_language,
                self.clear_button,
                self.generate_button,
                self.divider
            ]
        )

        self.content = self.main_box

        self.words_selection.value = "12"
        self.passphrase_language.value = "English"

        self.outputs.insert([
            self.outputs.qr_code_box,
            self.outputs.address_label,
            self.outputs.address_output,
            self.outputs.public_key_label,
            self.outputs.public_key_output,
            self.outputs.private_key_label,
            self.outputs.private_key_output,
            self.outputs.passphrase_label,
            self.outputs.passphrase_output
        ])

    
    def generate_address(self):
        self.generate_button.Enabled = False
        self.outputs.remove([self.outputs.qr_code_box])
        words = self.words_selection.value
        language = self.passphrase_language.value
        result = generate_taddress(words, language)
        if result:
            self.display_address_result(result)
        self.clear_button.Enabled = True


    def display_address_result(self, result):
        new_address = result.p2pkh_address()
        if new_address:
            self.outputs.address_output.value = new_address
        public_key = result.public_key()
        if public_key:
            self.outputs.public_key_output.value = public_key
        private_key = result.wif()
        if private_key:
            self.outputs.private_key_output.value = private_key
        passphrase = result.mnemonic()
        if passphrase:
            self.outputs.passphrase_output.value = passphrase
        qr_image = qr_generate(new_address)
        if qr_image:
            self.outputs.qr_code.image_path = qr_image
            self.outputs.insert([self.outputs.qr_code])



    def clear_outputs(self):
        self.outputs.remove([self.outputs.qr_code])
        self.outputs.insert([self.outputs.qr_code_box])
        self.outputs.address_output.value = ""
        self.outputs.public_key_output.value = ""
        self.outputs.private_key_output.value = ""
        self.outputs.passphrase_output.value = ""
        self.generate_button.Enabled = True
        self.clear_button.Enabled = False


    def change_words(self, value):
        self.words_selection.value = value

    def change_language(self, value):
        self.passphrase_language.value = value


    def is_already_running(self):
        if Os.File.Exists(self.lock_file):
            try:
                Os.File.Delete(self.lock_file)
            except Os.IOException:
                return True
        return False


    def create_lock_file(self):
        try:
            self.lock_file_stream = Os.FileStream(
                self.lock_file,
                Os.FileMode.CreateNew,
                Os.FileAccess.ReadWrite,
                Os.FileShare(0)
            )
        except Os.IOException:
            return False
        return True


    def remove_lock_file(self):
        if self.lock_file_stream:
            self.lock_file_stream.Close()
            self.lock_file_stream = None
        if Os.File.Exists(self.lock_file):
            try:
                Os.File.Delete(self.lock_file)
            except OSError as e:
                print(f"Error removing lock file: {e}")


    def run(self):
        if self.is_already_running():
            return
        if not self.create_lock_file():
            return
        try:
            super().run()
        finally:
            self.remove_lock_file()


def main():
    app = PaperZ()
    app.run()


if __name__ == "__main__":
    main()