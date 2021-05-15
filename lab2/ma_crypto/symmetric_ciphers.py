import random
import string

from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import pad, unpad

SYM_ENCRYPT = 0
SYM_DECRYPT = 1

ALGO_DICT = {
    "AES": AES,
    "DES": DES,
    "3DES": DES3
}

MODE_DICT = {
    "ECB": DES.MODE_ECB,
    "CBC": DES.MODE_CBC,
    "CFB": DES.MODE_CFB,
    "CTR": DES.MODE_CTR,
    "OFB": DES.MODE_OFB,
}

BLOCK_SIZE_DICT = {
    "AES": 16,
    "DES": 8,
    "3DES": 8
}

KEY_SIZE_DICT = {
    "AES": [16, 24, 32],
    "DES": [8],  # 64b key but only the first 56 are used.
    "3DES": [16, 24]
}

IV_SIZE_DICT = {
    "AES": 16,
    "DES": 8,
    "3DES": 8
}
IV_MODES = {"CBC", "OFB", "CFB"}
IV_MODES.update({"CTR"})  # Impossible to create a safe nonce for short block sizes, so I will use a iv instead


def sym_algo(algo_name, x, action, key, mode, iv):
    algo = ALGO_DICT[algo_name]
    assert mode in MODE_DICT.keys()
    assert iv not in IV_MODES or (iv is not None and len(iv) == IV_SIZE_DICT[algo_name])

    if mode in IV_MODES:
        if mode == "CTR":
            cipher = algo.new(key, MODE_DICT[mode], nonce=b'', initial_value=iv)
        else:
            cipher = algo.new(key, MODE_DICT[mode], iv=iv)

    else:
        cipher = algo.new(key, MODE_DICT[mode])

    if action == SYM_ENCRYPT:
        x = pad(x, BLOCK_SIZE_DICT[algo_name])
        return cipher.encrypt(x)
    elif action == SYM_DECRYPT:
        y = cipher.decrypt(x)
        try:
            y = unpad(y, BLOCK_SIZE_DICT[algo_name])
        except ValueError:
            print("*** DES: Got a ValueError when unpadding")  # Input data is not padded
        return y
    else:
        raise ValueError(f"Invalid value for action, got: {action}")


def generate_random_ascii_bytes(n):
    s = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))
    s = s.encode("ascii")
    return s


def test():
    random.seed(72)
    palme_1 = "Četrnaest palmi na otoku sreće" \
              "Žalo po kojem se valja val" \
              "I moja draga obasuta cvijećem" \
              "Leži kraj mene, sretan sam ja".encode("utf8")

    for i in range(2, len(palme_1) + 1):
        plaintext = palme_1[:i]
        for algo_name in ALGO_DICT.keys():
            for mode in MODE_DICT.keys():
                for key_size in KEY_SIZE_DICT[algo_name]:
                    print(f"Algo: {algo_name} -- Mode: {mode} -- key_size={key_size * 8}")
                    des_params = {
                        "key": generate_random_ascii_bytes(key_size),
                        "iv": generate_random_ascii_bytes(IV_SIZE_DICT[algo_name]),
                        "mode": mode
                    }
                    ciphertext = sym_algo(algo_name, plaintext, SYM_ENCRYPT, **des_params)
                    plaintext_decrypted = sym_algo(algo_name, ciphertext, SYM_DECRYPT, **des_params)
                    print(plaintext)
                    print(ciphertext)
                    print(plaintext_decrypted)
                    assert plaintext != ciphertext
                    assert plaintext == plaintext_decrypted
                    # assert plaintext.decode("utf8") == plaintext_decrypted.decode("utf8")
                    print("✓")


if __name__ == "__main__":
    test()
