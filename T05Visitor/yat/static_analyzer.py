from model import *

# Class PureCheckVisitor


class PureCheckVisitor:
    def __init__(self):
        pass

    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, tree):
        return True

    def visit_function(self, tree):
        result = True
        if tree.body:
            for command in tree.body:
                result = result and self.visit(command)
        return result

    def visit_function_definition(self, tree):
        return self.visit(tree.function)

    def visit_condition(self, tree):
        result = self.visit(tree.condition)
        if tree.if_true:
            for true_command in tree.if_true:
                result = result and self.visit(true_command)
        if tree.if_false:
            for false_command in tree.if_false:
                result = result and self.visit(false_command)
        return result

    def visit_print(self, tree):
        return False

    def visit_read(self, tree):
        return False

    def visit_function_call(self, tree):
        result = self.visit(tree.fun_expr)
        if tree.args:
            for arg in tree.args:
                result = result and self.visit(arg)
        return result

    def visit_reference(self, tree):
        return True

    def visit_binary_operation(self, tree):
        return self.visit(tree.lhs) and self.visit(tree.rhs)

    def visit_unary_operation(self, tree):
        return self.visit(tree.expr)

# Class NoReturnValueCheckVisitor, returns False if no return.


class NoReturnValueCheckVisitor:
    def __init__(self):
        pass

    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, tree):
        return True

    def visit_function(self, tree):
        if not tree.body:
            return False
        for command in tree.body:
            self.visit(command)
        return self.visit(tree.body[-1])

    def visit_function_definition(self, tree):
        if not self.visit(tree.function):
            print(tree.name)
        return True

    def visit_condition(self, tree):
        result = True
        if tree.if_true:
            result = self.visit(tree.if_true[-1]) & result
            for true_command in tree.if_true:
                self.visit(true_command)
        if tree.if_false:
            result = self.visit(tree.if_false[-1]) & result
            for false_command in tree.if_false:
                self.visit(false_command)
        if not tree.if_true or not tree.if_false:
            return False
        return result

    def visit_print(self, tree):
        return self.visit(tree.expr)

    def visit_read(self, tree):
        return True

    def visit_function_call(self, tree):
        func_result = self.visit(tree.fun_expr)
        if tree.args:
            for arg in tree.args:
                func_result = self.visit(arg) & func_result
        return func_result

    def visit_reference(self, tree):
        return True

    def visit_binary_operation(self, tree):
        res_rhs = self.visit(tree.rhs)
        res_lhs = self.visit(tree.lhs)
        return res_rhs & res_lhs

    def visit_unary_operation(self, tree):
        return self.visit(tree.expr)
