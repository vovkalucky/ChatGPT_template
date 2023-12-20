from bot.models.methods import sql_add_user, remove_user_from_database
from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated, Message

router: Router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(message: ChatMemberUpdated):
    user_id = message.chat.id
    #await db_start()
    await remove_user_from_database(user_id)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(message: ChatMemberUpdated):
    #await db_start()
    await sql_add_user(message)
