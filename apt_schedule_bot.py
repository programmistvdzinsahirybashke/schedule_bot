import calendar
import datetime
import time
import pendulum
import requests
import telebot
import sqlite3
import threading
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from telebot import types
from webdriver_manager.chrome import ChromeDriverManager
import configure
from telebot import custom_filters


def start_bot():
    global MY_GROUP
    global HELP_TEXT
    global GROUP_ID
    global CHAT_BY_DATETIME
    CHAT_BY_DATETIME = {}
    GROUP_ID = {
        'АВ221': 957,
        'АМ221': 950,
        'АМ223': 950,
        'АМ222': 949,
        'БУР221': 961,
        'БУР222': 962,
        'БУХ221': 947,
        'БУХ222': 947,
        'ГФ221': 960,
        'ИС221': 953,
        'СТ221': 955,
        'СТ222': 956,
        'СТ223': 954,
        'ИС222': 952,
        'ИС223': 971,
        'МЕХ221': 959,
        'АВ211': 827,
        'АМ211': 828,
        'АМ212': 829,
        'БУР211': 830,
        'БУР212': 831,
        'БУХ211': 832,
        'ГФ211': 833,
        'ИС211': 834,
        'ИС212': 835,
        'ИС213': 727,
        'МЕХ211': 836,
        'СА211': 846,
        'СА212': 846,
        'СМ211': 837,
        'СТ211': 838,
        'СТ212': 839,
        'СТ213': 840,
        'ЭКС211': 841,
        'ЭКС213': 841,
        'ЭКС212': 842,
        'ЭЛ211': 844,
        'ЭЛ212': 844,
        'ЭЛ1212': 845,
        'АВ201': 702,
        'АВ202': 702,
        'АД201': 698,
        'АМ201': 695,
        'АМ202': 694,
        'БУР201': 687,
        'БУР202': 688,
        'БУХ201': 692,
        'ГФ201': 689,
        'ИС201': 697,
        'ИС202': 696,
        'ИС203': 697,
        'МЕХ201': 690,
        'СМ201': 693,
        'СТ201': 701,
        'СТ202': 700,
        'СТ203': 699,
        'ЭКС201': 684,
        'ЭКС204': 684,
        'ЭКС202': 685,
        'ЭКС1203': 704,
        'ЭЛ201': 691,
        'ЭЛ202': 691,
        'ЭЛ1202': 703,
        'АВ191': 620,
        'АВ192': 620,
        'АД191': 548,
        'АМ191': 628,
        'АМ192': 629,
        'БУР191': 622,
        'БУР192': 625,
        'БУР193': 625,
        'ГФ191': 626,
        'ИС191': 547,
        'ИС192': 619,
        'МЕХ191': 549,
        'СМ191': 627,
        'CТ194': 544,
        'CТ191': 544,
        'СТ192': 617,
        'СТ193': 618,
        'ЭКС191': 621,
        'ЭКС192': 624,
        'ЭКС193': 631,
        'ЭКС195': 631,
        'ЭЛ191': 546,
        'ЭЛ192': 546,
    }
    HELP_TEXT = """Привет, это бот в котором ты можешь увидеть расписание своей группы в АПТ.
Сначала нужно указать свою группу, нажав кнопку "Изменить группу📎" и ввести группу без лишних букв и дефисов, например ИС211, МЕХ201.
Расписание на сегодня/завтра🗓 выводит расписание в виде текста.
Расписание на сегодня/завтра📱 выводит расписание в виде картинки.
Кнопка "Расписание на понедельник📅" работает только в субботу и воскресенье и выводит расписание на понедельник в виде текста, если расписание вышло.
Нажав кнопку "Изменить группу📎" еще раз, ты можешь поменять свою группу.
Нажав кнопку "Профиль📌" ты можешь увидеть свой id и группу.
Чтобы увидеть это сообщение еще раз, нажми кнопку "Помощь❓"
Может понадобиться несколько секунд для получения расписания!"""

    bot = telebot.TeleBot(configure.config["token"], threaded=True, num_threads=300)
    bot.add_custom_filter(custom_filters.TextMatchFilter())
    bot.add_custom_filter(custom_filters.ChatFilter())

    conn = sqlite3.connect('db_main.db', check_same_thread=False)
    cursor = conn.cursor()

    def format_result(result):
        result = result.split("Консультации преподавателей")[0]
        result = result.split("График учебного процесса")[0]
        result = result.replace("\n\n\n\n\n\n", " ")
        result = result.replace("\n\n\n\n", "\n")
        result = result.replace("\n\n\n", "\n")
        result = result.replace("\n\n", "\n")
        result = result.replace("0730 - 0850", "\n7:30 - 8:50\n")
        result = result.replace("0855 - 1015", "\n8:55 - 10:15\n")
        result = result.replace("1040 - 1200", "\n10:40 - 12:00\n")
        result = result.replace("1210 - 1330", "\n12:10 - 13:30\n")
        result = result.replace("1340 - 1500", "\n13:40 - 15:00\n")
        result = result.replace("1520 - 1640", "\n15:20 - 16:40\n")
        result = result.replace("0730 - 0840", "\n7:30 - 8:40\n")
        result = result.replace("0845 - 0955", "\n8:45 - 9:55\n")
        result = result.replace("1000 - 1110", "\n10:00 - 11:10\n")
        result = result.replace("1210 - 1330", "\n12:10 - 13:30\n")
        result = result.replace("1340 - 1500", "\n13:40 - 15:00\n")
        return result

    @bot.message_handler(commands=["start"])
    def start(message, res=False):
        current_time = datetime.datetime.now()
        CHAT_BY_DATETIME[message.chat.id] = current_time
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        button1 = types.KeyboardButton("Изменить группу📎")
        button2 = types.KeyboardButton("Помощь❓")

        markup.add(button1, button2)

        def db_table_val(user_id, nickname, username):
            register_user = "INSERT OR IGNORE INTO test (user_id, nickname, username) VALUES (?, ?, ?)"
            columns = (user_id, nickname, username)
            cursor.execute(register_user, columns)
            conn.commit()

        us_id = message.from_user.id
        us_name = message.from_user.first_name
        username = message.from_user.username

        db_table_val(user_id=us_id, nickname=us_name, username=username)
        bot.reply_to(message, HELP_TEXT, reply_markup=markup)
        bot.send_photo(message.chat.id, open("screenshots/apt_bot.jpg", 'rb'))

    @bot.message_handler(text=['Расписание на сегодня 🗓'])
    def get_text_today(message):
        need_seconds = 5
        current_time = datetime.datetime.now()
        last_datetime = CHAT_BY_DATETIME.get(message.chat.id)
        if not last_datetime:
            CHAT_BY_DATETIME[message.chat.id] = current_time
        else:
            delta_seconds = (current_time - last_datetime).total_seconds()
            seconds_left = int(need_seconds - delta_seconds)

            if seconds_left > 0:
                bot.reply_to(message, f'Подождите {seconds_left} секунд перед выполнение этой команды')
            else:
                CHAT_BY_DATETIME[message.chat.id] = current_time
                def get_result_today(user_id: int):
                    cursor.execute("SELECT user_group FROM test WHERE user_id = ?", (user_id,))
                    group = cursor.fetchone()

                    if group:
                        my_group = group[0]

                        today = pendulum.today('Europe/Moscow').format('YYYY-MM-DD')
                        response_today = requests.get(f"https://almetpt.ru/2020/site/schedule/group/{my_group}/{today}")
                        soup = BeautifulSoup(response_today.text, "lxml")
                        schedule = soup.find("div", class_="container")

                        if 'года не опубликовано' in schedule.text:
                            return "Расписания на сегодня нет."
                        else:
                            for item in schedule:
                                if item == "":
                                    item.replace("", "1")

                            result = f'{schedule.text}'
                            return format_result(result)

                bot.reply_to(message, get_result_today(message.from_user.id))

    @bot.message_handler(text=['Расписание на завтра 🗓'])
    def get_text_tomorrow(message):
        need_seconds = 5
        current_time = datetime.datetime.now()
        last_datetime = CHAT_BY_DATETIME.get(message.chat.id)
        if not last_datetime:
            CHAT_BY_DATETIME[message.chat.id] = current_time
        else:
            delta_seconds = (current_time - last_datetime).total_seconds()
            seconds_left = int(need_seconds - delta_seconds)

            if seconds_left > 0:
                bot.reply_to(message, f'Подождите {seconds_left} секунд перед выполнение этой команды')
            else:
                CHAT_BY_DATETIME[message.chat.id] = current_time
                def get_result_tomorrow(user_id: int):
                    cursor.execute("SELECT user_group FROM test WHERE user_id = ?", (user_id,))
                    group = cursor.fetchone()

                    if group:
                        my_group = group[0]

                        tomorrow = pendulum.tomorrow('Europe/Moscow').format('YYYY-MM-DD')
                        response_check_tomorrow = requests.get(
                            f'https://almetpt.ru/2020/site/schedule/group/{my_group}/{tomorrow}')
                        soup = BeautifulSoup(response_check_tomorrow.text, 'lxml')
                        schedule = soup.find("div", class_="container")

                        if 'года не опубликовано' in schedule.text:
                            return "Расписание на завтра еще не вышло!"
                        else:
                            for item in schedule:
                                if item == "":
                                    item.replace("", "1")
                            result = f'{schedule.text}'
                            return format_result(result)

                bot.reply_to(message, get_result_tomorrow(message.from_user.id))

    @bot.message_handler(text=['Расписание на сегодня 📱'])
    def get_screen_today(message):
        need_seconds = 8
        current_time = datetime.datetime.now()
        last_datetime = CHAT_BY_DATETIME.get(message.chat.id)
        if not last_datetime:
            CHAT_BY_DATETIME[message.chat.id] = current_time
        else:
            delta_seconds = (current_time - last_datetime).total_seconds()
            seconds_left = int(need_seconds - delta_seconds)

            if seconds_left > 0:
                bot.reply_to(message, f'Подождите {seconds_left} секунд перед выполнение этой команды')
            else:
                CHAT_BY_DATETIME[message.chat.id] = current_time
                def get_screenshot_today(user_id: int):
                    cursor.execute("SELECT user_group FROM test WHERE user_id = ?", (user_id,))
                    group = cursor.fetchone()

                    if group:
                        my_group = group[0]

                    if not last_datetime:
                        CHAT_BY_DATETIME[message.chat.id] = current_time
                    else:
                        delta_seconds = (current_time - last_datetime).total_seconds()
                        seconds_left = int(need_seconds - delta_seconds)

                        if seconds_left > 0:
                            bot.reply_to(message, f'Подождите {seconds_left} секунд перед выполнение этой команды')
                        else:
                            CHAT_BY_DATETIME[message.chat.id] = current_time
                            today = pendulum.today('Europe/Moscow').format('YYYY-MM-DD')
                            response_today = requests.get(f"https://almetpt.ru/2020/site/schedule/group/{my_group}/{today}")
                            soup = BeautifulSoup(response_today.text, "lxml")
                            schedule = soup.find("div", class_="container")

                            if 'года не опубликовано' in schedule.text:
                                return "Расписания на сегодня нет."
                            else:
                                options = webdriver.ChromeOptions()
                                options.add_argument('--no-sandbox')
                                options.add_argument("--disable-dev-shm-usage")
                                options.add_argument("--headless")
                                driver = webdriver.Chrome(
                                    chrome_options=options,
                                    service=Service(ChromeDriverManager().install())
                                )

                                today = pendulum.today('Europe/Moscow').format('YYYY-MM-DD')
                                url = f"https://almetpt.ru/2020/site/schedule/group/{my_group}/{today}"
                                try:
                                    driver.set_window_size(850, 1050)
                                    driver.get(url=url)
                                    driver.implicitly_wait(60)
                                    screen_id = message.from_user.id
                                    driver.get_screenshot_as_file(f"screenshots/{screen_id}_today.png")
                                except Exception as ex:
                                    print(ex)
                                finally:
                                    driver.close()
                                    driver.quit()
                                return f"screenshots/{screen_id}_today.png"

                screen = get_screenshot_today(message.from_user.id)
                if screen == "Расписания на сегодня нет.":
                    bot.reply_to(message, "Расписания на сегодня нет.")
                else:
                    bot.send_photo(message.chat.id, open(screen, 'rb'))

    @bot.message_handler(text=['Расписание на завтра 📱'])
    def get_screen_tomorrow(message):
        need_seconds = 8
        current_time = datetime.datetime.now()
        last_datetime = CHAT_BY_DATETIME.get(message.chat.id)
        if not last_datetime:
            CHAT_BY_DATETIME[message.chat.id] = current_time
        else:
            delta_seconds = (current_time - last_datetime).total_seconds()
            seconds_left = int(need_seconds - delta_seconds)

            if seconds_left > 0:
                bot.reply_to(message, f'Подождите {seconds_left} секунд перед выполнение этой команды')
            else:
                CHAT_BY_DATETIME[message.chat.id] = current_time
                def get_screenshot_tomorrow(user_id: int):
                    cursor.execute("SELECT user_group FROM test WHERE user_id = ?", (user_id,))
                    group = cursor.fetchone()

                    if group:
                        my_group = group[0]

                        tomorrow = pendulum.tomorrow('Europe/Moscow').format('YYYY-MM-DD')
                        response_check_tomorrow = requests.get(f'https://almetpt.ru/2020/site/schedule/group/{my_group}/{tomorrow}')
                        soup = BeautifulSoup(response_check_tomorrow.text, 'lxml')
                        schedule = soup.find("div", class_="container")

                        if 'года не опубликовано' in schedule.text:
                            return "Расписание на завтра еще не вышло!"
                        else:
                            options = webdriver.ChromeOptions()
                            options.add_argument("--headless")
                            options.add_argument('--no-sandbox')
                            options.add_argument("--disable-dev-shm-usage")
                            options.add_argument("--remote-debugging-port=9222")
                            driver = webdriver.Chrome(
                                chrome_options=options,
                                service=Service(ChromeDriverManager().install())
                            )

                            tomorrow = pendulum.tomorrow('Europe/Moscow').format('YYYY-MM-DD')
                            url = f'https://almetpt.ru/2020/site/schedule/group/{my_group}/{tomorrow}'
                            try:
                                driver.set_window_size(850, 1050)
                                driver.get(url=url)
                                driver.implicitly_wait(60)
                                screen_id = message.from_user.id
                                driver.get_screenshot_as_file(f"screenshots/{screen_id}_tomorrow.png")
                            except Exception as ex:
                                print(ex)
                            finally:
                                driver.close()
                                driver.quit()
                            return f"screenshots/{screen_id}_tomorrow.png"

                screen = get_screenshot_tomorrow(message.from_user.id)
                if screen == "Расписание на завтра еще не вышло!":
                    bot.reply_to(message, "Расписание на завтра еще не вышло!")
                else:
                    bot.send_photo(message.chat.id, open(screen, 'rb'))

    @bot.message_handler(text=['Изменить группу📎'])
    def request_group(message):
        need_seconds = 5
        current_time = datetime.datetime.now()
        last_datetime = CHAT_BY_DATETIME.get(message.chat.id)

        if not last_datetime:
            CHAT_BY_DATETIME[message.chat.id] = current_time
        else:
            delta_seconds = (current_time - last_datetime).total_seconds()
            seconds_left = int(need_seconds - delta_seconds)

            if seconds_left > 0:
                bot.reply_to(message, f'Подождите {seconds_left} секунд перед выполнение этой команды')
            else:
                CHAT_BY_DATETIME[message.chat.id] = current_time
                def update_group_val(user_group: str):
                    us_id = message.from_user.id
                    sqlite_update_query = 'UPDATE test SET user_group = ? WHERE user_id = ?'
                    column_values = (user_group, us_id)
                    cursor.execute(sqlite_update_query, column_values)
                    conn.commit()

                def update_group(message):
                    GROUP = message.text.upper()

                    if GROUP not in GROUP_ID:
                        def input_group(message):
                            msg = bot.reply_to(message, "Введите группу (без лишних букв и символов, например ИС211")
                            bot.register_next_step_handler(msg, active)

                        def active():
                            print(GROUP)

                        bot.reply_to(message, f"Группа введена неверно, нажмите кнопку снова и введите "
                                              f"группу в правильном формате!\nВы ввели: {GROUP}")
                        GROUP = message.text
                        return
                    else:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                        button1 = types.KeyboardButton("Расписание на сегодня 🗓")
                        button2 = types.KeyboardButton("Расписание на завтра 🗓")
                        button3 = types.KeyboardButton("Расписание на сегодня 📱")
                        button4 = types.KeyboardButton("Расписание на завтра 📱")
                        button5 = types.KeyboardButton("Изменить группу📎")
                        button6 = types.KeyboardButton("Расписание на понедельник📅")
                        button7 = types.KeyboardButton("Профиль📌")
                        button8 = types.KeyboardButton("Помощь❓")

                        markup.add(button1, button2)
                        markup.add(button3, button4)
                        markup.add(button5, button6)
                        markup.add(button7, button8)

                        bot.reply_to(message, f"Ваша группа: {GROUP}", reply_markup=markup)

                    MY_GROUP = GROUP_ID[GROUP]
                    update_group_val(user_group=MY_GROUP)

                get_group1 = bot.reply_to(message, "Введите группу (без лишних букв и символов, например ИС211):")
                bot.register_next_step_handler(get_group1, update_group)

    @bot.message_handler(text=['Расписание на понедельник📅'])
    def monday(message):
        need_seconds = 5
        current_time = datetime.datetime.now()
        last_datetime = CHAT_BY_DATETIME.get(message.chat.id)

        if not last_datetime:
            CHAT_BY_DATETIME[message.chat.id] = current_time
        else:
            delta_seconds = (current_time - last_datetime).total_seconds()
            seconds_left = int(need_seconds - delta_seconds)

            if seconds_left > 0:
                bot.reply_to(message, f'Подождите {seconds_left} секунд перед выполнение этой команды')
            else:
                CHAT_BY_DATETIME[message.chat.id] = current_time

                def check_monday(user_id: int):
                    cursor.execute("SELECT user_group FROM test WHERE user_id = ?", (user_id,))
                    group = cursor.fetchone()

                    if group:
                        my_group = group[0]

                    today = datetime.date.today()
                    if calendar.day_name[today.weekday()] == 'Saturday':
                        monday = today + datetime.timedelta(days=2)
                        response_check_tomorrow = requests.get(
                            f'https://almetpt.ru/2020/site/schedule/group/{my_group}/{monday}')
                        soup = BeautifulSoup(response_check_tomorrow.text, 'lxml')
                        schedule = soup.find("div", class_="container")

                        if 'года не опубликовано' in schedule.text:
                            return "Расписание на понедельник еще не вышло!"
                        else:
                            options = webdriver.ChromeOptions()
                            options.add_argument("--headless")
                            options.add_argument('--no-sandbox')
                            options.add_argument("--disable-dev-shm-usage")
                            options.add_argument("--remote-debugging-port=9222")
                            driver = webdriver.Chrome(
                                chrome_options=options,
                                service=Service(ChromeDriverManager().install())
                            )
                            url = f'https://almetpt.ru/2020/site/schedule/group/{my_group}/{monday}'
                            try:
                                driver.set_window_size(850, 1050)
                                driver.get(url=url)
                                driver.implicitly_wait(60)
                                screen_id = message.from_user.id
                                driver.get_screenshot_as_file(f"screenshots/{screen_id}_monday.png")
                            except Exception as ex:
                                print(ex)
                            finally:
                                driver.close()
                                driver.quit()
                            return f"screenshots/{screen_id}_monday.png"

                    elif calendar.day_name[today.weekday()] == 'Sunday':
                        monday = today + datetime.timedelta(days=1)
                        response_check_tomorrow = requests.get(
                            f'https://almetpt.ru/2020/site/schedule/group/{my_group}/{monday}')
                        soup = BeautifulSoup(response_check_tomorrow.text, 'lxml')
                        schedule = soup.find("div", class_="container")

                        if 'года не опубликовано' in schedule.text:
                            return "Расписание на понедельник еще не вышло!"
                        else:
                            options = webdriver.ChromeOptions()
                            options.add_argument("--headless")
                            options.add_argument('--no-sandbox')
                            options.add_argument("--disable-dev-shm-usage")
                            options.add_argument("--remote-debugging-port=9222")
                            driver = webdriver.Chrome(
                                chrome_options=options,
                                service=Service(ChromeDriverManager().install())
                            )
                            url = f'https://almetpt.ru/2020/site/schedule/group/{my_group}/{monday}'
                            try:
                                driver.set_window_size(850, 1050)
                                driver.get(url=url)
                                driver.implicitly_wait(60)
                                screen_id = message.from_user.id
                                driver.get_screenshot_as_file(f"screenshots/{screen_id}_monday.png")
                            except Exception as ex:
                                print(ex)
                            finally:
                                driver.close()
                                driver.quit()
                            return f"screenshots/{screen_id}_monday.png"

                screen = check_monday(message.from_user.id)
                if screen == "Расписание на завтра еще не вышло!":
                    bot.reply_to(message, "Расписание на завтра еще не вышло!")
                else:
                    bot.send_photo(message.chat.id, open(screen, 'rb'))

    @bot.message_handler(text=['Профиль📌'])
    def profile(message):
        need_seconds = 5
        current_time = datetime.datetime.now()
        last_datetime = CHAT_BY_DATETIME.get(message.chat.id)
        if not last_datetime:
            CHAT_BY_DATETIME[message.chat.id] = current_time
        else:
            delta_seconds = (current_time - last_datetime).total_seconds()
            seconds_left = int(need_seconds - delta_seconds)

            if seconds_left > 0:
                bot.reply_to(message, f'Подождите {seconds_left} секунд перед выполнение этой команды')
            else:
                CHAT_BY_DATETIME[message.chat.id] = current_time

                def show_profile(user_id: int):
                    cursor.execute("SELECT user_group FROM test WHERE user_id = ?", (user_id,))
                    group = cursor.fetchone()
                    cursor.execute("SELECT nickname FROM test WHERE user_id = ?", (user_id,))
                    nickname = cursor.fetchone()

                    if nickname:
                        result = nickname[0]

                    if group:
                        my_group = group[0]
                        switch_group_name = {v: k for k, v in GROUP_ID.items()}
                        group_name = switch_group_name[my_group]

                        return f"Ваш ник: {result}\n➖➖➖➖➖➖➖\nВаша группа: {group_name}\n➖➖➖➖➖➖➖\nВаш id: {message.from_user.id}"

                bot.reply_to(message, show_profile(message.from_user.id))

    @bot.message_handler(text=['Помощь❓'])
    def get_help(message):
        need_seconds = 5
        current_time = datetime.datetime.now()
        last_datetime = CHAT_BY_DATETIME.get(message.chat.id)
        if not last_datetime:
            CHAT_BY_DATETIME[message.chat.id] = current_time
        else:
            delta_seconds = (current_time - last_datetime).total_seconds()
            seconds_left = int(need_seconds - delta_seconds)

            if seconds_left > 0:
                bot.reply_to(message, f'Подождите {seconds_left} секунд перед выполнение этой команды')
            else:
                CHAT_BY_DATETIME[message.chat.id] = current_time
                bot.reply_to(message, HELP_TEXT)

    @bot.message_handler(chat_id=[702999620], commands=['admin_check'])
    def admin_rep(message):
        bot.send_message(message.chat.id, "Вам разрешено использовать эту команду.")

    @bot.message_handler(commands=['admin_check'])
    def not_admin(message):
        bot.send_message(message.chat.id, "Вам не разрешено использовать эту команду.")

    bot.polling(none_stop=True, skip_pending=True)


if __name__ == "__main__":
    while True:
        try:
            threading.Thread(target=start_bot()).start()
        except Exception as e:
            telebot.logger.error(e)
            time.sleep(2)
