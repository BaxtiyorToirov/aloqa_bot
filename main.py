import asyncio
import logging
import psycopg2

from config import host,user,db_name,password
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import *






BOT_TOKEN="6439387293:AAELSzKHZGMXti7rAV-qbjjpbElt0Nvs7nU"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)
ADMINS=5007710398
list=[]


@dp.message(CommandStart())
async def handler_start(message:types.Message):
    list.clear()
    # await message.answer(text='salom', reply_markup=menu)
    await message.answer(text=f"Ismingizni kiriting:\n")


@dp.message(Command("help"))
async def yordam (message:types.Message):
    await message.answer(text="Salom")

@dp.message()
async def ism(message:types.Message):
    print(message.text)
    if message.text.isalpha():
        ism = message.text
        list.append(ism)
        await message.answer(text=f"Nomeringizni kiriting {ism}:")
    elif (message.text[0]=="+" or message.text.isdigit()) and list[0]!=None:
        nomer=message.text
        list.append(nomer)
        await message.answer(text="Malumotingiz uchun rahmat tez orada bog'lanamiz✅")
        await message.answer(text="https://t.me/Aloqamarketingbot?start=start")


        await bot.send_message(chat_id='-1002002607206', text=f'Ism -> {list[0]} \nNomer -> {list[1]}')
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name)

            connection.autocommit = True
            print("ishladi")
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """CREATE TABLE users(
                        id varchar(50) NOT NULL,
                        name varchar(50) NOT NULL,
                        phone_number varchar(50) NOT NULL);"""
                    )
            except Exception as _er:
                print("xatolik")
                pass

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""INSERT INTO users(id,name,phone_number)
                            VALUES ('{message.from_user.id}','{list[0]}','{list[1]}');""")

                print("Qiymat qushildi")
                # with connection.cursor() as cursor:
                #     cursor.execute(
                #       """DROP TABLE users""")
                #     print("malumot uchirildi")


        except Exception as _ex:
            print("[Info] Postgresda xatolik buldi", _ex)
        finally:
            if connection:
                # cursor.close()
                connection.close()

    else:
        await message.answer(text="Xatolik !!!")




async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())