

from formz import (
    App, MainWindow, Box, Button, Color, Label,
    ImageBox, FontStyle, Selection, TextInput, Os,
    Toolbar, Command, Window, AlignForm,
    ImageEditor, SaveFile, Dialog, MessageButtons, MessageIcon
)

from utils import (
    generate_taddress, qr_generate, extract_passphrase, make_seed,
    language_selection_items, words_selection_items)


class AddressResult(Box):
    def __init__(self):
        super(AddressResult, self).__init__()

        self.size = (660, 280)
        self.location = (10, 35)
        self.background_color = Color.rgb(35,35,35)

        self.qr_code = ImageBox(
            location=(480, 20),
            size=(155, 155)
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
            location=(140, 200),
            aligne=AlignForm.CENTER
        )


class PaperZ(MainWindow):
    def __init__(self):
        super(PaperZ, self).__init__()

        icon = Os.Path.Combine(str(App().app_path), 'icons/paperz_logo.ico')
        self.lock_file = Os.Path.Combine(str(App().app_data), ".lock")
        self.lock_file_stream = None

        self.title = "Paper-Z"
        self.size = (700, 420)
        self.maxmizable = False
        self.resizable = False
        self.center_screen = True
        self.icon = icon

        self.outputs = AddressResult()
        self.toolbar = Toolbar(
            background_color=Color.rgb(200,200,200)
        )
        self.print_cmd = Command(
            title="Print paper",
            background_color=Color.rgb(200,200,200),
            icon="icons/print.png",
            action=self.print_address_template
        )
        self.print_cmd.Enabled = False
        self.file_menu = Command(
            title="File",
            icon="icons/file.png",
            sub_commands=[self.print_cmd]
        )

        self.memo_p2pkh_cmd = Command(
            title="Extract passphrase",
            background_color=Color.rgb(200,200,200),
            icon="icons/convert.png",
            action=self.diplay_extract_window
        )

        self.generate_electrum = Command(
            title="Generate electrum",
            background_color=Color.rgb(200,200,200),
            icon="icons/electrum.png",
            action=self.generate_electrum_seed
        )

        self.tools_menu = Command(
            title="Tools",
            sub_commands=[
                self.memo_p2pkh_cmd,
                self.generate_electrum
            ],
            icon="icons/tools.png"
        )
        self.toolbar.add_command(
            [
                self.file_menu,
                self.tools_menu
            ]
        )


        self.main_box = Box(
            size=(700, 400),
            background_color=Color.rgb(30,30,30)
        )

        self.divider = Box(
            size=(700,1),
            location=(0,325),
            background_color=Color.rgb(35,35,35)
        )

        self.words_label = Label(
            text="Words :",
            location=(20, 342),
            text_color=Color.GRAY
        )

        self.words_selection = Selection(
            size=(60,0),
            location=(90, 342),
            text_size=11,
            background_color=Color.rgb(35,35,35),
            color=Color.YELLOW,
            items=words_selection_items,
            on_change=self.change_words
        )

        self.language_label = Label(
            text="Language :",
            location=(170, 342),
            text_color=Color.GRAY
        )

        self.passphrase_language = Selection(
            size=(140,0),
            location=(260, 342),
            text_size=11,
            background_color=Color.rgb(35,35,35),
            color=Color.YELLOW,
            items=language_selection_items,
            on_change=self.change_language
        )

        self.generate_button = Button(
            text="Generate",
            location=(550, 340),
            size=(100, 30),
            background_color=Color.rgb(50,50,50),
            text_color=Color.YELLOW,
            on_click=self.generate_address
        )

        self.clear_button = Button(
            text="Clear",
            location=(430, 340),
            size=(100, 30),
            background_color=Color.rgb(50,50,50),
            text_color=Color.YELLOW,
            on_click=self.clear_outputs
        )
        self.clear_button.Enabled = False
        
        self.main_box.insert(
            [
                self.toolbar,
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
        self.print_cmd.Enabled = True
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
        self.print_cmd.Enabled = False
        self.generate_button.Enabled = True
        self.clear_button.Enabled = False


    def change_words(self, value):
        self.words_selection.value = value

    def change_language(self, value):
        self.passphrase_language.value = value


    def diplay_extract_window(self, command, enent):
        self.extract_title = Label(
            text="Paste your Passphrase here",
            location=(167,70),
            text_color=Color.WHITE,
            size=12
        )
        self.passphrase_input = TextInput(
            multiline=True,
            size=(440, 60),
            text_color=Color.WHITE,
            background_color=Color.rgb(35,35,35),
            location=(50, 100),
            aligne=AlignForm.CENTER,
            on_change=self.update_extract_button
        )

        self.extract_language = Selection(
            location=(140, 192),
            text_size=11,
            background_color=Color.rgb(35,35,35),
            color=Color.YELLOW,
            items=language_selection_items,
            on_change=self.change_extract_language
        )
        self.extract_language_label = Label(
            text="Language :",
            location=(45, 192),
            text_color=Color.GRAY
        )
        self.extract_language.value = "English"
        self.extract_button = Button(
            text="Extract",
            location=(280, 190),
            size=(100, 30),
            background_color=Color.rgb(50,50,50),
            text_color=Color.WHITE,
            on_click=self.extract_passphrase
        )
        self.extract_button.Enabled = False
        self.close_button = Button(
            text="Close",
            location=(390, 190),
            size=(100, 30),
            background_color=Color.RED,
            text_color=Color.WHITE,
            on_click=self.close_extract_window
        )
        self.extract_window = Window(
            size = (550, 250),
            center_screen=True,
            borderless=False
        )
        self.window_border = Box(
            size=(550,250),
            background_color=Color.rgb(20,20,20)
        )
        self.extract_box = Box(
            size=(540,240),
            background_color=Color.rgb(30,30,30),
            location=(5,5)
        )
        self.window_border.insert([self.extract_box])
        self.extract_box.insert(
            [
                self.extract_title,
                self.passphrase_input,
                self.extract_language_label,
                self.extract_language,
                self.extract_button,
                self.close_button
            ]
        )
        self.extract_window.content = self.window_border
        self.extract_window.show()


    def close_extract_window(self):
        self.extract_window.close()

    def change_extract_language(self, value):
        self.extract_language.value = value

    def update_extract_button(self, value):
        self.passphrase_input.value = value
        if value:
            words = value.split()
            if len(words) >= 12:
                self.extract_button.Enabled = True
            elif len(words) < 12:
                self.extract_button.Enabled = False


    def extract_passphrase(self):
        language = self.extract_language.value
        passphrase = self.passphrase_input.value
        result = extract_passphrase(language, passphrase)
        if not result:
            Dialog(
                title="Invalid",
                message="Invalid mnemonic words.",
                buttons=MessageButtons.OK,
                icon=MessageIcon.ERROR
            )
            return
        else:
            self.print_cmd.Enabled = True
            self.generate_button.Enabled = False
            self.clear_button.Enabled = True
            address = result.p2pkh_address()
            if address:
                self.outputs.address_output.value = address
            public_key = result.public_key()
            if public_key:
                self.outputs.public_key_output.value = public_key
            private_key = result.wif()
            if private_key:
                self.outputs.private_key_output.value = private_key
            passphrase = result.mnemonic()
            if passphrase:
                self.outputs.passphrase_output.value = passphrase
            qr_image = qr_generate(address)
            if qr_image:
                self.outputs.remove([self.outputs.qr_code_box])
                self.outputs.qr_code.image_path = qr_image
                self.outputs.insert([self.outputs.qr_code])
            
            self.extract_window.close()


    def generate_electrum_seed(self, command, event):
        result = make_seed('standard', num_bits=132)
        if result:
            self.outputs.passphrase_output.value = result


    def print_address_template(self, command, event):
        address = self.outputs.address_output.value
        private_key = self.outputs.private_key_output.value
        qr_private = qr_generate(private_key)
        template_path = Os.Path.Combine(App().app_path, 'template.jpg')

        if Os.File.Exists(template_path):
            self.image_editor = ImageEditor(template_path)
            
            self.image_editor.add_text(
                text=address,
                color=Color.BLACK,
                position=(276, 798),
                font_size=20
            )
            self.image_editor.add_text(
                text=private_key,
                color=Color.BLACK,
                font_size=14.5,
                position=(2360, 725)
            )
            self.image_editor.add_overlay(
                png_path = self.outputs.qr_code.image_path,
                position=(360, 422)
            )
            self.image_editor.add_overlay(
                png_path= qr_private,
                position=(2460, 352)
            )
            save_file = SaveFile(
                title="Save paper wallet",
                file_name=f"paper_{address}",
                result=self.save_template
            )
            save_file.show()
        
    def save_template(self, path):
        self.image_editor.save(path)


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