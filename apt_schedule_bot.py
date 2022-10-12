import configure
import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types
import pendulum
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



def main():
    bot = telebot.TeleBot(configure.config["token"])

    @bot.message_handler(commands=["start"])
    def start(m, res=False):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1 = types.KeyboardButton("Расписание на сегодня 🗓")
        item2 = types.KeyboardButton("Расписание на завтра 🗓")
        item3 = types.KeyboardButton("Расписание на сегодня 📱")
        item4 = types.KeyboardButton("Расписание на завтра 📱")
        item5 = types.KeyboardButton("О боте❓")

        markup.add(item1, item2)
        markup.add(item3, item4)
        markup.add(item5)

        bot.send_message(m.chat.id, "Нажми кнопку чтобы увидеть расписание", reply_markup=markup)

    def get_result_today():
        today = pendulum.today('Europe/Moscow').format('YYYY-MM-DD')
        response_today = requests.get(f'https://almetpt.ru/2020/site/schedule/group/834/{today}')

        soup = BeautifulSoup(response_today.text, 'lxml')
        schedule = soup.find('div', class_="container")

        for item in schedule:
            if item == "":
                item.replace("", "1")
        result = f'{schedule.text}'
        result = result.replace("\n\n\n\n\n\n", " ")
        result = result.replace("\n\n\n\n", "\n")
        result = result.replace("\n\n\n", "\n")
        result = result.replace("\n\n", "\n")
        result = result.replace("0730 - 0850", "\n7:30 - 8:50\n")
        result = result.replace("0855 - 1015", "\n8:55 - 10:15\n")
        result = result.replace("1040 - 1200", "\n10:40 - 12:00\n")
        result = result.replace("1210 - 1330", "\n12:10 - 13:30\n")
        result = result.replace("1340 - 1500", "\n13:40 - 15:00\n")
        count = 0
        x = count - 2120
        result = result[:x]
        for i in result:
            count += 1
        print(count)
        answer = result
        return answer

    def get_result_tomorrow():
        tomorrow = pendulum.tomorrow('Europe/Moscow').format('YYYY-MM-DD')
        response_today = requests.get(f'https://almetpt.ru/2020/site/schedule/group/834/{tomorrow}')

        soup = BeautifulSoup(response_today.text, 'lxml')
        date = soup.find('div', class_="header3")
        schedule = soup.find('div', class_="container")

        for item in schedule:
            if item == "":
                item.replace("", "1")
        result = f'{schedule.text}'

        result = result.replace("\n\n\n\n\n\n", " ")
        result = result.replace("\n\n\n\n", "\n")
        result = result.replace("\n\n\n", "\n")
        result = result.replace("\n\n", "\n")
        result = result.replace("0730 - 0850", "\n7:30 - 8:50\n")
        result = result.replace("0855 - 1015", "\n8:55 - 10:15\n")
        result = result.replace("1040 - 1200", "\n10:40 - 12:00\n")
        result = result.replace("1210 - 1330", "\n12:10 - 13:30\n")
        result = result.replace("1340 - 1500", "\n13:40 - 15:00\n")
        count = 0
        x = count - 2120
        result = result[:x]
        for i in result:
            count += 1
        print(count)
        answer = result
        return answer

    def get_screenshot_today():
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        driver = webdriver.Chrome(
            options=options,
            service=Service(ChromeDriverManager().install())
        )

        today = pendulum.today('Europe/Moscow').format('YYYY-MM-DD')
        url = f'https://almetpt.ru/2020/site/schedule/group/834/{today}'
        try:
            driver.set_window_size(850, 1050)
            driver.get(url=url)
            driver.implicitly_wait(3)
            driver.get_screenshot_as_file("screenshots/today.png")
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
        return "screenshots/today.png"

    def get_screenshot_tomorrow():
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        driver = webdriver.Chrome(
            options=options,
            service=Service(ChromeDriverManager().install())
        )

        tomorrow = pendulum.tomorrow('Europe/Moscow').format('YYYY-MM-DD')
        url = f'https://almetpt.ru/2020/site/schedule/group/834/{tomorrow}'
        try:
            driver.set_window_size(850, 1050)
            driver.get(url=url)
            driver.implicitly_wait(3)
            driver.get_screenshot_as_file("screenshots/tomorrow.png")
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
        return "screenshots/tomorrow.png"

    def send_today_text():
        return get_result_today()

    def send_tomorrow_text():
        return get_result_tomorrow()

    def send_today_screenshot():
        get_screenshot_today()

    def send_tomorrow_screenshot():
        return get_screenshot_tomorrow()

    def bot_reply():
        @bot.message_handler(content_types=["text"])
        def handle_text(message):
            if message.text.strip() == "Расписание на сегодня 🗓":
                answer = send_today_text()
                bot.send_message(message.chat.id, answer)
            if message.text.strip() == "Расписание на завтра 🗓":
                answer = send_tomorrow_text()
                bot.send_message(message.chat.id, answer)
            if message.text.strip() == "Расписание на сегодня 📱":
                send_today_screenshot()
                bot.send_photo(message.chat.id, open("screenshots/today.png", 'rb'))
            if message.text.strip() == "Расписание на завтра 📱":
                send_tomorrow_screenshot()
                bot.send_photo(message.chat.id, open("screenshots/tomorrow.png", 'rb'))
            if message.text.strip() == "О боте❓":
                bot.send_message(message.chat.id, 'Это бот в котором ты можешь увидеть расписание своей группы в '
                                                  'АПТ.\nРасписание на сегодня 🗓 выводит расписание в виде '
                                                  'текста.\nРасписание на сегодня 📱 выводит расписание в виде '
                                                  'картинки.\nМожет понадобиться несколько секунд для получения '
                                                  'расписания! ')
            if message.text.strip() != "Расписание на сегодня 🗓" and message.text.strip() != "Расписание на " \
                                                                                              "сегодня " \
                                                                                              "📱" and \
                    message.text.strip() != "Расписание на завтра 🗓" and message.text.strip() != "Расписание " \
                                                                                                  "на завтра " \
                                                                                                  "📱" \
                    and message.text.strip() != "О боте❓":
                bot.send_message(message.chat.id, 'Неизвестная команда')

    bot_reply()

    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
