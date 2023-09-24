import os
import counter

batch_size = 2

path_to_main_file = './main.py'
path_to_hash = './hash.txt'


# Функция нахождения ХЭШ-суммы файла
def get_hash_file(path):
    with open(path, 'rb') as file:
        batch = file.read(batch_size)
        cur_hash = batch
        while batch:  # Пока не дочитаем до конца файла
            batch = file.read(batch_size)
            if batch != b'':  # Если строка не байтовая, то сложение отрезка по xor
                if len(batch) < batch_size:
                    batch.zfill(batch_size)
                cur_hash = bytes(a ^ b for a, b in zip(cur_hash, batch))
    return cur_hash


# функция обновления количества запусков программы
def update_run_count():
    with open('counter.py', 'r') as file_read:
        old_count = file_read.read()
        old_count = old_count.split(' = ')
        old_count[1] = int(old_count[1]) + 1
    with open('counter.py', 'w') as file_write:
        file_write.write(str(old_count[0]) + ' = ' + str(old_count[1]))


# основной код программы
def run():
    print('Программа работает :-)')
    update_run_count()


if counter.RUN_COUNT == 0:
    with open(path_to_hash, 'w') as file:
        t = str(get_hash_file(path_to_main_file))
        file.write(t)
        print('Первый запуск программы, ХЭШ-сумма:', t)
        run()
elif not os.path.exists(path_to_hash):
    print('Не найден ХЭШ-файл контрольной суммы')
else:
    with open(path_to_hash, 'r') as file:
        hash_str = file.read()

    if str(get_hash_file(path_to_main_file)) != hash_str:
        print('ХЭШ-сумма программы измениласьи!')
    else:
        print('ХЭШ-сумма программы не изменилась)')
        run()


