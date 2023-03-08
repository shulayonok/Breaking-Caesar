import random
from collections import Counter
from tkinter import *
from tkinter import messagebox
import tkinter.filedialog as fd


# Предупреждение о том, что файл не выбран
def exception(param):
    messagebox.showwarning("Предупреждение", param)


# Выбираем файл
def choose_file():
    global filename
    try:
        filetype = (("Текстовый файл", '*.txt'), ("All files", '*.*'))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetype)
        if filename == "":
            raise Exception("Файл не выбран")
    except Exception as e:
        exception(e)
        return False
    return True


# Подсчитываем общее количество букв
def count_letters():
    count = 0
    for i in range(len(letters)):
        count += counter[letters[i]]
    return count


# Находим частоту каждой буквы
def frequency(count):
    arr_my_frequency = []
    for i in range(len(letters)):
        frequency = counter[letters[i]] / count * 100
        arr_my_frequency.append(frequency)
    return arr_my_frequency


# Функция шифрования
def caesar_cipher():
    global counter
    global arr
    with open(filename, encoding='utf-8', newline='') as file:
        text_for_encrypt = file.read().lower()
        counter = Counter(text_for_encrypt)
        # на месте этой частоты может быть обычная частота букв в русском языке, взятая из Википедии
        freq1 = dict(sorted(dict(zip(letters, frequency(count_letters()))).items(), key=lambda item: item[1])).keys()
        arr = []
        # генерируем ключ
        while True:
            step = random.randint(-1000, 1000)
            if step % 33 != 0:
                break
        # шифруем текст шифром Цезаря
        for i in text_for_encrypt:
            if letters.find(i) == -1:
                arr.append(i)
            else:
                arr.append(letters[(letters.find(i) + step) % len(letters)])
        text_for_decrypt = ''.join(arr)
        counter = Counter(text_for_decrypt)
        freq2 = dict(sorted(dict(zip(letters, frequency(count_letters()))).items(), key=lambda item: item[1])).keys()
        return text_for_decrypt, freq1, freq2


# Применяем частотный анализ
def decrypt_text(text_for_decrypt, freq1, freq2):
    arr_encrypt_text = []
    dictionary = dict(zip(freq2, freq1))
    print(dictionary)
    for i in text_for_decrypt:
        if letters.find(i) == -1:
            arr_encrypt_text.append(i)
        else:
            arr_encrypt_text.append(dictionary.get(i))
    text_for_decrypt = ''.join(arr_encrypt_text)
    print(dictionary.get('а'))
    letter = dictionary.get('а')
    key = 33-letters.find(letter)
    return text_for_decrypt, key


# Функция запуска взлома
def hack():
    if choose_file():
        text_for_decrypt, freq1, freq2 = caesar_cipher()
        result, key = decrypt_text(text_for_decrypt, freq1, freq2)
        encrypted.insert(1.0, text_for_decrypt)
        decrypted.insert(1.0, result)
        messagebox.showinfo("Ключ", f"Ключ: {key}")


# расположение файла
filename = ""
# алфавит
letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# окно
window = Tk()
window.title('Взлом Цезаря')
window.geometry('600x600')
window.resizable(0, 0)
window['bg'] = "#efefef"
font = ("Century Gothic", 16)

# поля вывода зашифрованного текста
encryptLabel = Label(window, text='Зашифрованный текст:', font=font)
encryptLabel.place(x=20, y=15)
encrypted = Text(width=47, height=10, font=font)
encrypted.place(x=20, y=45)
scroll = Scrollbar(command=encrypted.yview)
scroll.place(x=0, y=15)
encrypted.config(yscrollcommand=scroll.set)

# поля вывода расшифрованного текста
decryptLabel = Label(window, text='Расшифрованный текст:', font=font)
decryptLabel.place(x=20, y=315)
decrypted = Text(width=47, height=8, font=font)
decrypted.place(x=20, y=345)
scroll2 = Scrollbar(command=decrypted.yview)
scroll2.place(x=0, y=320)
decrypted.config(yscrollcommand=scroll2.set)

button = Button(window, text="Взлом", font=font, command=hack)
button.place(x=30, y=550)

window.mainloop()
