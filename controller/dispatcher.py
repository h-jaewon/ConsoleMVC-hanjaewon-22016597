from model.todo import TodoModel
from view.console import ConsoleView


class Dispatcher:
    def __init__(self):
        self._model = TodoModel()
        self._view = ConsoleView()
        self._commands = {
            "add":    self._handle_add,
            "list":   self._handle_list,
            "done":   self._handle_done,
            "delete": self._handle_delete,
            "help":   self._handle_help,
        }

    def handle(self, raw_input: str) -> None:
        parts = raw_input.strip().split(maxsplit=1)
        if not parts:
            return
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        handler = self._commands.get(cmd)
        if handler:
            handler(arg)
        else:
            self._view.render_error(f"알 수 없는 명령: '{cmd}'  ('help' 입력 시 목록 확인)")

    # --- 개별 명령 핸들러 ---

    def _handle_add(self, arg: str) -> None:
        if not arg:
            self._view.render_error("내용을 입력하세요.  예) add 장보기")
            return
        todo = self._model.add(arg)
        self._view.render_success(f"추가됨 → {todo.title}")

    def _handle_list(self, _: str) -> None:
        self._view.render_list(self._model.list())

    def _handle_done(self, arg: str) -> None:
        id = self._parse_id(arg, "done")
        if id is None:
            return
        todo = self._model.complete(id)
        if todo:
            self._view.render_success(f"완료 처리됨 → {todo.title}")
        else:
            self._view.render_error(f"ID {id} 항목을 찾을 수 없습니다.")

    def _handle_delete(self, arg: str) -> None:
        id = self._parse_id(arg, "delete")
        if id is None:
            return
        todo = self._model.delete(id)
        if todo:
            self._view.render_success(f"삭제됨 → {todo.title}")
        else:
            self._view.render_error(f"ID {id} 항목을 찾을 수 없습니다.")

    def _handle_help(self, _: str) -> None:
        self._view.render_help()

    def _parse_id(self, arg: str, cmd: str) -> int | None:
        try:
            return int(arg)
        except ValueError:
            self._view.render_error(f"ID는 숫자여야 합니다.  예) {cmd} 1")
            return None
