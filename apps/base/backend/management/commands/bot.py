import asyncio
from django.conf import settings
import os
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, BotCommandScopeAllPrivateChats, BotCommand, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import CommandStart, Command
from asgiref.sync import sync_to_async
from aiogram.enums.parse_mode import ParseMode

from django.contrib.auth.models import User

API_TOKEN = settings.BOT_TOKEN

privat = [BotCommand(command='start', description='Начало работы с ботом')]

bot_answer_phone_number = {}
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)

markup_get_reg = ReplyKeyboardBuilder().add(
    types.KeyboardButton(text='Регистрация'))

markup_get_contact = ReplyKeyboardBuilder().add(
    types.KeyboardButton(text='Отправить свой контакт ☎️', request_contact=True))

dp = Dispatcher()


def get_organization_token_or_check_superuser(user):
    return user.organization.get_bot_token, user.user.is_superuser


@dp.message(CommandStart())
async def start(message: Message):
    await message.reply(
        f"Здравствуйте, это чат-бот для получения уведомлений! \n"
        f"Для получения уведомлений пройдите регистрацию! \n",
        reply_markup=markup_get_reg.as_markup(
            resize_keyboard=True))


@dp.message(F.text.lower() == 'регистрация')
async def registrations(message: Message):
    answer = await message.reply("Для пользования ботом необходим номер телефона",
                                 reply_markup=markup_get_contact.as_markup(
                                     resize_keyboard=True))
    bot_answer_phone_number[message.from_user.id] = answer.message_id


# @dp.message(F.contact)
# async def register_user_contact(message):
#     if message.contact.user_id in bot_answer_phone_number:
#         try:
#             if "+" in message.contact.phone_number:
#                 user = await sync_to_async(Profile.objects.get)(contact_phone=message.contact.phone_number[1:])
#             else:
#                 user = await sync_to_async(Profile.objects.get)(contact_phone=message.contact.phone_number)
#
#             bot_token, is_super_user = await sync_to_async(get_organization_token_or_check_superuser)(user)
#
#             if bot_token == API_TOKEN or is_super_user:
#
#                 if not user.telegram_chat_id:
#                     user.telegram_chat_id = message.contact.user_id
#                     await sync_to_async(user.save)()
#
#                     if user.telegram_chat_id:
#                         await message.reply("Вы успешно прошли регистацию",
#                                             reply_markup=types.ReplyKeyboardRemove())
#                     else:
#                         await message.reply("Упс.. \n"
#                                             "Что то пошло не так...\n"
#                                             "Попробуйте еще раз",
#                                             reply_markup=markup_get_contact.as_markup(
#                                                 resize_keyboard=True))
#                 else:
#                     await message.reply("Вы уже проходили регистацию!",
#                                         reply_markup=types.ReplyKeyboardRemove())
#             else:
#                 await message.reply("Вы не являетесь сотрудником данной организации!",
#                                     reply_markup=types.ReplyKeyboardRemove())
#
#         except Profile.DoesNotExist:
#             await message.reply("Пользователь с данным номером телефона не зарегестрирован в базе!",
#                                 reply_markup=types.ReplyKeyboardRemove())
#         bot_answer_phone_number.pop(message.contact.user_id, None)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=privat, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


class Command(BaseCommand):

    help = 'Бот для авторизацией '

    def handle(self, *args, **kwargs):
        asyncio.run(main())
