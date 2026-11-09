import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from huggingface_hub import InferenceClient

# သင့်ရဲ့ Hugging Face Token နဲ့ Model
HF_TOKEN = "Hf_cHYhDfmwLHsJjAuyDxviuaifzQFVbYvskU"
MODEL_NAME = "Orion-zhen/Qwen2.5-7B-Instruct-Uncensored"

client = InferenceClient(api_key=HF_TOKEN)

# Telegram ကနေ စာဝင်လာရင် AI ဆီ ပို့ပြီး ပြန်ဖြေမယ့် function
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    try:
        # Hugging Face API ကို လှမ်းခေါ်ခြင်း
        messages = [{"role": "user", "content": user_message}]
        completion = client.chat.completion(
            model=MODEL_NAME,
            messages=messages,
        )
        ai_reply = completion.choices[0].message.content
    except Exception as e:
        ai_reply = f"Error ဂျင်နေပါသည်: {str(e)}"

    # User ဆီကို အဖြေပြန်ပို့ရန်
    await context.bot.send_message(chat_id=chat_id, text=ai_reply)

if __name__ == '__main__':
    # သင့်ရဲ့ Telegram Bot Token ကို ထည့်ပါ
    BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Text မက်ဆေ့ချ်မှန်သမျှကို လက်ခံရန်
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot စတင် အလုပ်လုပ်နေပါပြီ...")
    application.run_polling()
