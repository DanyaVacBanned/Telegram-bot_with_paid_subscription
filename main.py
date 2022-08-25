import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from db import Database
import navigation as nav

import time
import datetime
logging.basicConfig(level=logging.INFO)
YOOTOKEN = 'YOOCASSA TOKEN'
bot = Bot(token='BOT TOKEN')
dp=Dispatcher(bot)

db = Database('db.db')
def days_to_seconds(days):
    return days * 24 * 60 * 60

def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now

    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        return(dt)


@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Set your nickname!")
    else:
        await bot.send_message(message.from_user.id, 'You are already registered', reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Profile':
            user_nickname = 'Your nickname' + db.get_nickname(message.from_user.id)
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            if user_sub == False:
                user_sub = "Нет"

            user_sub = "\nSubscription " + user_sub
            await bot.send_message(message.from_user.id, user_nickname + user_sub)

        elif message.text == 'Subscription':
            await bot.send_message(message.from_user.id, "Subscription description", reply_markup=nav.sub_inline_markup)
        elif message.text == 'For subscriber':
            if db.get_sub_status(message.from_user.id):
                await bot.send_message(message.from_user.id, "All works, subscriber!")
            else:
                await bot.send_message(message.from_user.id, "Please, buy subscription for see the private content!")
        else:
            if db.get_signup(message.from_user.id) == 'setnickname':
                if (len(message.text) > 15):
                    await bot.send_message(message.from_user.id, "The nickname must not exceed 15 characters!")
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, 'You are entered the unavailable symbol!')
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "done")
                    await bot.send_message(message.from_user.id, 'Registration was successful!', reply_markup=nav.mainMenu)
            else:
                await bot.send_message(message.from_user.id, "I dont understand:(")

@dp.callback_query_handler(text='submonth')
async def submonth(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id, title='Making a subscription', description='Test product description', payload='month_sub', provider_token=YOOTOKEN, currency='RUB', start_parameter='test_bot', prices = [{"label": "Руб", "amount": 15000}])


@dp.pre_checkout_query_handler()
async def procces_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'month_sub':
        time_sub = int(time.time()) + days_to_seconds(30)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, "Congratulations! Now you are have a month subscription!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
