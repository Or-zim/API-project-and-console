import json

file_name = 'wallet.json'
class User:
    def __init__(self, name, lastname, phone, email):
        self.name = name
        self.lastname = lastname
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'name': self.name,
            'lastname': self.lastname,
            'phone': self.phone,
            'email': self.email,
        }


class Managar:
    def __init__(self, file_name, data):
        self.file_name = file_name
        self.inf = data

    @classmethod
    def save_data(cls, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
                cls.data = json.load(f)
                return cls.data

    @classmethod
    def write_data(cls, file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(cls.data, f, indent=4, ensure_ascii=False)


    def load_data(self):
        try:
            self.save_data(self.file_name)
        except FileNotFoundError:
            self.data = []

        if not self.data:
            self.inf['ID'] = 1
            self.data.append(self.inf)
        else:
            self.inf['ID'] = self.data[-1]['ID'] + 1
            self.data.append(self.inf)

        try:
            self.write_data(self.file_name)
        except:
            print('Файл неисправен в обработке')


    def print_data(self, id=False):
        try:
            self.save_data(self.file_name)
        except:
            print('Файл неисправен')

        if not id:
            for item in self.data:
                print(f"ID: {item['ID']}, Имя: {item['name']}, Фамилия: {item['lastname']}, Тел.: {item['phone']}, Email: {item['email']}")
        if id:
            for item in self.data:
                if item['ID'] == id:
                    print(f"ID: {item['ID']}, Имя: {item['name']}, Фамилия: {item['lastname']}, Тел.: {item['phone']}, Email: {item['email']}")
                    return
            print('Пользователя с таким ID не существует')

    def delete_data(self, id=None):
        try:
            self.save_data(self.file_name)
        except:
            print('Файл неисправен')

        if not id:
            self.data.clear()
        if id:
            for item in self.data:
                if item['ID'] == id:
                    print(123)
                    self.data.remove(item)
                    self.write_data(self.file_name)
                    return

        try:
            self.write_data(self.file_name)
        except:
            print('ERROR')




def main():
    print("Это записная книжка для пользователей.\n1. Чтобы добавить новые данные, введите: add\n2. Чтобы просмотрнеть текущие записи, введите: list\n3. Чтобы удалить имеющиеся записи, введите: del")
    while True:
        signal = input()
        try:
            if signal == 'add':
                data = input('Введите данные пользователя через пробел по такому принцепу:\n ПРИМЕР: Иван Иванов 89999999999 ivan@gmail.com\n').split()
                user = User(name=data[0], lastname=data[1], phone=data[2], email=data[3])
                managar = Managar(file_name, user.to_dict())
                managar.load_data()
            
            elif signal == 'list':
                data = input("Введите ID пользователя если для(если хотите вывести список всех данных ничего не вводите):\n")
                
        except:
            print("Ошибка ввода данных")
            
if __name__ == "__main__":
    main()