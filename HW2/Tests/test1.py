"""
Задание 1.
Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и разархивирования с путями (x).
"""

import subprocess

def checkout(command, expected_output):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print("Вывод команды:", result.stdout)
        print("Ошибка команды:", result.stderr)
        return expected_output in result.stdout
    except Exception as e:
        print("Ошибка при выполнении команды:", e)
        return False


folder_in = "/home/parallels/test"
folder_out = "/home/parallels/out"
folder_ext = "/home/parallels/folder1"
folder_ext2 = "/home/parallels/folder2"
list_of_files = ["file1.txt", "file2.txt", "file3.txt"]

def test_step1():
    # test1
    assert checkout("cd /home/parallels/test; 7z a ../out/arx2", "Everything is Ok"), \
        "test1 FAIL"


def test_step2():
    # test2
    assert checkout("cd /home/parallels/test; 7z e arx2.7z -o/home/parallels/folder1 -y",
                    "Everything is Ok"), "test2 FAIL"


def test_step3():
    # test3
    assert checkout("cd /home/parallels/out; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"
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
    # test 8 - вывод списка файлов
    assert checkout("ls {}".format(folder_out), "arx2.7z"), "test8 FAIL"


def test_step9():
    # test 9 - Проверка разархивирования
    assert checkout("cd {}; 7z x arx2.7z -o{} -y".format(folder_out, folder_ext),
                    "Everything is Ok"), "test9 FAIL"

    assert checkout("ls {}".format(folder_ext), "test1.txt"), "test9 FAIL: test1.txt not found"
    assert checkout("ls {}".format(folder_ext), "test2.txt"), "test9 FAIL: test2.txt not found"

  