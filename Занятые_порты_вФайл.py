import psutil

def get_used_ports():
    # Получаем все соединения
    connections = psutil.net_connections(kind='inet')
    
    # Список для хранения занятых портов
    used_ports = []
    
    for conn in connections:
        used_ports.append(conn.laddr.port)  # Добавляем порт из локального адреса
    
    # Удаляем дубликаты и сортируем
    used_ports = sorted(set(used_ports))
    
    return used_ports

if __name__ == '__main__':
    ports = get_used_ports()
    
    # Печатаем занятые порты в консоль
    print("Занятые порты:")
    for port in ports:
        print(port)
    
    # Записываем занятые порты в файл
    with open("Занятые_порты.txt", "w") as file:
        file.write("Порты. Найдёт занятые!\n")
        file.write("В ИИ - описание - какие порты можно задействовать для\n")
        file.write("своего сервера.\n")
        file.write("https://poe.com/s/XhfUf1IcKRs5lkh89cYH\n\n")
        file.write("Занятые порты:\n")
        for port in ports:
            file.write(f"{port}\n")