import aiogram
import asyncio
import contextlib
import logging
from aiogram import Bot,Dispatcher,F
from aiogram.types import Message
from aiogram.filters import CommandStart
import openai
from config import TOKEN,GPT_KEY





# openai_messeges = [
#     {
#         'role':'system',
#     }           
# ]



async def get_start(message:Message):
    await message.answer('Привет ! С моей помощью ты можешь задать вопросы ChatGPT')


async def get_chat_gpt(message:Message):
    user_text = message.text
    msg_for_users = await openai_message(msg_for_openai = user_text)
    await message.answer(text=msg_for_users)


async def openai_message(msg_for_openai:str):
    openai.api_key = GPT_KEY
    model = 'gpt-3.5-turbo'
    data_openai = [{'role':'user','content':msg_for_openai}]
    responce = openai.ChatCompletion.create(model=model,messages = data_openai)
    print(responce)
    return responce.choices[0].message.content


async def start():

    bot = Bot(token= TOKEN,parse_mode = "HTML")
    dp = Dispatcher()

    dp.message.register(get_start,CommandStart())
    dp.message.register(get_chat_gpt,F.text)
    

    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}",exc_info=True)
    finally:
        await bot.session.close()



if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt,SystemExit):
        asyncio.run(start())