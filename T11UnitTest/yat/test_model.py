import pytest
import sys
from io import *
from model import *


def get_value(number):
    sys.stdout = StringIO()
    Print(number).evaluate(None)
    res = int(sys.stdout.getvalue())
    return res


class TestNumber:
    def test_evaluate(self):
        number_test_obj = Number(666)
        assert number_test_obj == number_test_obj.evaluate(None)


class TestPrint:
    def test_evaluate(self):
        sys.stdout = StringIO()
        Print(Number(13)).evaluate(None)
        assert int(sys.stdout.getvalue()) == 13


class TestScope:
    def test_set_get_item(self):
        scope = Scope()
        scope['Num1'] = Number(666)
        res = get_value(scope['Num1'])
        assert 666 == res

    def test_inheritance(self):
        num1 = Number(666)
        num2 = Number(13)
        parent = Scope()
        scope = Scope(parent)
        parent['num1'] = num1
        parent['num2'] = Number(10)
        scope['num1'] = num2
        assert get_value(scope['num1']) == 13
        assert get_value(parent['num1']) == 666
        assert get_value(scope['num2']) == 10


class TestFunction:
    def test_evaluate_empty_body(self):
        test_function = Function(None, None)
        res = test_function.evaluate(None)
        assert res

    def test_evaluate(self):
        function = Function(('hello', 'world'), [Number(10), Number(2)])
        assert 2 == get_value(function.evaluate(None))


class TestFunctionDefinition:
    def test_evaluate(self):
        scope = Scope()
        function = Function(('hello', 'world'), [Number(10), Number(2)])
        function_definition = FunctionDefinition('NewFunc', function)
        function_definition.evaluate(scope)
        assert scope['NewFunc'] is function


class TestConditional:
    def test_evaluate_empty_body(self):
        test_conditional = Conditional(Number(1), None, None)
        res = test_conditional.evaluate(None)
        assert res

        test_conditional = Conditional(Number(0), None, None)
        res = test_conditional.evaluate(None)
        assert res

    def test_evaluate(self):
        condition = Conditional(Number(10), [Number(10), Number(12)],
                                [Number(10), Number(40)])
        result = condition.evaluate(None)
        assert get_value(result) == 12

        condition = Conditional(Number(0), [Number(10), Number(12)],
                                [Number(10), Number(40)])
        result = condition.evaluate(None)
        assert get_value(result) == 40


class TestRead:
    def test_evaluate(self, monkeypatch):
        scope = Scope()
        monkeypatch.setattr(sys, "stdin", StringIO("30"))
        assert get_value(Read("Num").evaluate(scope)) == 30
        assert get_value(scope["Num"]) == 30


class TestReference:
    def test_evaluate(self):
        scope = Scope()
        scope['Num'] = Number(100)
        assert scope['Num'] is Reference('Num').evaluate(scope)


class TestBinaryOpertation:
    def test_evaluate(self):
        scope = Scope()

        bin_opt = BinaryOperation(Number(10), '||', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res != 0

        bin_opt = BinaryOperation(Number(10), '==', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 0

        bin_opt = BinaryOperation(Number(10), '/', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 5

        bin_opt = BinaryOperation(Number(10), '*', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 20

        bin_opt = BinaryOperation(Number(10), '+', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 12

        bin_opt = BinaryOperation(Number(10), '%', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 0

        bin_opt = BinaryOperation(Number(10), '==', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 0

        bin_opt = BinaryOperation(Number(10), '!=', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 1

        bin_opt = BinaryOperation(Number(10), '>', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 1

        bin_opt = BinaryOperation(Number(10), '<', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 0

        bin_opt = BinaryOperation(Number(10), '<=', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 0

        bin_opt = BinaryOperation(Number(10), '>=', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res == 1

        bin_opt = BinaryOperation(Number(10), '&&', Number(2))
        res = get_value(bin_opt.evaluate(scope))
        assert res != 0


class TestUnaryOperation:
    def test_evaluate(self):
        scope = Scope()

        un_opt = UnaryOperation('-', Number(2))
        res = get_value(un_opt.evaluate(scope))
        assert res == -2

        un_opt = UnaryOperation('!', Number(2))
        res = get_value(un_opt.evaluate(scope))
        assert res == 0

        un_opt = UnaryOperation('!', Number(0))
        res = get_value(un_opt.evaluate(scope))
        assert res == 1


class TestFunctionCall:
    def test_evaluate_simple(self):
        scope = Scope()
        function = Function(('hello', 'world'), [Number(10), Number(2)])
        assert get_value(FunctionCall(FunctionDefinition('foo', function),
                         [Number(1), Number(3)]).evaluate(scope)) == 2

    def test_evaluate(self):
        parent = Scope()
        scope = Scope(parent)
        parent["foo"] = Function(('hello', 'world'),
                                 [BinaryOperation(Reference('hello'),
                                                  '+', Reference('world'))])
        res = FunctionCall(FunctionDefinition('foo', parent['foo']),
                           [Number(5),
                            UnaryOperation('-', Number(3))]).evaluate(scope)
        assert get_value(res) == 2
