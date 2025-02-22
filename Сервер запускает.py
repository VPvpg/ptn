from flask import Flask  # Импортируем класс Flask из библиотеки flask

app = Flask(__name__)  # Создаем экземпляр приложения Flask

@app.route('/')  # Определяем маршрут для корневого URL
def hello():  # Функция, которая будет выполнена при обращении к маршруту
    return "Слава яйцам - я запустил СЕРВЕР!"  # Возвращаем строку "Hello, World!"

#if __name__ == '__main__':  # Проверяем, запущен ли файл напрямую
#    app.run(debug=True)  # Запускаем сервер в режиме отладки
    
if __name__ == '__main__': # запуск без отладки
    app.run(port=8080)    
    
    
"""
https://poe.com/s/nVj2a8tal62GUTh6DuzQ
https://poe.com/s/tyUDAB4hw6JCrd2woLyh
https://poe.com/s/MChpj4BTAhLMexuFRZUT
порты
https://poe.com/s/DBPu21TfAVi7JEahlT5K

На порту 5000 - НЕ ЗАПУСКАЕТ в браузере :(


Это сервер.

В браузере набери

http://127.0.0.1:8080/



=== Дальше не нужное..

app.run(debug=True, port=8080)

"""