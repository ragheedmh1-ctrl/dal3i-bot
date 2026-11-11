import os
import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# جلب التوكن ومفتاح الذكاء الاصطناعي من متغيرات البيئة بأمان تام
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# الـ ID الخاص بك حتى البوت يراسلك شخصياً
MY_CHAT_ID = "635397827"

# إعداد عميل Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# الشخصية والتوجيهات الصارمة باللهجة العراقية الصميمة
SYSTEM_INSTRUCTION = """
أنت صديق عراقي مقرب جداً للمستخدم (اسمه رغيد)، تسكن في العراق. 
قواعدك الأساسية:
1. تتحدث حصراً باللهجة العراقية اليومية الصميمة (مثل: شلونك رغيد، شكو ماكو، تدلل عيني، حبيبي، شعندك اليوم، وين غاطس، إلخ).
2. ممنوع نهائياً استخدام اللغة العربية الفصحى أو الكلام الرسمي أو لغة الروبوتات.
3. كلامك عفوي، دافئ، قصير ومباشر، وكأنك دتراسل صديقك على الواتساب أو تيليجرام.
4. اهتم بتفاصيل يومه واسأله أسئلة طبيعية عن شغله أو شسوّى اليوم، وشاركني الحديث بكل أريحية.
"""

# دالة توليد الرد باللهجة العراقية باستخدام النموذج المحدث
async def generate_iraqi_reply(user_message: str) -> str:
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=user_message,
            config={
                'system_instruction': SYSTEM_INSTRUCTION,
                'temperature': 0.85,
            }
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"ها حبيبي رغيد، صار عندي خطأ بالاتصال: {e}"

# وظيفة لإرسال رسالة عشوائية من البوت إليك تلقائياً كل فترة
async def send_random_proactive_message(context: ContextTypes.DEFAULT_TYPE):
    greetings = [
        "ها رغيد، وين غاطس اليوم؟ شكو ماكو بالشغل؟",
        "كاعد لو دتشتغل؟ شلونه الجو يمك؟",
        "بشرفي اجيت عبالي، شكو ماكو شغل اليوم؟",
        "ها عيني، خلصت شغل لو بعدك تفر بالطريق؟",
        "شلونها امورك اليوم؟ مطوّل بالشغل لو تعبت؟"
    ]
    chosen_msg = random.choice(greetings)
    
    try:
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=chosen_msg)
    except Exception as e:
        print(f"خطأ بإرسال الرسالة التلقائية: {e}")

# الاستجابة لرسائلك عندما ترد على البوت
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_text = update.message.text
    print(f"وصلتني رسالة من الـ ID: {user_id} ونصه: '{user_text}'")
    
    if user_id == MY_CHAT_ID:
        reply_text = await generate_iraqi_reply(user_text)
        await update.message.reply_text(reply_text)
    else:
        print(f"تم تجاهل رسالة من مستخدم غريب: {user_id}")

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    job_queue = application.job_queue
    job_queue.run_repeating(send_random_proactive_message, interval=10800, first=10)

    print("البوت اشتغل وصار يشتغل عراقي صميم ويستمع للرسائل...")
    application.run_polling()

if __name__ == '__main__':
    main()
