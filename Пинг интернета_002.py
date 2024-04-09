#https://poe.com/s/JlqkiRJUm5ZrreSW0G5m
# библиотека speedtest-cli

import speedtest

print("Пингуем.")

def test_internet_speed():
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 10**6  # Скорость загрузки в Мбит/с
        upload_speed = st.upload() / 10**6  # Скорость отдачи в Мбит/с
        print(f'Скорость загрузки: {download_speed:.2f} Мбит/с')
        print(f'Скорость отдачи: {upload_speed:.2f} Мбит/с')
    except Exception as e:
        print(f'Ошибка при тестировании скорости интернета: {e}')

# Запускаем тестирование скорости интернета
test_internet_speed()

# Добавляем код, чтобы окно не закрывалось сразу после выполнения программы
input("Нажмите Enter, чтобы закрыть окно...")