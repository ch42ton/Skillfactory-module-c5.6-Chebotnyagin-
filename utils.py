import requests
import json
from config import APIKEY, VALUES

#классы исключений
class ConvertionException(Exception):
    pass

class ServerException(Exception):
    pass



#Конвертер
class Converter:

    def __init__(self, text):

#дополнительная функция для запроса и парсинга данных
        def _getter(link):
            x = requests.get(link)
            x = json.loads(x.content)
            try:
                return x['rates']
#тут же ловится ошибка сервера
            except Exception:
                raise ServerException('ошибка на сервере')

        self.listofkeys = list(text.split(' '))
        self.listofvalues = []
        self.cofficient = float()
#на этом этапе определяется действие и ловится ошибка ввода 

#показать стоимости валют
        if 'convert' not in self.listofkeys:
            for i in self.listofkeys:
                if i.lower() not in list(VALUES.keys()):
                    raise ConvertionException('неверный ввод')
                else: self.listofvalues.append(VALUES[i])
#конверсия
        else:
            self.listofkeys.remove('convert')
            if len(self.listofkeys) == 2 and self.listofkeys[0].lower() in list(VALUES.keys()):
                try:
                    self.cofficient = float(self.listofkeys[1])
                    self.listofvalues.append(VALUES[self.listofkeys[0]])
                    self.listofkeys.pop()
                except Exception:
                    raise ConvertionException('неверный ввод')
            else:
                raise ConvertionException('неверный ввод')
                    
        self.vals = ','.join(self.listofvalues) 
        self.link = str(f'http://api.exchangeratesapi.io/v1/latest?access_key={APIKEY}&symbols={self.vals}')
        self.content = _getter(self.link)

#геттеры чтобы был феншуй
    def get_content(self):
        return self.content

    def get_keys(self):
        return self.listofkeys

    def get_cofficient(self):
        return self.cofficient

