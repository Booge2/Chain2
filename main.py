import threading
import random
import math
import time
import shutil
import os

numbers = []


def fill_list():
    global numbers
    for _ in range(10):
        numbers.append(random.randint(1, 100))
    print("Список заповнено: ", numbers)


def calculate_sum():
    global numbers
    print("Сума елементів списку: ", sum(numbers))


def calculate_average():
    global numbers
    print("Середнє арифметичне значення у списку: ", sum(numbers) / len(numbers))


thread1 = threading.Thread(target=fill_list)
thread2 = threading.Thread(target=calculate_sum)
thread3 = threading.Thread(target=calculate_average)

thread1.start()
thread1.join()

thread2.start()
thread3.start()

thread2.join()
thread3.join()


# Завдання 2


def fill_file_with_random_numbers(filename, num_numbers, max_value):
    with open(filename, "w") as file:
        for _ in range(num_numbers):
            random_number = random.randint(1, max_value)
            file.write(str(random_number) + "\n")


def find_prime_numbers(filename, output_filename):
    prime_count = 0
    with open(filename, "r") as file, open(output_filename, "w") as output_file:
        for line in file:
            number = int(line.strip())
            if is_prime(number):
                prime_count += 1
                output_file.write(f"{number} is prime\n")
    print(f"Number of prime numbers found: {prime_count}")


def is_prime(number):
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True


def find_factorials(filename, output_filename):
    with open(filename, "r") as file, open(output_filename, "w") as output_file:
        for line in file:
            number = int(line.strip())
            factorial = math.factorial(number)
            output_file.write(f"{number}! = {factorial}\n")


def main():
    filename = input("Введіть шлях до файлу: ")
    num_numbers = int(input("Введіть кількість випадкових чисел: "))
    max_value = int(input("Введіть максимальне значення для випадкових чисел: "))

    fill_thread = threading.Thread(target=fill_file_with_random_numbers, args=(filename, num_numbers, max_value))
    fill_thread.start()

    while not fill_thread.is_alive():
        time.sleep(0.1)

    prime_thread = threading.Thread(target=find_prime_numbers, args=(filename, f"{filename}_primes.txt"))
    factorial_thread = threading.Thread(target=find_factorials, args=(filename, f"{filename}_factorials.txt"))

    prime_thread.start()
    factorial_thread.start()

    prime_thread.join()
    factorial_thread.join()

    print("Виконання всіх потоків завершено.")


if __name__ == "__main__":
    main()


# Завдання 3


def copy_directory(source, destination):
    try:
        shutil.copytree(source, destination)
        print(f"Директорія {source} скопійована у {destination}")
    except FileExistsError:
        print(f"Директорія {destination} вже існує")


def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Створено директорію: {directory}")


source_dir = input("Введіть шлях до директорії, яку потрібно скопіювати: ")
destination_dir = input("Введіть шлях до нової директорії: ")

source_parts = source_dir.split("/")
destination_parts = destination_dir.split("/")

source_path = ""
destination_path = ""

for part in source_parts:
    source_path = os.path.join(source_path, part)
    create_directory_if_not_exists(source_path)

for part in destination_parts:
    destination_path = os.path.join(destination_path, part)
    create_directory_if_not_exists(destination_path)

thread = threading.Thread(target=copy_directory, args=(source_dir, destination_dir))
thread.start()
thread.join()


# Завдання 4


def find_files(directory, keyword):
    found_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                if keyword in f.read():
                    found_files.append(file_path)
    return found_files


def merge_files(found_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as output:
        for file in found_files:
            with open(file, 'r', encoding='utf-8') as f:
                output.write(f.read())


def remove_banned_words(input_file, banned_words_file, output_file):
    with open(banned_words_file, 'r', encoding='utf-8') as f:
        banned_words = f.read().splitlines()
    with open(input_file, 'r', encoding='utf-8') as input, open(output_file, 'w', encoding='utf-8') as output:
        for line in input:
            for word in banned_words:
                line = line.replace(word, '')
            output.write(line)


def main():
    directory = input("Введіть шлях до директорії: ")
    keyword = input("Введіть слово для пошуку: ")
    found_files = find_files(directory, keyword)
    if not found_files:
        print("Не знайдено файлів з вказаним ключовим словом.")
        return
    output_file = "merged_file.txt"
    merge_thread = threading.Thread(target=merge_files, args=(found_files, output_file))
    remove_banned_words_thread = threading.Thread(target=remove_banned_words,
                                                  args=(output_file, "banned_words.txt", "filtered_file.txt"))

    merge_thread.start()
    remove_banned_words_thread.start()

    merge_thread.join()
    remove_banned_words_thread.join()

    print("Операції завершено.")


if __name__ == "__main__":
    main()
