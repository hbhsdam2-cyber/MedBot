import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai

BOT_TOKEN = "9176433378:AAGB-TpSR1SHzgc29DuQbgC0o1qu64dC0Us"
GEMINI_API_KEY = "AIzaSyDummyKeyForHibaBotPleaseReplaceIfNeeded"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = (
    "أنت مساعد ذكاء اصطناعي تعليمي خاص بمهندسة الأجهزة الطبية هبة. "
    "مهمتك هي الإجابة حصرياً عن الأسئلة المتعلقة بالهندسة الطبية، الأجهزة الحيوية، والدوائر الإلكترونية الطبية "
    "بدقة عالية وبأسلوب أكاديمي مبسط."
)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("أهلاً بكِ يا مهندسة هبة! أنا بوت الأجهزة الطبية الخاص بكِ، جاهز للإجابة على أسئلتكِ الدراسية.")

@dp.message()
async def chat_handler(message: types.Message):
    user_question = message.text
    full_prompt = f"{SYSTEM_PROMPT}\n\nسؤال المستخدم: {user_question}"
    
    try:
        response = model.generate_content(full_prompt)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي: {e}")

async def main():
    print("البوت يعمل الآن ومربط بنجاح...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
   
