from lark import Lark, Transformer, v_args
from lark.exceptions import LarkError

grammar = r"""
?start: pair+

?pair: NAME ":" value -> assign

?value: NUMBER        -> number
      | STRING        -> string
      | array
      | const_ref

array: "'" "(" value* ")" -> array

const_ref: "@{" NAME "}" -> const_ref

MULTILINE_COMMENT: /\(\*[^*]*(?:\*(?!\))[^*]*)*\*\)/
NAME: /[a-z][a-z0-9_]*/
STRING: /"([^"\\]*(\\.[^"\\]*)*)"/
NUMBER: /\d+(\.\d*)?/

%import common.WS
%ignore WS
%ignore MULTILINE_COMMENT
"""

parser = Lark(grammar, parser='lalr', lexer='standard')


class ConfigTransformer(Transformer):
    def __init__(self):
        self.constants = {}

    def number(self, n):
        return float(n[0])

    def string(self, s):
        # Убираем кавычки и обрабатываем escape-последовательности
        text = str(s[0])
        # Убираем внешние кавычки
        text = text[1:-1]
        # Обрабатываем простые escape-последовательности
        text = text.replace('\\"', '"').replace('\\\\', '\\')
        return text

    def array(self, items):
        return list(items)

    def const_ref(self, items):
        name = str(items[0])
        if name not in self.constants:
            raise ValueError(f"Константа '{name}' не найдена")
        return self.constants[name]

    def assign(self, items):
        key = str(items[0])
        val = items[1]
        self.constants[key] = val
        return key, val


def parse_config(text):
    try:
        tree = parser.parse(text)
        transformer = ConfigTransformer()
        transformer.transform(tree)
        return transformer.constants
    except LarkError as e:
        raise ValueError(f"Синтаксическая ошибка: {str(e)}")
    except ValueError as e:
        raise ValueError(str(e))
