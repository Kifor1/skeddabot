
import logging # Logger package to track error messages.
import requests # Package to download a file.
import icalendar # Package to adjust calendar data.
import os
import datetime


# python-telegram-bot package.
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram.messageentity import MessageEntity 

# Logger deploy.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Have no idea why it should be here. Maybe when the parameter is returned to a range the MessageHandler gets trigered.
MAIN_MENU, DEPUTY_LINK_REQUEST, CALENDAR_REQUEST,  MAIN_MENU_RETURN, FAVORITE_STATION_1, FAVORITE_STATION_2, FAVORITE_STATION_3, FAVORITE_STATION_4, FAVORITE_STATION_5 = range(9)

# Stations list with corresponding station numbers.
station_name_list = ['A1',  'A2',  'A3',  'A4',  'A5',  'A6',  'A7',  'A8',  'A9',  'A10',  'A11',  'A12',  'A13',  'A14',  'A15',  'A16',  'A17',  'A18',  'A19',  'A20',  'A21',  'A22',  'A23',  'A24',  'A25',  'A26',  'A27',  'A28',  'A29',  'A30',  'A31',  'A32',  'A33',  'A34',  'A35',  'A36',  'A37',  'A38',  'B1',  'B2',  'B3',  'B4',  'B5',  'B6',  'B7',  'B8',  'B9',  'B10',  'B11',  'B12',  'B13',  'B14',  'B15',  'B16',  'B17',  'B18',  'B19',  'B20',  'B21',  'B22',  'B23',  'B24',  'B25',  'B26',  'B27',  'B28',  'B29',  'B30',  'B31',  'B32',  'B33',  'B34',  'B35',  'B36',  'B37',  'B38',  'B39',  'Ops 1',  'Ops 2',  'Ops 3',  'Ops 4',  'Ops 5',  'Ops 6',  'Ops 7',  'Ops 8',  'Ops 9',  'Ops 10',  'Ops 11',  'Ops 12',  'Ops 13',  'Ops 14',  'Ops 15',  'Ops 16',  'Ops 17',  'Ops 18',  'Ops 19',  'Ops 20']
station_number_list = ['A1',  '774734',  'A2',  '774770',  'A3',  '774771',  'A4',  '774772',  'A5',  '774773',  'A6',  '774774',  'A7',  '774775',  'A8',  '774776',  'A9',  '774777',  'A10',  '774778',  'A11',  '774779',  'A12',  '774780',  'A13',  '774781',  'A14',  '774782',  'A15',  '774783',  'A16',  '774784',  'A17',  '774785',  'A18',  '774786',  'A19',  '774800',  'A20',  '774799',  'A21',  '774798',  'A22',  '774797',  'A23',  '774796',  'A24',  '774795',  'A25',  '774801',  'A26',  '774794',  'A27',  '774792',  'A28',  '774791',  'A29',  '774790',  'A30',  '774789',  'A31',  '774788',  'A32',  '774787',  'A33',  '774769',  'A34',  '774793',  'A35',  '774768',  'A36',  '774758',  'A37',  '774735',  'A38',  '774736',  'B1',  '774737',  'B2',  '774738',  'B3',  '774739',  'B4',  '774740',  'B5',  '774741',  'B6',  '774742',  'B7',  '774743',  'B8',  '774744',  'B9',  '774745',  'B10',  '774746',  'B11',  '774747',  'B12',  '774748',  'B13',  '774749',  'B14',  '774750',  'B15',  '774751',  'B16',  '774765',  'B17',  '774764',  'B18',  '774763',  'B19',  '774762',  'B20',  '774761',  'B21',  '774760',  'B22',  '774766',  'B23',  '774759',  'B24',  '774757',  'B25',  '774756',  'B26',  '774755',  'B27',  '774754',  'B28',  '774753',  'B29',  '774752',  'B30',  '774767',  'B31',  '774802',  'B32',  '774803',  'B33',  '774804',  'B34',  '774805',  'B35',  '774806',  'B36',  '774807',  'B37',  '774808',  'B38',  '774809',  'B39',  '774810',  'Ops 1',  '774812',  'Ops 2',  '774813',  'Ops 3',  '774814',  'Ops 4',  '774815',  'Ops 5',  '774816',  'Ops 6',  '774817',  'Ops 7',  '774818',  'Ops 8',  '774724',  'Ops 9',  '774725',  'Ops 10',  '774726',  'Ops 11',  '774727',  'Ops 12',  '774728',  'Ops 13',  '774811',  'Ops 14',  '777917',  'Ops 15',  '805716',  'Ops 16',  '805717',  'Ops 17',  '805718',  'Ops 18',  '805719',  'Ops 19',  '805720',  'Ops 20',  '805721']

date_today = datetime.date.today()
year, today_week_number, day_of_week = date_today.isocalendar()

# Functions to run. The program starts below after all fuctions.

# Main Menu, called when /start command is given, replies with text and deploys reply buttons.
def main_menu(update: Update, context: CallbackContext) -> int:
    
    user_id = update.message.from_user.id
    user_file_deputy = "deputydb/%s.txt" % user_id
    user_file_stations = "stationsdb/%s.txt" % user_id
    if os.path.isfile(user_file_deputy) and os.path.isfile(user_file_stations):
        reply_keyboard_set = [['Request Skedda Links', 'Update Deputy Link', 'Update Favorite Stations']]
    else:
        reply_keyboard_set= [['Update Deputy Link', 'Update Favorite Stations']]
    update.message.reply_animation(
        animation = 'https://media.giphy.com/media/ThHSCmkz0CUI8/giphy.gif',
        caption = 'Hello! My name is Slacky The Sloth Jr. I will help you book stations in Skedda.\n\n'
        'Send /cancel to stop talking to me.\n'
        'And /start to being again.\n\n'
        'But for now, what do you want to do?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard_set, one_time_keyboard = True, input_field_placeholder = 'At your service!'
        ),
    )

    return MAIN_MENU # After that some function is triggered.

# Requests Deputy link, proceeds to the fuction of writing link into the database, deploys Return to Main Menu button.
def deputy_link_request(update: Update, context: CallbackContext) -> int:

    # Replies with GIF instructions file. 
    reply_keyboard = [['Return to Main Menu']]
    update.message.reply_animation(
        animation = 'https://i.ibb.co/SdWfxdM/How-To-Get-Deputy-Calendar-Link.gif',
        caption = 'Please provide me your Deputy calendar link.',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, input_field_placeholder = 'Only URLs please!'
        ),
    )

    return DEPUTY_LINK_REQUEST # After that some function is triggered.

# Writes received URL into a file.
def deputy_link_write(update: Update, context: CallbackContext) -> int:
    
    # Creates a file with named as user id and writes down link into a file. Overwrites file on update.
    user_id = update.message.from_user.id
    link = update.message.text
    user_file = "deputydb/%s.txt" % user_id
    print(link, file = open(user_file, 'w'))
    open(user_file, "r").close()

    # Replies and deploys Return to Main Menu button.
    reply_keyboard = [['Return to Main Menu']]
    update.message.reply_animation(
        animation = 'https://media.giphy.com/media/1xkMJIvxeKiDS/giphy.gif',
        caption = 'Your Deputy Link was updated!\n'
        'Thank you!',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, input_field_placeholder = 'At your service!'
        ),
    )

    return MAIN_MENU_RETURN # After that some function is triggered.

def favorite_station_1_request(update: Update, context: CallbackContext) -> int:

    update.message.reply_photo(photo = 'https://i.ibb.co/89DnLFy/stations.jpg',
        caption = "Let's start updating your 5 favorite stations.\n"
        'Tell me, what will be the first one?\n\n'
        'Please keep in mind that I can acept only existing stations.'),
    
    return FAVORITE_STATION_1

def favorite_station_2_request(update: Update, context: CallbackContext) -> int:

    user_id = update.message.from_user.id
    station = update.message.text
    user_file = "stationsdb/%s.txt" % user_id
    print(station, file = open(user_file, 'w'))
    open(user_file, "r").close()

    update.message.reply_text('What about second one?'),

    return FAVORITE_STATION_2
    
def favorite_station_3_request(update: Update, context: CallbackContext) -> int:

    user_id = update.message.from_user.id
    station = update.message.text
    user_file = "stationsdb/%s.txt" % user_id
    print(station, file = open(user_file, 'a'))
    open(user_file, "r").close()

    update.message.reply_text('Third?'),

    return FAVORITE_STATION_3

def favorite_station_4_request(update: Update, context: CallbackContext) -> int:

    user_id = update.message.from_user.id
    station = update.message.text
    user_file = "stationsdb/%s.txt" % user_id
    print(station, file = open(user_file, 'a'))
    open(user_file, "r").close()

    update.message.reply_text('Fourth?'),

    return FAVORITE_STATION_4

def favorite_station_5_request(update: Update, context: CallbackContext) -> int:

    user_id = update.message.from_user.id
    station = update.message.text
    user_file = "stationsdb/%s.txt" % user_id
    print(station, file = open(user_file, 'a'))
    open(user_file, "r").close()

    update.message.reply_text('And the last one?'),

    return FAVORITE_STATION_5

def favorite_station_done(update: Update, context: CallbackContext) -> int:

    user_id = update.message.from_user.id
    station = update.message.text
    user_file = "stationsdb/%s.txt" % user_id
    print(station, file = open(user_file, 'a'))
    open(user_file, "r").close()

    reply_keyboard = [['Return to Main Menu']]
    update.message.reply_animation(
        animation = 'https://media.giphy.com/media/Pcmc6KhxNL6hi/giphy.gif',
        caption = 'Your Favorite Stations were updated!\n'
        'Thank you!',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, input_field_placeholder = 'At your service!'
        ),
    )

    return MAIN_MENU_RETURN

# Requests what week user wants their shifts for.
def calendar_request(update: Update, context: CallbackContext) -> int:

    reply_keyboard = [['This Week', 'Next Week']]
    update.message.reply_text(
        text = 'What week you want Skeeda links for?',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, input_field_placeholder = 'At your service!'
        ),
    )

    return CALENDAR_REQUEST

# Downloads ics file using provided Deputy Link from database.
def calendar_output(update: Update, context: CallbackContext) -> int:

    global station_name_list, station_number_list, today_week_number
    
    # Finds user id in the message ("Request Skeeda Links"), looks for match in Data Base, once foud assigns next line (Link) to varable as a string.
    user_id = update.message.from_user.id
    week_number_specified = update.message.text
    user_file_deputy = "deputydb/%s.txt" % user_id
    with open(user_file_deputy) as user_file_deputy:
        user_link = user_file_deputy.readline()
        user_file_deputy.close()

    # Creates a file and writes everything that's inside o a lik into a ics (calendar file).
    deputy_file = requests.get(user_link, allow_redirects=True)
    open('calendardeputy.ics', 'wb').write(deputy_file.content)

    # Using icalendar package, formats ICS file into Event Summary Startime Endtime.
    ical_file = open('calendardeputy.ics', 'rb')
    g_cal = icalendar.Calendar.from_ical(ical_file.read())
    user_shifts = []
    reply_markup_setup = []

    # Sets parameter what shifts to exclude from the list.
    if week_number_specified == 'This Week':
        requested_week_number = str(today_week_number).zfill(2)
    else:
        requested_week_number = str(today_week_number + 1).zfill(2)

    # Searches for the events in calendar file that are happening during specified week.
    for component in g_cal.walk():
        if component.name == 'VEVENT' and component.get('dtstart').dt.strftime('%W') == requested_week_number:
            week_number = component.get('dtstart').dt.strftime('%W')
            summary = component.get('summary')
            start_dt = component.get('dtstart').dt
            end_dt = component.get('dtend').dt
            if summary == '[TLL] ROPS Shift Lead':
                station_number = '774767'
                station_name = 'B30'
            elif summary == '[TLL] ROPS Helper Shift Lead':
                station_number = '774734'
                station_name = 'A1'
            elif summary == '[TLL] ROPS RC Testing' or summary == '[GBA] ROPS RC Testing' :
                station_number = '774739'
                station_name = 'B3'
            elif summary == '[TLL] ROPS Meetings' or summary == '[GBA] ROPS Meetings' or summary == '[TLL] ROPS Training' or summary == '[GBA] ROPS Training' or summary == '[TLL] ROPS Practical Trainer' or summary == '[GBA] ROPS Practical Trainer':
                pass
            else:
                user_file_stations = open("stationsdb/%s.txt" % user_id, 'r')
                favorite_station_names = open('stationsdb/%s.txt' % user_id).read().splitlines()
                user_file_stations.close()
                favorite_station_numbers = [station_number_list[station_number_list.index(favorite_station_names[0]) + 1], station_number_list[station_number_list.index(favorite_station_names[1]) + 1], station_number_list[station_number_list.index(favorite_station_names[2]) + 1], station_number_list[station_number_list.index(favorite_station_names[3]) + 1], station_number_list[station_number_list.index(favorite_station_names[4]) + 1]]
                
            format_message = '{0}\n{1} {2} - {4}\n{3} - {5} Week {6}'.format(summary, start_dt.strftime('%A'), start_dt.strftime('%d/%m/%Y'), start_dt.strftime('%H:%M'), end_dt.strftime('%d/%m/%Y'), end_dt.strftime('%H:%M'), week_number)
            format_link = (end_dt.strftime('%Y'), end_dt.strftime('%m'), end_dt.strftime('%d'), end_dt.strftime('%H'), end_dt.strftime('%M'), start_dt.strftime('%Y'), start_dt.strftime('%m'), start_dt.strftime('%d'), start_dt.strftime('%H'), start_dt.strftime('%M'))
            
            # Shift Leading shift midnight fix.
            if summary == '[TLL] ROPS Shift Lead' and start_dt.strftime('%H') == '23' and start_dt.strftime('%M') == '59':
                user_shifts.append(format_message)
                reply_markup_setup.append(InlineKeyboardMarkup([[InlineKeyboardButton(station_name, url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={1}-{2}-{3}T00%3A00%3A00".format(station_number, *format_link))]]))
            # Shift Leading shift.
            elif summary == '[TLL] ROPS Shift Lead':
                user_shifts.append(format_message)
                reply_markup_setup.append(InlineKeyboardMarkup([[InlineKeyboardButton(station_name, url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(station_number, *format_link))]]))
            # Helper Shift Leading shift midnight fix.
            elif summary == '[TLL] ROPS Helper Shift Lead' and start_dt.strftime('%H') == '23' and start_dt.strftime('%M') == '59':
                user_shifts.append(format_message)
                reply_markup_setup.append(InlineKeyboardMarkup([[InlineKeyboardButton(station_name, url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={1}-{2}-{3}T00%3A00%3A00".format(station_number, *format_link))]]))                 
            # Helper Shift Leading shift over midnight fix.
            elif summary == '[TLL] ROPS Helper Shift Lead' and start_dt.strftime('%D') != end_dt.strftime('%D') and end_dt.strftime('%H') != '00' and summary != '[TLL] ROPS Shift Lead':
                user_shifts.append(format_message)
                reply_markup_setup.append(InlineKeyboardMarkup([[
                    InlineKeyboardButton(station_name, url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T00%3A00%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(station_number, *format_link)),
                    InlineKeyboardButton(station_name, url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&{1}-{2}-{3}T00%3A00%3A00".format(station_number, *format_link)),]]))
            # Helper Shift Leading shift.
            elif summary == '[TLL] ROPS Helper Shift Lead':
                user_shifts.append(format_message)
                reply_markup_setup.append(InlineKeyboardMarkup([[InlineKeyboardButton(station_name, url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(station_number, *format_link))]]))
            # RC Testing shift.
            elif summary == '[TLL] ROPS RC Testing' or summary == '[GBA] ROPS RC Testing':
                user_shifts.append(format_message)
                reply_markup_setup.append(InlineKeyboardMarkup([[InlineKeyboardButton(station_name, url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(station_number, *format_link))]]))
            elif summary == '[TLL] ROPS Meetings' or summary == '[GBA] ROPS Meetings' or summary == '[TLL] ROPS Training' or summary == '[GBA] ROPS Training' or summary == '[TLL] ROPS Practical Trainer' or summary == '[GBA] ROPS Practical Trainer':
                pass
            # Over midnight shifts. Replies with two links first - until midnight second - after midnight. Excludes Shift Lead to avoid collision.
            elif start_dt.strftime('%D') != end_dt.strftime('%D') and end_dt.strftime('%H') != '00':
                user_shifts.append(format_message)
                reply_markup_setup.append(InlineKeyboardMarkup([[
                    InlineKeyboardButton(favorite_station_names[0], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T00%3A00%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[0], *format_link)),
                    InlineKeyboardButton(favorite_station_names[1], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T00%3A00%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[1], *format_link)),
                    InlineKeyboardButton(favorite_station_names[2], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T00%3A00%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[2], *format_link)),
                    InlineKeyboardButton(favorite_station_names[3], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T00%3A00%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[3], *format_link)),
                    InlineKeyboardButton(favorite_station_names[4], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T00%3A00%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[4], *format_link)),
                        ],[
                    InlineKeyboardButton(favorite_station_names[0], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={1}-{2}-{3}T00%3A00%3A00".format(favorite_station_numbers[0], *format_link)),
                    InlineKeyboardButton(favorite_station_names[1], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={1}-{2}-{3}T00%3A00%3A00".format(favorite_station_numbers[1], *format_link)),
                    InlineKeyboardButton(favorite_station_names[2], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={1}-{2}-{3}T00%3A00%3A00".format(favorite_station_numbers[2], *format_link)),
                    InlineKeyboardButton(favorite_station_names[3], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={1}-{2}-{3}T00%3A00%3A00".format(favorite_station_numbers[3], *format_link)),
                    InlineKeyboardButton(favorite_station_names[4], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={1}-{2}-{3}T00%3A00%3A00".format(favorite_station_numbers[4], *format_link)),]]))
            # Regular shifts.
            else:
                user_shifts.append(format_message)
                reply_markup_setup.append(InlineKeyboardMarkup([[
                    InlineKeyboardButton(favorite_station_names[0], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[0], *format_link)),
                    InlineKeyboardButton(favorite_station_names[1], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[1], *format_link)),
                    InlineKeyboardButton(favorite_station_names[2], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[2], *format_link)),
                    InlineKeyboardButton(favorite_station_names[3], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[3], *format_link)),
                    InlineKeyboardButton(favorite_station_names[4], url = "https://starshipvenue.skedda.com/booking?nbend={1}-{2}-{3}T{4}%3A{5}%3A00&nbspaces={0}&nbstart={6}-{7}-{8}T{9}%3A{10}%3A00".format(favorite_station_numbers[4], *format_link))]]))

    # Counts number of shifts in the list and sends user shifts that many times.
    number_of_shifts = len(user_shifts)
    start_number = 0
    while start_number < number_of_shifts:
        context.bot.send_message(chat_id = update.effective_chat.id, text = user_shifts[start_number], reply_markup = reply_markup_setup[start_number], parse_mode = ParseMode.HTML)
        start_number += 1

    # Clears file with calendar data. Will be moved to the end of a fuction.
    clear_output = open('calendardeputy.ics', 'w')
    clear_output.write('')
    clear_output.close()

    # Replies and deploys Return to Main Menu button.
    reply_keyboard = [['Return to Main Menu']]
    update.message.reply_text(
        'Your shifts are served, just pick yourself a station and confirm booking.\n'
        "Don't forget to Check In before the shift, good luck!",
        reply_markup = ReplyKeyboardMarkup( 
            reply_keyboard, one_time_keyboard = True, input_field_placeholder = 'At your service!'
        ),
    )

    return MAIN_MENU_RETURN # After that some function is triggered.

# Cancels and ends the conversation.
def cancel(update: Update, context: CallbackContext) -> int:
    
    user = update.message.from_user
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup = ReplyKeyboardRemove()
    )

    return ConversationHandler.END

# Replies upon receiving an error, requesting user to restat a bot.
def error_handler(update: Update, context: CallbackContext) -> int:

    reply_keyboard = [['/cancel']]
    update.message.reply_text(
        'Something went wrong!\n\n'
        'You will need to restart me.\n'
        'Use /start command for that.\n'
        'Try updating Deputy link.',
        reply_markup = ReplyKeyboardMarkup( 
            reply_keyboard, one_time_keyboard = True, input_field_placeholder = 'At your service!'
        ),
    )

    return MAIN_MENU_RETURN # For some reason doesn't trigger a function.

# Function that runs the bot defining what bot will do when input messages are received.
def main() -> None:
    
    global station_name_list

    # Creates the Updater and passes it bot's token.
    updater = Updater("5088897257:AAEn14YSvkVk0gbpmCxQZHE-JlANk0U0cX8")

    # Gets the dispatcher to register handlers.
    dispatcher = updater.dispatcher

    # Adds conversation handler with the states.'Update Favorite Stations'
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', main_menu)],
        states = {
            MAIN_MENU: [MessageHandler(Filters.regex('^(Request Skedda Links)$') & ~Filters.command, calendar_request), MessageHandler(Filters.regex('^(Update Deputy Link)$') & ~Filters.command, deputy_link_request), MessageHandler(Filters.regex('^(Update Favorite Stations)$') & ~Filters.command, favorite_station_1_request)], # In Start function that returns START, if certain button is clicked corresponding function is called.
            DEPUTY_LINK_REQUEST: [MessageHandler(Filters.entity(MessageEntity.URL), deputy_link_write), MessageHandler(Filters.regex('^(Return to Main Menu)$') & ~Filters.command, main_menu)], #In Deputy Link Request fuction, if person sends a link function two rite the link in Data Base is called.
            CALENDAR_REQUEST: [MessageHandler(Filters.regex('^(This Week)$' ) & ~Filters.command, calendar_output), MessageHandler(Filters.regex('^(Next Week)$') & ~Filters.command, calendar_output)],
            MAIN_MENU_RETURN: [MessageHandler(Filters.regex('^(Return to Main Menu)$') & ~Filters.command, main_menu)], # Returns to Main Menu.
            FAVORITE_STATION_1: [MessageHandler(Filters.text(station_name_list) & ~Filters.command, favorite_station_2_request)],
            FAVORITE_STATION_2: [MessageHandler(Filters.text(station_name_list) & ~Filters.command, favorite_station_3_request)],
            FAVORITE_STATION_3: [MessageHandler(Filters.text(station_name_list) & ~Filters.command, favorite_station_4_request)],
            FAVORITE_STATION_4: [MessageHandler(Filters.text(station_name_list) & ~Filters.command, favorite_station_5_request)],
            FAVORITE_STATION_5: [MessageHandler(Filters.text(station_name_list) & ~Filters.command, favorite_station_done)],
        },
        fallbacks = [CommandHandler('cancel', cancel)],
        
    )

    dispatcher.add_handler(conv_handler)
    
    # Adds error handler
    dispatcher.add_error_handler(error_handler)

    # Starts the Bot.
    updater.start_polling()

    # Runs the bot until Ctrl-C is pressed or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
             # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

# Actuall start of the program, have no ide how it works.
if __name__ == '__main__':
    main()

# Future updates
# Set up favorite table picker