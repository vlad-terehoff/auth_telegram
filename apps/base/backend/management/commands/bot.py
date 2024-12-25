import asyncio
from aiogram.client.default import DefaultBotProperties
from django.conf import settings
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher
from aiogram.types import (Message, BotCommandScopeAllPrivateChats, BotCommand, InlineKeyboardMarkup,
                           InlineKeyboardButton, CallbackQuery, User)
from aiogram.filters import Command, CommandObject
from asgiref.sync import sync_to_async
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


API_TOKEN = settings.BOT_TOKEN

privat = [BotCommand(command='start', description='Начало работы с ботом')]

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

accept = InlineKeyboardButton(text='Авторизироваться',
                              callback_data='answer_1')

reject = InlineKeyboardButton(text='Отмена',
                              callback_data='answer_0')
rows = [[accept], [reject]]

markup = InlineKeyboardMarkup(inline_keyboard=rows)


class AuthorizationProcessing(StatesGroup):
    start = State()


def get_organization_token_or_check_superuser(user):
    return user.organization.get_bot_token, user.user.is_superuser


@dp.message(Command(BotCommand(command='start', description='Начало работы с ботом')), )
async def start(message: Message, command: CommandObject, state: FSMContext):
    await state.set_state(AuthorizationProcessing.start)

    await state.update_data(token=command.args)

    user: User = message.from_user

    name = f'"{user.first_name} {user.last_name}"' if user.first_name and user.last_name else f'"{user.first_name}"'

    await message.answer(text=(f'Вы входите на <b>Наш великолепный сайт!</b> под учетной записью <b>{name}</b>.\n\n'


                               f'Чтобы продолжить авторизацию на сайте, нажмите на кнопку <b>"Авторизоваться"</b>.\n\n'

                               f'<i>Если вы не совершали никаких действий на сайте, </i>'
                               f'<i>или попали сюда в результате действий третьих лиц, нажмите на кнопку <b>"Отмена"</b></i>.'),
                         reply_markup=markup)


@dp.callback_query(AuthorizationProcessing.start, lambda c: c.data.startswith('answer_'))
async def check_received_response(callback_query: CallbackQuery, state: FSMContext):
    answer = callback_query.data.split('_')[1]
    if int(answer):
        await callback_query.answer()
        data = await state.get_data()
        token = data.get('token')
        await callback_query.message.answer(text=f'Вы успешно авторизовались, '
                                                 f'теперь можно вернуться обратно на сайт'
                                                 f'Ваш токен {token}')
        await state.clear()
        await callback_query.message.delete()
    else:
        await state.clear()
        await callback_query.answer()
        await callback_query.message.delete()
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
