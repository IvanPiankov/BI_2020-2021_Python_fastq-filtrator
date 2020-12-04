import sys


fasta = str(sys.argv[-1])   # fastq - позиционный аргумент поэтому он
file_list = sys.argv        # всегда будет последним в списке передаваемых аргументов
min_length = 1              # Объявляем флаги, для того, чтобы с их использованием запускать те -
gc_counter = False          # или иные акты в коде
not_filtered_file = False
name_flag = False

if "--min_length" in file_list:         # Идея с if не самый элегантный вариант,
    i = file_list.index("--min_length") # Но если мы будем искать аргументы через for это будет дольше
    min_length = file_list[i + 1]       # Пробывал и сравнивал время работы
if "--keep_filtered" in file_list:      # При помощи if мы пытаемся найти тот или иной флаг из ком.строки
    not_filtered_file = True
if "--gc_bounds" in file_list:
    i = file_list.index("--gc_bounds")
    min_gc = float(file_list[i + 1])
    gc_counter = True
    try:
        max_gc = float(file_list[i + 2])
    except ValueError:
        max_gc = min_gc
if "--output_base_name" in file_list:
    i = file_list.index("--output_base_name")
    file_names = file_list[i + 1]
    name_flag = True

if name_flag is False:                  # Проверяем есть ли у нас имя выходного файла
    file_names = fasta[:-6]             # И выполняем сопутствующие действия
    good_name = file_names + "_passed"
    bad_name = file_names + "_faild"
else:
    good_name = file_names + "_passed.fastq"
    bad_name = file_names + "_faild.fastq"

if not_filtered_file is True:           # Проверяем есть ли у нас флаг для создания файла с
    good_file = open(good_name, "w")    # С не прошед. фильтр ридами
    bad_file = open(bad_name, "w")      # Создаем и открываем файлы для записи
else:
    good_file = open(good_name, "w")


def filtration_for_lengt (lin2, min_length):    # Функция для прохождения ридами фильтра по длине
    int_length = len(lin2)
    min_length = int(min_length)
    if int_length >= min_length:
        return True
    else:
        return False


def gc_counter_filter(lin2, min_gc, max_gc):    # Функция для прохождения ридами фильтра по GC%
    min_gc = int(min_gc)
    max_gc = int(max_gc)
    total = len(lin2)
    c = lin2.count("C")
    g = lin2.count("G")
    gc_total = g + c
    gc_content = (gc_total / total) * 100
    if max_gc == min_gc:
        if min_gc <= gc_total:
            return True
        else:
            return False
    else:
        if min_gc <= gc_total <= max_gc:
            return True
        else:
            return False


def writing_file(lin1, lin2, lin3, lin4, length_filter, gc_filter):   # Функция для записи ридов
    if length_filter is True and gc_filter is True:             # Запись происходит в разные файлы по результатом
        good_file.write(lin1 + "\n")                            # Значения флага, которое мы ранее получили
        good_file.write(lin2 + "\n")
        good_file.write(lin3 + "\n")
        good_file.write(lin4 + "\n")
    elif not_filtered_file is True:
        bad_file.write(lin1 + "\n")
        bad_file.write(lin2 + "\n")
        bad_file.write(lin3 + "\n")
        bad_file.write(lin4 + "\n")
    else:
        pass


with open(fasta, "r") as fastq:
    lin1 = fastq.readline().rstrip("\n")            # Считываем первую строку для входа в цикл
    while lin1 != "":                               # Вроде бы каждый fastq файл заканчивается ""
        lin2 = fastq.readline().rstrip("\n")        # Так мы можем ловить конец файла
        lin3, lin4 = fastq.readline().rstrip("\n"), fastq.readline().rstrip("\n")
        length_filter = filtration_for_lengt(lin2, min_length)      # Запуск сторонних функций для
        if gc_counter is True:                                      # Прохождения различных фильтров
            gc_filter = gc_counter_filter(lin2, min_gc, max_gc)
        else:
            gc_filter = True
        writing_file(lin1, lin2, lin3, lin4, length_filter, gc_filter)
        lin1 = fastq.readline().rstrip("\n")        # Записываем следующую линию, для того, чтобы цикл не ушел в небеса

if not_filtered_file is True:                       # Обязательно! Закрываем файлы
    good_file.close()
    bad_file.close()
else:
    good_file.close()

