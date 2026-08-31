# 📝 NotaBelajar

Nota pembelajaran untuk pelajar sekolah rendah (SK) dan menengah (SMK) Malaysia.

## Struktur

```
src/
├── content/
│   └── notes/
│       ├── sk/               # Sekolah Rendah (Tahun 1-6)
│       │   ├── bm/           # Bahasa Melayu
│       │   ├── english/      # English
│       │   ├── matematik/    # Matematik
│       │   ├── sains/        # Sains
│       │   └── sejarah/      # Sejarah
│       └── smk/              # Sekolah Menengah (Tingkatan 1-5)
│           ├── bm/
│           ├── english/
│           ├── matematik/
│           ├── sains/
│           ├── sejarah/
│           ├── geografi/
│           ├── fizik/
│           ├── kimia/
│           ├── biologi/
│           └── matematik-tambahan/
├── layouts/
│   └── BaseLayout.astro
├── pages/
│   ├── index.astro
│   ├── [...slug].astro
│   ├── [level]/
│   │   └── [subject].astro
│   ├── sk/
│   │   └── index.astro
│   └── smk/
│       └── index.astro
└── content.config.ts
```

## Tambah Nota Baru

1. Buat fail `.md` dalam folder subjek yang sesuai:
   `src/content/notes/<level>/<subject>/nama-nota.md`

2. Set frontmatter:
   ```yaml
   ---
   title: "Nama Nota"
   description: "Penerangan ringkas"
   subject: matematik
   level: sk        # atau smk
   year: "1"
   topic: "Topik"
   pubDate: 2026-01-15
   tags:
     - tag1
     - tag2
   ---
   ```

3. Tulis kandungan dalam Markdown

4. Commit dan push — auto-deploy ke Pages

## Tech Stack

- [Astro](https://astro.build) — Static site generator
- Content Collections — Structured notes management
- GitHub Pages — Hosting
- [Kapa.ai](https://kapa.ai) — Astro Docs MCP backend

Dihasilkan dengan 🐱 oleh Kai