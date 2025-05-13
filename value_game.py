import secrets


    
def run_game():
    win_value = secrets.randbelow(100)
    print('Добро пожаловать в игру на угадывание чисел!\nЯ думаю о числе от 1 до 100.\nВыберете уровень сложности:')
    print('\nПожалуйста, выберите уровень сложности:\n1. Легкий (10 попыток)\n2. Средний (5 попыток)\n3. Безумный (3 попытки)\n')
    level = input('Введи номер сложности: ')
    if level == '1':
        print('Выбрана легкая сложность')
        attemps = 10
    if level == '2':
        print('Выбрана средняя сложность')
        attemps = 5
    if level == '3':
        print('Выбрана безумная сложность')
        attemps = 3

    att = 1

    while True:
        player_value = int(input('Введите свою догадку о числе: '))
        
        if att == attemps:
            print(f'Увы попытки закончились, вы проиграли, АХХАХАХАХАХАХА, я загадал: {win_value}')
            return
        
        if player_value == win_value:
            if att == 1:
                print(f'Вы просто сумашедший, вам понадобилась всего {att} попытка')
                att = 1
                return
            if att > 1 and att < 5:
                print(f'Вы догадливый, вам понадобилась всего {att} попытки')
                att = 1
                return
            if att >= 5:
                print(f'Вы успешно победили, вам понадобилась всего {att} попыток')
                att = 1
                return

        if player_value != win_value:
            print('Упс! вы не угадали, попробуйте еще!')
            if player_value < win_value:
                print(f"{player_value} меньше моего числа\nОсталось {attemps-att} попыток(-а)")
                att = att + 1
            elif player_value > win_value:
                print(f"{player_value} больше моего числа\nОсталось {attemps-att} попыток(-а)")
                att = att + 1

        
run_game()