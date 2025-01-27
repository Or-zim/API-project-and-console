
import json
import os
import sys
from datetime import datetime

# Константа для имени файла JSON
TASKS_FILE = "tasks.json"


class Task:
    """Класс, представляющий задачу."""

    def __init__(self, id, description, status="todo", createdAt=None, updatedAt=None):
        self.id = id
        self.description = description
        self.status = status
        self.createdAt = createdAt if createdAt else datetime.now().isoformat()
        self.updatedAt = updatedAt if updatedAt else self.createdAt

    def to_dict(self):
        """Возвращает словарь для сериализации в JSON."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }

    @classmethod
    def from_dict(cls, data):
        """Создает объект Task из словаря."""
        return cls(
            data["id"],
            data["description"],
            data["status"],
            data["createdAt"],
            data["updatedAt"],
        )


class TaskManager:
    """Класс для управления списком задач."""

    def __init__(self):
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        """Загружает задачи из файла JSON или возвращает пустой список."""
        if not os.path.exists(TASKS_FILE):
            return []
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Task.from_dict(task_data) for task_data in data]
        except (json.JSONDecodeError, IOError):
            print(f"Ошибка: Не удалось прочитать файл {TASKS_FILE}. Возможно файл поврежден.")
            return []

    def _save_tasks(self):
        """Сохраняет задачи в файл JSON."""
        try:
            with open(TASKS_FILE, "w", encoding="utf-8") as file:
                task_dicts = [task.to_dict() for task in self.tasks]
                json.dump(task_dicts, file, indent=4, ensure_ascii=False)
        except IOError:
            print("Ошибка: Не удалось сохранить задачи.")

    def add_task(self, description):
        """Добавляет новую задачу в список."""
        new_id = len(self.tasks) + 1
        new_task = Task(new_id, description)
        self.tasks.append(new_task)
        self._save_tasks()
        print("Задача успешно добавлена.")

    def update_task(self, task_id, new_description):
        """Обновляет описание существующей задачи."""
        for task in self.tasks:
            if task.id == task_id:
                task.description = new_description
                task.updatedAt = datetime.now().isoformat()  # Обновляем время обновления
                self._save_tasks()
                print("Задача успешно обновлена.")
                return
        print("Ошибка: Задача не найдена.")

    def delete_task(self, task_id):
        """Удаляет задачу из списка."""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self._save_tasks()
        print("Задача успешно удалена.")

    def mark_task(self, task_id, status):
        """Помечает задачу как выполненную или невыполненную."""
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                task.updatedAt = datetime.now().isoformat()  # Обновляем время обновления
                self._save_tasks()
                print("Статус задачи обновлен.")
                return
        print("Ошибка: Задача не найдена.")

    def list_tasks(self, status=None):
        """Выводит список задач с фильтрацией по статусу."""
        if not self.tasks:
          print("Нет ни одной задачи")
          return
        if status:
           filtered_tasks = [task for task in self.tasks if task.status == status]
        else:
          filtered_tasks = self.tasks

        if not filtered_tasks:
            print("Нет задач с заданным статусом")
            return

        for task in filtered_tasks:
             print(f"ID: {task.id}, Описание: {task.description}, Статус: {task.status}, Создана: {task.createdAt}, Обновлена: {task.updatedAt}")


def main():
    """Основная функция для обработки аргументов командной строки."""
    manager = TaskManager()

    if len(sys.argv) < 2:
        print("Использование: python task_tracker.py [команда] [аргументы]")
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
