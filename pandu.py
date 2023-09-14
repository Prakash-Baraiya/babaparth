import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Define the token for making requests to the external API
external_api_token = "YOUR_EXTERNAL_API_TOKEN"

# Define the token for your Telegram bot
telegram_bot_token = "YOUR_TELEGRAM_BOT_TOKEN"

# Define the states for the conversation
START, PROCESS_TEXT = range(2)

# Function to send the final output to the user
def send_final_output(update: Update, context: CallbackContext) -> int:
    user_text = update.message.text
    response = requests.post(
        "https://learnyst.devsrajput.com/free", 
        data={
            "link": external_api_token,
        }
    )
    
    if response.status_code == 200:
        try:
            data = response.json()
            name = data["TITLE"]
            link = data["MPD"]
            keys = data["KEY_STRING"]
            final_output = f"{name}\n{link}\n{external_api_token}\n\n{keys}"
            update.message.reply_text(final_output)
        except ValueError as e:
            update.message.reply_text("Failed to process data from the API response.")
    else:
        update.message.reply_text("Request Failed! Possible reasons:\n1). Token Expired\n2). API Not Working")
    
    return ConversationHandler.END

# Function to start the conversation
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Welcome! Please send me the text to process.")
    return PROCESS_TEXT

# Function to cancel the conversation
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Conversation cancelled.")
    return ConversationHandler.END

def main():
    updater = Updater(telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Create a conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PROCESS_TEXT: [MessageHandler(Filters.text & ~Filters.command, send_final_output)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add the conversation handler to the dispatcher
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
