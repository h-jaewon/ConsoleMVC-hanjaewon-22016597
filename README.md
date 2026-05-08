# ConsoleMVC-hanjaewon-22016597

Python으로 구현한 콘솔 기반 Todo 애플리케이션입니다. **MVC(Model-View-Controller)** 패턴을 적용하여 각 역할을 명확하게 분리하였습니다.

---

## 프로젝트 구조

```
mvc-poc/
├── main.py                    # 진입점 (REPL 루프)
├── controller/
│   ├── __init__.py
│   └── dispatcher.py          # Controller: 입력 파싱 및 명령 처리
├── model/
│   ├── __init__.py
│   └── todo.py                # Model: Todo 데이터 및 비즈니스 로직
└── view/
    ├── __init__.py
    └── console.py             # View: 콘솔 출력 담당
```

---

## MVC 구조 설명

### Model — `model/todo.py`

데이터와 비즈니스 로직을 담당합니다.

- **`Todo`** : 할 일 항목 하나를 나타내는 클래스입니다.
  - `id` : 고유 식별자
  - `title` : 할 일 내용
  - `done` : 완료 여부 (기본값 `False`)

- **`TodoModel`** : Todo 항목들을 관리하는 클래스입니다.
  - `add(title)` : 새 Todo를 생성하고 내부 딕셔너리에 저장합니다.
  - `list()` : 저장된 모든 Todo를 리스트로 반환합니다.
  - `complete(id)` : 해당 ID의 Todo를 완료 상태로 변경합니다.
  - `delete(id)` : 해당 ID의 Todo를 삭제합니다.

```python
class Todo:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title
        self.done = False

class TodoModel:
    def add(self, title: str) -> Todo: ...
    def list(self) -> list[Todo]: ...
    def complete(self, id: int) -> Todo | None: ...
    def delete(self, id: int) -> Todo | None: ...
```

---

### View — `view/console.py`

사용자에게 보여줄 출력만을 담당합니다. 데이터를 직접 수정하지 않습니다.

- `render_todo(todo)` : Todo 항목 1개를 `[V] 1. 장보기` 형식으로 출력합니다.
- `render_list(todos)` : 전체 Todo 목록을 출력합니다. 비어있으면 안내 메시지를 출력합니다.
- `render_success(msg)` : 성공 메시지를 `OK  ...` 형식으로 출력합니다.
- `render_error(msg)` : 오류 메시지를 `ERR ...` 형식으로 출력합니다.
- `render_help()` : 사용 가능한 명령어 목록을 출력합니다.

```python
class ConsoleView:
    def render_todo(self, todo: Todo) -> None: ...
    def render_list(self, todos: list[Todo]) -> None: ...
    def render_success(self, msg: str) -> None: ...
    def render_error(self, msg: str) -> None: ...
    def render_help(self) -> None: ...
```

---

### Controller — `controller/dispatcher.py`

사용자 입력을 파싱하여 적절한 Model 메서드를 호출하고, 결과를 View에 전달합니다.

- **`Dispatcher`** : 명령어를 처리하는 컨트롤러 클래스입니다.
  - `handle(raw_input)` : 입력 문자열을 명령어와 인자로 분리하여 해당 핸들러를 호출합니다.
  - `_handle_add(arg)` : `add` 명령 처리 — Model에 Todo 추가
  - `_handle_list(_)` : `list` 명령 처리 — Model에서 목록 조회 후 View에 전달
  - `_handle_done(arg)` : `done` 명령 처리 — Model에서 완료 처리
  - `_handle_delete(arg)` : `delete` 명령 처리 — Model에서 삭제
  - `_handle_help(_)` : `help` 명령 처리 — View에 도움말 출력 요청
  - `_parse_id(arg, cmd)` : 인자를 정수 ID로 변환, 실패 시 오류 출력

```python
class Dispatcher:
    def handle(self, raw_input: str) -> None:
        parts = raw_input.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        handler = self._commands.get(cmd)
        if handler:
            handler(arg)
        else:
            self._view.render_error(f"알 수 없는 명령: '{cmd}'")
```

---

### 진입점 — `main.py`

REPL(Read-Eval-Print Loop) 루프를 실행합니다. 사용자 입력을 읽어 `Dispatcher.handle()`에 전달하며, `quit` / `exit` / `q` 입력 시 종료합니다.

```python
def main() -> None:
    dispatcher = Dispatcher()
    while True:
        raw = input("> ").strip()
        if raw.lower() in ("quit", "exit", "q"):
            break
        dispatcher.handle(raw)
```

---

## 데이터 흐름

```
사용자 입력
    │
    ▼
 main.py  (REPL: 입력 수집)
    │
    ▼
 Dispatcher.handle()  (Controller: 파싱 및 라우팅)
    │
    ├──▶ TodoModel  (Model: 데이터 변경/조회)
    │         │
    │         └── 결과 반환
    │
    └──▶ ConsoleView  (View: 결과 출력)
```

---

## 실행 방법

```bash
python main.py
```

## 사용 가능한 명령어

| 명령어 | 설명 | 예시 |
|---|---|---|
| `add <내용>` | 할 일 추가 | `add 장보기` |
| `list` | 전체 목록 보기 | `list` |
| `done <id>` | 완료 처리 | `done 1` |
| `delete <id>` | 항목 삭제 | `delete 2` |
| `help` | 도움말 | `help` |
| `quit` | 종료 | `quit` |

## 실행 예시

```
=== Todo REPL  [MVC 구조] ===
'help' 를 입력하면 명령 목록을 볼 수 있습니다.

> add 장보기
  OK  추가됨 → 장보기

> add 과제 제출
  OK  추가됨 → 과제 제출

> list
  [ ] 1. 장보기
  [ ] 2. 과제 제출

> done 1
  OK  완료 처리됨 → 장보기

> list
  [V] 1. 장보기
  [ ] 2. 과제 제출

> delete 2
  OK  삭제됨 → 과제 제출

> quit
종료합니다.
```
