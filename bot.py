import os
import time
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Konfigurasi API Mail.tm
BASE_URL = "https://api.mail.tm"

# Fungsi untuk mengambil domain yang tersedia
def get_domains():
    try:
        res = requests.get(f"{BASE_URL}/domains").json()
        return res['hydra:member'][0]['domain']
    except:
        return "tempmail.com"

# Perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 **Halo! Selamat datang di Temp Mail Bot.**\n\n"
        "Saya bisa membuatkan email sementara untukmu agar inbox aslimu tetap bersih dari spam."
    )
    keyboard = [[InlineKeyboardButton("📧 Generate Email Baru", callback_data="gen_email")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# Logika penanganan tombol
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Tombol Buat Email
    if query.data == "gen_email":
        domain = get_domains()
        user_id = query.from_user.id
        # Membuat username unik berdasarkan ID user dan waktu
        username = f"user_{user_id}_{int(time.time())}"[-15:] 
        email = f"{username}@{domain}"
        password = "password_rahasia_123"

        # 1. Daftarkan Akun ke Mail.tm
        reg_res = requests.post(f"{BASE_URL}/accounts", json={"address": email, "password": password})
        
        if reg_res.status_code == 201:
            # 2. Ambil Token Akses
            token_res = requests.post(f"{BASE_URL}/token", json={"address": email, "password": password}).json()
            token = token_res['token']
            
            # Simpan data di memori bot (sementara)
            context.user_data['email'] = email
            context.user_data['token'] = token

            text = f"✅ **Email Berhasil Dibuat!**\n\n📧 Address: `{email}`\n🔑 Password: `{password}`\n\n*Silakan kirim email ke alamat di atas, lalu tekan tombol Refresh.*"
            keyboard = [
                [InlineKeyboardButton("🔄 Refresh Inbox", callback_data="check_inbox")],
                [InlineKeyboardButton("🆕 Buat Baru", callback_data="gen_email")]
            ]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        else:
            await query.edit_message_text("❌ Gagal membuat email. Coba lagi nanti.")

    # Tombol Cek Pesan Masuk
    elif query.data == "check_inbox":
        token = context.user_data.get('token')
        if not token:
            await query.message.reply_text("Silakan generate email terlebih dahulu.")
            return

        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get(f"{BASE_URL}/messages", headers=headers).json()
        messages = res.get('hydra:member', [])

        if not messages:
            await query.message.reply_text("📭 Inbox masih kosong.")
        else:
            for m in messages[:3]: # Ambil 3 email terbaru saja
                # Ambil detail isi pesan
                m_id = m['id']
                detail = requests.get(f"{BASE_URL}/messages/{m_id}", headers=headers).json()
                
                msg_box = (
                    f"📩 **Pesan Baru!**\n"
                    f"👤 **Dari:** {m['from']['address']}\n"
                    f"📝 **Subjek:** {m['subject']}\n"
                    f"📅 **Waktu:** {m['createdAt']}\n\n"
                    f"📄 **Isi:**\n{detail['text'] or 'Hanya tersedia format HTML'}"
                )
                await query.message.reply_text(msg_box, parse_mode="Markdown")

# Menjalankan Bot
if __name__ == '__main__':
    # Token diambil dari Environment Variable Railway
    TOKEN_TELEGRAM = os.getenv("BOT_TOKEN")
    
    if not TOKEN_TELEGRAM:
        print("Error: BOT_TOKEN tidak ditemukan di Environment Variables!")
    else:
        app = Application.builder().token(TOKEN_TELEGRAM).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_callback))
        
        print("Bot sedang berjalan...")
        app.run_polling()
