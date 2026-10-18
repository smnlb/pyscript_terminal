from itertools import product
from random import shuffle, random

SAD = '(︶︹︺)'
CONFUSED = '(o_O)'
GIVE_UP = '┐(￣ヘ￣)┌'

DAYS = [
    'в понедельник',
    'во вторник',
    'в среду',
    'в четверг',
    'в пятницу',
    'в субботу',
]

def ask_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
        except (ValueError, EOFError):
            print(SAD)
            continue
        if value <= 0:
            print(CONFUSED)
            continue
        return value

def ask_schedule(nn):
    while True:
        schedule = []
        print('\nВведите номера учебников.')
        for day_name in DAYS:
            print(f'    {day_name}:')
            day_textbooks = []
            while True:
                try:
                    line = input('    ')
                except EOFError:
                    line = ''
                if line == '':
                    break
                for token in line.split():
                    try:
                        num = int(token)
                    except ValueError:
                        print(SAD)
                        continue
                    if 1 <= num <= nn:
                        day_textbooks.append(num)
                    else:
                        print(f'{CONFUSED}\nНомер не записан')
            schedule.append(day_textbooks)
        if any(schedule):
            return schedule
        print(CONFUSED)

def ask_textbook_params(idx):
    print(f'Введите размеры {idx} учебника:\n')
    while True:
        try:
            pages = int(input('    количество страниц: '))
            cover = int(input('    тип обложки:\n     1-мягкая\n     2-твёрдая   '))
            length = int(input('    длина(см): '))
            width = int(input('    ширина(см): '))
        except (ValueError, EOFError):
            print(SAD)
            continue
        if pages < 0 or cover not in (1, 2) or length <= 0 or width <= 0:
            print(f'{CONFUSED}\nПопробуйте ещё раз')
            continue
        return (pages + cover * 5) * length * width


def compute_solution(nn, schedule, per_day_weights, amplitude):
    usage_count = [0] * nn
    for day in schedule:
        for num in day:
            usage_count[num - 1] += 1

    total_weights = [per_day_weights[i] * usage_count[i] for i in range(nn)]
    grand_total = sum(total_weights)

    active_days = [day for day in schedule if day]
    if not active_days:
        return None

    target = grand_total / len(active_days)

    if nn > 1:
        tail_combos = list(product([0, 1], repeat=nn - 1))
    else:
        tail_combos = [()]
    shuffle(tail_combos)

    best_diff = float('inf')
    best_combo = None

    for tail in tail_combos:
        # Суммарные веса
        weight_a = total_weights[0]
        weight_b = 0
        for i, bit in enumerate(tail):
            if bit == 0:
                weight_a += total_weights[i + 1]
            else:
                weight_b += total_weights[i + 1]

        diff = abs(weight_a - weight_b)
        if diff >= best_diff:
            continue 

        valid = True
        for day in active_days:
            w_a = 0
            w_b = 0
            for num in day:
                idx = num - 1
                if idx == 0 or tail[idx - 1] == 0:
                    w_a += per_day_weights[idx]
                else:
                    w_b += per_day_weights[idx]
            if target > 0:
                dev_a = abs(w_a - target) / target
                dev_b = abs(w_b - target) / target
                if dev_a > amplitude or dev_b > amplitude:
                    valid = False
                    break

        if valid:
            best_diff = diff
            best_combo = (0,) + tail

    if best_combo is None:
        return None

    n1 = [i + 1 for i, bit in enumerate(best_combo) if bit == 0]
    n2 = [i + 1 for i, bit in enumerate(best_combo) if bit == 1]

    if random() < 0.5:
        n1, n2 = n2, n1

    return n1, n2, best_diff, target

def main():
    nn = ask_positive_int('Введите количество ваших учебников:\n    ')
    schedule = ask_schedule(nn)
    per_day_weights = [ask_textbook_params(j + 1) for j in range(nn)]

    if nn > 18:
        print(f'\nВнимание: для {nn} учебников перебор может занять продолжительное время.')

    amplitude = 0.6

    while True:
        result = compute_solution(nn, schedule, per_day_weights, amplitude)

        if result is None:
            print('\nНе удалось найти подходящее распределение.')
            print('Попробуйте изменить максимальную амплитуду весов.\n')
            try:
                amplitude = float(input('Введите новое значение: '))
                continue
            except (ValueError, EOFError):
                print(GIVE_UP)
            print('\nЧтобы изменить расписание, введите "расписание".')
            if input('    ') == 'расписание':
                schedule = ask_schedule(nn)
                continue
            if input('Чтобы выйти из программы, введите "выйти".\n    ') == 'выйти':
                break
            break

        n1, n2, min_diff, _target = result
        print(f'\nМинимальная разница в весе = {min_diff},')
        print(f'соответствующее распределение: {n1},{n2}')
        print()
        print('Чтобы изменить максимальную амплитуду весов, введите "амплитуда".')
        print('Чтобы изменить расписание, введите "расписание".')
        print('Чтобы выйти, введите "выйти".')
        answer = input('    ')

        if answer == 'амплитуда':
            try:
                amplitude = float(input('Введите новое значение: '))
            except (ValueError, EOFError):
                print(GIVE_UP)
            continue
        if answer == 'расписание':
            schedule = ask_schedule(nn)
            continue
        break  # в том числе "выйти" и любой другой ввод — завершаем

    try:
        __terminal__.clear()
    except (NameError, AttributeError):
        pass
    print('\nДля нового запуска программы, перезагрузите страницу.')

main()
