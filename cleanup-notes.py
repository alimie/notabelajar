#!/usr/bin/env python3
"""
Cleanup semua nota migrated:
1. Buang semua artifact WordPress ('n' literal, nnnn, nnn, dsb)
2. Format semula content yang compact jadi proper Markdown
3. Tambah struktur note yang lebih teratur (heading, sections, tips, latihan)
4. Ringkaskan content yang terlalu verbose
"""

import os, re, glob

NOTES_DIR = os.path.join(os.path.dirname(__file__), 'src', 'content', 'notes')

def clean_artifact(text):
    """Buang semua WordPress formatting artifacts."""
    # Remove literal 'n' that appears as standalone (was <br/>)
    text = re.sub(r'(?<!\w)n(?!\w)', '', text)
    
    # Clean up multiple newlines
    text = re.sub(r'\n{4,}', '\n\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove leftover WordPress-style asterisk formatting *_text_*
    text = re.sub(r'\*_([^*]+)_\*', r'*\1*', text)
    
    return text.strip()

def remove_empty_lines(text):
    """Buang empty lines berlebihan."""
    lines = text.split('\n')
    result = []
    prev_empty = False
    for line in lines:
        is_empty = line.strip() == ''
        if is_empty and prev_empty:
            continue
        result.append(line)
        prev_empty = is_empty
    return '\n'.join(result)

def restructure_daya_tarikan_tolakan(text):
    """Restructure Daya Tarikan dan Tolakan."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    body = '---'.join(text.split('---')[2:]).strip()
    
    new_body = """## Apakah Daya?

**Daya** ialah **tarikan atau tolakan** yang bertindak ke atas sesuatu objek.

- Daya **tarikan** — menyebabkan objek bergerak *mendekati* kita
- Daya **tolakan** — menyebabkan objek bergerak *menjauhi* kita

Aktiviti harian manusia boleh melibatkan daya tarikan sahaja, daya tolakan sahaja, atau kedua-duanya sekali.

---

### Daya Tarikan

| Aktiviti | Penerangan |
|----------|------------|
| Menarik tali | Tali ditarik ke arah badan |
| Menarik/menghampiri patung | Patung ditarik ke sisi |
| Menuntun haiwan | Haiwan ditarik ke arah kita |

> 💡 **Daya tarikan** menyebabkan objek bergerak *menghampiri* kita.

---

### Daya Tolakan

| Aktiviti | Penerangan |
|----------|------------|
| Menolak stroller | Stroller bergerak menjauhi |
| Tekan tubi | Badan ditolak ke atas |
| Menyimbah air | Air ditolak keluar dari bekas |

> 💡 **Daya tolakan** menyebabkan objek bergerak *menjauhi* kita.

---

### Gabungan Daya Tarikan dan Tolakan

| Aktiviti | Daya Tarikan | Daya Tolakan |
|----------|:---:|:---:|
| Mendayung perahu | ✅ | ✅ |
| Menggergaji kayu | ✅ | ✅ |
| Memanjat tebing | ✅ | ✅ |

Kebanyakan aktiviti sukan dan kerja harian melibatkan kedua-dua daya secara serentak.

---

## Rumusan

| Jenis Daya | Kesan | Contoh |
|------------|-------|--------|
| **Tarikan** | Objek bergerak mendekati kita | Menarik tali, menuntun haiwan |
| **Tolakan** | Objek bergerak menjauhi kita | Menolak meja, tekan tubi |

> **Tips:** Cuba perhatikan aktiviti harian kamu — yang mana daya tarikan? Yang mana daya tolakan?"""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_kesan_daya(text):
    """Restructure Kesan Daya."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    new_body = """## 5 Kesan Daya

Kita tidak nampak daya, tetapi kita dapat melihat dan merasai **kesannya**.

| Kesan | Penerangan | Contoh |
|-------|-----------|--------|
| ① Mengubah bentuk objek | Objek berubah bentuk apabila dikenakan daya | Memicit span, menguli tanah liat |
| ② Mengubah arah gerakan | Arah objek bertukar apabila dikenakan daya | Memukul bola dengan kayu hoki |
| ③ Menghentikan objek bergerak | Objek yang bergerak boleh berhenti | Menangkap bola |
| ④ Menggerakkan objek pegun | Objek yang pegun boleh mula bergerak | Menolak kereta sorong |
| ⑤ Mengubah kelajuan objek | Objek boleh menjadi lebih laju atau perlahan | Mengayuh basikal lebih kuat |

---

### Percubaan Ringkas

1. **Belon dalam air** — Tolak belon ke dalam bekas air, kamu akan rasa air melawan tolakan kamu
2. **Tarik spring** — Tarik spring dengan kedua-dua tangan, kamu akan rasa spring menarik balik

> **Kesimpulan:** Daya sentiasa ada kesan — sama ada mengubah bentuk, arah, pergerakan, atau kelajuan sesuatu objek.

## Latihan

1. Senaraikan 5 kesan daya.
2. Apakah kesan daya apabila kamu menangkap bola?
3. Berikan satu contoh daya boleh mengubah bentuk objek."""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_kesan_geseran(text):
    """Restructure Kesan Daya Geseran."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    new_body = """Daya geseran terhasil apabila **dua permukaan bersentuhan**. Ia memberikan kesan baik dan buruk bergantung kepada situasi.

| Situasi | ✅ Kebaikan | ❌ Keburukan |
|---------|:---|:---|
| Geseran kasut & jalan | Berjalan tanpa tergelincir | Tapak kasut haus |
| Geseran perabot & lantai | Perabot tidak bergerak senang | Sukar nak alih perabot berat |
| Geseran brek & tayar | Basikal boleh berhenti | Brek haus kena tukar |
| Geseran tapak tangan | Boleh panaskan badan | — |
| Geseran mancis & kotak | Boleh hasilkan api | — |
| Geseran bola golf & padang | — | Bola terhenti sebelum masuk lubang |
| Geseran gergaji & kayu | — | Bunyi bising |

---

### Kesimpulan

Bergantung kepada situasi, daya geseran boleh:
- ✅ **Memberi kesan baik** — memudahkan pergerakan dan kawalan
- ❌ **Memberi kesan buruk** — menyebabkan haus, bunyi bising
- ⚠️ **Kedua-duanya sekali** — bergantung pada konteks

> **Tips:** Cuba perhatikan geseran di sekeliling kamu — mana satu yang membantu dan mana satu yang merugikan?"""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_daya_geseran(text):
    """Restructure Daya Geseran dan Faktor."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    new_body = """## Apakah Daya Geseran?

**Daya geseran** ialah daya yang terhasil apabila **dua permukaan bersentuhan** antara satu sama lain.

Daya geseran:
- Sentiasa bergerak **berlawanan arah** dengan pergerakan objek
- Menyebabkan objek bergerak **makin perlahan** dan akhirnya **terhenti**

### Contoh Situasi

| Situasi | Kesan Geseran |
|---------|--------------|
| Tapak kasut dengan jalan | Membolehkan kita berjalan |
| Bawah almari dengan lantai | Menahan almari daripada bergerak |
| Buah karom dengan papan karom | Buah karom akhirnya terhenti |
| Bola dengan padang | Bola semakin perlahan |

---

## Faktor yang Mempengaruhi Daya Geseran

### ① Jenis Permukaan

| Permukaan | Daya Geseran | Kesan |
|-----------|:---:|-------|
| **Licin** (lantai basah, papan karom bertabur tepung) | ✅ Rendah | Objek bergerak lebih jauh |
| **Kasar** (padang, jalan batu) | ✅ Tinggi | Objek sukar bergerak |

> **Semakin licin** permukaan → **semakin kurang** daya geseran
> **Semakin kasar** permukaan → **semakin tinggi** daya geseran

### ② Jisim Objek

| Objek | Jisim | Daya Geseran | Senang/Takut Digerak |
|-------|:---:|:---:|:---:|
| Kotak A | 🟢 Kecil | Rendah | ✅ Senang |
| Kotak B | 🔴 Besar | Tinggi | ❌ Sukar |

> **Semakin berat** objek → **semakin tinggi** daya geseran
> **Semakin ringan** objek → **semakin rendah** daya geseran

---

## Rumusan

| Faktor | Kesan terhadap Daya Geseran |
|--------|:---------------------------:|
| Permukaan licin | ⬇️ Berkurang |
| Permukaan kasar | ⬆️ Bertambah |
| Jisim besar/berat | ⬆️ Bertambah |
| Jisim kecil/ringan | ⬇️ Berkurang |"""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_peredaran_darah(text):
    """Restructure Sistem Peredaran Darah."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    new_body = """**Sistem peredaran darah** mengangkut **oksigen, nutrien, air dan bahan kumuh** ke seluruh tubuh manusia.

---

## Organ Yang Terlibat

| Organ | Peranan |
|-------|---------|
| ❤️ **Jantung** | Mengepam darah ke peparu dan seluruh tubuh |
| 🫁 **Peparu** | Tempat pertukaran oksigen & karbon dioksida |
| 🩸 **Darah** | Mengangkut oksigen, nutrien, air, bahan kumuh |
| 🔴 **Salur darah** | Tiub laluan untuk darah mengalir |

---

### Jantung

- Bahagian **kiri** (merah) — mengepam **darah beroksigen** ke seluruh tubuh
- Bahagian **kanan** (biru) — mengepam **darah berkarbon dioksida** ke peparu

### Peparu

- Tempat pertukaran gas:
  - **Oksigen** dari udara → masuk ke dalam darah
  - **Karbon dioksida** dari darah → dikeluarkan ke udara

### Darah

Darah mengangkut:
- ✅ **Oksigen** — dari peparu ke seluruh tubuh
- ✅ **Nutrien** — dari usus ke seluruh tubuh
- ✅ **Air** — ke seluruh sel badan
- ✅ **Bahan kumuh** — ke organ perkumuhan

### Salur Darah

Tiub yang membolehkan darah mengalir ke setiap bahagian tubuh.

---

## Rumusan Ringkas

```
Peparu (tukar gas) 
    → Jantung (pam darah) 
        → Seluruh tubuh (guna oksigen) 
            → Jantung (pam balik) 
                → Peparu (buang CO2)
```

> **Tips:** Sistem peredaran darah dan pernafasan sangat berkait rapat — oksigen yang disedut akan diedarkan oleh darah ke seluruh tubuh!"""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_laluan_darah(text):
    """Restructure Laluan Peredaran Darah."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    new_body = """Sistem peredaran darah berkait rapat dengan sistem pernafasan. 

Berikut adalah **laluan darah** dalam tubuh manusia:

---

## 🚶 Laluan Peredaran Darah

```
① Hidung menarik nafas (oksigen masuk)
       ↓
② Peparu — pertukaran gas
   ┌─ CO2 dari darah → dikeluarkan
   └─ Oksigen → masuk ke dalam darah
       ↓
③ Jantung — darah beroksigen dipam
       ↓
④ Ke seluruh tubuh (hati, perut, otot, dll.)
       ↓
⑤ Karbon dioksida dari sel→ darah
       ↓
⑥ Jantung — dipam ke peparu
       ↓
⑦ Kembali ke langkah ① (berulang)
```

> Proses ini **berulang setiap kali kita bernafas**.

---

## Kepentingan Sistem Peredaran Darah

| Fungsi | Penerangan |
|--------|-----------|
| 🫁 **Angkut oksigen** | Dari peparu ke seluruh tubuh |
| 🥗 **Angkut nutrien** | Dari usus → jantung → seluruh tubuh |
| 💨 **Angkut CO2** | Dari sel → peparu untuk dibuang |
| 🚽 **Angkut bahan kumuh** | Ke ginjal untuk disingkirkan |

---

> **Fakta:** Darah dalam badan kita mengambil masa kurang dari 1 minit untuk melengkapkan satu pusingan penuh peredaran!"""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_perkaitan_sistem(text):
    """Restructure Perkaitan Sistem Dalam Tubuh."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    new_body = """Tubuh manusia terdiri daripada beberapa sistem yang **saling berkaitan**:

| Sistem | Fungsi Utama |
|--------|-------------|
| 🦴 **Rangka** | Memberi bentuk, melindungi organ |
| 🫁 **Pernafasan** | Membekalkan oksigen |
| 🥗 **Pencernaan** | Memproses makanan |
| ❤️ **Peredaran Darah** | Mengangkut oksigen & nutrien |

---

## Bagaimana Sistem Berkaitan?

### Sistem Pernafasan ↔ Sistem Peredaran Darah

```
Pernafasan → Oksigen → Darah → Seluruh tubuh
Seluruh tubuh → CO2 → Darah → Pernafasan (hembus)
```

### Sistem Pencernaan ↔ Sistem Peredaran Darah

```
Pencernaan → Nutrien → Darah → Jantung → Seluruh tubuh
```

### Sistem Rangka ↔ Sistem Peredaran Darah & Pernafasan

- Darah membawa **oksigen & nutrien** kepada tulang untuk pertumbuhan
- Rangka **melindungi** peparu, jantung dan organ penting lain

---

## Situasi Gangguan Sistem

### 🚨 1. Tercekik Makanan

**Sistem terjejas:** Pencernaan + Pernafasan

Makanan terperangkap di esofagus → menghalang trakea → sukar bernafas

### 🚨 2. Patah Tulang

**Sistem terjejas:** Rangka + Peredaran Darah

Tulang patah → sistem rangka terganggu → bengkak akibat aliran darah terjejas

---

> **Kesimpulan:** Sistem dalam tubuh TIDAK boleh berfungsi secara sendiri. Kegagalan satu sistem akan menjejaskan sistem yang lain.
> 
> *Bayangkan seperti pasukan bola sepak — setiap pemain ada peranan, tapi kalau seorang tak jalan, seluruh pasukan terganggu!*"""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_kepentingan_penjagaan(text):
    """Restructure Kepentingan Menjaga Sistem Tubuh."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    new_body = """Semua sistem dalam tubuh **perlu dijaga** untuk mengelakkan penyakit dan memastikan ia berfungsi dengan baik.

---

### ❤️ Menjaga Sistem Peredaran Darah

| Amalan | Kesan Jika Tidak |
|--------|-----------------|
| ✅ Makan makanan seimbang | ❌ Plak kolesterol dalam salur darah |
| ✅ Bersenam | ❌ Jantung sukar mengepam darah |
| ✅ Kawal tekanan darah | ❌ Sakit jantung |

> 💡 **Tips:** Kurangkan makanan bergoreng dan banyakkan buah-buahan!

---

### 🫁 Menjaga Sistem Pernafasan

| Amalan | Kesan Jika Tidak |
|--------|-----------------|
| ✅ Jangan merokok | ❌ Kanser peparu, batuk berterusan |
| ✅ Elak habuk & asap | ❌ Sesak nafas |
| ✅ Pakai mask bila perlu | ❌ Jangkitan pernafasan |

> 💡 **Tips:** Amalkan senaman kardio seperti berlari untuk paru-paru yang sihat!

---

### 🦴 Menjaga Sistem Rangka

| Amalan | Kesan Jika Tidak |
|--------|-----------------|
| ✅ Pakai topi keledar | ❌ Tengkorak retak, otak cedera |
| ✅ Guna peralatan sukan lengkap | ❌ Patah tulang |
| ✅ Makan kalsium cukup | ❌ Tulang rapuh |

> 💡 **Tips:** Susu, keju dan sayur hijau bagus untuk tulang!

---

### 🥗 Menjaga Sistem Pencernaan

| Amalan | Kesan Jika Tidak |
|--------|-----------------|
| ✅ Makan ikut jadual | ❌ Sakit perut |
| ✅ Makan serat (sayur, buah) | ❌ Sembelit |
| ✅ Minum air cukup | ❌ Cirit-birit, dehidrasi |

> 💡 **Tips:** Minum 6-8 gelas air sehari untuk pencernaan yang lancar!"""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_kelajuan(text):
    """Restructure Kelajuan."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    new_body = """## Apakah Kelajuan?

**Kelajuan** bermaksud **ukuran cepat atau lambat** sesuatu objek yang bergerak dari satu tempat ke tempat lain.

- Kereta bergerak perlahan → lambat sampai destinasi
- Kereta bergerak laju → cepat sampai destinasi
- Jika dua kenderaan bergerak dengan kelajuan sama → masa sampai sama

---

## Unit Ukuran Kelajuan

Kelajuan melibatkan gabungan **unit jarak** dan **unit masa**.

| Unit Jarak | Unit Masa |
|:---|:---:|
| milimeter (mm) / millimetre (mm) | saat (s) / second (s) |
| sentimeter (cm) / centimetre (cm) | minit (m) / minute (m) |
| meter (m) / metre (m) | jam (j) / hour (h) |
| kilometer (km) / kilometre (km) | |

### Unit Kelajuan Biasa

| Unit | Maksud |
|------|--------|
| cm/s | sentimeter per saat |
| m/s | meter per saat |
| km/j | kilometer per jam |

### Contoh Penggunaan

| Objek | Jarak | Masa | Kelajuan | Unit Sesuai |
|-------|:---:|:---:|:---:|:---:|
| 🐌 Siput | 2 cm | 1 saat | 2 cm/s | cm/s |
| 🐿️ Tupai | 12 m | 2 saat | 6 m/s | m/s |
| 🐴 Kuda | 77 km | 1 jam | 77 km/j | km/j |

> **Nota:** km/j tidak sesuai untuk siput kerana siput terlalu perlahan. cm/s tidak sesuai untuk kuda kerana kuda terlalu laju.

---

## Speedometer (Meter Kelajuan)

Kenderaan seperti kereta dan motosikal mempunyai **speedometer** yang mengukur kelajuan:

- Jarum pada speedometer menunjukkan kelajuan semasa
- Jika jarum menunjuk angka 80 → kelajuan **80 km/j**

| Simbol | Maksud |
|:---:|---|
| km/j | kilometer per jam (BM) |
| km/h | kilometre per hour (BI) |

> **Latihan:** Jika sebuah basikal bergerak sejauh 30 km dalam masa 2 jam, berapakah kelajuannya?
> 
> (Jawapan: 30 ÷ 2 = **15 km/j**)"""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_kps(text):
    """Restructure KPS."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    new_body = """Dari Tahun 1 hingga Tahun 6, murid diajar **Kemahiran Proses Sains (KPS)**. Terdapat **12 KPS** — 7 Asas dan 5 Bersepadu.

---

## 🔬 KPS Asas (7)

| No. | Kemahiran | Penerangan | Contoh |
|:---:|-----------|-----------|--------|
| 1 | **Memerhati** | Mencatat peristiwa/objek dengan teliti | Perubahan warna daun musim luruh |
| 2 | **Mengelas** | Menyusun maklumat untuk capai kesimpulan | Mengelas haiwan mengikut habitat |
| 3 | **Mengukur & Guna Nombor** | Tentukan saiz/kuantiti dengan alat ukur | Ukur panjang dan lebar meja |
| 4 | **Membuat Inferens** | Simpulan berdasarkan bukti | Pokok layu — mungkin kurang air |
| 5 | **Meramal** | Jangkaan berdasarkan pemerhatian | Ramal cuaca berdasarkan awan |
| 6 | **Berkomunikasi** | Sampaikan hasil kajian dengan jelas | Bentang laporan eksperimen |
| 7 | **Hubungan Ruang & Masa** | Fahami pergerakan ikut masa & jarak | Kira tempoh perjalanan |

---

## 🧪 KPS Bersepadu (5)

| No. | Kemahiran | Penerangan | Contoh |
|:---:|-----------|-----------|--------|
| 1 | **Mentafsir Data** | Analisis data untuk pola/trend | Baca graf peningkatan suhu |
| 2 | **Definisi Secara Operasi** | Takrif yang tepat & konsisten | Suhu = ukuran panas sejuk |
| 3 | **Kawal Pembolehubah** | Kawal faktor yang boleh ubah hasil | Suhu tetap dalam eksperimen |
| 4 | **Membuat Hipotesis** | Ramalan berdasarkan pengetahuan | Jika cahaya banyak → tumbuhan subur |
| 5 | **Mengeksperimen** | Rancang & jalankan ujian | Ujian kesan baja pada pokok |

---

> **Tips:** KPS Asas dipelajari di Tahun 1-3, KPS Bersepadu pula diperkenalkan di Tahun 4-6. Cuba amalkan dalam kehidupan seharian!"""

    return frontmatter_str + '\n\n' + new_body.strip()

def restructure_senarai_topik(text, year, title):
    """Restructure senarai topik KSSR."""
    frontmatter = text.split('---')[0:3]
    frontmatter_str = '---'.join(frontmatter) + '---'
    
    # Extract the list items
    lines = text.split('\n')
    topics = []
    for line in lines:
        line = line.strip()
        if line.startswith('- '):
            topics.append(line[2:].strip())
    
    if not topics:
        return text  # keep original if can't extract
    
    # Group topics by heading
    current_heading = None
    sections = []
    for item in topics:
        if item == item.upper() and len(item) > 3 and not item.startswith('http'):
            current_heading = item
        elif current_heading:
            sections.append((current_heading, item))
    
    # Rebuild
    new_body = f"""Berikut ialah senarai topik Sains Tahun {year} KSSR:

"""
    if sections:
        current = None
        for heading, item in sections:
            if heading != current:
                new_body += f"\n### {heading}\n\n"
                current = heading
            new_body += f"- {item}\n"
    else:
        for item in topics:
            new_body += f"- {item}\n"
    
    return frontmatter_str + '\n\n' + new_body.strip()


def process_file(filepath):
    """Process a single note file."""
    with open(filepath) as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    original = content
    
    # Apply specific restructure based on filename
    if 'apakah-daya-daya-tarikan' in filename:
        content = restructure_daya_tarikan_tolakan(content)
    elif filename.startswith('kesan-daya-') and 'geseran' not in filename:
        content = restructure_kesan_daya(content)
    elif filename == 'kesan-daya-geseran-baik-dan-buruk-tahun-6.md':
        content = restructure_kesan_geseran(content)
    elif 'daya-geseran-dan-faktor' in filename:
        content = restructure_daya_geseran(content)
    elif filename.startswith('sistem-peredaran-darah-tahun-5.md'):
        content = restructure_peredaran_darah(content)
    elif filename.startswith('laluan-peredaran-darah'):
        content = restructure_laluan_darah(content)
    elif 'perkaitan-antara-sistem' in filename:
        content = restructure_perkaitan_sistem(content)
    elif 'kepentingan-menjaga-sistem' in filename:
        content = restructure_kepentingan_penjagaan(content)
    elif 'maksud-kelajuan' in filename:
        content = restructure_kelajuan(content)
    elif 'kemahiran-proses-sains-kps' in filename:
        content = restructure_kps(content)
    elif 'senarai-topik-sains-tahun-1' in filename:
        content = restructure_senarai_topik(content, '1', 'Senarai Topik Sains Tahun 1 KSSR')
    elif 'senarai-topik-sains-tahun-2' in filename:
        content = restructure_senarai_topik(content, '2', 'Senarai Topik Sains Tahun 2 KSSR')
    elif 'senarai-topik-sains-tahun-3' in filename:
        content = restructure_senarai_topik(content, '3', 'Senarai Topik Sains Tahun 3 KSSR')
    elif 'senarai-topik-sains-tahun-4' in filename:
        content = restructure_senarai_topik(content, '4', 'Senarai Topik Sains Tahun 4 KSSR')
    elif 'senarai-topik-sains-tahun-5' in filename:
        content = restructure_senarai_topik(content, '5', 'Senarai Topik Sains Tahun 5 KSSR')
    elif 'senarai-topik-sains-tahun-6' in filename:
        content = restructure_senarai_topik(content, '6', 'Senarai Topik Sains Tahun 6 KSSR')
    else:
        # General cleanup
        content = clean_artifact(content)
        content = remove_empty_lines(content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False


def main():
    all_files = glob.glob(os.path.join(NOTES_DIR, 'sk', 'sains', '*.md'))
    all_files += glob.glob(os.path.join(NOTES_DIR, 'sk', 'english', '*.md'))
    all_files += glob.glob(os.path.join(NOTES_DIR, 'sk', 'matematik', '*.md'))
    all_files += glob.glob(os.path.join(NOTES_DIR, 'smk', '**', '*.md'))
    
    updated = []
    for fp in sorted(all_files):
        try:
            if process_file(fp):
                updated.append(os.path.basename(fp))
        except Exception as e:
            print(f"❌ {os.path.basename(fp)}: {e}")
    
    print(f"Cleanup selesai: {len(updated)} fail dikemas kini")
    for f in updated:
        print(f"  ✅ {f}")

if __name__ == '__main__':
    main()