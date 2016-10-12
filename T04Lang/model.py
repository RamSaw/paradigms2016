class Scope(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.d = {}

    def __setitem__(self, key, value):
        self.d[key] = value

    def __getitem__(self, item):
        if item not in self.d:
            return self.parent[item]
        return self.d[item]


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
        if not self.body:
            return Number(0)
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
        if self.condition.evaluate(scope).value:
            if not self.if_true:
                return Number(1)
            for true_command in self.if_true[:-1]:
                true_command.evaluate(scope)
            return self.if_true[-1].evaluate(scope)
        else:
            if not self.if_false:
                return Number(1)
            for false_command in self.if_false[:-1]:
                false_command.evaluate(scope)
            return self.if_false[-1].evaluate(scope)


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
        scope[self.name] = Number(int(input()))
        return scope[self.name]


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for name_arg, arg in zip(function.args, self.args):
            call_scope[name_arg] = arg.evaluate(scope)
        return function.evaluate(call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    operations = {'/': lambda x, y: x // y,
                  '*': lambda x, y: x * y,
                  '+': lambda x, y: x + y,
                  '-': lambda x, y: x - y,
                  '%': lambda x, y: x % y,
                  '==': lambda x, y: int(x == y),
                  '!=': lambda x, y: int(x != y),
                  '<': lambda x, y: int(x < y),
                  '>': lambda x, y: int(x > y),
                  '<=': lambda x, y: int(x <= y),
                  '>=': lambda x, y: int(x >= y),
                  '&&': lambda x, y: x and y,
                  '||': lambda x, y: x or y}

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self, scope):
        return Number(self.operations[self.op]
                      (self.lhs.evaluate(scope).value,
                       self.rhs.evaluate(scope).value))


class UnaryOperation:
    operations = {'-': lambda x: -x,
                  '!': lambda x: int(not x)}

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        return Number(self.operations[self.op]
                     (self.expr.evaluate(scope).value))


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
    # Test scope class
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

    # Test function class
    function = Function(('hello', 'world'), [Number(10), Number(2)])
    function_definition = FunctionDefinition('NewFunc', function)
    function_definition.evaluate(scope)
    assert scope['NewFunc'] == function

    # Test condition class
    condition = Conditional(Number(10), [Number(10), Number(12)],
                            [Number(10), scope['NewFunc']])
    result = condition.evaluate(scope)
    assert result.value == 12

    condition = Conditional(Number(0), [Number(10), Number(12)],
                            [Number(10), scope['NewFunc']])
    result = condition.evaluate(scope)
    assert result.value == 2

    # Test print class
    print("It should print 10:")
    print_obj = Print(Number(10))
    assert print_obj.evaluate(scope).value == 10

    # Test read class
    read_obj = Read('ReadNum')
    print("Input a number: ")
    assert read_obj.evaluate(scope).value == scope['ReadNum'].value
    print("Input a number: ")
    assert read_obj.evaluate(scope).value == scope['ReadNum'].value
    print_obj = Print(scope['ReadNum'])
    print("It should print the last input number: ")
    print_obj.evaluate(scope)

    # Test FunctionCall class
    assert FunctionCall(FunctionDefinition('foo', function),
                        [Number(1), Number(2)]).evaluate(scope).value == 2

    # Test BinaryOperation class
    bin_opt = BinaryOperation(Number(10), '||', Number(2))
    res = bin_opt.evaluate(scope).value
    assert res != 0
    bin_opt = BinaryOperation(Number(10), '==', Number(2))
    res = bin_opt.evaluate(scope).value
    assert res == 0
    bin_opt = BinaryOperation(Number(10), '/', Number(2))
    res = bin_opt.evaluate(scope).value
    assert res == 5

    # Test UnaryOperation class
    un_opt = UnaryOperation('!', Number(10))
    res = un_opt.evaluate(scope).value
    assert res == 0

    # Check empty condition and empty function
    condition = Conditional(Number(0), None, [])
    res = condition.evaluate(scope)
    assert res.value == 1
    condition = Conditional(Number(0), [], None)
    res = condition.evaluate(scope)
    assert res.value == 1
    function = Function([], [])
    res = function.evaluate(scope)
    assert res.value == 0
    print()

    # Check Read class, needed to int
    read_test = Read('Read')
    print("Input a number, will fail if input is 0:")
    read_res = read_test.evaluate(scope)
    condition = Conditional(read_res, [Number(2)], [Number(10)])
    res = condition.evaluate(scope)
    assert res.value == 2

    # Test scope doesn't rewrite values in parent scope
    first_scope = Scope()
    first_scope['num1'] = Number(1)
    first_scope['num2'] = Number(2)
    second_scope = Scope(first_scope)
    second_scope['num1'] = Number(3)
    assert second_scope['num1'].value != first_scope['num1'].value

    # Check that FunctionCall creates new scope
    parent = Scope()
    parent["hello"] = Number(10)
    parent["world"] = Number(20)
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    print('Test new scope. It should print 2, not 30, because created new scope: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)
    print("parent['hello'] + parent['world'] = ",
          parent['hello'].value + parent['world'].value)

if __name__ == '__main__':
    example()
    my_tests()
