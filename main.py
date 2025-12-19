import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Конфигурационный транслятор в TOML")
    parser.add_argument("--input", "-i", required=True, help="Путь к входному файлу")
    parser.add_argument("--output", "-o", required=True, help="Путь к выходному файлу")
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
        # Пока что просто копируем содержимое в выходной файл
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Файл '{args.input}' успешно скопирован в '{args.output}'")
    except FileNotFoundError:
        print(f"Ошибка: файл '{args.input}' не найден", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
