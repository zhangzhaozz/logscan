__author__ = 'zhangzhao'

from queue import Queue
import threading
import logging
import re


class Token:
    LEFT_BRACKETS = 'LEFT_BRACKETS'
    RIGHT_BRACKETS = 'RIGHT_BRACKETS'
    SYMBOL = 'SYMBOL'
    EXPRESSION = 'EXPRESSION'
    SYMBOLS = '&!|'

    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return '{0}<{1}>'.format(self.value, self.type)

    def __repr__(self):
        return self.__str__()

# 定义AST树类
class ASTree:
    def __init__(self, token):
        self.root = token
        self.left = None
        self.right = None

    # 层序遍历
    def visit(self):
        ret = []
        q = Queue()
        q.put(self)
        while not q.empty():
            t = q.get()
            ret.append(t.root)
            if t.left:
                q.put(t.left)
            if t.right:
                q.put(t.right)
        return ret

# 定义生成tokenzie函数
def tokenize(origin):
    tokens = []
    expr = []
    is_expr = False
    for c in origin:
        if c == '#':
            if not is_expr:
                is_expr = True
            else:
                is_expr = False
                token = Token(''.join(expr), Token.EXPRESSION)
                tokens.append(token)
                expr = []
        elif c in Token.SYMBOLS and not is_expr:
            token = Token(c, Token.SYMBOL)
            tokens.append(token)
        elif c == '(' and not is_expr:
            token = Token(c, Token.LEFT_BRACKETS)
            tokens.append(token)
        elif c == ')' and not is_expr:
            token = Token(c, Token.RIGHT_BRACKETS)
            tokens.append(token)
        elif is_expr:
            expr.append(c)
    return tokens

# 定义生成子树函数
def make_sub_ast(stack, t):
    current = t
    while stack and stack[-1].root.type != Token.LEFT_BRACKETS:
        node = stack.pop()
        if node.root.type != Token.SYMBOL:
            raise Exception('parse error, excepted {0} but {1}'.format(Token.SYMBOL, node.root))
        node.right = current
        if node.root.value == '&' or node.root.value == '|':
            left = stack.pop()
            if left.root.type != Token.SYMBOL and left.root.type != Token.EXPRESSION:
                raise Exception('parse error, excepted {0} or {1} but {2}'.format(Token.SYMBOL,
                                                                                  Token.EXPRESSION, left.root))
            node.left = left
        current = node
    stack.append(current)


# 定义生成树函数
def make_ast(tokens):
    stack = []
    for t in tokens:
        tree = ASTree(t)
        if tree.root.type == Token.SYMBOL or tree.root.type == Token.LEFT_BRACKETS:
            stack.append(tree)
        elif tree.root.type == Token.EXPRESSION:
            # 如果是表达式,调用生成子树函数
            make_sub_ast(stack, tree)
        else:
            sub_tree = stack.pop()
            if sub_tree.root.type != Token.SYMBOL and sub_tree.root.type != Token.EXPRESSION:
                raise Exception('parse error, excepted {0} or {1} but {2}'.format(Token.SYMBOL,
                                                                                  Token.EXPRESSION, sub_tree.root))

            tmp = stack.pop()
            if tmp.root.type != Token.LEFT_BRACKETS:
                raise Exception('parser error, excepted {0} but {1}'.format(Token.LEFT_BRACKETS, tmp))
            make_sub_ast(stack, sub_tree)
    return stack.pop()

# 定义运算函数
def cacl(ast, line):
    if ast.root.type != Token.EXPRESSION:
        if ast.root.value == '!':
            return not cacl(ast.right, line)
        if ast.root.value == '&':
            return cacl(ast.left, line) and cacl(ast.right, line)
        if ast.root.value == '|':
            return cacl(ast.left, line) or cacl(ast.right, line)
    else:
        return re.search(ast.root.value, line) is not None

# 调用以上类和方法,返回匹配结果bool值
class Matcher:
    def __init__(self, name, origin):
        self.name = name
        self.origin = origin
        self.ast = make_ast(tokenize(origin))

    # 定义match方法
    def match(self, line):
        return cacl(self.ast, line)


if __name__ == '__main__':
    e = '#test# & #abc# | (!#123# | #456#)'
    s = 'test cdf 123 156'
    # print(tokenize(e))
    # print([str(x) for x in tokenize(e)])
    # for t in tokenize(e):
    #     print(t)

    # ast = make_ast(tokenize(e))
    # # print(ast.visit())
    # print(cacl(ast, s))

    m = Matcher(e)
    print(m.match(s))
