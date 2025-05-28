import math
from sympy import factorint


def is_valid_params(a, b, m):
    # Условие 1: b и m взаимно просты
    if math.gcd(b, m) != 1:
        return False
    # Условие 2: a-1 делится на все простые делители m
    prime_factors = factorint(m).keys()
    if not all((a - 1) % p == 0 for p in prime_factors):
        return False
    # Условие 3: если m делится на 4, то a-1 должно делиться на 4
    if m % 4 == 0:
        if (a-1) % 4 !=0:
            return False
    return True

def find_valid_params(m, a_start=2, b_start=1):
    a = a_start
    b = b_start
    while not is_valid_params(a, b, m):
        b += 1
        if b >= m:
            b = 1
            a += 1
    return a, b

def select_or_generate_params(a, b, m):
    print(f"Проверяем введённые параметры: a = {a}, b = {b}, m = {m}")
    if is_valid_params(a, b, m):
        print("Введённые параметры корректны")
        return a, b
    else:
        print("Введённые параметры не прошли проверку. Подбор корректных")
        new_a, new_b = find_valid_params(m, a_start=a, b_start=b)
        if is_valid_params(new_a, new_b, m):
            print(f"Найдены подходящие параметры: a = {new_a}, b = {new_b}\n")
            return new_a, new_b
        else:
            raise ValueError("Не удалось найти подходящие параметры.\n")


def pretty_print(seq, decimals=8, show_index=True):
    print("Округлённая последовательность:")
    for i, x in enumerate(seq):
        if show_index:
            print(f"{i + 1}: {round(x, decimals)}")
        else:
            print(round(x, decimals))

    # print("\nОригинальная последовательность:\n", seq)

def lcg(a, b, m, seed, size):
    result = []
    x = seed
    for i in range(size):
        x = (a * x + b) % m
        result.append(x / m) # Нормализация
    return result

def extended_congruential(seed_values, n, m=2**32 - 5):
    assert len(seed_values) >= 3, "Нужно минимум 3 стартовых значения"
    results = seed_values[:3]
    for i in range(3, n):
        next_val = (2**13 * (results[i-1] + results[i-2] + results[i-3])) % m
        results.append(next_val)
        # Вывод с нормализацией
    return [x / m for x in results]


def modinv(x, m):
    try:
        return pow(x, -1, m)
    except ValueError:
        return None  # нет обратного

def inversive_congruential(seed, a, c, m, n):
    results = [seed]
    for _ in range(1, n):
        prev = results[-1]
        inv = modinv(prev, m)
        if inv is None:
            print(f"Не удалось найти обратного, используем 1")
            inv = 1
        next_val = (a * (inv + c)) % m
        results.append(next_val)
    return [x / m for x in results]


run = 2 # 0 - проверка генераторов, 1 - для линейного задача, 2 - для расширенного, 3 - для инверсивного


if run == 0:
    # Изначальные вводимые значения
    m = 2**31 # Константа
    a_input = 5
    b_input = 12
    size = 10

    print("\nЛинейный конгруэнтный генератор:")
    # Проверяем на правильность введённых данных. Если не верные, подбираем ближайшие верные
    a_final, b_final = select_or_generate_params(a_input, b_input, m)

    # Пример для обычного 1
    sequence = lcg(a_final, b_final, m, seed=123, size=10)

    # Пример для обычного 2
    sequence2 = lcg(a_final, b_final, m, seed=124, size=10)

    # Вывод 2 примеров обычного в нормальном виде
    pretty_print(sequence)
    pretty_print(sequence2)

    print("\nРасширенный конгруэнтный генератор:")
    initial_seeds = [123, 456, 789]
    seq_ecg = extended_congruential(initial_seeds, n=size, m=m)
    pretty_print(seq_ecg)

    print("\nИнверсивный конгруэнтный генератор:")
    icg_a = 17
    icg_c = 31
    icg_seed = 123
    seq_icg = inversive_congruential(icg_seed, icg_a, icg_c, m, n=size)
    pretty_print(seq_icg)


elif run == 1:
    # Параметры генератора
    a, b = 5, 13
    m = 2**32-1
    seed = 123
    n = 1000  # количество клиентов
    p_event = 0.02 # Вероятность
    payout = 100_000  # страховая выплата в рублях

    # Генерация случайных чисел
    random_numbers = lcg(a, b, m, seed, n)

    # Смоделируем обращения
    events = []
    for x in random_numbers:
        if x < p_event:
            events.append(1)  # произошло страховое событие
        else:
            events.append(0)  # не произошло
    total_events = sum(events)
    total_payout = total_events * payout

    # Статистика
    mean_payout = total_payout / n
    event_probability_empirical = total_events / n

    print(f"Количество страховых случаев: {total_events} из {n}")
    print(f"Сумма выплат: {total_payout} ₽")
    print(f"Средняя выплата на клиента: {mean_payout:.2f} ₽")
    print(f"Эмпирическая вероятность события: {event_probability_empirical:.4f}")

elif run == 2:
    # Монте-Карло на расширенном генераторе
    m = 2**32 - 5
    initial_seeds = [123, 456, 789] # Заранее расчитал
    n = 1000
    p_event = 0.02
    payout = 100_000

    random_numbers = extended_congruential(initial_seeds, n, m)

    events = []
    for x in random_numbers:
        if x < p_event:
            events.append(1)
        else:
            events.append(0)

    total_events = sum(events)
    total_payout = total_events * payout
    mean_payout = total_payout / n
    event_probability_empirical = total_events / n

    print("Расширенный — страховое моделирование:")
    print(f"Количество страховых случаев: {total_events} из {n}")
    print(f"Сумма выплат: {total_payout} ₽")
    print(f"Средняя выплата на клиента: {mean_payout:.2f} ₽")
    print(f"Эмпирическая вероятность события: {event_probability_empirical:.4f}")

elif run == 3:
    # Монте-Карло на инверсивном генераторе
    m = 2**32 - 5
    a = 17
    c = 31
    seed = 123
    n = 1000
    p_event = 0.02
    payout = 100_000

    random_numbers = inversive_congruential(seed, a, c, m, n)

    events = []
    for x in random_numbers:
        if x < p_event:
            events.append(1)
        else:
            events.append(0)

    total_events = sum(events)
    total_payout = total_events * payout
    mean_payout = total_payout / n
    event_probability_empirical = total_events / n

    print("Инверсивный КГ — страховое моделирование:")
    print(f"Количество страховых случаев: {total_events} из {n}")
    print(f"Сумма выплат: {total_payout} ₽")
    print(f"Средняя выплата на клиента: {mean_payout:.2f} ₽")
    print(f"Эмпирическая вероятность события: {event_probability_empirical:.4f}")