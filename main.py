import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
import schedule
from datetime import datetime, timedelta



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
latestCommand = ""

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('<Your bot> is online ✅')


def addBirthday(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Input birthdate to be added in the following format:\nNAME - DDMM') 
    global latestCommand
    latestCommand = "birthdayAdd"


def removeBirthday(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Input birthdate to be removed in the following format:\nNAME - DDMM') 
    global latestCommand
    latestCommand = "birthdayRemove"


def addReminder(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Input reminder to be added in the following format:\nEVENT - DDMM - HHMM')
    global latestCommand
    latestCommand = "reminderAdd"


def removeReminder(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Input reminder to be marked as done in the following format:\nEVENT - DDMM - HHMM')
    global latestCommand
    latestCommand = "reminderRemove"


def manageDatabase(update, context):
  if (latestCommand[0] == "b"):
    if (latestCommand == "birthdayAdd"):
      with open("birthdays.txt", "a") as f:
        f.write(update.message.text)
        f.write("\n")
      update.message.reply_text('Birthday added ✅') 
      
    else:
      with open("birthdays.txt", "r") as f:
        lines = f.readlines()
      with open("birthdays.txt", "w") as f:
        for line in lines:
          if line.strip("\n") != update.message.text:
            f.write(line)
      update.message.reply_text('Birthday removed ✅') 

  elif (latestCommand[0] == "r"):
    if (latestCommand == "reminderAdd"):
      with open("reminders.txt", "a") as f:
        f.write(update.message.text)
        f.write("\n")
      update.message.reply_text('Reminder added ✅') 

    else:
      with open("reminders.txt", "r") as f:
        lines = f.readlines()
      with open("reminders.txt", "w") as f:
        for line in lines:
          if line.strip("\n") != update.message.text:
            f.write(line)
      update.message.reply_text('Reminder marked as done ✅') 


def dailyChecker():
    nextDay = datetime.now() + timedelta(1)
    with open("birthdays.txt", "r") as f:
      lines = f.readlines()
      for line in lines:
        if nextDay in line.strip("\n"):
          update.message.reply_text("Birthday in 3 hours!\n" + line.strip("\n"))
    with open("reminders.txt", "r") as f:
      lines = f.readlines()
      for line in lines:
        if nextDay in line.strip("\n"):
          update.message.reply_text("Remember to do the below tomorrow!\n" + line.strip("\n"))
    
  

def invalid(update, context):
    """Echo the user message."""
    update.message.reply_text("Invalid command")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # create the Updater and pass it your bot's token.
    updater = Updater("<your pin>", use_context=True)

    # get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands 
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", addBirthday))
    dp.add_handler(CommandHandler("remove", removeBirthday))
    dp.add_handler(CommandHandler("create", addReminder))
    dp.add_handler(CommandHandler("clear", removeReminder))

    # on noncommand 
    dp.add_handler(MessageHandler(Filters.text, manageDatabase))


    # log all errors
    dp.add_error_handler(error)


    # start the Bot
    updater.start_polling()
    updater.idle()
    schedule.every().day.at("09:30").do(dailyChecker)

    
    


    

if __name__ == '__main__':
  main()