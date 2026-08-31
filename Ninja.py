# anony/plugins/Ninja.py
import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from anony import app, userbot, db, config, logger

async def send_startup_logo():
    try:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        day = now.strftime("%A")
        
        # جلب معلومات الحساب المساعد
        assistant = userbot.one  # الحساب المساعد الرئيسي
        assistant_info = await assistant.get_me()
        assistant_name = assistant_info.first_name or "Unknown"
        assistant_id = assistant_info.id
        assistant_username = f"@{assistant_info.username}" if assistant_info.username else "No Username"
        
        # جلب معلومات البوت
        bot_info = await app.get_me()
        bot_name = bot_info.first_name or "Unknown"
        bot_id = bot_info.id
        bot_username = f"@{bot_info.username}" if bot_info.username else "No Username"
        
        # الشعار
        logo = f"""
╔══════════════════════════════════════════╗
║         🤖 BOT STARTED SUCCESSFULLY      ║
╠══════════════════════════════════════════╣
║  🤖 Bot Name: {bot_name}                 ║
║  🆔 Bot ID: {bot_id}                     ║
║  👤 Bot Username: {bot_username}         ║
╠══════════════════════════════════════════╣
║  📱 Assistant Name: {assistant_name}     ║
║  🆔 Assistant ID: {assistant_id}         ║
║  👤 Assistant Username: {assistant_username}║
╠══════════════════════════════════════════╣
║  📅 Date: {date}                         ║
║  ⏰ Time: {time}                         ║
║  📆 Day: {day}                           ║
║  ✅ Status: Running                      ║
╚══════════════════════════════════════════╝
        """
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 المطور", url="https://t.me/DEV_1")],
            [InlineKeyboardButton("📢 القناة", url="https://t.me/SOURCE_0")]
        ])
        
        # إرسال عبر الحساب المساعد فقط
        await assistant.send_message(
            8368077406,  # يمكن تغيير هذا المعرف إلى معرفك
            logo,
            reply_markup=buttons
        )
        
        logger.info("✅ تم إرسال شعار بدء التشغيل بواسطة الحساب المساعد")
        return True
        
    except Exception as e:
        logger.error(f"❌ فشل إرسال شعار بدء التشغيل: {e}")
        return False
        
# أضف هذا في نهاية ملف Ninja.py
async def startup():
    await send_startup_logo()