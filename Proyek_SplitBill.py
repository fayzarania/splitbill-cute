import math
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aplikasi Split Bill Proporsional", page_icon="🧾", layout="centered")

st.markdown("""
<style>
/* 1. Subjudul (1. Daftar Peserta, dll.) Pakai Font Sambung Berjarak Lega & Lebih Tebal */
h1, h2, h3, h3 span, [data-testid="stHeadingWithActionElements"] h3, [data-testid="stMarkdownContainer"] h3 {
    font-family: 'Segoe Script', 'Lucida Handwriting', 'Brush Script MT', cursive !important;
    font-size: 29px !important;
    font-weight: 900 !important;
    letter-spacing: 2px !important;
    word-spacing: 5px !important;
    color: #D61C7A !important;
    -webkit-text-stroke: 0.9px #D61C7A !important;
    text-shadow: 2px 2px 0px #FFD1DC !important;
    line-height: 1.5 !important;
}

/* 2. Tulisan Kecil Pakai Font Halus & Berwarna Plum Lembut */
label, label p, .stRadio label p, .stMultiSelect label p, .stNumberInput label p, .stTextInput label p, .stCaption, p {
    font-family: 'Segoe UI', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    color: #8A3B63 !important;
}

/* 3. Latar Belakang Pink Pastel + Bintik Polkadot Murni CSS */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #FFF4F8 !important;
    background-image: radial-gradient(#FFB3C1 2.2px, transparent 2.2px), radial-gradient(#FFC2D1 2.2px, #FFF4F8 2.2px) !important;
    background-size: 44px 44px !important;
    background-position: 0 0, 22px 22px !important;
}

/* 4. Tombol Timbul 3D Ala Game Lucu */
div.stButton > button:first-child {
    font-family: 'Segoe UI', sans-serif !important;
    font-weight: 800 !important;
    background: linear-gradient(180deg, #FF758F 0%, #FF4D6D 100%) !important;
    color: white !important;
    border: 3px solid #FFF0F3 !important;
    border-radius: 25px !important;
    padding: 10px 26px !important;
    font-size: 16px !important;
    box-shadow: 0px 5px 0px #C9184A, 0px 8px 15px rgba(255, 77, 109, 0.35) !important;
}
/* Wadah Utama di Tengah Berbentuk Kartu Pop-Up Putih Menggemaskan */
[data-testid="stMainBlockContainer"], .block-container {
    background-color: rgba(255, 255, 255, 0.94) !important;
    border: 4px solid #FFC2D1 !important;
    border-radius: 36px !important;
    padding: 32px 28px !important;
    margin-top: 24px !important;
    margin-bottom: 30px !important;
    box-shadow: 0px 12px 30px rgba(255, 117, 143, 0.25), 0px 0px 0px 6px rgba(255, 240, 245, 0.8) !important;
}
/* 5. Kotak Form Pesanan Ala Kartu Game */
div[data-testid="stForm"] {
    background-color: rgba(255, 255, 255, 0.92) !important;
    border: 3px dashed #FF8FA3 !important;
    border-radius: 24px !important;
    padding: 22px !important;
}

/* 6. Kotak Input Membulat */
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
    border-radius: 15px !important;
    border: 2px solid #FFB3C1 !important;
    background-color: #FFFDFD !important;
}

/* Dekorasi Mengambang Matematika & Makanan di Pinggir Layar */
.bg-dekor {
    position: fixed;
    pointer-events: none;
    z-index: 0;
    opacity: 0.32;
    font-weight: bold;
    color: #FF4D6D;
    user-select: none;
}
@media (max-width: 768px) {
    .boneka-atas { font-size: 22px !important; top: 52px !important; }
    .boneka-bawah { font-size: 22px !important; bottom: 8px !important; opacity: 0.75; }
}
</style>

<!-- Ornamen Simbol Matematika & Makanan di Sekeliling Layar -->
<div class="bg-dekor" style="top: 12%; left: 4%; font-size: 32px;">∑</div>
<div class="bg-dekor" style="top: 28%; left: 7%; font-size: 30px;">🍰</div>
<div class="bg-dekor" style="top: 48%; left: 3%; font-size: 30px;">÷</div>
<div class="bg-dekor" style="top: 68%; left: 6%; font-size: 30px;">🧋</div>
<div class="bg-dekor" style="top: 85%; left: 4%; font-size: 30px;">π</div>

<div class="bg-dekor" style="top: 15%; right: 5%; font-size: 30px;">🍓</div>
<div class="bg-dekor" style="top: 34%; right: 4%; font-size: 30px;">%</div>
<div class="bg-dekor" style="top: 54%; right: 6%; font-size: 30px;">🍜</div>
<div class="bg-dekor" style="top: 74%; right: 4%; font-size: 30px;">√x</div>
<div class="bg-dekor" style="top: 88%; right: 7%; font-size: 28px;">✨</div>
<div class="boneka-bawah" style="position: fixed; bottom: 18px; left: 22px; font-size: 62px; z-index: 99; pointer-events: none; filter: drop-shadow(2px 4px 6px rgba(214,28,122,0.25)); transform: rotate(-8deg);">🧸</div>
<div class="boneka-bawah" style="position: fixed; bottom: 18px; right: 22px; font-size: 62px; z-index: 99; pointer-events: none; filter: drop-shadow(2px 4px 6px rgba(214,28,122,0.25)); transform: rotate(8deg);">🐰</div>
<div class="boneka-atas" style="position: fixed; top: 75px; left: 10px; font-size: 54px; z-index: 99; pointer-events: none; filter: drop-shadow(2px 4px 6px rgba(214,28,122,0.22)); transform: rotate(-10deg);">🐱</div>

<div class="boneka-atas" style="position: fixed; top: 75px; right: 6px; font-size: 54px; z-index: 99; pointer-events: none; filter: drop-shadow(2px 4px 6px rgba(214,28,122,0.22)); transform: rotate(10deg);">🐼</div>
<!-- Banner Utama: Rangkaian Rapat & Ekstra Tebal -->
<div style="background: linear-gradient(135deg, #FF758F 0%, #FF9EBB 50%, #FF5C8A 100%); padding: 28px 20px; border-radius: 28px; text-align: center; margin-bottom: 24px; border: 4px solid #FFFFFF; box-shadow: 0px 8px 20px rgba(255, 92, 138, 0.38);">
<div style="font-size: 36px; margin-bottom: 6px;">🍰 🧋 🍓 ✨ 🎀</div>
<div style="font-family: 'Brush Script MT', 'Segoe Script', cursive; font-size: 54px; font-weight: 900; letter-spacing: 0px; color: #FFFFFF; -webkit-text-stroke: 1px #FFFFFF; text-shadow: 3px 3px 0px #C9184A; line-height: 1.2;">Split Bill Proporsional</div>
<div style="margin-top: 12px; font-family: 'Segoe UI', sans-serif; font-size: 13.5px; color: #FFFFFF; font-weight: 700; background: rgba(255,255,255,0.25); display: inline-block; padding: 6px 18px; border-radius: 20px;">🎮 Porsi Per Orang • 🎟️ Voucher Min-Max • 💖 Multi-Pembayar • 🪙 Pembulatan Adil</div>
</div>
""", unsafe_allow_html=True)
if "halaman" not in st.session_state:
    st.session_state.halaman = "depan"

if st.session_state.halaman == "depan":
    st.markdown("""
    <div style="text-align: center; padding: 15px 10px;">
        <div style="font-size: 52px; margin-bottom: 10px;">🧸 🍰 🧮 🧋 🐰</div>
        <h3 style="margin-bottom: 8px;">Sweet Hangout, Fair Split!</h3>
        <p style="font-size: 15px !important; max-width: 520px; margin: 0 auto 20px auto; line-height: 1.6;">
            Hitung pembagian tagihan nongkrong, makan bareng, atau pesan online secara <b>proporsional</b> lengkap dengan porsi per orang, syarat voucher min-max, multi-pembayar, hingga pencatatan sisa utang!
        </p>
        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin-bottom: 24px;">
            <span style="background: #FFE5EC; color: #D61C7A; padding: 6px 14px; border-radius: 15px; font-weight: 700; font-size: 13px;">✨ Adil & Transparan</span>
            <span style="background: #FFE5EC; color: #D61C7A; padding: 6px 14px; border-radius: 15px; font-weight: 700; font-size: 13px;">🎟️ Voucher Min-Max</span>
            <span style="background: #FFE5EC; color: #D61C7A; padding: 6px 14px; border-radius: 15px; font-weight: 700; font-size: 13px;">📱 Siap Kirim ke WA</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    if col_btn2.button("🚀 Mulai Hitung Split Bill", use_container_width=True):
        st.session_state.halaman = "kalkulator"
        st.rerun()

    st.stop()

if st.button("⬅️ Kembali ke Halaman Depan"):
    st.session_state.halaman = "depan"
    st.rerun()
st.subheader("1. Daftar Peserta")
input_nama = st.text_input("Masukkan nama peserta (pisahkan dengan koma)", placeholder="Contoh: Fayza, Amira, Navia")
daftar_peserta = list(dict.fromkeys(nama.strip() for nama in input_nama.split(",") if nama.strip()))

if "pesanan" not in st.session_state:
    st.session_state.pesanan = []

st.subheader("2. Tambah Menu Pesanan")
with st.form("form_item", clear_on_submit=True):
    col1, col2 = st.columns((2, 1.5))
    nama_menu = col1.text_input("Nama Menu (misal: Mie Gacoan)")
    harga_satuan = col2.number_input("Harga Satuan (Rp)", min_value=0, step=1000)
    
    st.write("**Masukkan jumlah porsi tiap peserta** *(Isi 0 jika tidak pesan, atau 0.5 jika patungan berdua)*:")
    cols_porsi = st.columns(4) if daftar_peserta else ()
    porsi_peserta = {}
    for idx, nama in enumerate(daftar_peserta):
        kolom_aktif = cols_porsi.__getitem__(idx % 4)
        porsi_peserta.update({nama: kolom_aktif.number_input(f"{nama}", min_value=0.0, value=0.0, step=0.5, key=f"porsi_{nama}")})
            
    submitted = st.form_submit_button("Masukkan ke Keranjang")
    if submitted:
        pemesan_aktif = {k: v for k, v in porsi_peserta.items() if v > 0}
        if not nama_menu or harga_satuan <= 0 or not pemesan_aktif:
            st.warning("Isi nama menu, harga satuan, dan masukkan minimal 1 porsi peserta ya!")
        else:
            total_qty = sum(pemesan_aktif.values())
            total_item = harga_satuan * total_qty
            rincian_porsi_str = ", ".join(f"{k} ({v:g}x)" for k, v in pemesan_aktif.items())
            st.session_state.pesanan.append({
                "Menu": nama_menu,
                "Qty": total_qty,
                "Total Harga": total_item,
                "Harga Satuan": harga_satuan,
                "Porsi Detail": pemesan_aktif,
                "Keterangan": rincian_porsi_str
            })
            st.toast(f"{nama_menu} ({total_qty:g} porsi) masuk keranjang!")

if st.session_state.pesanan:
    st.write("**Keranjang Pesanan Saat Ini:**")
    df_tampil = pd.DataFrame(
        {
            "No": idx + 1,
            "Menu": item.get("Menu"),
            "Total Porsi": f"{item.get('Qty'):g}",
            "Total (Rp)": f"Rp {item.get('Total Harga'):,.0f}",
            "Rincian Porsi": item.get("Keterangan")
        }
        for idx, item in enumerate(st.session_state.pesanan)
    )
    st.dataframe(df_tampil, use_container_width=True, hide_index=True)
    
    col_del1, col_del2, col_del3 = st.columns((2, 1, 1.2))
    opsi_hapus = tuple(f"{idx+1}. {item.get('Menu')} ({item.get('Qty'):g} porsi)" for idx, item in enumerate(st.session_state.pesanan))
    item_dipilih = col_del1.selectbox("Pilih item yang salah:", opsi_hapus, label_visibility="collapsed")
    if col_del2.button("Hapus Item Ini"):
        idx_hapus = int(item_dipilih.split(".").__getitem__(0)) - 1
        st.session_state.pesanan.pop(idx_hapus)
        st.rerun()
    if col_del3.button("Hapus Semua"):
        st.session_state.pesanan = []
        st.rerun()

st.subheader("3. Pajak, Biaya Tambahan & Voucher Promo")
c1, c2 = st.columns(2)
persen_service = c1.number_input("Service Charge (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
persen_pajak = c2.number_input("Pajak Restoran / PB1 (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0)

c3, c4 = st.columns(2)
biaya_ongkir = c3.number_input("Ongkir & Biaya Aplikasi (Rp)", min_value=0, step=1000)
biaya_parkir = c4.number_input("Biaya Parkir - Dibagi Rata Adil (Rp)", min_value=0, step=1000)

jenis_diskon = st.radio(
    "Pilih Jenis Voucher Promo:",
    ("Tidak Ada", "Potongan Nominal (Rp)", "Persentase (%) dengan Syarat Min & Maks"),
    horizontal=True
)

nilai_diskon = 0.0
min_belanja = 0
maks_diskon = 0

if jenis_diskon == "Potongan Nominal (Rp)":
    cd1, cd2 = st.columns(2)
    nilai_diskon = cd1.number_input("Nominal Potongan (Rp)", min_value=0, step=1000)
    min_belanja = cd2.number_input("Minimal Belanja (Rp)", min_value=0, step=5000)
elif jenis_diskon == "Persentase (%) dengan Syarat Min & Maks":
    cd1, cd2, cd3 = st.columns(3)
    nilai_diskon = cd1.number_input("Diskon (%)", min_value=0.0, max_value=100.0, step=5.0)
    min_belanja = cd2.number_input("Min. Belanja (Rp)", min_value=0, step=5000)
    maks_diskon = cd3.number_input("Maks. Potongan (0 = Tanpa Batas)", min_value=0, step=1000)

st.write("**Pengaturan Pembulatan (Selalu ke Atas Agar Pentalang Tidak Rugi):**")
mode_bulat = st.radio(
    "Pilih kelipatan pembulatan praktis:",
    ("Tanpa Pembulatan (100% Eksak)", "Bulatkan ke Rp500 (ke atas)", "Bulatkan ke Rp1.000 (ke atas)"),
    horizontal=True
)

subtotal_orang = {nama: 0.0 for nama in daftar_peserta}
for item in st.session_state.pesanan:
    detail = item.get("Porsi Detail", {})
    harga_sat = item.get("Harga Satuan", 0)
    for p, jml_porsi in detail.items():
        if p in subtotal_orang:
            subtotal_orang.update({p: subtotal_orang.get(p, 0.0) + (harga_sat * jml_porsi)})

subtotal_semua = sum(subtotal_orang.values())
nom_diskon = 0.0
pesan_promo = ""
if jenis_diskon != "Tidak Ada" and subtotal_semua > 0:
    if subtotal_semua < min_belanja:
        kurang = min_belanja - subtotal_semua
        pesan_promo = f"Voucher tidak aktif! Belanja (Rp {subtotal_semua:,.0f}) masih kurang Rp {kurang:,.0f} dari minimal Rp {min_belanja:,.0f}."
    else:
        if jenis_diskon == "Potongan Nominal (Rp)":
            nom_diskon = min(nilai_diskon, subtotal_semua)
        else:
            nom_diskon = subtotal_semua * (nilai_diskon / 100) if maks_diskon == 0 else min(subtotal_semua * (nilai_diskon / 100), maks_diskon)
        pesan_promo = f"Voucher Aktif! Hemat Rp {nom_diskon:,.0f}"

nom_service = subtotal_semua * (persen_service / 100)
nom_pajak = (subtotal_semua + nom_service) * (persen_pajak / 100)
total_proporsional_bersih = nom_service + nom_pajak + biaya_ongkir - nom_diskon
grand_total_estimasi = subtotal_semua + total_proporsional_bersih + biaya_parkir

st.subheader("4. Pembayaran di Kasir (Bisa Lebih dari 1 Orang)")
if subtotal_semua > 0:
    st.info(f"Total Tagihan Kasir Saat Ini: **Rp {grand_total_estimasi:,.0f}** *(Gunakan patokan ini untuk mengisi talangan)*")

pembayar_terpilih = st.multiselect(
    "Pilih siapa saja yang menalangi bayar di kasir:",
    daftar_peserta,
    default=daftar_peserta[:1]
)

nominal_talangan = {nama: 0.0 for nama in daftar_peserta}

if pembayar_terpilih:
    if len(pembayar_terpilih) == 1:
        p_tunggal = ", ".join(pembayar_terpilih)
        nominal_talangan.update({p_tunggal: grand_total_estimasi})
        st.caption(f"**{p_tunggal}** menalangi penuh sebesar **Rp {grand_total_estimasi:,.0f}**.")
    else:
        st.write("Masukkan nominal talangan pertama, sisanya otomatis untuk pentalang terakhir:")
        sudah_dibayar = 0.0
        for idx_p, p_nama in enumerate(pembayar_terpilih):
            if idx_p < len(pembayar_terpilih) - 1:
                val_byr = st.number_input(f"Talangan {p_nama} (Rp)", min_value=0.0, step=5000.0, key=f"byr_{p_nama}")
                nominal_talangan.update({p_nama: val_byr})
                sudah_dibayar += val_byr
            else:
                sisa_byr = max(0.0, grand_total_estimasi - sudah_dibayar)
                nominal_talangan.update({p_nama: sisa_byr})
                st.success(f"Sisa otomatis ditalangi **{p_nama}**: **Rp {sisa_byr:,.0f}**")

st.markdown("---")
if st.button("HITUNG PEMBAGIAN TAGIHAN", type="primary", use_container_width=True):
    st.session_state.sudah_hitung = True
    if "df_pelunasan" in st.session_state:
        del st.session_state.df_pelunasan

if st.session_state.get("sudah_hitung"):
    if not st.session_state.pesanan or not daftar_peserta or not pembayar_terpilih:
        st.error("Pastikan pesanan sudah diisi dan minimal ada 1 orang pembayar di kasir!")
    else:
        parkir_per_orang = biaya_parkir / len(daftar_peserta)
        grand_total = grand_total_estimasi

        st.balloons()
        if pesan_promo:
            if "tidak aktif" in pesan_promo:
                st.warning(pesan_promo)
            else:
                st.info(pesan_promo)

        m1, m2, m3 = st.columns(3)
        m1.metric("Subtotal Makanan", f"Rp {subtotal_semua:,.0f}")
        m2.metric("Pajak + Ongkir + Parkir - Diskon", f"Rp {total_proporsional_bersih + biaya_parkir:,.0f}")
        m3.metric("GRAND TOTAL KASIR", f"Rp {grand_total:,.0f}")

        max_belanja = max(subtotal_orang.values())
        min_belanja_orang = min(subtotal_orang.values())
        net_balance = {}
        hasil_rincian = []

        for nama in daftar_peserta:
            sub_orang = subtotal_orang.get(nama, 0.0)
            talang_orang = nominal_talangan.get(nama, 0.0)
            rasio = (sub_orang / subtotal_semua) if subtotal_semua > 0 else 0
            jatah_asli = sub_orang + (rasio * total_proporsional_bersih) + parkir_per_orang

            if mode_bulat == "Bulatkan ke Rp500 (ke atas)":
                jatah_bulat = math.ceil(jatah_asli / 500) * 500
            elif mode_bulat == "Bulatkan ke Rp1.000 (ke atas)":
                jatah_bulat = math.ceil(jatah_asli / 1000) * 1000
            else:
                jatah_bulat = jatah_asli

            net_balance.update({nama: talang_orang - jatah_bulat})

            if talang_orang > 0:
                kategori = "Pembayar Kasir"
            elif sub_orang == max_belanja and max_belanja > 0:
                kategori = "Pesanan Terbanyak"
            elif sub_orang == min_belanja_orang:
                kategori = "Pesanan Terhemat"
            else:
                kategori = "Peserta"

            hasil_rincian.append({
                "Nama": nama,
                "Kategori": kategori,
                "Pesanan": f"Rp {sub_orang:,.0f}",
                "Porsi": f"{rasio*100:.1f}%",
                "Tagihan Asli": f"Rp {jatah_asli:,.0f}",
                "Tagihan Bulat": f"Rp {jatah_bulat:,.0f}",
                "Talangi Kasir": f"Rp {talang_orang:,.0f}"
            })

        st.subheader("1. Rincian Pembagian Tagihan")
        st.dataframe(pd.DataFrame(hasil_rincian), use_container_width=True, hide_index=True)

        debitur = list({"nama": nama, "sisa": -bal} for nama, bal in net_balance.items() if bal < -1)
        kreditur = list({"nama": nama, "sisa": bal} for nama, bal in net_balance.items() if bal > 1)
        
        instruksi_transfer = []
        i, j = 0, 0
        while i < len(debitur) and j < len(kreditur):
            deb_item = debitur.__getitem__(i)
            kre_item = kreditur.__getitem__(j)
            jumlah_tf = round(min(deb_item.get("sisa"), kre_item.get("sisa")))
            
            instruksi_transfer.append({
                "Pengirim": deb_item.get("nama"),
                "Penerima": kre_item.get("nama"),
                "Tagihan (Rp)": int(jumlah_tf),
                "Sudah Dibayar (Rp)": 0,
                "Metode Bayar": "Transfer Bank",
                "Waktu / Catatan": "-"
            })
            
            deb_item.update({"sisa": deb_item.get("sisa") - jumlah_tf})
            kre_item.update({"sisa": kre_item.get("sisa") - jumlah_tf})
            if deb_item.get("sisa") <= 1:
                i += 1
            if kre_item.get("sisa") <= 1:
                j += 1

        st.markdown("---")
        st.subheader("2. Pencatatan Pelunasan, Metode & Sisa Utang")
        st.caption("Isi kolom 'Sudah Dibayar (Rp)', pilih 'Metode Bayar', atau tambah 'Waktu / Catatan' (opsional):")
        if instruksi_transfer:
            if "df_pelunasan" not in st.session_state:
                for item in instruksi_transfer:
                    item.update({"Status Pelunasan": f"❌ BELUM BAYAR (Kurang Rp {item.get('Tagihan (Rp)'):,})"})
                st.session_state.df_pelunasan = pd.DataFrame(instruksi_transfer)

            df_edit_tf = st.data_editor(
                st.session_state.df_pelunasan,
                key="editor_pelunasan",
                column_config={
                    "Tagihan (Rp)": st.column_config.NumberColumn("Tagihan (Rp)", format="Rp %d"),
                    "Sudah Dibayar (Rp)": st.column_config.NumberColumn("Sudah Dibayar (Rp)", min_value=0, step=1000, format="Rp %d"),
                    "Metode Bayar": st.column_config.SelectboxColumn(
                        "Metode Bayar",
                        options=("Transfer Bank", "QRIS / E-Wallet", "Uang Tunai (Cash)"),
                        required=True
                    ),
                    "Waktu / Catatan": st.column_config.TextColumn("Waktu / Catatan", help="Isi tanggal/jam bayar atau biarkan '-'"),
                    "Status Pelunasan": st.column_config.TextColumn("Status Pelunasan (Otomatis)", width="large")
                },
                disabled=("Pengirim", "Penerima", "Tagihan (Rp)", "Status Pelunasan"),
                use_container_width=True,
                hide_index=True
            )

            daftar_tf_final = df_edit_tf.to_dict("records")
            ringkasan_status = []
            ada_perubahan = False

            for idx_row, tf in enumerate(daftar_tf_final):
                tgh = int(tf.get("Tagihan (Rp)", 0))
                byr = int(tf.get("Sudah Dibayar (Rp)", 0))
                metode = tf.get("Metode Bayar")
                catatan = str(tf.get("Waktu / Catatan", "-")).strip()
                sisa = max(0, tgh - byr)
                info_waktu = f" | {catatan}" if catatan and catatan != "-" else ""

                if sisa == 0:
                    ket = f"✅ LUNAS ({metode}{info_waktu})"
                elif byr > 0:
                    ket = f"⏳ KURANG Rp {sisa:,.0f} (Baru bayar Rp {byr:,.0f} - {metode}{info_waktu})"
                else:
                    ket = f"❌ BELUM BAYAR (Kurang Rp {tgh:,.0f}{info_waktu})"

                if tf.get("Status Pelunasan") != ket:
                    df_edit_tf.at[idx_row, "Status Pelunasan"] = ket
                    ada_perubahan = True

                ringkasan_status.append({
                    "Dari": tf.get("Pengirim"),
                    "Ke": tf.get("Penerima"),
                    "Status Pelunasan": ket
                })

            if ada_perubahan:
                st.session_state.df_pelunasan = df_edit_tf
                st.rerun()
        else:
            st.success("Semua tagihan sudah pas dan lunas!")
            ringkasan_status = ()
       

        if subtotal_semua > 0 and len(daftar_peserta) > 1:
            nama_terbanyak = max(subtotal_orang, key=subtotal_orang.get)
            nama_terhemat = min(subtotal_orang, key=subtotal_orang.get)
            
            st.subheader("3. Sorotan & Rekor Peserta")
            col_rek1, col_rek2 = st.columns(2)
            col_rek1.success(
                f"🏆 **Rekor Pesanan Terbanyak:**\n\n"
                f"**{nama_terbanyak}** (Pesanan awal **Rp {subtotal_orang.get(nama_terbanyak):,.0f}**)"
            )
            col_rek2.info(
                f"🌱 **Rekor Paling Hemat:**\n\n"
                f"**{nama_terhemat}** (Pesanan awal **Rp {subtotal_orang.get(nama_terhemat):,.0f}**)"
            )

        chat_wa = "*REKAP SPLIT BILL*\n"
        chat_wa += f"Total Struk Kasir: *Rp {grand_total:,.0f}*\n"
        if mode_bulat != "Tanpa Pembulatan (100% Eksak)":
            chat_wa += f"Catatan: _{mode_bulat} (angka asli tetap tercatat di tabel)_\n"
        chat_wa += "\n*Rincian Pelunasan:*\n"
        for st_item in ringkasan_status:
            chat_wa += f"- *{st_item.get('Dari')}* -> ke *{st_item.get('Ke')}*: {st_item.get('Status Pelunasan')}\n"

        with st.expander("Salin Pesan Siap Kirim ke Grup WhatsApp (Opsional)"):
         st.text_area("Blok dan salin teks di bawah ini untuk dikirim ke grup:", value=chat_wa, height=180)
        st.download_button(
            label="Download Struk Lengkap (.txt)",
            data=chat_wa.replace("*", "").replace("_", ""),
            file_name="rekap_split_bill_pro.txt",
            mime="text/plain"
        )

