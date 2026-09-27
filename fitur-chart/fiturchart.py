import argparse
import sys

PRODUK = [
    {"nama": "Cangkir Keramik Senja", "kategori": "Rumah", "harga": 129000, "rating": 4.9},
    {"nama": "Kopi Arabika Lereng", "kategori": "Rasa", "harga": 89000, "rating": 4.8},
    {"nama": "Lilin Aromaterapi Kayu", "kategori": "Rumah", "harga": 75000, "rating": 4.7},
    {"nama": "Totebag Kanvas Harian", "kategori": "Gaya", "harga": 149000, "rating": 4.9},
    {"nama": "Teh Melati Pagi", "kategori": "Rasa", "harga": 59000, "rating": 4.8},
    {"nama": "Vas Keramik Organik", "kategori": "Rumah", "harga": 179000, "rating": 4.6},
    {"nama": "Dompet Kulit Minimal", "kategori": "Gaya", "harga": 219000, "rating": 4.9},
    {"nama": "Madu Hutan Murni", "kategori": "Rasa", "harga": 99000, "rating": 4.8},
]

TIPE_GRAFIK = {
    "harga": "GRAFIK HARGA PRODUK (Rupiah)",
    "kategori": "JUMLAH PRODUK PER KATEGORI",
    "rating": "GRAFIK RATING PRODUK (skala 0-5)",
}


def rupiah(angka):
    return "Rp" + format(int(angka), ",").replace(",", ".")


def potong(teks, panjang):
    if len(teks) <= panjang:
        return teks
    return teks[: panjang - 1] + "…"


def bar_chart(judul, label, nilai, lebar=28, simbol="#"):
    if not nilai:
        return "%s\n(tidak ada data)\n" % judul

    tertinggi = max(nilai)
    if tertinggi <= 0:
        return "%s\n(tidak ada data)\n" % judul

    lebar_label = max(len(str(item)) for item in label)
    kolom = []
    for item, angka in zip(label, nilai):
        panjang = int(round(angka / tertinggi * lebar)) if angka > 0 else 0
        kolom.append((potong(str(item), lebar_label), simbol * panjang, "%g" % angka))

    lebar_bar = max(len(bar) for _, bar, _ in kolom)
    lebar_nilai = max(len(teks) for _, _, teks in kolom)
    garis = "-" * (lebar_label + lebar_bar + lebar_nilai + 4)

    baris = [judul, garis]
    for teks_label, bar, teks_nilai in kolom:
        baris.append("%s | %s %s" % (teks_label, bar.ljust(lebar_bar), teks_nilai.ljust(lebar_nilai)))
    return "\n".join(baris) + "\n"


def data_harga():
    return [produk["nama"] for produk in PRODUK], [produk["harga"] for produk in PRODUK]


def data_kategori():
    kategori = []
    for produk in PRODUK:
        if produk["kategori"] not in kategori:
            kategori.append(produk["kategori"])
    jumlah = [sum(1 for p in PRODUK if p["kategori"] == k) for k in kategori]
    return kategori, jumlah


def data_rating():
    return [produk["nama"] for produk in PRODUK], [produk["rating"] for produk in PRODUK]


def gambar_grafik(tipe, lebar=28):
    if tipe == "harga":
        label, nilai = data_harga()
    elif tipe == "kategori":
        label, nilai = data_kategori()
    else:
        label, nilai = data_rating()
    return bar_chart(TIPE_GRAFIK[tipe], label, nilai, lebar=lebar)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Chart sederhana data produk Ruang Rasa")
    parser.add_argument(
        "--tipe",
        choices=sorted(TIPE_GRAFIK) + ["semua"],
        default="semua",
        help="jenis chart yang ditampilkan (default: semua)",
    )
    parser.add_argument("--lebar", type=int, default=28, help="lebar bar chart (default: 28)")
    args = parser.parse_args(argv)

    if args.lebar < 1:
        parser.error("--lebar minimal 1")

    if args.tipe == "semua":
        for tipe in TIPE_GRAFIK:
            print(gambar_grafik(tipe, args.lebar))
        print(
            "Ringkasan: %d produk, harga %s - %s, rata-rata rating %.2f"
            % (
                len(PRODUK),
                rupiah(min(p["harga"] for p in PRODUK)),
                rupiah(max(p["harga"] for p in PRODUK)),
                sum(p["rating"] for p in PRODUK) / len(PRODUK),
            )
        )
        return 0

    print(gambar_grafik(args.tipe, args.lebar))
    return 0


if __name__ == "__main__":
    sys.exit(main())
