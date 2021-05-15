#!/usr/bin/env python3
import argparse
import os
import pathlib

from ma_crypto.digital import create_digital_envelope, open_digital_envelope, create_digital_signature, \
    verify_digital_signature, create_digital_certificate, open_digital_certificate
from ma_crypto.hash import HASHES
from ma_crypto.rsa import MaRSA
from ma_crypto.symmetric_ciphers import ALGO_DICT, KEY_SIZE_DICT, IV_SIZE_DICT, MODE_DICT

actions = ["envelope", "sign", "cert"]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def generate_keys(args):
    assert pathlib.Path(args.savedir).is_dir()

    private_keypair = MaRSA.generate_keypair(args.n)
    public_key = MaRSA.extract_public_key(private_keypair)

    private_key_path = os.path.join(args.savedir, args.private_key_filename)
    with open(private_key_path, "wb") as f:
        f.write(MaRSA.export_key(private_keypair))
        print(f"Path to private key: {private_key_path}")

    public_key_path = os.path.join(args.savedir, args.public_key_filename)
    with open(public_key_path, "wb") as f:
        f.write(MaRSA.export_key(public_key))
        print(f"Path to public key: {public_key_path}")


def create_envelope(args):
    assert pathlib.Path(args.envelope_savedir).is_dir()

    with open(args.message_path, "rb") as f:
        message = f.read()
        print("Message loaded")
    with open(args.public_key_path, "rb") as f:
        public_key = MaRSA.import_key(f.read())
        print("Public key loaded")

    algo_name = args.sym_algo
    key = args.sym_key.encode("utf-8")
    mode = args.sym_mode
    iv = args.sym_iv.encode("utf-8") if args.sym_iv is not None else None
    sym_enc_msg, pub_enc_secret = create_digital_envelope(message, public_key, algo_name, key, mode,
                                                          iv)

    print(f"Envelope (sym_enc_msg, pub_enc_secret)")
    envelope_part1_path = os.path.join(args.envelope_savedir, args.envelope_part1_filename)
    envelope_part2_path = os.path.join(args.envelope_savedir, args.envelope_part2_filename)
    with open(envelope_part1_path, "wb") as f:
        f.write(sym_enc_msg)
    with open(envelope_part2_path, "wb") as f:
        f.write(pub_enc_secret)
    print(f"Envelope part1 (sym_enc_msg) path: {envelope_part1_path}")
    print(f"Envelope part2 (pub_enc_secret) path: {envelope_part2_path}")


def open_envelope(args):
    assert pathlib.Path(args.envelope_savedir).is_dir()

    with open(args.private_key_path, "rb") as f:
        private_key = MaRSA.import_key(f.read())
        print("Private key loaded")

    envelope_part1_path = os.path.join(args.envelope_savedir, args.envelope_part1_filename)
    envelope_part2_path = os.path.join(args.envelope_savedir, args.envelope_part2_filename)
    print(f"Envelope part1 (sym_enc_msg) path given as: {envelope_part1_path}")
    print(f"Envelope part2 (pub_enc_secret) path given as: {envelope_part2_path}")
    with open(envelope_part1_path, "rb") as f:
        sym_enc_msg = f.read()
    with open(envelope_part2_path, "rb") as f:
        pub_enc_secret = f.read()
    print("Envelope loaded")

    algo_name = args.sym_algo
    key_length = args.sym_key_length
    mode = args.sym_mode
    envelope = (sym_enc_msg, pub_enc_secret)
    message, sym_key, sym_iv = open_digital_envelope(envelope, private_key, algo_name, key_length, mode)

    print(f"Sym Key ('b'): {sym_key}")
    print(f"Sym Key (utf-8): {sym_key.decode('utf-8')}")
    print(f"Sym IV ('b'): {sym_iv}")
    print(f"Sym IV (utf-8): {sym_iv.decode('utf-8')}")
    print(f"Message ('b'): {message}")
    print(f"Message (utf8): {message.decode('utf8')}")


def sign(args):
    with open(args.message_path, "rb") as f:
        message = f.read()
        print("Message loaded")
    with open(args.private_key_path, "rb") as f:
        private_key = MaRSA.import_key(f.read())
        print("Private key loaded")

    signed_hash = create_digital_signature(message, private_key, args.hash_fn_name)
    with open(args.signature_path, "wb") as f:
        f.write(signed_hash)
    print(f"Signed saved: {args.signature_path}")


def verify_signature(args):
    with open(args.message_path, "rb") as f:
        message = f.read()
        print("Message loaded")
    with open(args.public_key_path, "rb") as f:
        public_key = MaRSA.import_key(f.read())
        print("Public key loaded")
    with open(args.signature_path, "rb") as f:
        signed_hash = f.read()
        print("Signed hash loaded")

    if verify_digital_signature(message, signed_hash, public_key, args.hash_fn_name):
        print("Signature OK")
    else:
        print("Signature INVALID")


def create_cert(args):
    with open(args.message_path, "rb") as f:
        message = f.read()
        print("Message loaded")
    with open(args.public_key_path, "rb") as f:
        public_key = MaRSA.import_key(f.read())
        print("Public key loaded")
    with open(args.private_key_path, "rb") as f:
        private_key = MaRSA.import_key(f.read())
        print("Private key loaded")

    hash_fn_name = args.hash_fn_name
    algo_name = args.sym_algo
    key = args.sym_key.encode("utf-8")
    mode = args.sym_mode
    iv = args.sym_iv.encode("utf-8") if args.sym_iv is not None else None
    sym_enc_msg, pub_enc_secret, signed_hash = create_digital_certificate(message, public_key, private_key,
                                                                          hash_fn_name, algo_name, key, mode, iv)
    print(f"Certificate (sym_enc_msg, pub_enc_secret, signed_hash)")
    cert_part1_path = os.path.join(args.cert_savedir, args.cert_part1_filename)
    cert_part2_path = os.path.join(args.cert_savedir, args.cert_part2_filename)
    cert_part3_path = os.path.join(args.cert_savedir, args.cert_part3_filename)
    with open(cert_part1_path, "wb") as f:
        f.write(sym_enc_msg)
    with open(cert_part2_path, "wb") as f:
        f.write(pub_enc_secret)
    with open(cert_part3_path, "wb") as f:
        f.write(signed_hash)
    print(f"Certificate part1 (sym_enc_msg) path: {cert_part1_path}")
    print(f"Certificate part2 (pub_enc_secret) path: {cert_part2_path}")
    print(f"Certificate part3 (signed_hash) path: {cert_part3_path}")


def open_cert(args):
    with open(args.public_key_path, "rb") as f:
        public_key = MaRSA.import_key(f.read())
        print("Public key loaded")
    with open(args.private_key_path, "rb") as f:
        private_key = MaRSA.import_key(f.read())
        print("Private key loaded")

    print(f"Certificate (sym_enc_msg, pub_enc_secret, signed_hash)")
    cert_part1_path = os.path.join(args.cert_savedir, args.cert_part1_filename)
    cert_part2_path = os.path.join(args.cert_savedir, args.cert_part2_filename)
    cert_part3_path = os.path.join(args.cert_savedir, args.cert_part3_filename)
    with open(cert_part1_path, "rb") as f:
        sym_enc_msg = f.read()
    with open(cert_part2_path, "rb") as f:
        pub_enc_secret = f.read()
    with open(cert_part3_path, "rb") as f:
        signed_hash = f.read()
    cert = (sym_enc_msg, pub_enc_secret, signed_hash)
    print(f"Certificate part1 (sym_enc_msg) path given as: {cert_part1_path}")
    print(f"Certificate part2 (pub_enc_secret) path given as: {cert_part2_path}")
    print(f"Certificate part3 (signed_hash) path given as: {cert_part3_path}")
    print(f"Certificate loaded.")

    algo_name = args.sym_algo
    key_length = args.sym_key_length
    mode = args.sym_mode
    envelope = (sym_enc_msg, pub_enc_secret)
    hash_fn_name = args.hash_fn_name
    validity, message, sym_key, sym_iv = open_digital_certificate(public_key, private_key, hash_fn_name, algo_name,
                                                                  key_length, mode, cert)

    if not validity:
        print("Signature INVALID")
        return
    print("Singature OK")

    print(f"Sym key ('b'): {sym_key}")
    print(f"Sym key (utf-8): {sym_key.decode('utf-8')}")
    print(f"Sym IV ('b'): {sym_iv}")
    print(f"Sym IV (utf-8): {sym_iv.decode('utf-8')}")
    print(f"Message ('b'): {message}")
    print(f"Message (utf8): {message.decode('utf8')}")


if __name__ == '__main__':
    # ~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~ HEADER ~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~ #

    # print("Second laboratory exercise -- digital envelope, signature and certificate")
    # print("Advanced Operating Systems, 2021")
    # print("FER, University of Zagreb, Croatia")
    # print("")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~ HELPING PARSERS ~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    symmetric_parser = argparse.ArgumentParser(add_help=False)
    symmetric_parser.add_argument("--sym_algo", "-sa", choices=ALGO_DICT.keys())
    symmetric_parser.add_argument("--sym_key", "-sk", help=f"key lengths: {KEY_SIZE_DICT}")
    symmetric_parser.add_argument("--sym_key_length", "-skl", type=int)
    symmetric_parser.add_argument("--sym_iv", "-si", help=f"iv lengths: {str(IV_SIZE_DICT)}")
    symmetric_parser.add_argument("--sym_mode", "-sm", choices=MODE_DICT.keys())
    # 3DES + ECB
    # --sym_algo 3DES --sym_key 12345678abcdefgh87654321 --sym_key_length 24 --sym_mode ECB
    # --sym_algo 3DES --sym_key_length 24 --sym_mode ECB
    # AES192 + OFB
    # --sym_algo AES --sym_key 12345678abcdefgh87654321 --sym_key_length 24 --sym_iv 12345678abcdefgh --sym_mode OFB
    # --sym_algo AES --sym_key_length 24 --sym_mode OFB
    # AES256 + CFB
    # --sym_algo AES --sym_key 12345678abcdefgh87654321hgfedcba --sym_key_length 32 --sym_iv 12345678abcdefgh --sym_mode CFB
    # --sym_algo AES --sym_key_length 32 --sym_mode CFB

    hash_fn_parser = argparse.ArgumentParser(add_help=False)
    hash_fn_parser.add_argument("--hash_fn_name", "-hfn", choices=HASHES.keys())
    # --hash_fn_name MD5
    # --hash_fn_name SHA256
    # --hash_fn_name SHA3_512
    # --hash_fn_name SHA384

    message_path_parser = argparse.ArgumentParser(add_help=False)
    message_path_parser.add_argument("--message_path", "-mp", required=True)

    public_key_path_parser = argparse.ArgumentParser(add_help=False)
    public_key_path_parser.add_argument("--public_key_path", '-pubp', required=True)

    private_key_path_parser = argparse.ArgumentParser(add_help=False)
    private_key_path_parser.add_argument("--private_key_path", '-privp', required=True)

    signature_path_parser = argparse.ArgumentParser(add_help=False)
    signature_path_parser.add_argument("--signature_path", "-sp", required=True)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~ MAIN PARSER ~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ #
    main_parser = argparse.ArgumentParser()
    action_subparsers = main_parser.add_subparsers(
        title="action", dest="action_command",
        help="choose from actions to generate key, create an digital envelope, signature or certificate"
    )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~ RSA KEY GENERATOR PARSER ~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    gen_parser = action_subparsers.add_parser("gen", help="generate a RSA keypair")
    gen_parser.add_argument("--n", "-n", type=int, default=1024, help="length of RSA key to generate")
    gen_parser.add_argument("--savedir", "-s", required=True)
    gen_parser.add_argument("--private_key_filename", "-privf", default="id_rsa")
    gen_parser.add_argument("--public_key_filename", "-pubf", default="id_rsa.pub")

    # USAGE
    # mkdir keys
    # ./main.py gen --n 3072 --savedir keys

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~ ENVELOPE PARSERS ~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    envelope_parser = action_subparsers.add_parser("envelope", help="work with digital envelopes")
    envelope_subparsers = envelope_parser.add_subparsers(title="envelope_action", dest="envelope_action")

    create_envelope_parser = envelope_subparsers.add_parser("create", parents=[symmetric_parser, message_path_parser,
                                                                               public_key_path_parser])
    create_envelope_parser.add_argument("--envelope_savedir", "-es", required=True)
    create_envelope_parser.add_argument("--envelope_part1_filename", '-e1f', default="envelope.part1")
    create_envelope_parser.add_argument("--envelope_part2_filename", '-e2f', default="envelope.part2")

    open_envelope_parser = envelope_subparsers.add_parser("open", parents=[symmetric_parser, private_key_path_parser])
    open_envelope_parser.add_argument("--envelope_savedir", "-es", required=True)
    open_envelope_parser.add_argument("--envelope_part1_filename", '-e1f', default="envelope.part1")
    open_envelope_parser.add_argument("--envelope_part2_filename", '-e2f', default="envelope.part2")

    # USAGE
    # mkdir envelope messages
    # echo "jure i mate" > messages/alice.txt
    # ./main.py envelope create --message_path messages/alice.txt --public_key_path keys/id_rsa.pub --envelope_savedir envelope --sym_algo AES --sym_key 12345678abcdefgh87654321 --sym_key_length 24 --sym_iv 12345678abcdefgh --sym_mode OFB
    #
    # ./main.py envelope open --envelope_savedir envelope --private_key_path keys/id_rsa --envelope_savedir envelope --sym_algo AES --sym_key_length 24 --sym_mode OFB

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~ SIGNATURE PARSERS ~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    signature_parser = action_subparsers.add_parser("signature", help="work with digital signatures")
    signature_subparsers = signature_parser.add_subparsers(title="signature_action", dest="signature_action")

    sign_signature_parser = signature_subparsers.add_parser(
        "sign", parents=[hash_fn_parser, message_path_parser, private_key_path_parser, signature_path_parser])
    verify_signature_parser = signature_subparsers.add_parser(
        "verify", parents=[hash_fn_parser, message_path_parser, public_key_path_parser, signature_path_parser])

    # USAGE EXAMPLE
    # mkdir signatures
    # ./main.py signature sign --message_path messages/alice.txt --signature_path signatures/alice.sign --private_key_path keys/id_rsa --hash_fn_name SHA3_512
    #
    # ./main.py signature verify --message_path messages/alice.txt --signature_path signatures/alice.sign  --public_key_path keys/id_rsa.pub --hash_fn_name SHA3_512
    # --> Signatue OK
    #
    # cp messages/alice.txt messages/alice_modified.txt && echo "." >> messages/alice_modified.txt
    # ./main.py signature verify --message_path messages/alice_modified.txt --signature_path signatures/alice.sign  --public_key_path keys/id_rsa.pub --hash_fn_name SHA3_512
    ##  --> Signatue INVALID <-- as the message changed

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~ SIGNATURE PARSERS ~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    certificate_parser = action_subparsers.add_parser("cert")
    certificate_subparsers = certificate_parser.add_subparsers(title="certificate_action", dest="certificate_action")

    certificate_location_parser = argparse.ArgumentParser(add_help=False)
    certificate_location_parser.add_argument("--cert_savedir", "-cs", required=True)
    certificate_location_parser.add_argument("--cert_part1_filename", '-c1f', default="cert.part1")
    certificate_location_parser.add_argument("--cert_part2_filename", '-c2f', default="cert.part2")
    certificate_location_parser.add_argument("--cert_part3_filename", '-c3f', default="cert.part3")

    # create
    create_certificate_parser = certificate_subparsers.add_parser(
        "create", help="create a certificate",
        parents=[hash_fn_parser, message_path_parser, private_key_path_parser, public_key_path_parser, symmetric_parser,
                 certificate_location_parser])
    open_certificate_parser = certificate_subparsers.add_parser(
        "open", help="open a certificate",
        parents=[hash_fn_parser, private_key_path_parser, public_key_path_parser, symmetric_parser,
                 certificate_location_parser])

    # USAGE
    ## ~~~ ALICE ~~~ #
    # mkdir -p keys/alice
    # ./main.py gen --n 2048 --savedir keys/alice
    ## ~~~ BOB ~~~ #
    # mkdir -p keys/bob
    # ./main.py gen --n 3072 --savedir keys/bob
    #
    ## ~~~ ALICE ~~~ #
    # mkdir -p certificates/alice
    # ./main.py cert create --message_path messages/alice.txt --cert_savedir certificates/alice  --public_key_path keys/bob/id_rsa.pub --private_key_path keys/alice/id_rsa --hash_fn_name SHA3_512 --sym_algo AES --sym_key 12345678abcdefgh87654321 --sym_key_length 24 --sym_iv 12345678abcdefgh --sym_mode OFB
    #
    ## ~~~ BOB ~~~ #
    # ./main.py cert open --cert_savedir certificates/alice --public_key_path keys/alice/id_rsa.pub --private_key_path keys/bob/id_rsa --hash_fn_name SHA3_512 --sym_algo AES --sym_key_length 24 --sym_mode OFB
    ##  --> Signatue OK
    #
    # ./main.py cert open --cert_savedir certificates/alice --public_key_path keys/bob/id_rsa.pub --private_key_path keys/alice/id_rsa --hash_fn_name SHA3_512 --sym_algo AES --sym_key_length 24 --sym_mode OFB
    ##  --> Signatue INVALID <-- as the keys are switched
    #
    # ./main.py cert open --cert_part1_filename cert.part2 --cert_savedir certificates/alice --public_key_path keys/alice/id_rsa.pub --private_key_path keys/bob/id_rsa --hash_fn_name SHA3_512 --sym_algo AES --sym_key_length 24 --sym_mode OFB
    ##  --> Signatue INVALID <-- as sym_enc_msg changed

    # ~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~ RUN DEMO ~~~~~~ #
    # ~~~~~~~~~~~~~~~~~~~~~~ #
    args = main_parser.parse_args()
    print(args)

    if args.action_command == "gen":
        generate_keys(args)
    elif args.action_command == "envelope":
        if args.envelope_action == "create":
            create_envelope(args)
        else:
            open_envelope(args)
    elif args.action_command == "signature":
        if args.signature_action == "sign":
            sign(args)
        else:
            verify_signature(args)
    elif args.action_command == "cert":
        if args.certificate_action == "create":
            create_cert(args)
        else:
            open_cert(args)

    print(bcolors.OKGREEN + "✓" + bcolors.ENDC)
