import pytest
from config_parser import parse_config


def test_number():
    cfg = parse_config("a: 123")
    assert cfg['a'] == 123.0


def test_decimal_number():
    cfg = parse_config("a: 123.45")
    assert cfg['a'] == 123.45


def test_string():
    cfg = parse_config('a: "hello"')
    assert cfg['a'] == "hello"


def test_string_with_escape():
    cfg = parse_config('a: "hello\\"world"')
    assert cfg['a'] == 'hello"world'


def test_array():
    cfg = parse_config("arr: '(1 2 3)")
    assert cfg['arr'] == [1.0, 2.0, 3.0]


def test_array_with_strings():
    cfg = parse_config('arr: \'("hello" "world" "test")')
    assert cfg['arr'] == ["hello", "world", "test"]


def test_array_with_mixed_types():
    cfg = parse_config('arr: \'(1 "two" 3.5)')
    assert cfg['arr'] == [1.0, "two", 3.5]


def test_const_reference():
    cfg = parse_config("a: 10\nb: @{a}")
    assert cfg['b'] == 10.0


def test_const_reference_in_array():
    cfg = parse_config("base: 10\narr: '(@{base} 20 30))")
    assert cfg['arr'] == [10.0, 20.0, 30.0]


def test_multiline_comment():
    cfg = parse_config("""
    (* This is a
       multiline comment *)
    a: 5
    """)
    assert cfg['a'] == 5.0


def test_multiple_consts():
    cfg = parse_config("""
    a: 1.0
    b: 2.0
    c: @{a}
    """)
    assert cfg['c'] == 1.0


def test_nested_const_reference():
    cfg = parse_config("""
    a: 10
    b: @{a}
    c: @{b}
    """)
    assert cfg['c'] == 10.0


def test_nested_array():
    cfg = parse_config("inner: '((1 2) (3 4))")
    # Вложенные массивы
    assert cfg['inner'] == [[1.0, 2.0], [3.0, 4.0]]


def test_array_with_const_ref():
    cfg = parse_config("""
    base: 10
    arr: '(@{base} 20 30))
    """)
    assert cfg['arr'] == [10.0, 20.0, 30.0]


def test_lowercase_names_only():
    # Имена должны быть только в нижнем регистре
    cfg = parse_config("test_name: 123")
    assert cfg['test_name'] == 123.0


def test_error_undefined_constant():
    with pytest.raises(ValueError, match="Константа 'x' не найдена"):
        parse_config("a: @{x}")


def test_error_syntax():
    with pytest.raises(ValueError):
        parse_config("a: @{")  # Незакрытая константа


def test_empty_array():
    cfg = parse_config("arr: '()")
    assert cfg['arr'] == []


def test_complex_example():
    cfg = parse_config("""
    (* Конфигурация сервера *)
    port: 8080
    host: "localhost"
    timeout: 30.5

    (* Массив портов *)
    ports: '(8080 8081 8082)

    (* Использование константы *)
    port_value: @{port}
    host_value: @{host}
    """)
    assert cfg['port'] == 8080.0
    assert cfg['host'] == "localhost"
    assert cfg['timeout'] == 30.5
    assert cfg['ports'] == [8080.0, 8081.0, 8082.0]
    assert cfg['port_value'] == 8080.0
    assert cfg['host_value'] == "localhost"
