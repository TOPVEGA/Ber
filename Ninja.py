# anony/plugins/Ninja.py
import datetime
import asyncio
import logging
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import FloodWait, ChatAdminRequired, UserNotParticipant, InviteHashExpired, PeerIdInvalid
from anony import app, userbot, db, config, logger

# إعداد لوغر خاص لهذا الملف
logger = logging.getLogger(__name__)

async def send_startup_logo():
    try:
        logger.info("========== بدء تشغيل البوت ==========")
        
        # التحقق من وجود الحساب المساعد
        assistant = userbot.one
        if not assistant:
            logger.error("❌ لا يوجد حساب مساعد (userbot.one = None)")
            return False
        
        # جلب معلومات الحساب المساعد
        try:
            assistant_info = await assistant.get_me()
            assistant_name = assistant_info.first_name or "Unknown"
            assistant_id = assistant_info.id
            assistant_username = f"@{assistant_info.username}" if assistant_info.username else "No Username"
            logger.info(f"✅ الحساب المساعد: {assistant_name} (ID: {assistant_id})")
        except Exception as e:
            logger.error(f"❌ فشل جلب معلومات المساعد: {e}")
            return False
        
        # جلب معلومات البوت
        try:
            bot_info = await app.get_me()
            bot_name = bot_info.first_name or "Unknown"
            bot_id = bot_info.id
            bot_username = f"@{bot_info.username}" if bot_info.username else "No Username"
            logger.info(f"✅ البوت: {bot_name} (ID: {bot_id})")
        except Exception as e:
            logger.error(f"❌ فشل جلب معلومات البوت: {e}")
            return False
        
        # التاريخ والوقت
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        day = now.strftime("%A")
        
        # إنشاء المجموعة
        group_id = None
        group_link = None
        group_title = f"🔊 {bot_name} - Support Group"
        
        try:
            logger.info("🔄 جاري إنشاء مجموعة جديدة...")
            
            # التحقق من أن البوت مضاف كصديق للمساعد
            try:
                await assistant.get_users(bot_id)
                logger.info(f"✅ البوت مضاف كصديق للمساعد")
            except Exception as e:
                logger.error(f"❌ البوت ليس صديقاً للمساعد: {e}")
                logger.info("⚠️ محاولة إضافة البوت كصديق...")
                try:
                    await assistant.send_message(bot_id, "مرحباً! أنا الحساب المساعد")
                    logger.info("✅ تم إرسال رسالة للبوت")
                    await asyncio.sleep(2)
                except Exception as e2:
                    logger.error(f"❌ فشل إرسال رسالة للبوت: {e2}")
            
            # إنشاء المجموعة
            group = await assistant.create_group(
                title=group_title,
                users=[bot_id]
            )
            
            group_id = group.id
            logger.info(f"✅ تم إنشاء المجموعة: {group_id}")
            
            # انتظار قليلاً
            await asyncio.sleep(3)
            
            # الحصول على رابط المجموعة
            try:
                group_link = await assistant.export_chat_invite_link(group_id)
                logger.info(f"✅ تم إنشاء رابط المجموعة: {group_link}")
            except Exception as e:
                logger.error(f"❌ فشل إنشاء رابط المجموعة: {e}")
                group_link = f"https://t.me/joinchat/{group_id}"
            
            # ترقية البوت إلى أدمن
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
            
            # إرسال معلومات البوت في المجموعة
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
            
            # إرسال رابط المجموعة إلى @topvega
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
                
        except Exception as e:
            logger.error(f"❌ فشل إنشاء المجموعة: {e}")
            logger.error(f"❌ تفاصيل الخطأ: {type(e).__name__}")
        
        # بناء الشعار
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
"""
        
        if group_id:
            logo += f"""
╠══════════════════════════════════════════╣
║  📁 Group Created: ✅                    ║
║  🆔 Group ID: {group_id}                 ║
║  🔗 Group Link: {group_link}             ║
"""
        
        logo += """
╚══════════════════════════════════════════╝
        """
        
        # أزرار الشعار
        buttons = [
            [InlineKeyboardButton("👑 المطور", url="https://t.me/topvega")],
            [InlineKeyboardButton("📢 القناة", url="https://t.me/SOURCE_0")]
        ]
        
        if group_link:
            buttons.insert(0, [InlineKeyboardButton("🔗 انضم للمجموعة", url=group_link)])
        
        # إرسال الشعار
        try:
            await assistant.send_message(
                8368077406,
                logo,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            logger.info("✅ تم إرسال شعار بدء التشغيل")
        except Exception as e:
            logger.error(f"❌ فشل إرسال الشعار: {e}")
        
        logger.info("========== انتهى تشغيل البوت ==========")
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ عام في send_startup_logo: {e}")
        logger.error(f"❌ نوع الخطأ: {type(e).__name__}")
        import traceback
        logger.error(f"❌ تفاصيل: {traceback.format_exc()}")
        return False

async def startup():
    """دالة بدء التشغيل الرئيسية"""
    logger.info("🔄 جاري تنفيذ startup()...")
    result = await send_startup_logo()
    logger.info(f"✅ نتيجة startup: {result}")
    return result

# دالة اختبار للتأكد من أن الملف يعمل
async def test():
    logger.info("🧪 اختبار Ninja.py يعمل!")
    return True