import pytest
import sys
from io import *
from model import *


def get_value(number):
    sys.stdout = StringIO()
    Print(number).evaluate({})
    res = int(sys.stdout.getvalue())
    return res


class TestNumber:
    def test_evaluate(self):
        number_test_obj = Number(666)
        assert number_test_obj is number_test_obj.evaluate({})
        assert get_value(number_test_obj) == 666


class TestPrint:
    def test_evaluate(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        Print(Number(13)).evaluate({})
        assert sys.stdout.getvalue() == "13\n"


class TestScope:
    def test_set_get_item(self):
        scope = Scope()
        scope['Num1'] = Number(666)
        res = get_value(scope['Num1'])
        assert 666 == res

        parent = Scope()
        parent['Num1'] = Number(10)
        parent['Num2'] = Number(4)
        scope = Scope(parent)
        scope['Num4'] = scope['Num2']
        assert get_value(parent["Num2"]) == 4
        assert get_value(scope['Num4']) == 4

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

    def test_inheritance_equality_of_variables(self):
        first_scope = Scope()
        first_scope['num1'] = Number(1)
        first_scope['num2'] = Number(2)
        second_scope = Scope(first_scope)
        second_scope['num1'] = Number(3)
        assert get_value(second_scope['num1']) == 3
        assert get_value(first_scope['num1']) == 1


class TestFunction:
    def test_evaluate_empty_body(self):
        test_function = Function([], [])
        test_function.evaluate({})

    def test_evaluate(self):
        function = Function(('hello', 'world'), [Number(10), Number(2)])
        assert 2 == get_value(function.evaluate({}))


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
        test_conditional.evaluate({})

        test_conditional = Conditional(Number(0), None, None)
        test_conditional.evaluate({})

        test_conditional = Conditional(Number(1), [], [])
        test_conditional.evaluate({})

        test_conditional = Conditional(Number(0), [], [])
        test_conditional.evaluate({})

    def test_evaluate_true(self):
        condition = Conditional(Number(10), [Number(10), Number(12)],
                                [Number(10), Number(40)])
        result = condition.evaluate({})
        assert get_value(result) == 12

    def test_evaluate_false(self):
        condition = Conditional(Number(0), [Number(10), Number(12)],
                                [Number(10), Number(40)])
        result = condition.evaluate({})
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
    def test_evaluate_or(self):
        bin_opt = BinaryOperation(Number(10), '||', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert res

    def test_evaluate_equal(self):
        scope = Scope()

        bin_opt = BinaryOperation(Number(10), '==', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert not res

    def test_evaluate_dividing(self):
        bin_opt = BinaryOperation(Number(10), '/', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert res == 5

    def test_evaluate_multiplication(self):
        bin_opt = BinaryOperation(Number(10), '*', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert res == 20

    def test_evaluate_sum(self):
        bin_opt = BinaryOperation(Number(10), '+', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert res == 12

    def test_evaluate_mod(self):
        bin_opt = BinaryOperation(Number(10), '%', Number(3))
        res = get_value(bin_opt.evaluate({}))
        assert res == 1

    def test_evaluate_not_equal(self):
        bin_opt = BinaryOperation(Number(10), '!=', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert res

    def test_evaluate_more(self):
        bin_opt = BinaryOperation(Number(10), '>', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert res

    def test_evaluate_less(self):
        bin_opt = BinaryOperation(Number(10), '<', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert not res

    def test_evaluate_not_more(self):
        bin_opt = BinaryOperation(Number(10), '<=', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert not res

    def test_evaluate_not_less(self):
        bin_opt = BinaryOperation(Number(10), '>=', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert res

    def test_evaluate_and(self):
        bin_opt = BinaryOperation(Number(10), '&&', Number(2))
        res = get_value(bin_opt.evaluate({}))
        assert res


class TestUnaryOperation:
    def test_evaluate_invert_number(self):
        un_opt = UnaryOperation('-', Number(2))
        res = get_value(un_opt.evaluate({}))
        assert res == -2

    def test_evaluate_not_true(self):
        un_opt = UnaryOperation('!', Number(2))
        res = get_value(un_opt.evaluate({}))
        assert not res

    def test_evaluate_not_false(self):
        un_opt = UnaryOperation('!', Number(0))
        res = get_value(un_opt.evaluate({}))
        assert res


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

    def test_creating_new_scope(self):
        scope = Scope()
        parent = Scope()
        scope["hello"] = Number(10)
        scope["world"] = Number(20)
        parent["foo"] = Function(('hello', 'world'),
                                 [Print(BinaryOperation(Reference('hello'),
                                                        '+',
                                                        Reference('world')))])
        FunctionCall(FunctionDefinition('foo', parent['foo']),
                     [Number(5),
                      UnaryOperation('-', Number(3))]).evaluate(scope)
        assert get_value(scope['hello']) == 10
        assert get_value(scope['world']) == 20
