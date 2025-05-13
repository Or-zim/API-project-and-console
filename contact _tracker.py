import json

file_name = 'data.json'

def replace_dict(args): 

    data = {
        'name': args[0],
        'phone': args[1],
        'email': args[2],
    }
    return data


def load_data_in_json(file_name, inf):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    if not data:
        inf['id'] = 1
        data.append(inf)
    else:
        inf['id'] = data[-1]['id'] + 1
        data.append(inf)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



def print_data_in_json(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data:
                print(f"Имя: {i['name']}    Тел.: {i['phone']}    Email: {i['email']}")
                    
    except:
        print('Ошибка')


def delete_data(file_name, id):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            new_data = data
            
            for item in data:
                if item['id'] == int(id):
                    new_data.remove(item)
        
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)

    except:
        print('Файл пуст или неисправен или такого id не существует')
    


def main():
    
    while True:
        print('Введите свои данные через пробел')
        print('Для просмотра всех данных введите LIST')
        print('Для удаления данных введите DEL пользователя')
        print('Для отмены введите EXIT')
        data = input('\n').split()
        print('\n')

        if len(data) == 3:
            load_data_in_json(file_name, replace_dict(data))


        elif len(data) == 1 and data[0] == 'LIST':
            print_data_in_json(file_name)
            print('\n')


        elif len(data) == 1 and data[0] == 'DEL':
            id = input('Введите id пользователя: ')
            delete_data(file_name, id)


        elif len(data) == 1 and data[0] == 'EXIT':
            break

        else:
            ('команда не распознана, повторите попытку')



if __name__ == "__main__":
    main()
