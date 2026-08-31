#!/usr/bin/env python3
"""
Migrate articles from workspace/article/ to notabelajar/src/content/notes/
- Clean WordPress formatting artifacts
- Add Astro-compatible YAML frontmatter
- Map subjects, levels, years
- Add Unsplash image headers for visual appeal
"""

import os, re, shutil, subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLE_DIR = os.path.join(SCRIPT_DIR, '..', 'article')
NOTES_DIR = os.path.join(SCRIPT_DIR, 'src', 'content', 'notes')
MIGRATED_LOG = os.path.join(SCRIPT_DIR, '.migrated-articles.txt')

# ── Mapping: article filename → Astro metadata ──
MIGRATIONS = {
    # --- Sains SK ---
    '0159-senarai-topik-sains-tahun-1-kssr.md': {
        'title': 'Senarai Topik Sains Tahun 1 KSSR',
        'description': 'Senarai lengkap topik Sains Tahun 1 KSSR merangkumi kemahiran saintifik, manusia, haiwan, tumbuhan, magnet dan penyerapan.',
        'subject': 'sains', 'level': 'sk', 'year': '1', 'topic': 'KSSR — Senarai Topik',
        'tags': ['sains', 'kssr', 'tahun 1', 'senarai topik'],
        'pubDate': '2022-10-16',
    },
    '0157-senarai-topik-sains-tahun-2-kssr.md': {
        'title': 'Senarai Topik Sains Tahun 2 KSSR',
        'description': 'Senarai lengkap topik Sains Tahun 2 KSSR merangkumi kemahiran saintifik, manusia, haiwan, tumbuh-tumbuhan, cahaya, elektrik dan campuran.',
        'subject': 'sains', 'level': 'sk', 'year': '2', 'topic': 'KSSR — Senarai Topik',
        'tags': ['sains', 'kssr', 'tahun 2', 'senarai topik'],
        'pubDate': '2022-10-16',
    },
    '0153-senarai-topik-sains-tahun-3-kssr.md': {
        'title': 'Senarai Topik Sains Tahun 3 KSSR',
        'description': 'Senarai lengkap topik Sains Tahun 3 KSSR merangkumi kemahiran saintifik, manusia, haiwan, tumbuh-tumbuhan, pengukuran dan banyak lagi.',
        'subject': 'sains', 'level': 'sk', 'year': '3', 'topic': 'KSSR — Senarai Topik',
        'tags': ['sains', 'kssr', 'tahun 3', 'senarai topik'],
        'pubDate': '2022-10-16',
    },
    '0155-senarai-topik-sains-tahun-4-kssr.md': {
        'title': 'Senarai Topik Sains Tahun 4 KSSR',
        'description': 'Senarai lengkap topik Sains Tahun 4 KSSR merangkumi kemahiran saintifik, manusia, haiwan, tumbuh-tumbuhan, cahaya, tenaga dan bumi.',
        'subject': 'sains', 'level': 'sk', 'year': '4', 'topic': 'KSSR — Senarai Topik',
        'tags': ['sains', 'kssr', 'tahun 4', 'senarai topik'],
        'pubDate': '2022-10-16',
    },
    '0015-senarai-topik-sains-tahun-5-kssr.md': {
        'title': 'Senarai Topik Sains Tahun 5 KSSR',
        'description': 'Senarai lengkap topik Sains Tahun 5 KSSR merangkumi kemahiran saintifik, manusia, haiwan, tumbuh-tumbuhan, elektrik, cahaya dan sains fizik.',
        'subject': 'sains', 'level': 'sk', 'year': '5', 'topic': 'KSSR — Senarai Topik',
        'tags': ['sains', 'kssr', 'tahun 5', 'senarai topik'],
        'pubDate': '2021-06-16',
    },
    '0020-senarai-topik-sains-tahun-6-kssr.md': {
        'title': 'Senarai Topik Sains Tahun 6 KSSR',
        'description': 'Senarai lengkap topik Sains Tahun 6 KSSR merangkumi kemahiran saintifik, manusia, mikroorganisma, interaksi, daya, dan sains fizik.',
        'subject': 'sains', 'level': 'sk', 'year': '6', 'topic': 'KSSR — Senarai Topik',
        'tags': ['sains', 'kssr', 'tahun 6', 'senarai topik'],
        'pubDate': '2021-06-16',
    },
    '0024-apakah-daya-daya-tarikan-dan-daya-tolakan.md': {
        'title': 'Apakah Daya? Daya Tarikan dan Daya Tolakan',
        'description': 'Nota mengenai maksud daya serta contoh daya tarikan dan daya tolakan dalam kehidupan seharian.',
        'subject': 'sains', 'level': 'sk', 'year': '6', 'topic': 'Daya',
        'tags': ['daya', 'daya tarikan', 'daya tolakan', 'sains'],
        'pubDate': '2021-06-16',
    },
    '0051-kesan-daya.md': {
        'title': 'Kesan Daya',
        'description': 'Nota mengenai 5 kesan daya: mengubah bentuk, arah, henti, gerak, dan kelajuan objek.',
        'subject': 'sains', 'level': 'sk', 'year': '6', 'topic': 'Daya',
        'tags': ['daya', 'kesan daya', 'sains'],
        'pubDate': '2021-06-16',
    },
    '0086-daya-geseran-dan-faktor-mempengaruhi-daya-geseran.md': {
        'title': 'Daya Geseran dan Faktor Mempengaruhi Daya Geseran',
        'description': 'Nota mengenai daya geseran, situasi kewujudan serta faktor yang mempengaruhinya.',
        'subject': 'sains', 'level': 'sk', 'year': '6', 'topic': 'Daya',
        'tags': ['daya geseran', 'geseran', 'sains'],
        'pubDate': '2021-06-24',
    },
    '0106-kesan-daya-geseran-kesan-baik-dan-kesan-buruk.md': {
        'title': 'Kesan Daya Geseran — Baik dan Buruk',
        'description': 'Nota mengenai kesan baik dan buruk daya geseran dalam pelbagai situasi kehidupan seharian.',
        'subject': 'sains', 'level': 'sk', 'year': '6', 'topic': 'Daya',
        'tags': ['daya geseran', 'kesan', 'sains'],
        'pubDate': '2021-06-30',
    },
    '0076-sistem-peredaran-darah-manusia.md': {
        'title': 'Sistem Peredaran Darah Manusia',
        'description': 'Nota mengenai organ yang terlibat dalam sistem peredaran darah manusia — jantung, salur darah, darah dan peparu.',
        'subject': 'sains', 'level': 'sk', 'year': '5', 'topic': 'Sistem Peredaran Darah',
        'tags': ['sistem peredaran darah', 'jantung', 'darah', 'sains'],
        'pubDate': '2021-06-21',
    },
    '0100-laluan-peredaran-darah-manusia.md': {
        'title': 'Laluan Peredaran Darah Manusia',
        'description': 'Nota mengenai perjalanan darah dalam sistem peredaran darah manusia dan kepentingannya.',
        'subject': 'sains', 'level': 'sk', 'year': '5', 'topic': 'Sistem Peredaran Darah',
        'tags': ['peredaran darah', 'jantung', 'oksigen', 'sains'],
        'pubDate': '2021-06-28',
    },
    '0118-perkaitan-antara-sistem-dalam-tubuh-manusia.md': {
        'title': 'Perkaitan Antara Sistem Dalam Tubuh Manusia',
        'description': 'Nota mengenai perkaitan antara sistem rangka, pernafasan, pencernaan dan peredaran darah dalam tubuh manusia.',
        'subject': 'sains', 'level': 'sk', 'year': '5', 'topic': 'Sistem Tubuh Manusia',
        'tags': ['sistem tubuh', 'manusia', 'sains', 'kesihatan'],
        'pubDate': '2021-07-05',
    },
    '0141-kepentingan-menjaga-sistem-dalam-tubuh-manusia.md': {
        'title': 'Kepentingan Menjaga Sistem Dalam Tubuh Manusia',
        'description': 'Nota mengenai kepentingan menjaga sistem peredaran darah, pernafasan, rangka dan pencernaan manusia.',
        'subject': 'sains', 'level': 'sk', 'year': '5', 'topic': 'Sistem Tubuh Manusia',
        'tags': ['sistem tubuh', 'kesihatan', 'penjagaan', 'sains'],
        'pubDate': '2021-07-11',
    },
    '0128-maksud-kelajuan-dan-unit-ukuran-kelajuan.md': {
        'title': 'Maksud Kelajuan dan Unit Ukuran Kelajuan',
        'description': 'Nota mengenai maksud kelajuan serta unit-unit ukuran kelajuan seperti cm/s, m/s dan km/j.',
        'subject': 'sains', 'level': 'sk', 'year': '6', 'topic': 'Kelajuan',
        'tags': ['kelajuan', 'unit ukuran', 'sains', 'fizik'],
        'pubDate': '2021-07-07',
    },
    '0901-kemahiran-proses-sains-kps-asas-dan-kps-bersepadu.md': {
        'title': 'Kemahiran Proses Sains — KPS Asas dan KPS Bersepadu',
        'description': 'Nota mengenai 12 Kemahiran Proses Sains — 7 KPS Asas dan 5 KPS Bersepadu yang diajar dari Tahun 1 hingga Tahun 6.',
        'subject': 'sains', 'level': 'sk', 'year': '1', 'topic': 'Kemahiran Saintifik',
        'tags': ['kemahiran proses sains', 'kps', 'sains', 'kemahiran saintifik'],
        'pubDate': '2024-02-20',
    },
    # --- English SK ---
    '0869-lets-explore-verbs-100-words-full-of-action.md': {
        'title': "Let's Explore Verbs — 100 Words Full of Action!",
        'description': 'Senarai 100 kata kerja (verbs) dalam Bahasa Inggeris dengan penerangan dan contoh ayat mudah.',
        'subject': 'english', 'level': 'sk', 'year': '4', 'topic': 'Grammar — Verbs',
        'tags': ['verbs', 'kata kerja', 'english', 'grammar', 'vocabulary'],
        'pubDate': '2024-02-20',
    },
    '0910-spice-up-your-writing-with-adverb.md': {
        'title': 'Spice Up Your Writing with Adverb',
        'description': 'Belajar tentang adverb (kata keterangan) dan bagaimana ia menjadikan penulisan lebih menarik.',
        'subject': 'english', 'level': 'sk', 'year': '4', 'topic': 'Grammar — Adverbs',
        'tags': ['adverbs', 'kata keterangan', 'english', 'grammar', 'writing'],
        'pubDate': '2024-02-20',
    },
    '0920-english-kssr-8-parts-of-speech.md': {
        'title': 'English KSSR — 8 Parts of Speech',
        'description': 'Pengenalan kepada 8 bahagian ucapan dalam Bahasa Inggeris — noun, verb, adjective, adverb, pronoun, preposition, conjunction, interjection.',
        'subject': 'english', 'level': 'sk', 'year': '4', 'topic': 'Grammar — Parts of Speech',
        'tags': ['parts of speech', 'english', 'grammar', 'tatabahasa'],
        'pubDate': '2024-02-24',
    },
    '0959-list-of-irregular-verbs.md': {
        'title': 'List of Irregular Verbs',
        'description': 'Senarai lengkap irregular verbs dalam Bahasa Inggeris beserta past simple dan past participle.',
        'subject': 'english', 'level': 'sk', 'year': '5', 'topic': 'Grammar — Irregular Verbs',
        'tags': ['irregular verbs', 'english', 'grammar', 'vocabulary'],
        'pubDate': '2024-02-26',
    },
}

# ── Skip list (halaman statik) ──
SKIP = {'0011-tentang-nb.md', '0012-privacy-policy.md', '0953-arkib-nota.md'}

# ── Unsplash cover images mapping ──
UNSPLASH = {
    'sains': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&q=80',
    'english': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&q=80',
}

UNSPLASH_TOPIC = {
    'daya': 'https://images.unsplash.com/photo-1560264357-8bb1ff0e3f2c?w=800&q=80',
    'peredaran darah': 'https://images.unsplash.com/photo-1576670157476-f51db6ec13d2?w=800&q=80',
    'kelajuan': 'https://images.unsplash.com/photo-1473969631237-f4665ed28cfa?w=800&q=80',
    'kemahiran saintifik': 'https://images.unsplash.com/photo-1564325724739-bae0bd19862b?w=800&q=80',
}


def clean_content(text):
    """Clean WordPress formatting artifacts from article content."""
    # Remove old YAML frontmatter (between --- delimiters)
    text = re.sub(r'^---\n.*?\n---\n\n', '', text, flags=re.DOTALL)

    # Fix literal 'n' on its own line (WordPress <br> artifact)
    # Pattern: newline + 'n' + newline
    text = re.sub(r'\nn\n', '\n\n', text)
    # Start or end of file
    text = re.sub(r'^n\n', '', text)
    text = re.sub(r'\nn$', '', text)

    # Multiple newlines → double newlines (paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove broken image tags (notabelajar.com URLs)
    text = re.sub(r'!\[Image\]\(https?://notabelajar\.com[^)]*\)\n*', '', text)

    # Remove empty image tags
    text = re.sub(r'!\[Image\]\([^)]*\)\n*', '', text)

    # Remove credit/caption sections
    text = re.sub(r'\nKredit gambar:[^\n]*(\n[^\n]*)*', '', text)
    text = re.sub(r'\nPhoto by.*', '', text)
    text = re.sub(r'\n\*_([^_]*)_\*\n?', r'\n\n*_\1_*\n', text)  # clean italic captions

    # Clean up old WordPress shortcodes
    text = re.sub(r'\[display-posts[^\]]*\]', '', text)

    # Clean up trailing/leading whitespace
    text = text.strip()

    return text


def make_frontmatter(title, description, subject, level, year, topic, tags, pub_date):
    """Generate Astro-compatible YAML frontmatter."""
    tags_yaml = '\n'.join(f'  - {t}' for t in tags)

    return f'''---
title: "{title}"
description: "{description}"
subject: {subject}
level: {level}
year: "{year}"
topic: "{topic}"
pubDate: {pub_date}
tags:
{tags_yaml}
---'''


def add_image_banner(text, subject, topic):
    """Add a relevant Unsplash image after the first heading if it's a proper note (not just a topic list)."""
    is_topic_list = text.startswith('-') or 'Senarai' in text[:100]
    if is_topic_list:
        return text  # Don't add images to topic lists

    # Find the right image
    img_url = UNSPLASH.get(subject, UNSPLASH.get('sains'))

    # Add image after the first heading
    heading_match = re.search(r'^## (.+)$', text, re.MULTILINE)
    if heading_match:
        pos = heading_match.end()
        banner = f'\n\n[![]({img_url})]({img_url})\n\n*Ilustrasi berkaitan*'
        text = text[:pos] + banner + text[pos:]

    return text


def migrate():
    migrated = []
    errors = []

    # Read already-migrated list
    already = set()
    if os.path.exists(MIGRATED_LOG):
        with open(MIGRATED_LOG) as f:
            already = set(line.strip() for line in f if line.strip())

    for filename, meta in MIGRATIONS.items():
        if filename in already:
            print(f"⏭️  {filename} — already migrated, skipping")
            continue

        src = os.path.join(ARTICLE_DIR, filename)
        if not os.path.exists(src):
            errors.append(f"{filename}: source not found")
            continue

        with open(src) as f:
            raw = f.read()

        # Clean content
        body = clean_content(raw)
        if not body.strip():
            errors.append(f"{filename}: empty after cleaning")
            continue

        # Build frontmatter
        front = make_frontmatter(
            meta['title'], meta['description'],
            meta['subject'], meta['level'], meta['year'],
            meta['topic'], meta['tags'], meta['pubDate']
        )

        # Optional: add Unsplash image
        body = add_image_banner(body, meta['subject'], meta['topic'])

        # Determine output path
        out_dir = os.path.join(NOTES_DIR, meta['level'], meta['subject'])
        os.makedirs(out_dir, exist_ok=True)

        # Generate filename
        slug = re.sub(r'[^a-z0-9]', '-', meta['title'].lower())
        slug = re.sub(r'-+', '-', slug).strip('-')
        out_name = f"{slug}-tahun-{meta['year']}.md"
        out_path = os.path.join(out_dir, out_name)

        # Write
        with open(out_path, 'w') as f:
            f.write(front + '\n\n' + body)

        migrated.append(filename)
        print(f"✅  {filename} → {out_name}")

    # Log migrated files
    if migrated:
        with open(MIGRATED_LOG, 'a') as f:
            for fname in migrated:
                f.write(fname + '\n')

    print(f"\n{'='*50}")
    print(f"Migrated: {len(migrated)}")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors:
            print(f"  ❌ {e}")
    return len(migrated), len(errors)


if __name__ == '__main__':
    migrate()