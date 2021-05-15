from ma_crypto.hash import hash_fn
from ma_crypto.rsa import MaRSA
from ma_crypto.symmetric_ciphers import sym_algo, IV_MODES, IV_SIZE_DICT, SYM_ENCRYPT, SYM_DECRYPT


def create_digital_envelope(message, public_key, algo_name, key, mode, iv):
    sym_enc_msg = sym_algo(algo_name, message, SYM_ENCRYPT, key, mode, iv)

    if mode in IV_MODES:
        secret = key + iv
    else:
        secret = key
    pub_enc_secret = MaRSA.encrypt(secret, public_key)

    return sym_enc_msg, pub_enc_secret


def open_digital_envelope(envelope, private_key, algo_name, key_length, mode):
    sym_enc_msg, pub_enc_secret = envelope
    secret = MaRSA.decrypt(private_key, pub_enc_secret)

    key = secret[:key_length]
    iv = secret[key_length:]
    assert len(key) == key_length
    assert mode not in IV_MODES or iv and len(iv) == IV_SIZE_DICT[algo_name]
    message = sym_algo(algo_name, sym_enc_msg, SYM_DECRYPT, key, mode, iv)

    return message, key, iv


def create_digital_signature(message, private_key, hash_fn_name):
    msg_hash = hash_fn(hash_fn_name, message)
    signed_hash = MaRSA.sign(private_key, msg_hash)
    return signed_hash


def verify_digital_signature(message, signed_hash, public_key, hash_fn_name):
    msg_hash = hash_fn(hash_fn_name, message)
    return MaRSA.verify_signature(public_key, msg_hash, signed_hash)


def create_digital_certificate(message, public_key, private_key, hash_fn_name, algo_name, key, mode, iv):
    sym_enc_msg, pub_enc_secret = create_digital_envelope(message, public_key, algo_name, key, mode, iv)
    signed_hash = create_digital_signature(sym_enc_msg + pub_enc_secret, private_key, hash_fn_name)
    return sym_enc_msg, pub_enc_secret, signed_hash


def open_digital_certificate(public_key, private_key, hash_fn_name, algo_name, key_length, mode, cert):
    sym_enc_msg, pub_enc_secret, signed_hash = cert
    envelope = (sym_enc_msg, pub_enc_secret)

    if not verify_digital_signature(sym_enc_msg + pub_enc_secret, signed_hash, public_key, hash_fn_name):
        return False, None, None, None

    message, key, iv = open_digital_envelope(envelope, private_key, algo_name, key_length, mode)
    return True, message, key, iv
