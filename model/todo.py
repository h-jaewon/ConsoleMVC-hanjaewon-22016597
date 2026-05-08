class Todo:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title
        self.done = False


class TodoModel:
    def __init__(self):
        self._todos: dict[int, Todo] = {}
        self._next_id = 1

    def add(self, title: str) -> Todo:
        todo = Todo(self._next_id, title)
        self._todos[self._next_id] = todo
        self._next_id += 1
        return todo

    def list(self) -> list[Todo]:
        return list(self._todos.values())

    def complete(self, id: int) -> Todo | None:
        todo = self._todos.get(id)
        if todo:
            todo.done = True
        return todo

    def delete(self, id: int) -> Todo | None:
        return self._todos.pop(id, None)
