import requests
import xml.etree.ElementTree as ET

class CurrencyFetcher:
    def __init__(self):
        self.url = 'https://www.cbr.ru/scripts/XML_daily.asp'
        self.currency_data = {}

    def update_currency_data(self):
        try:
            response = requests.get(self.url)
            response.encoding = 'windows-1251'  # Устанавливаем правильную кодировку
            
            if response.status_code == 200:
                tree = ET.ElementTree(ET.fromstring(response.text))
                root = tree.getroot()
                
                self.currency_data = {}
                for currency in root.findall('Valute'):
                    char_code = currency.find('CharCode').text
                    nominal = currency.find('Nominal').text
                    value = currency.find('Value').text
                    name = currency.find('Name').text
                    self.currency_data[char_code] = f'{nominal} {name} = {value} RUB'
                
                print("Обновленные данные:", self.currency_data)
            else:
                print(f"Ошибка при получении данных: {response.status_code}")
                raise Exception(f"Ошибка сервера: код {response.status_code}")
        
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            raise Exception("Ошибка при обновлении данных: " + str(e))

    def get_currency_rate(self, currency_code):
        return self.currency_data.get(currency_code, 'Currency not found')

    def get_all_currencies(self):
        if not self.currency_data:
            return 'Данные о валюте отсутствуют. Пожалуйста, обновите курсы.'
        
        all_currencies = "Доступные курсы валют:\n\n"
        for code, rate in self.currency_data.items():
            all_currencies += f"{code}: {rate}\n"
        
        return all_currencies
