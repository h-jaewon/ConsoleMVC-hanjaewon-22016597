from model.todo import Todo


class ConsoleView:
    def render_todo(self, todo: Todo) -> None:
        status = "V" if todo.done else " "
        print(f"  [{status}] {todo.id}. {todo.title}")

    def render_list(self, todos: list[Todo]) -> None:
        if not todos:
            print("  (할 일이 없습니다)")
            return
        for todo in todos:
            self.render_todo(todo)

    def render_success(self, msg: str) -> None:
        print(f"  OK  {msg}")

    def render_error(self, msg: str) -> None:
        print(f"  ERR {msg}")

    def render_help(self) -> None:
        print(
            "\n  사용 가능한 명령:"
            "\n    add <내용>    - 할 일 추가"
            "\n    list          - 목록 보기"
            "\n    done <id>     - 완료 처리"
            "\n    delete <id>   - 삭제"
            "\n    help          - 도움말"
            "\n    quit          - 종료\n"
        )
