import asyncio
import aiohttp
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GROUP_ID = -1001234567890  # Replace with your group ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

roman_facts = [
    "The Roman Empire lasted for over 1,000 years, from 27 BC to 476 AD.",
    "Romans built over 250,000 miles of roads across their empire.",
    "Julius Caesar was assassinated on the Ides of March (March 15) in 44 BC.",
    "Roman soldiers were paid in salt — that’s where the word ‘salary’ comes from.",
    "Concrete made by the Romans is still stronger than most modern types.",
    "The Colosseum could hold up to 50,000 spectators for gladiator games.",
]

async def get_answer(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.monkedev.com/fun/chat?msg={query}") as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("response", "I couldn’t find an answer for that.")
            return "I couldn’t fetch data right now."

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "🏛 Ave! I am *Rome Legacy*, your Roman historian and knowledge oracle.\n\n"
        "Ask me anything about history or the modern world — I shall answer wisely.",
        parse_mode="Markdown"
    )

@dp.message()
async def handle_message(message: Message):
    if message.chat.type in ["group", "supergroup"] and not message.from_user.is_bot:
        text = message.text.lower()
        if "rome" in text or "?" in text:
            answer = await get_answer(text)
            await message.reply(answer)

async def auto_post_facts():
    while True:
        fact = random.choice(roman_facts)
        try:
            await bot.send_message(GROUP_ID, f"🏺 *Roman Fact:*\n{fact}", parse_mode="Markdown")
        except Exception as e:
            print("Fact error:", e)
        await asyncio.sleep(1200)

async def main():
    asyncio.create_task(auto_post_facts())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
