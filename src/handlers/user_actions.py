from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from src.dispatcher import dp
from src.users.models import User, Subscribe
from src.tasks import task_bomber, app

from src.bomber.models import Spam
from src.bomber.bomber import CountSms


keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*[
        'Начать спам',
        'VIP Статус',
        'Моя статистика',
    ]
)


class Victim(StatesGroup):
    number = State()


@dp.message_handler(state='*', commands=['start'])
async def on_start(msg: types.Message, state: FSMContext):
    await state.finish()

    if User.objects.filter(user_id=msg.from_user.id).count() < 1:
        User.objects.create(
            user_id=msg.from_user.id,
            spam=Spam().save(),
            subscribe=Subscribe().save()
        )

    return await msg.reply('Привет, я СМС-Бомбер!\n'
                           'Кого-то нужно бомбануть?)', reply_markup=keyboard)


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(msg: types.Message, state: FSMContext):
    await state.finish()
    return await msg.reply('Отмена', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Начать спам')
async def get_number_for_spam(msg: types.Message):
    await Victim.number.set()
    # if await msg.bot.get_chat_member(CHANNEL_ID, msg.from_user.id):
    return await msg.reply('На чей номер?\nВ формате: +7 или +38')


@dp.message_handler(state=Victim.number)
async def start_spam(msg: types.Message, state: FSMContext):
    if len(msg.text) == 13 and msg.text.startswith('+38') or \
       len(msg.text) == 11 and msg.text.startswith('+7'):
        await state.finish()

        user = User.objects.get(user_id=msg.from_user.id)
        if not user.spam.stopped:
            return await msg.reply('Спам еще запущен.')

        if not user.subscribe:
            task_id = task_bomber.delay(
                user_id=msg.from_user.id,
                phone_number=msg.text,
                count_services=5,
                delay=20,
                end_time_in_minutes=10
            )
            user.spam = Spam(task_id=str(task_id)).save()
        else:
            task_id = task_bomber.delay(
                user_id=msg.from_user.id,
                phone_number=msg.text,
                count_services='all',
                delay=0,
                end_time_in_minutes='inf'
            )
            user.spam = Spam(task_id=str(task_id)).save()
        user.save()

        stop_spam_button = types.InlineKeyboardButton('Остановить спам', callback_data='stop_spam')
        stop_spam_button = types.InlineKeyboardMarkup().add(stop_spam_button)

        return await msg.reply(
            'Спам начат. Он будет длится 10 минут.\n'
            'Для отключения спама нажмите кнопку "Остановить спам"',
            reply_markup=stop_spam_button
        )
    await msg.answer('Номер не корректен', reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add('/cancel'))


@dp.callback_query_handler(lambda c: c.data == 'stop_spam')
async def stop_spam(callback_query: types.CallbackQuery):
    user = User.objects.get(user_id=callback_query.from_user.id)
    app.control.revoke(user.spam.task_id, terminate=True)  # Terminate = True - for task kill

    CountSms(callback_query.from_user.id).save_count_sent_sms_to_mongo()

    return await callback_query.answer('Спам остановлен')


@dp.message_handler(lambda message: message.text == 'VIP Доступ')
async def get_number_for_spam(msg: types.Message):
    pay = types.InlineKeyboardButton('Оплатить', callback_data='pay_vip')
    pay = types.InlineKeyboardMarkup().add(pay)

    return await msg.reply(
        'В бесплатной версии доступно всего 5 сервисов для спама, '
        'длительность работы до 10 минут.'
        'После оплаты вам будет доступно 15 активных сервисов,\n'
        'скорость отправки максимальная, а также безграничное время спама.',
        reply_markup=pay
    )


@dp.message_handler(lambda message: message.text == 'Моя статистика')
async def get_my_statistic(msg: types.Message):
    user = User.objects.get(user_id=msg.from_user.id)

    return await msg.reply(
        f'Ваш id: {user.user_id}\n'
        f'Количество оправленных смс: {user.count_sent_sms}\n'
        f'Статус: {user.subscribe.status}'
    )
