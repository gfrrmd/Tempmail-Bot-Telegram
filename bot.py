import os
import random
import string
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Setup Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# API Mailsac (Public Access)
API_URL = "https://mailsac.com/api/addresses"

def generate_user(length=8):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📮 **Mailsac Temp Mail Bot**\n\n"
        "Email dari Mailsac lebih stabil dan jarang ditolak oleh website."
    )
    btns = [[InlineKeyboardButton("📧 Buat Email Mailsac", callback_data="generate")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(btns), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "generate":
        user = generate_user()
        email = f"{user}@mailsac.com"
        
        context.user_data['email'] = email
        context.user_data['user'] = user

        msg = (
            f"✅ **Email Berhasil Dibuat!**\n\n"
            f"📧 `{email}`\n\n"
            "⚠️ *Catatan: Mailsac Public bersifat publik. Jangan kirim data yang sangat rahasia.*"
        )
        btns = [
            [InlineKeyboardButton("🔄 Cek Inbox", callback_data="refresh")],
            [InlineKeyboardButton("🆕 Email Lain", callback_data="generate")]
        ]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(btns), parse_mode="Markdown")

    elif query.data == "refresh":
        email = context.user_data.get('email')
        
        if not email:
            await query.message.reply_text("Silakan buat email dulu!")
            return

        # Mailsac menggunakan endpoint ini untuk cek pesan
        # Tanpa API Key, kita hanya bisa akses inbox publik
        res = requests.get(f"https://mailsac.com/api/addresses/{email}/messages").json()
        
        if not res:
            await query.message.reply_text("📭 Inbox masih kosong. Tunggu 10-20 detik lalu refresh kembali.")
        else:
            for m in res[:2]: # Tampilkan 2 email terbaru
                m_id = m['_id']
                # Mengambil isi pesan dalam bentuk teks
                # Kita arahkan ke link web mailsac agar user bisa baca full HTML jika teksnya rumit
                link_baca = f"https://mailsac.com/public/dirty_envoy/{email}/{m_id}"
                
                info = (
                    f"📩 **Pesan Masuk!**\n"
                    f"👤 **Dari:** {m['from']}\n"
                    f"📝 **Subjek:** {m['subject']}\n"
                    f"📅 **Tgl:** {m['received']}\n\n"
                    f"🔗 **Link Baca Lengkap:** [Klik Disini]({link_baca})"
                )
                await query.message.reply_text(info, parse_mode="Markdown")

if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("BOT_TOKEN tidak ditemukan!")
    else:
        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_callback))
        print("Bot Mailsac Running...")
        app.run_polling(drop_pending_updates=True)
