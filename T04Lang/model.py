#!/usr/bin/env python3


class Scope(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.dict = dict()

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __getitem__(self, item):
        if item not in self.dict.keys():
            return self.parent[item]
        return self.dict[item]


class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        for command in self.body[:-1]:
            command.evaluate(scope)
        return self.body[-1].evaluate(scope)


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if not self.condition.evaluate(scope).value:
            if not self.if_false:
                return 0
            for false_command in self.if_false[:-1]:
                false_command.evaluate(scope)
            return self.if_false[-1].evaluate(scope)

        if not self.if_true:
            return 0
        for true_command in self.if_true[:-1]:
            true_command.evaluate(scope)
        return self.if_true[-1].evaluate(scope)


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        number_result = self.expr.evaluate(scope)
        print(number_result.value)
        return number_result


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(input())
        return scope[self.name]


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        evaluated_args = list()
        for arg in self.args:
            evaluated_args.append(arg.evaluate(scope))
        call_scope = Scope(scope)
        for name_arg, evaluated_arg in zip(function.args, evaluated_args):
            call_scope[name_arg] = evaluated_arg
        return function.evaluate(call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        replaces = {'/': '//', '&&': 'and', '||': 'or'}
        for replaced, replacing in replaces.items():
            op = op.replace(replaced, replacing)
        self.op = op

    def evaluate(self, scope):
        return Number(eval(str(self.lhs.evaluate(scope).value) + ' ' +
                           self.op + ' ' + str(self.rhs.evaluate(scope).value)))


class UnaryOperation:
    def __init__(self, op, expr):
        if op == '!':
            op = 'not '
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        return Number(eval(self.op + str(self.expr.evaluate(scope).value)))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def my_tests():
    parent = Scope()
    parent['Num1'] = Number(10)
    assert 10 == parent["Num1"].value
    parent['Num2'] = Number(4)
    assert 4 == parent["Num2"].value
    parent['Num3'] = Number(parent['Num2'].value + parent['Num1'].value)
    assert 14 == parent["Num3"].value
    scope = Scope(parent)
    scope['Num4'] = scope['Num2']
    assert scope['Num4'].value == parent["Num2"].value

    function = Function(('hello', 'world'), [Number(10), Number(2)])
    function_definition = FunctionDefinition('NewFunc', function)
    function_definition.evaluate(scope)
    assert scope['NewFunc'] == function

    condition = Conditional(Number(10), [Number(10), Number(12)], [Number(10), scope['NewFunc']])
    result = condition.evaluate(scope)
    assert result.value == 12

    condition = Conditional(Number(0), [Number(10), Number(12)], [Number(10), scope['NewFunc']])
    result = condition.evaluate(scope)
    assert result.value == 2

    print_obj = Print(Number(10))
    assert print_obj.evaluate(scope).value == 10

    print_obj = Print(function)
    assert print_obj.evaluate(scope).value == 2

    read_obj = Read('ReadNum')
    assert read_obj.evaluate(scope).value == scope['ReadNum'].value
    assert read_obj.evaluate(scope).value == scope['ReadNum'].value
    print_obj = Print(scope['ReadNum'])
    print_obj.evaluate(scope)

    assert FunctionCall(FunctionDefinition('foo', function),
                        [Number(1), Number(2)]).evaluate(scope).value == 2

    bin_opt = BinaryOperation(Number(1), '<=', Number(1))
    assert bin_opt.evaluate(scope).value != 0

    un_opt = UnaryOperation('-', Number(-2))
    assert un_opt.evaluate(scope).value == 2


if __name__ == '__main__':
    example()
    my_tests()
