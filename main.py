import argparse
import sys
import toml
from parser import parse_config

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

        # Разбор конфигурации
        parsed = parse_config(content)

        # Запись в TOML
        with open(args.output, "w", encoding="utf-8") as f:
            toml.dump(parsed.constants, f)

        print(f"Файл '{args.input}' успешно обработан. Результат записан в '{args.output}'")

    except FileNotFoundError:
        print(f"Ошибка: файл '{args.input}' не найден", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
