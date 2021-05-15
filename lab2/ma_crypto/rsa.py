import itertools
from functools import reduce

from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA3_512
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme

from ma_crypto.hash import HASHES
from ma_crypto.symmetric_ciphers import KEY_SIZE_DICT


class MaRSA:
    @staticmethod
    def generate_keypair(n=3072):
        return RSA.generate(n)

    @staticmethod
    def extract_public_key(keypair):
        return keypair.publickey()

    @staticmethod
    def export_key(key):
        return key.exportKey("PEM")

    @staticmethod
    def import_key(exported_key):
        return RSA.import_key(exported_key)

    @staticmethod
    def encrypt(msg, public_key):
        encryptor = PKCS1_v1_5.new(public_key)
        encrypted = encryptor.encrypt(msg)
        return encrypted

    @staticmethod
    def decrypt(private_key, encrypted_data):
        decryptor = PKCS1_v1_5.new(private_key)
        decrypted = decryptor.decrypt(encrypted_data, None)
        assert decrypted != None
        return decrypted

    @staticmethod
    def sign(private_key, msg_hash):
        signer = PKCS115_SigScheme(private_key)
        signature = signer.sign(msg_hash)
        return signature

    @staticmethod
    def verify_signature(public_key, msg_hash, signature):
        verifier = PKCS115_SigScheme(public_key)
        try:
            verifier.verify(msg_hash, signature)
            return True
        except:
            return False


def test():
    palme_2 = "Četrnaest palmi se nadvilo nad nama" \
              "Sa žala šumi zapjenjeni val" \
              "A moja draga obasuta cvijećem" \
              "Strasno me ljubi, sretan sam ja.".encode("utf8")

    sym_key_sizes = set(reduce(lambda x, y: x + y, [sizes for _, sizes in KEY_SIZE_DICT.items()]))
    hash_digest_sizes = set([digest_size for _, digest_size in HASHES.values()])
    print(f"sym_key_sizes: {sym_key_sizes}")
    print(f"hash_digest_sizes: {hash_digest_sizes}")

    all_possible_sizes = set([a + b for a, b in itertools.product(sym_key_sizes, hash_digest_sizes)])
    all_possible_sizes.update(sym_key_sizes)
    all_possible_sizes.update(hash_digest_sizes)
    print(f"all_possible_sizes: {all_possible_sizes}")

    for i in all_possible_sizes:
        data = palme_2[:i]
        print(f"RSA -- len(data)={len(data)}")

        # Key generation
        private_keypair = MaRSA.generate_keypair(1025)
        exported_key = MaRSA.export_key(private_keypair)
        print(exported_key)
        assert private_keypair == MaRSA.import_key(exported_key)

        # encryption
        public_key = MaRSA.extract_public_key(private_keypair)
        encrypted = MaRSA.encrypt(data, public_key)
        decrypted = MaRSA.decrypt(private_keypair, encrypted)
        print(data)
        print(decrypted)
        assert data == decrypted

        # Signature
        hash = SHA3_512.new(data, False)
        signature = MaRSA.sign(private_keypair, hash)
        assert MaRSA.verify_signature(private_keypair, hash, signature)
        assert not MaRSA.verify_signature(private_keypair, "Jure i Mate", signature)

        print("✓")


if __name__ == '__main__':
    test()
