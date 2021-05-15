from Crypto.Hash import MD5, SHA1, SHA224, SHA256, SHA3_224, SHA3_256, SHA3_384, SHA3_512, SHA384

HASHES = {
    "MD5": (MD5, MD5.MD5Hash.digest_size),
    "SHA1": (SHA1, SHA1.SHA1Hash.digest_size),
    "SHA224": (SHA224, SHA224.SHA224Hash.digest_size),
    "SHA256": (SHA256, SHA256.SHA256Hash.digest_size),
    "SHA3_224": (SHA3_224, SHA3_224.SHA3_224_Hash.digest_size),
    "SHA3_256": (SHA3_256, SHA3_256.SHA3_256_Hash.digest_size),
    "SHA3_384": (SHA3_384, SHA3_384.SHA3_384_Hash.digest_size),
    "SHA3_512": (SHA3_512, SHA3_512.SHA3_512_Hash.digest_size),
    "SHA384": (SHA384, SHA384.SHA384Hash.digest_size),
}


def hash_fn(hash_fn_name, data):
    assert hash_fn_name in HASHES
    if hash_fn_name.startswith("SHA3_"):
        return HASHES[hash_fn_name][0].new(data, update_after_digest=False)
    else:
        return HASHES[hash_fn_name][0].new(data)


def test():
    print(f"Supported hashes: {' '.join(HASHES)}")
    palme_3 = "Četrnaest palmi sad više ne rastu" \
              "Žalom se više ne valja val" \
              "A moja draga obasuta cvijećem" \
              "Nije kraj mene, tužan sam ja.".encode("utf8")

    for i in range(2, len(palme_3) + 1):
        data = palme_3[:i]
        print(f"Data: {data}")
        for h_name, h_algo in HASHES.items():
            print(f"{h_name} --> {h_algo}")
            hash_fn(h_name, data)
            print("✓")


if __name__ == '__main__':
    test()
