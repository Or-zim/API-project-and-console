import json
import os
import sys
from datetime import datetime
#completed
#not done
#in progress
TASKS_FILE = "tasks.json"

class Task:
    """класс который представляет каждую задачу"""
    def __init__(self, id, description, status='todo', createdAT=None, updatedAT=None):
        """инициализация свойств задачь"""
        self.id = id
        self.description = description
        self.status = status
        self.createdAT = createdAT if createdAT else datetime.now().isoformat
        self.updatedA = updatedAT if updatedAT else self.createdAT
    
    def to_dict(self):
        """возвращает словарь для сериализации в JSON"""
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'createdAT': self.createdAT,
            'updateAT': self.updatedAT
        }
    

    @classmethod
    def from_dict(cls, data):
        """создает объект Task из словаря"""
        return cls(
            data['id'],
            data['description'],
            data['status'],
            data['createdAT'],
            data['updatedAT'],
        )
    

class TaskManager:

    """Класс для управления списком задач"""
    def __init__(self):
        self.tasks = self._load_task()


    def _load_task(self):
        """Загружает задачи из файла JSON или возвращает пустой список"""
        if not os.path.exists(TASKS_FILE):
            return []
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Task.from_dict(task_data) for task_data in data]
        except(json.JSONDecodeError, IOError):
            print(f"Ошибка: Не удалось прочитать файл {TASKS_FILE}. Возможно файл поврежден.")
            return []


    def _save_tasks(self):
        """сохраняет задачи в файл JSON"""
        try:
            with open(TASKS_FILE, 'w', encoding='utf-8') as file:
                task_dicts = [task.to_dict() for task in self.tasks]
                json.dump(task_dicts, file, indent=4, ensure_ascii=False)
        except IOError:
            print("Ошибка: Не удалось сохранить задачи.")


    def add_task(self, description):
        """добавляет новую задачу"""
        new_id = len(self.tasks) + 1
        new_task = Task(new_id, description)
        self.tasks.append(new_task)
        self._save_tasks()
        print("Задача успешно добалена")


    def update_task(self, task_id, new_description):
        """Обновляет описание существующей задачи"""
        for task in self.tasks:
            if task_id == task.id:
                task.description = new_description
                task.updatedAT = datetime.now().isoformat()
                self._save_tasks()
                print('Задача успешно обновленна')
                return 
        print("Ошибка: Задача не найдена.")    


    def delete_task(self, task_id):
        """удаляет задачу из списка"""
        new_tasks = []
        for task in self.tasks:
            if task.id != task_id:
                new_tasks.append(task)
        self.tasks = new_tasks
        self._save_tasks()
        print('Задача успешно удалена')


    def mark_task(self, task_id, status):
        """помечает задачу как выполнению или нет"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                task.updatedAT = datetime.now().isoformat()
                self._save_tasks()
                print('Статус обновлен')
                return
        print("Ошибка: Задача не найдена.")


    def list_tasks(self, status=None):
        """фильтрация задач по статусу"""
        if not self.tasks:
            print('Нету ни одной задачи')
            return
        
        if status:
            filter_task = [task for task in self.tasks if task.status == status]

        if len(filter_task) == 0:
            print('Нету задач с таким статусом')
            return

        for task in filter_task:
            print(f"ID: {task.id}, Описание: {task.description}, Статус: {task.status}, Создана: {task.createdAT}, Обновлена: {task.updatedAT}")


def main():
    """Основная функция для обработки аргументов командной строки."""
    
    manager = TaskManager()

    if len(sys.argv) < 2:
        print("Использование: python task_project.py [команда] [аргументы]")
        print("Команды: add, update, delete, mark, list, list_todo, list_in_progress, list_done")
        return
    
    command = sys.argv[1].lower()

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Использование: add <описание>")
                return
            description = " ".join(sys.argv[2:])
            manager.add_task(description)
        elif command == "update":
            if len(sys.argv) < 4:
                print("Использование: update <id> <новое_описание>")
                return
            task_id = int(sys.argv[2])
            new_description = " ".join(sys.argv[3:])
            manager.update_task(task_id, new_description)
        elif command == "delete":
            if len(sys.argv) < 3:
                print("Использование: delete <id>")
                return
            task_id = int(sys.argv[2])
            manager.delete_task(task_id)
        elif command == "mark":
            if len(sys.argv) < 4:
                print("Использование: mark <id> <todo/in_progress/done>")
                return
            task_id = int(sys.argv[2])
            status = sys.argv[3].lower()
            if status not in ["todo", "in-progress", "done"]:
                print("Неверный статус. Допустимые значения: todo, in-progress, done")
                return
            manager.mark_task(task_id, status)
        elif command == "list":
            manager.list_tasks()
        elif command == "list_todo":
            manager.list_tasks("todo")
        elif command == "list_in_progress":
            manager.list_tasks("in-progress")
        elif command == "list_done":
            manager.list_tasks("done")
        else:
            print("Неизвестная команда.")
    except ValueError:
        print("Ошибка: ID задачи должно быть целым числом.")

if __name__ == "__main__":
    main()
