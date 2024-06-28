import telebot
from telebot import types
from modules.currency_fetcher import CurrencyFetcher
import config

class CurrencyBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.fetcher = CurrencyFetcher()

        # Инициализация команд и обработчиков
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(func=lambda message: True)(self.handle_message)

    def create_main_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        update_button = types.KeyboardButton('Обновить курсы')
        list_button = types.KeyboardButton('Список валют')
        all_currencies_button = types.KeyboardButton('Все валюты')
        keyboard.add(update_button, list_button, all_currencies_button)
        return keyboard

    def create_currency_list_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        currencies = ['USD', 'EUR', 'GBP', 'CNY', 'JPY', 'Назад']
        buttons = [types.KeyboardButton(currency) for currency in currencies]
        keyboard.add(*buttons)
        return keyboard

    def send_welcome(self, message):
        self.bot.reply_to(message, "Привет! Нажми 'Обновить курсы' для получения свежих данных, 'Список валют' для выбора валюты или 'Все валюты' для просмотра всех доступных курсов.", reply_markup=self.create_main_keyboard())

    def handle_message(self, message):
        if message.text == 'Обновить курсы':
            try:
                self.fetcher.update_currency_data()
                self.bot.reply_to(message, "Курсы валют обновлены.", reply_markup=self.create_main_keyboard())
            except Exception as e:
                self.bot.reply_to(message, f"Ошибка при обновлении данных: {e}", reply_markup=self.create_main_keyboard())

        elif message.text == 'Список валют':
            self.bot.reply_to(message, "Выберите валюту из списка:", reply_markup=self.create_currency_list_keyboard())
        
        elif message.text == 'Все валюты':
            all_currencies = self.fetcher.get_all_currencies()
            self.bot.reply_to(message, all_currencies, reply_markup=self.create_main_keyboard())

        elif message.text == 'Назад':
            self.bot.reply_to(message, "Возвращаемся в главное меню.", reply_markup=self.create_main_keyboard())

        else:
            currency_code = message.text.upper()
            rate = self.fetcher.get_currency_rate(currency_code)
            
            if rate == 'Currency not found':
                self.bot.reply_to(message, "Информация о валюте не найдена. Обновляем курсы, пожалуйста подождите...")
                try:
                    self.fetcher.update_currency_data()
                    rate = self.fetcher.get_currency_rate(currency_code)
                    if rate == 'Currency not found':
                        self.bot.reply_to(message, "Валюта не найдена. Выберите валюту из списка:", reply_markup=self.create_currency_list_keyboard())
                    else:
                        self.bot.reply_to(message, rate, reply_markup=self.create_main_keyboard())
                except Exception as e:
                    self.bot.reply_to(message, f"Ошибка при обновлении данных: {e}", reply_markup=self.create_main_keyboard())
            else:
                self.bot.reply_to(message, rate, reply_markup=self.create_main_keyboard())

    def run(self):
        print("Бот запущен и работает...")
        self.bot.polling()

# Инициализация и запуск бота
if __name__ == '__main__':
    currency_bot = CurrencyBot(config.API_TOKEN)
    currency_bot.run()


