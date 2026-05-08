from controller.dispatcher import Dispatcher


def main() -> None:
    dispatcher = Dispatcher()
    print("=== Todo REPL  [MVC 구조] ===")
    print("'help' 를 입력하면 명령 목록을 볼 수 있습니다.")

    while True:
        try:
            raw = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n종료합니다.")
            break

        if not raw:
            continue
        if raw.lower() in ("quit", "exit", "q"):
            print("종료합니다.")
            break

        dispatcher.handle(raw)  # Read → Eval(Controller→Model) → Print(View)


if __name__ == "__main__":
    main()
