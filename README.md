# 📧 Tempmail Bot Telegram

Bot Telegram untuk membuat **email sementara (temporary email)** secara instan menggunakan API [mail.tm](https://mail.tm). Buat email sekali pakai, refresh inbox, dan baca email langsung dari Telegram — tanpa perlu keluar aplikasi.

---

## ✨ Fitur

- 🆕 **Generate Email Baru** — buat alamat email sementara dengan satu klik
- 🔄 **Refresh Inbox** — cek email masuk secara real-time
- 📩 **Baca Isi Email** — lihat detail email (pengirim, subjek, isi pesan)
- 🔀 **Ganti Email** — generate ulang alamat email kapan saja
- ⌨️ Navigasi penuh via **Inline Keyboard** (tidak perlu ketik perintah)

---

## 🛠️ Tech Stack

| Komponen | Detail |
|---|---|
| Bahasa | Python 3.11 |
| Library Bot | `python-telegram-bot` v21.1.1 |
| API Email | [mail.tm](https://api.mail.tm) |
| HTTP Client | `requests` |
| Deployment | Railway (Worker) |

---

## 🚀 Deploy ke Railway

### Prasyarat
- Akun [Railway](https://railway.app)
- Telegram Bot Token dari [@BotFather](https://t.me/BotFather)
- Akun GitHub (untuk fork/connect repo)

### Langkah-langkah

1. **Fork atau clone repo ini** ke akun GitHub kamu.

2. **Buka [Railway](https://railway.app)** dan login, lalu klik **New Project → Deploy from GitHub repo**.

3. **Pilih repo** `Tempmail-Bot-Telegram` dari daftar.

4. Setelah project dibuat, buka tab **Variables** dan tambahkan environment variable berikut:

   | Variable | Value |
   |---|---|
   | `BOT_TOKEN` | Token bot dari BotFather |

5. Railway akan otomatis mendeteksi `Procfile` dan menjalankan bot sebagai **Worker**:
   ```
   worker: python bot.py
   ```

6. Klik **Deploy** — bot akan langsung berjalan. Cek tab **Logs** untuk memastikan tidak ada error.

> ⚠️ Pastikan service type-nya adalah **Worker** (bukan Web Service), karena bot ini tidak membuka HTTP port.

---

## ⚙️ Menjalankan Secara Lokal

```bash
# Clone repo
git clone https://github.com/gfrrmd/Tempmail-Bot-Telegram.git
cd Tempmail-Bot-Telegram

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export BOT_TOKEN="token_bot_kamu"

# Jalankan bot
python bot.py
```

---

## 📂 Struktur File

```
Tempmail-Bot-Telegram/
├── bot.py            # Main bot logic
├── requirements.txt  # Python dependencies
├── Procfile          # Railway worker config
├── runtime.txt       # Python version config
└── README.md
```

---

## 💬 Cara Pakai

1. Start bot di Telegram → `/start`
2. Klik **🆕 Generate Email Baru**
3. Salin alamat email yang muncul dan gunakan di mana saja
4. Klik **🔄 Refresh Inbox** untuk mengecek email masuk
5. Klik subjek email untuk membaca isinya
6. Klik **🆕 Ganti Email** jika ingin alamat baru

---

## 📄 Lisensi

MIT License — bebas digunakan dan dimodifikasi.
