
import math
import ecdsa
import os
import unicodedata
import hashlib
import hmac
import binascii
import string

from formz import App, Os
import qrcode
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from mnemonic import Mnemonic
import old_memo

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

word_strength_map = {
    "12": 128,
    "15": 160,
    "18": 192,
    "21": 224,
    "24": 256
}


SEED_PREFIX = '01'  # Standard wallet

filenames = {
    'en':'english.txt',
    'es':'spanish.txt',
    'ja':'japanese.txt',
    'pt':'portuguese.txt',
    'zh':'chinese_simplified.txt'
}

bfh = bytes.fromhex
hfu = binascii.hexlify
hmac_sha_512 = lambda x, y: hmac.new(x, y, hashlib.sha512).digest()


CJK_INTERVALS = [
    (0x4E00, 0x9FFF, 'CJK Unified Ideographs'),
    (0x3400, 0x4DBF, 'CJK Unified Ideographs Extension A'),
    (0x20000, 0x2A6DF, 'CJK Unified Ideographs Extension B'),
    (0x2A700, 0x2B73F, 'CJK Unified Ideographs Extension C'),
    (0x2B740, 0x2B81F, 'CJK Unified Ideographs Extension D'),
    (0xF900, 0xFAFF, 'CJK Compatibility Ideographs'),
    (0x2F800, 0x2FA1D, 'CJK Compatibility Ideographs Supplement'),
    (0x3190, 0x319F , 'Kanbun'),
    (0x2E80, 0x2EFF, 'CJK Radicals Supplement'),
    (0x2F00, 0x2FDF, 'CJK Radicals'),
    (0x31C0, 0x31EF, 'CJK Strokes'),
    (0x2FF0, 0x2FFF, 'Ideographic Description Characters'),
    (0xE0100, 0xE01EF, 'Variation Selectors Supplement'),
    (0x3100, 0x312F, 'Bopomofo'),
    (0x31A0, 0x31BF, 'Bopomofo Extended'),
    (0xFF00, 0xFFEF, 'Halfwidth and Fullwidth Forms'),
    (0x3040, 0x309F, 'Hiragana'),
    (0x30A0, 0x30FF, 'Katakana'),
    (0x31F0, 0x31FF, 'Katakana Phonetic Extensions'),
    (0x1B000, 0x1B0FF, 'Kana Supplement'),
    (0xAC00, 0xD7AF, 'Hangul Syllables'),
    (0x1100, 0x11FF, 'Hangul Jamo'),
    (0xA960, 0xA97F, 'Hangul Jamo Extended A'),
    (0xD7B0, 0xD7FF, 'Hangul Jamo Extended B'),
    (0x3130, 0x318F, 'Hangul Compatibility Jamo'),
    (0xA4D0, 0xA4FF, 'Lisu'),
    (0x16F00, 0x16F9F, 'Miao'),
    (0xA000, 0xA48F, 'Yi Syllables'),
    (0xA490, 0xA4CF, 'Yi Radicals'),
]


__b58chars = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
assert len(__b58chars) == 58

__b43chars = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$*+-./:'
assert len(__b43chars) == 43


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
        box_size=12,
        border=1,
    )
    qr.add_data(address)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    with open(qr_path, 'wb') as f:
        qr_img.save(f)
        
    return qr_path


def generate_taddress(words, language):
    STRENGTH = word_strength_map.get(words)
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



def extract_passphrase(language, passphrase):
    LANGUAGE = language_map.get(language)

    mnemo = Mnemonic(LANGUAGE)
    if not mnemo.check(passphrase):
        print("Invalid mnemonic words.")
        return None
    
    hdwallet = HDWallet(symbol="BTCZ")
    hdwallet.from_mnemonic(mnemonic=passphrase, language=LANGUAGE)
    hdwallet.from_index(44, hardened=True)
    hdwallet.from_index(177, hardened=True)
    hdwallet.from_index(0, hardened=True)
    hdwallet.from_index(0)
    hdwallet.from_index(0)

    return hdwallet



def is_CJK(c):
    n = ord(c)
    for imin,imax,name in CJK_INTERVALS:
        if n>=imin and n<=imax: return True
    return False


def load_wordlist(filename):
    path = Os.Path.Combine(Os.Path.GetDirectoryName(__file__), 'wordlist', filename)
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read().strip()
    s = unicodedata.normalize('NFKD', s)
    lines = s.split('\n')
    wordlist = []
    for line in lines:
        line = line.split('#')[0]
        line = line.strip(' \r')
        assert ' ' not in line
        if line:
            wordlist.append(line)
    return wordlist


def mnemonic_encode(i):
    lang = 'en'
    filename = filenames.get(lang[0:2], 'english.txt')
    wordlist = load_wordlist(filename)
    n = len(wordlist)
    words = []
    while i:
        x = i%n
        i = i//n
        words.append(wordlist[x])
    return ' '.join(words)


def mnemonic_decode(seed):
    lang = 'en'
    filename = filenames.get(lang[0:2], 'english.txt')
    wordlist = load_wordlist(filename)
    n = len(wordlist)
    words = seed.split()
    i = 0
    while words:
        w = words.pop()
        k = wordlist.index(w)
        i = i*n + k
    return i


def seed_prefix(seed_type):
    if seed_type == 'standard':
        return SEED_PREFIX
    

def normalize_text(seed):
    seed = unicodedata.normalize('NFKD', seed)
    seed = seed.lower()
    seed = u''.join([c for c in seed if not unicodedata.combining(c)])
    seed = u' '.join(seed.split())
    seed = u''.join([seed[i] for i in range(len(seed)) if not (seed[i] in string.whitespace and is_CJK(seed[i-1]) and is_CJK(seed[i+1]))])
    return seed
    

def is_old_seed(seed):
    seed = normalize_text(seed)
    words = seed.split()
    try:
        # checks here are deliberately left weak for legacy reasons
        old_memo.mn_decode(words)
        uses_electrum_words = True
    except Exception:
        uses_electrum_words = False
    try:
        seed = bfh(seed)
        is_hex = (len(seed) == 16 or len(seed) == 32)
    except Exception:
        is_hex = False
    return is_hex or (uses_electrum_words and (len(words) == 12 or len(words) == 24))


def is_new_seed(x, prefix=SEED_PREFIX):
    x = normalize_text(x)
    s = bh2u(hmac_sha_512(b"Seed version", x.encode('utf8')))
    return s.startswith(prefix)


def bh2u(x):
    return hfu(x).decode('ascii')


def make_seed(seed_type='standard', num_bits=132):
    lang = 'en'
    filename = filenames.get(lang[0:2], 'english.txt')
    wordlist = load_wordlist(filename)
    prefix = seed_prefix(seed_type)
    bpw = math.log(len(wordlist), 2)
    n = int(math.ceil(num_bits/bpw) * bpw)
    entropy = 1
    while entropy < pow(2, n - bpw):
        entropy = ecdsa.util.randrange(pow(2, n))
    nonce = 0
    while True:
        nonce += 1
        i = entropy + nonce
        seed = mnemonic_encode(i)
        if i != mnemonic_decode(seed):
            raise Exception('Cannot extract same entropy from mnemonic!')
        if is_old_seed(seed):
            continue
        if is_new_seed(seed, prefix):
            break
    print('%d words'%len(seed.split()))
    return seed

    