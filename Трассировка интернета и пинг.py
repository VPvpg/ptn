#пингует на сайт гугла.
#сразу выдаст тайминг, потом жди - выдаст трассировку.

import ping3
import subprocess

adress = "www.google.com" #можно подставить свой (любой) адресс для трассировки
print(adress)


def ping(host):
    try:
        response_time = ping3.ping(host)
        if response_time is not None:
            print(f"Ping successful! Response time: {response_time} ms")
        else:
            print("Ping failed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        

def trace_route(hostname):
    try:
        result = subprocess.check_output(["tracert", hostname], shell=True, universal_newlines=True)
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Пример использования
ping(adress)
trace_route(adress)


input("Нажмите Enter, чтобы закрыть программу...")