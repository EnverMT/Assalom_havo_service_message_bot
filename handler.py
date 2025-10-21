from aiogram import F, Router
from config import load_config
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER, KICKED, LEFT
from aiogram.types import ChatMemberUpdated, Message
from logger import logger

config = load_config(".env")
router = Router()
# router.message.filter(F.chat.id == config.obs_group.id)


@router.message(F.new_chat_members | F.left_chat_member)
async def delete_service_message(message):    
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Error deleting service message: {e}")


@router.message(F.text.regexp(r'(https?://\S+)'))
async def delete_message_with_link(message: Message):    
    print(message.model_dump_json())
    try:
        await message.delete()
        logger.info(f"Deleted message with link from user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error deleting message with link: {e}")


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> KICKED))
async def log_user_kicked(event: ChatMemberUpdated):

    kicker = event.from_user
    new_member = event.new_chat_member.user

    kicker_url = f"<a href='tg://user?id={kicker.id}'>{kicker.first_name}</a>"
    new_member_url = f"<a href='tg://user?id={new_member.id}'>{new_member.first_name}</a>"

    text = f"User banned: {new_member_url} (ID:<code>{new_member.id}</code>)\n"
    text += f"Banned by: {kicker_url}\n"

    await event.bot.send_message(
        chat_id=config.log_group.id,
        message_thread_id=config.log_group.thread_id,
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> LEFT))
async def log_user_left(event: ChatMemberUpdated):
    new_member = event.new_chat_member.user
    new_member_url = f"<a href='tg://user?id={new_member.id}'>{new_member.first_name}</a>"

    text = f"User left: {new_member_url} (ID:<code>{new_member.id}</code>)\n"

    await event.bot.send_message(
        chat_id=config.log_group.id,
        message_thread_id=config.log_group.thread_id,
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def log_approved_join_request(event: ChatMemberUpdated):
    approver = event.from_user
    new_member = event.new_chat_member.user

    approver_url = f"<a href='tg://user?id={approver.id}'>{approver.first_name}</a>"
    new_member_url = f"<a href='tg://user?id={new_member.id}'>{new_member.first_name}</a>"

    text = f"User joined: {new_member_url} (ID:<code>{new_member.id}</code>)\n" f"Approved by: {approver_url}\n"

    await event.bot.send_message(
        chat_id=config.log_group.id,
        message_thread_id=config.log_group.thread_id,
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


@router.message(F.text == "/healthcheck")
async def send_healthcheck_message(message: Message):
    await message.answer("Bot is running smoothly!")
