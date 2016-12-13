import model


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
