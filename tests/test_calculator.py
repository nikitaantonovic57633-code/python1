import pytest

from toolkit.calculator import calculate, tokenize
from toolkit.errors import CalculatorError


# Поддержать целые и вещественные числа.
def test_tokenize():
    assert tokenize("2 + 3 * 4") == ["2", "+", "3", "*", "4"]
    assert tokenize("1.23") == ["1.23"]


# Поддержать +, -, *, /.
# Соблюдать приоритет * и / над + и -.
def test_priority():
    assert calculate("1 - 2 * 2 / 4") == 0
    assert calculate("2 + 3 * 4") == 14


# Поддержать целые и вещественные числа.
def test_calc():
    assert calculate("1 * 2 - 3") == -1
    assert calculate("2+2") == 4
    assert calculate("10/4") == 2.5
    assert calculate("10/2") == 5.0


# Поддержать унарный + и - перед числом.
def test_unary():
    assert calculate("-1") == -1
    assert calculate("+2") == 2
    assert calculate("1+-2") == -1
    assert calculate("-2*-3") == 6


# Игнорировать пробелы между токенами.
def test_space():
    assert calculate("  1   +   2 * 3  ") == 7


# Пустое выражение.
def test_empty():
    with pytest.raises(CalculatorError):
        calculate("")


# Недопустимый символ.
def test_char():
    with pytest.raises(CalculatorError):
        calculate("2+a")
    with pytest.raises(CalculatorError):
        calculate("2@3")


# Пропущенный операнд.
def test_operand():
    with pytest.raises(CalculatorError):
        calculate("1 +")


# Два бинарных оператора подряд.
def test_two_operators():
    with pytest.raises(CalculatorError):
        calculate("2*/3")


# Деление на ноль.
def test_zero():
    with pytest.raises(CalculatorError):
        calculate("1/0")