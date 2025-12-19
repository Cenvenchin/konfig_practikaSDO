from lark import Lark, Transformer, v_args

grammar = r"""
start: statement*

?statement: const_declare
          | COMMENT

const_declare: NAME ":" value   -> declare
value: NUMBER                    -> number
     | STRING                    -> string
     | array

array: "'" "(" [value (value)*] ")" -> array

COMMENT: /\(\*[\s\S]*?\*\)/

NAME: /[a-z][a-z0-9_]*/
NUMBER: /\d+\.\d*/
STRING: /"([^"\\]|\\.)*"/

%import common.WS
%ignore WS
%ignore COMMENT
"""

@v_args(inline=True)
class ConfigTransformer(Transformer):
    def __init__(self):
        self.constants = {}

    def declare(self, name, value):
        self.constants[str(name)] = value
        return (str(name), value)

    def number(self, token):
        return float(token)

    def string(self, token):
        return str(token)[1:-1]  # убираем кавычки

    def array(self, *values):
        return list(values)

def parse_config(text):
    parser = Lark(grammar, parser='lalr', transformer=ConfigTransformer())
    return parser.parse(text)
