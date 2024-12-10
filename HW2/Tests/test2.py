"""
Задание 2.
Установить пакет для расчета crc32 sudo apt install libarchive-zip-perl
Доработать проект, добавив тест команды
расчета хеша (h). Проверить, что хеш совпадает с рассчитанным командой crc32.
"""

import subprocess
import zlib


def checkout(command, expected_output):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, encoding='UTF-8')
        print("Вывод команды:", result.stdout)
        print("Ошибка команды:", result.stderr)
        return expected_output in result.stdout
    except Exception as e:
        print("Ошибка при выполнении команды:", e)
        return False


folder_in = "/home/Anna/test"
folder_out = "/home/Anna/out"
folder_ext = "/home/Anna/folder1"


def test_step1():
    # test1
    assert checkout("cd /home/Anna/test; 7z a ../out/arx2", "Everything is Ok"), "test1 FAIL"


def test_step2():
    # test2
    assert checkout("cd /home/Anna/test; 7z e arx2.7z -o/home/urban/folder1 -y",
                    "Everything is Ok"), "test2 FAIL"


def test_step3():
    # test3
    assert checkout("cd /home/Anna/out; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test 4
    res1 = checkout("cd {}; 7z a {}/arx2".format(folder_in, folder_out), "Everything is Ok")
    res2 = checkout("ls {}".format(folder_out), "arx2.7z")
    assert res1 and res2, "test4 FAIL"


def test_step5():
    # test 5
    res1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(folder_out, folder_ext), "Everything is Ok")
    res2 = checkout("ls {}".format(folder_ext), "test1.txt")
    res3 = checkout("ls {}".format(folder_ext), "test2.txt")
    assert res1 and res2 and res3, "test5 FAIL"


def test_step6():
    # test 6
    assert checkout("cd {}; 7z u arx2.7z".format(folder_in), "Everything is Ok"), "test6 FAIL"


def test_step7():
    # test 7
    assert checkout("cd {}; 7z d arx2.7z".format(folder_out), "Everything is Ok"), "test7 FAIL"


def test_step8():
    # test 8 - вывод списка файлов (l)
    assert checkout("ls {}".format(folder_out), "arx2.7z"), "test8 FAIL"


def test_step9():
    # test 9 - Проверка разархивирования
    assert checkout("cd {}; 7z x arx2.7z -o{} -y".format(folder_out, folder_ext),
                    "Everything is Ok"), "test9 FAIL"

    # Проверка наличия файлов после разархивирования
    assert checkout("ls {}".format(folder_ext), "test1.txt"), "test9 FAIL: test1.txt not found"
    assert checkout("ls {}".format(folder_ext), "test2.txt"), "test9 FAIL: test2.txt not found"



def test_step10():
    # test 10 - Проверка команды расчета хэша и совпадения с расчетным
    test_file = f"{folder_in}/test1.txt"
    with open(test_file, 'wb') as f:
        content = b'File for hash calculation'
        f.write(content)

    expected_hash = format(zlib.crc32(content) & 0xFFFFFFFF, '08x').upper()
    hash_output = subprocess.run(f"cd {folder_in}; 7z h {test_file}", shell=True,
                                 text=True, capture_output=True, encoding='UTF-8')



    actual_hash = next((line.split()[-1] for line in hash_output.stdout.splitlines()
                        if "CRC32  for data:" in line), None)

    assert expected_hash == actual_hash, f'test10 FAIL: expected {expected_hash}, got {actual_hash}'