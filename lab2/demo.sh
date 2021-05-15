#!/usr/bin/env bash

#!/bin/bash
function title(){
  w=$((${#1}))
  printf "\e[1;34m# ~~~~~~"
  printf '~%.0s' $(seq 1 $w)
  printf "~~~~~~ #\n"

  printf "# ~~~~  $1  ~~~~ #\e[1;37m\n"

  printf "\e[1;34m# ~~~~~~"
  printf '~%.0s' $(seq 1 $w)
  printf "~~~~~~ #\e[0m\n"
}

function subtitle(){
  printf "\e[1;35m# ~~~~  $1  ~~~~ #\e[0m\n"
}


title "KEY GENERATION"

mkdir -p keys
./main.py gen --n 3072 --savedir keys


title "ENVELOPE"

mkdir -p envelope messages
echo "jure i mate" > messages/alice.txt

subtitle "AES192 + OFB"
subtitle "CREATE ENVELOPE"
./main.py envelope create --message_path messages/alice.txt --public_key_path keys/id_rsa.pub --envelope_savedir envelope --sym_algo AES --sym_key 12345678abcdefgh87654321 --sym_key_length 24 --sym_iv 12345678abcdefgh --sym_mode OFB
subtitle "OPEN ENVELOPE"
./main.py envelope open --envelope_savedir envelope --private_key_path keys/id_rsa --envelope_savedir envelope --sym_algo AES --sym_key_length 24 --sym_mode OFB

subtitle "AES256 + CFB"
subtitle "CREATE ENVELOPE"
./main.py envelope create --message_path messages/alice.txt --public_key_path keys/id_rsa.pub --envelope_savedir envelope --sym_algo AES --sym_key 12345678abcdefgh87654321hgfedcba --sym_key_length 24 --sym_iv 12345678abcdefgh --sym_mode CFB
subtitle "OPEN ENVELOPE"
./main.py envelope open --envelope_savedir envelope --private_key_path keys/id_rsa --envelope_savedir envelope --sym_algo AES --sym_key_length 32 --sym_mode CFB

subtitle "3DES + ECB"
subtitle "CREATE ENVELOPE"
./main.py envelope create --message_path messages/alice.txt --public_key_path keys/id_rsa.pub --envelope_savedir envelope --sym_algo 3DES --sym_key 12345678abcdefgh87654321 --sym_key_length 24 --sym_mode ECB
subtitle "OPEN ENVELOPE"
./main.py envelope open --envelope_savedir envelope --private_key_path keys/id_rsa --envelope_savedir envelope --sym_algo 3DES --sym_key_length 24 --sym_mode ECB


title "SIGNATURE"

for hash_fn in  "MD5" "SHA256" "SHA3_512" "SHA384"
do
  subtitle hash_fn
  mkdir signatures
  subtitle "SIGN MESSAGE"
  ./main.py signature sign --message_path messages/alice.txt --signature_path signatures/alice.sign --private_key_path keys/id_rsa --hash_fn_name $hash_fn

  subtitle "VERIFY VALID SIGNATURE"
  ./main.py signature verify --message_path messages/alice.txt --signature_path signatures/alice.sign  --public_key_path keys/id_rsa.pub --hash_fn_name $hash_fn

  subtitle "VERIFY INVALID SIGNATURE"
  cp messages/alice.txt messages/alice_modified.txt && echo "." >> messages/alice_modified.txt
  ./main.py signature verify --message_path messages/alice_modified.txt --signature_path signatures/alice.sign  --public_key_path keys/id_rsa.pub --hash_fn_name $hash_fn
done



title "CERTIFICATE"
subtitle "ALICE GENERATES HER KEYS -- RSA 2048"
mkdir -p keys/alice
./main.py gen --n 2048 --savedir keys/alice

subtitle "BOB GENERATES HIS KEYS -- RSA 3072"
mkdir -p keys/bob
./main.py gen --n 3072 --savedir keys/bob
echo

subtitle "ALICE CREATES A CERTIFICATE"
mkdir -p certificates/alice
./main.py cert create --message_path messages/alice.txt --cert_savedir certificates/alice  --public_key_path keys/bob/id_rsa.pub --private_key_path keys/alice/id_rsa --hash_fn_name SHA3_512 --sym_algo AES --sym_key 12345678abcdefgh87654321 --sym_key_length 24 --sym_iv 12345678abcdefgh --sym_mode OFB

subtitle "BOB OPENS THE CERTIFICATE -- BUT FORGETS WHICH KEY WAS WHICH AND SWITCHES THEM"
./main.py cert open --cert_savedir certificates/alice --public_key_path keys/bob/id_rsa --private_key_path keys/alice/id_rsa.pub --hash_fn_name SHA3_512 --sym_algo AES --sym_key_length 24 --sym_mode OFB

subtitle "BOB OPENS THE CERTIFICATE -- WITH CORRECT KEYS"
./main.py cert open --cert_savedir certificates/alice --public_key_path keys/alice/id_rsa.pub --private_key_path keys/bob/id_rsa --hash_fn_name SHA3_512 --sym_algo AES --sym_key_length 24 --sym_mode OFB

subtitle "BOB OPENS THE CERTIFICATE -- BUT EVE TRIED TO CHANGE the encrypted message sym_enc_msg (cert.part1)"
cp certificates/alice/cert.part1 certificates/alice/cert.part1.eve && echo "." >> certificates/alice/cert.part1.eve
./main.py cert open --cert_part1_filename cert.part1.eve --cert_savedir certificates/alice --public_key_path keys/alice/id_rsa.pub --private_key_path keys/bob/id_rsa --hash_fn_name SHA3_512 --sym_algo AES --sym_key_length 24 --sym_mode OFB

