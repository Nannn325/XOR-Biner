"""
Aplikasi Operasi XOR Data Biner & Teks
Menggunakan Flask Framework
Tanpa Emoticon
"""

import os
from flask import Flask, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR)


def hitung_xor_biner(bin1: str, bin2: str) -> tuple[dict, str]:
    """
    Menghitung XOR dari dua string biner (hanya berisi 0 dan 1).
    Mengembalikan data detail bit-by-bit dan string hasil XOR.
    """
    # Bersihkan spasi
    b1 = bin1.replace(" ", "").strip()
    b2 = bin2.replace(" ", "").strip()

    # Validasi hanya karakter 0 dan 1
    if not all(c in '01' for c in b1) or not all(c in '01' for c in b2):
        raise ValueError("Input biner hanya boleh berisi angka 0 dan 1.")

    if not b1 or not b2:
        raise ValueError("Input biner tidak boleh kosong.")

    # Samakan panjang bit dengan menambahkan leading zero (0 di kiri)
    max_len = max(len(b1), len(b2))
    b1_padded = b1.zfill(max_len)
    b2_padded = b2.zfill(max_len)

    bit_details = []
    hasil_bits = []

    for i in range(max_len):
        bit_a = int(b1_padded[i])
        bit_b = int(b2_padded[i])
        xor_res = bit_a ^ bit_b

        bit_details.append({
            'pos': i + 1,
            'bit1': bit_a,
            'bit2': bit_b,
            'hasil': xor_res,
            'ekspresi': f"{bit_a} XOR {bit_b} = {xor_res}"
        })
        hasil_bits.append(str(xor_res))

    hasil_biner = "".join(hasil_bits)

    # Hitung nilai desimal
    dec1 = int(b1_padded, 2)
    dec2 = int(b2_padded, 2)
    dec_hasil = int(hasil_biner, 2)

    data_ringkasan = {
        'b1_padded': b1_padded,
        'b2_padded': b2_padded,
        'hasil_biner': hasil_biner,
        'dec1': dec1,
        'dec2': dec2,
        'dec_hasil': dec_hasil,
        'bit_details': bit_details
    }

    return data_ringkasan


def hitung_xor_teks(teks: str, kunci: str) -> dict:
    """
    Menghitung XOR dari teks ASCII dengan kunci teks/biner.
    """
    if not teks or not kunci:
        raise ValueError("Teks dan Kunci tidak boleh kosong.")

    bytes_teks = teks.encode('utf-8')
    bytes_kunci = kunci.encode('utf-8')

    detail_karakter = []
    hasil_bytes = bytearray()
    hasil_biner_list = []

    for i, char_byte in enumerate(bytes_teks):
        key_byte = bytes_kunci[i % len(bytes_kunci)]
        xor_byte = char_byte ^ key_byte
        hasil_bytes.append(xor_byte)

        bin_char = format(char_byte, '08b')
        bin_key = format(key_byte, '08b')
        bin_xor = format(xor_byte, '08b')
        hasil_biner_list.append(bin_xor)

        detail_karakter.append({
            'char': chr(char_byte) if 32 <= char_byte <= 126 else '?',
            'key_char': chr(key_byte) if 32 <= key_byte <= 126 else '?',
            'bin_char': bin_char,
            'bin_key': bin_key,
            'bin_xor': bin_xor,
            'dec_xor': xor_byte,
            'hex_xor': f"0x{xor_byte:02X}"
        })

    # Konversi hasil byte ke string jika printable
    hasil_teks = "".join(chr(b) if 32 <= b <= 126 else '.' for b in hasil_bytes)
    hasil_hex = " ".join(f"{b:02X}" for b in hasil_bytes)
    hasil_biner = " ".join(hasil_biner_list)

    return {
        'hasil_teks': hasil_teks,
        'hasil_hex': hasil_hex,
        'hasil_biner': hasil_biner,
        'detail': detail_karakter
    }


@app.route("/", methods=["GET", "POST"])
def index():
    mode = "biner"
    bin1 = ""
    bin2 = ""
    teks = ""
    kunci = ""
    hasil_data = None
    error = None

    if request.method == "POST":
        mode = request.form.get("mode", "biner")

        if mode == "biner":
            bin1 = request.form.get("bin1", "").strip()
            bin2 = request.form.get("bin2", "").strip()
            try:
                hasil_data = hitung_xor_biner(bin1, bin2)
            except ValueError as e:
                error = str(e)

        elif mode == "teks":
            teks = request.form.get("teks", "").strip()
            kunci = request.form.get("kunci", "").strip()
            try:
                hasil_data = hitung_xor_teks(teks, kunci)
            except ValueError as e:
                error = str(e)

    # Tabel Kebenaran XOR (Truth Table)
    tabel_kebenaran = [
        {'a': 0, 'b': 0, 'res': 0},
        {'a': 0, 'b': 1, 'res': 1},
        {'a': 1, 'b': 0, 'res': 1},
        {'a': 1, 'b': 1, 'res': 0},
    ]

    return render_template(
        "index.html",
        mode=mode,
        bin1=bin1,
        bin2=bin2,
        teks=teks,
        kunci=kunci,
        hasil_data=hasil_data,
        error=error,
        tabel_kebenaran=tabel_kebenaran
    )


if __name__ == "__main__":
    app.run(debug=True, port=5003)
