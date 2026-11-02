import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai

# التوكن الخاص ببوتكِ على تيليجرام
BOT_TOKEN = "9176433378:AAGB-TpSR1SHzgc29DuQbgC0o1qu64dC0Us"

# ضعي هنا مفتاح Google AI Studio API الخاص بـ Gemini (استبدلي ما بين القوسين بمفتاحكِ الفعلي)
GEMINI_API_KEY = "ضعي_مفتاح_جيميناي_هنا"

# إعدادات جيميناي
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# إنشاء كائن البوت والموزع
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# تعليمات النظام لجعل البوت متخصصاً في الأجهزة الطبية والمادة الدراسية الخاصة بكِ
SYSTEM_PROMPT = (
    "أنت مساعد ذكاء اصطناعي تعليمي خاص بمهندسة الأجهزة الطبية هبة. "
    "مهمتك هي الإجابة حصرياً عن الأسئلة المتعلقة بالهندسة الطبية، الأجهزة الحيوية، والدوائر الإلكترونية الطبية "
    "بدقة عالية وبأسلوب أكاديمي مبسط."
)

# التفاعل عند بدء البوت (/start)
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("أهلاً بكِ يا مهندسة هبة! أنا بوت الأجهزة الطبية الخاص بكِ، جاهز للإجابة على أسئلتكِ الدراسية.")

# استقبال أي رسالة نصية والرد عليها عبر جيميناي
@dp.message()
async def chat_handler(message: types.Message):
    user_question = message.text
    full_prompt = f"{SYSTEM_PROMPT}\n\nسؤال المستخدم: {user_question}"
    
    try:
        response = model.generate_content(full_prompt)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي: {e}")

# الدالة الرئيسية لتشغيل البوت
async def main():
    print("البوت يعمل الآن ومربط بنجاح...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
