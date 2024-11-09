
from formz import App, Os
import qrcode
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTCZ
from typing import Optional

app_path = str(App().app_path)
qr_cache = Os.Path.Combine(app_path, 'qr_images')


language_selection_items = [
    "English",
    "French",
    "Italian",
    "Japanese",
    "Korean",
    "Spanish",
    "Chinese Simplified",
    "Chinese Traditional"
]

words_selection_items = [
    "12",
    "15",
    "18",
    "21",
    "24"
]


def qr_generate(address):
    if not Os.Directory.Exists(qr_cache):
        Os.Directory.CreateDirectory(qr_cache)   
    qr_filename = f"qr_{address}.png"
    qr_path = Os.Path.Combine(qr_cache, qr_filename)
    if Os.File.Exists(qr_path):
        return qr_path
        
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )
    qr.add_data(address)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    with open(qr_path, 'wb') as f:
        qr_img.save(f)
        
    return qr_path


def generate_taddress(words, language):
    word_strength_map = {
        "12": 128,
        "15": 160,
        "18": 192,
        "21": 224,
        "24": 256
    }
    STRENGTH = word_strength_map.get(words)

    language_map = {
        "English": "english",
        "French": "french",
        "Italian": "italian",
        "Japanese": "japanese",
        "Korean": "korean",
        "Spanish": "spanish",
        "Chinese Simplified": "chinese_simplified",
        "Chinese Traditional": "chinese_traditional"
    }
    LANGUAGE = language_map.get(language)

    ENTROPY: str = generate_entropy(strength=STRENGTH)

    hdwallet = HDWallet("BTCZ", use_default_path=False)
    hdwallet.from_entropy(entropy=ENTROPY, language=LANGUAGE)

    hdwallet.from_index(44, hardened=True)
    hdwallet.from_index(177, hardened=True)
    hdwallet.from_index(0, hardened=True)
    hdwallet.from_index(0)
    hdwallet.from_index(0)

    return hdwallet

    