import sys
import ply.lex as lex
import ply.yacc as yacc

# sbml AST
# Shawn Li 110807126

indent_level = 0


class Node():
    def __init__(self, parent=None, lineno=0, colno=0):
        self.parent = parent
        self.lineno = lineno
        self.colno = colno
        self.ret_val = 'undefined'


class Statement(Node):
    def __init__(self, parent=None, lineno=0, colno=0, statement=None, next_statement=None):
        super().__init__(parent, lineno, colno)
        self.statement = statement
        self.next_statement = next_statement

    def __str__(self):
        r = "List_Node:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Statement:  " + str(self.statement)
        r += "\n" + ("  " * indent_level) + "Next_Statement:  " + str(self.next_statement)
        indent_level -= 1
        return r


class Name(Node):
    def __init__(self, parent=None, lineno=0, colno=0, called=None):
        super().__init__(parent, lineno, colno)
        self.called = called

    def __str__(self):
        r = "Name:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Called: " + str(self.called)
        indent_level -= 1
        return r


class Assignment(Node):
    def __init__(self, parent=None, lineno=0, colno=0, name=None, assigned=None):
        super().__init__(parent, lineno, colno)
        self.name = name
        self.assigned = assigned

    def __str__(self):
        r = "Assignment:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Name:  " + str(self.name)
        r += "\n" + ("  " * indent_level) + "Assigned:  " + str(self.assigned)
        indent_level -= 1
        return r


class If_Statement(Node):
    def __init__(self, parent=None, lineno=0, colno=0, condition=None, true_statement=None):
        super().__init__(parent, lineno, colno)
        self.condition = condition
        self.true_statement = true_statement

    def __str__(self):
        r = "If_Statement:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "condition:  " + str(self.condition)
        r += "\n" + ("  " * indent_level) + "true_statement:  " + str(self.true_statement)
        indent_level -= 1
        return r


class If_Else_Statement(Node):
    def __init__(self, parent=None, lineno=0, colno=0, condition=None, true_statement=None, false_statement=None):
        super().__init__(parent, lineno, colno)
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement

    def __str__(self):
        r = "If_Else_Statement:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "condition:  " + str(self.condition)
        r += "\n" + ("  " * indent_level) + "true_statement:  " + str(self.true_statement)
        r += "\n" + ("  " * indent_level) + "false_statement:  " + str(self.false_statement)
        indent_level -= 1
        return r


class While_Loop(Node):
    def __init__(self, parent=None, lineno=0, colno=0, condition=None, true_statement=None):
        super().__init__(parent, lineno, colno)
        self.condition = condition
        self.true_statement = true_statement

    def __str__(self):
        r = "While_Loop:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "condition:  " + str(self.condition)
        r += "\n" + ("  " * indent_level) + "true_statement:  " + str(self.true_statement)
        indent_level -= 1
        return r


class Print_Statement(Node):
    def __init__(self, parent=None, lineno=0, colno=0, parameter=None):
        super().__init__(parent, lineno, colno)
        self.parameter = parameter

    def __str__(self):
        r = "Parameter:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Parameter:  " + str(self.parameter)
        indent_level -= 1
        return r


class Negation(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def __str__(self):
        r = "Negation:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Child:  " + str(self.child)
        indent_level -= 1
        return r


class My_None(Node):
    def __init__(self, parent=None, lineno=0, colno=0):
        super().__init__(parent, lineno, colno)
        self.child = None

    def __str__(self):
        r = "None:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Value:  " + str(self.child)
        indent_level -= 1
        return r


class Integer(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def __str__(self):
        r = "Integer:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Child: " + str(self.child)
        indent_level -= 1
        return r


class Real(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def __str__(self):
        r = "Real:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Child: " + str(self.child)
        indent_level -= 1
        return r


class String(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child

    def __str__(self):
        r = "String:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Child: " + str(self.child)
        indent_level -= 1
        return r


class Boolean(Node):
    def __init__(self, parent=None, lineno=0, colno=0, child=None):
        super().__init__(parent, lineno, colno)
        self.child = child
        self.ret_val = 'bool'

    def __str__(self):
        r = "Boolean:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Child: " + str(self.child)
        indent_level -= 1
        return r


class List_Node(Node):
    def __init__(self, parent=None, lineno=0, colno=0, element=None, list_tail=None):
        super().__init__(parent, lineno, colno)
        self.element = element
        self.list_tail = list_tail

    def __str__(self):
        r = "List_Node:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Element:  " + str(self.element)
        r += "\n" + ("  " * indent_level) + "List_Tail:  " + str(self.list_tail)
        indent_level -= 1
        return r


class Tuple_Node(Node):
    def __init__(self, parent=None, lineno=0, colno=0, element=None, tuple_tail=None):
        super().__init__(parent, lineno, colno)
        self.element = element
        self.tuple_tail = tuple_tail

    def __str__(self):
        r = "Tuple_Node:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Element:  " + str(self.element)
        r += "\n" + ("  " * indent_level) + "Tuple_Tail:  " + str(self.tuple_tail)
        indent_level -= 1
        return r


class Addition(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def __str__(self):
        r = "Addition:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Subtraction(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def __str__(self):
        r = "Subtraction:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Multiplication(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def __str__(self):
        r = "Multiplication:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Division(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def __str__(self):
        r = "Division:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Exponentiation(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def __str__(self):
        r = "Exponentiation:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Modulus(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def __str__(self):
        r = "Modulus:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Intdivision(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right

    def __str__(self):
        r = "Intdivision:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class List_Indexing(Node):
    def __init__(self, parent=None, lineno=0, colno=0, list_node=None, index=None):
        super().__init__(parent, lineno, colno)
        self.list_node = list_node
        self.index = index

    def __str__(self):
        r = "List_Indexing:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "List_Node:  " + str(self.list_node)
        r += "\n" + ("  " * indent_level) + "Index:  " + str(self.index)
        indent_level -= 1
        return r


class Tuple_Indexing(Node):
    def __init__(self, parent=None, lineno=0, colno=0, index=None, tuple_node=None):
        super().__init__(parent, lineno, colno)
        self.index = index
        self.tuple_node = tuple_node

    def __str__(self):
        r = "Tuple_Indexing:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Index:  " + str(self.index)
        r += "\n" + ("  " * indent_level) + "Tuple_Node:  " + str(self.tuple_node)
        indent_level -= 1
        return r


class Member(Node):
    def __init__(self, parent=None, lineno=0, colno=0, element=None, list_node=None):
        super().__init__(parent, lineno, colno)
        self.element = element
        self.list_node = list_node
        self.ret_val = 'bool'

    def __str__(self):
        r = "Member:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Element:  " + str(self.element)
        r += "\n" + ("  " * indent_level) + "List_Node:  " + str(self.list_node)
        indent_level -= 1
        return r


class Cons(Node):
    def __init__(self, parent=None, lineno=0, colno=0, element=None, list_node=None):
        super().__init__(parent, lineno, colno)
        self.element = element
        self.list_node = list_node

    def __str__(self):
        r = "Cons:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Element:  " + str(self.element)
        r += "\n" + ("  " * indent_level) + "List_Node:  " + str(self.list_node)
        indent_level -= 1
        return r


class Conjunction(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        self.ret_val = 'bool'

    def __str__(self):
        r = "Conjunction:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Disjunction(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        self.ret_val = 'bool'

    def __str__(self):
        r = "Disjunction:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Equal(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        self.ret_val = "bool"

    def __str__(self):
        r = "Equal:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Nequal(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        self.ret_val = 'bool'

    def __str__(self):
        r = "Nequal:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Gte(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        self.ret_val = 'bool'

    def __str__(self):
        r = "Gte:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Gt(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        self.ret_val = 'bool'

    def __str__(self):
        r = "Gt:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Lte(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        self.ret_val = 'bool'

    def __str__(self):
        r = "Lte:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r


class Lt(Node):
    def __init__(self, parent=None, lineno=0, colno=0, left=None, right=None):
        super().__init__(parent, lineno, colno)
        self.left = left
        self.right = right
        self.ret_val = 'bool'

    def __str__(self):
        r = "Lt:"
        global indent_level
        indent_level += 1
        r += "\n" + ("  " * indent_level) + "Left:  " + str(self.left)
        r += "\n" + ("  " * indent_level) + "Right:  " + str(self.right)
        indent_level -= 1
        return r

# Tokenizer, Parser, Evaluator

# Token Names


reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE'
}


tokens = (
    'INT_VAL',
    'REAL_VAL',
    'BOOLEAN',
    'STRING',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'SEMICOLON',
    'INDEXTUPES',
    'EXPONENTIATION',
    'MULTIPLICATION',
    'DIVISION',
    'INTDIVISION',
    'MODULUS',
    'ADDITION',
    'SUBTRACTION',
    'MEMBER',
    'CONS',
    'NEGATION',
    'CONJUNCTION',
    'DISJUNCTION',
    'LTE',
    'NEQUAL',
    'LT',
    'EQUAL',
    'GTE',
    'GT',
    'ASSIGN',
    'PRINT',
    'NAME',
) + tuple(reserved.values())

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_INDEXTUPES = r'\#'
t_EXPONENTIATION = r'\*{2}'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_ADDITION = r'\+'
t_SUBTRACTION = r'-'
t_CONS = r'\:{2}'

t_LTE = r'<='
t_NEQUAL = r'<>'
t_LT = r'<'
t_EQUAL = r'=='
t_GTE = r'>='
t_GT = r'>'
t_ASSIGN = r'='
t_ignore = ' \t'


def t_INTDIVISION(t): 
    r'div'
    return t


def t_MODULUS(t): 
    r'mod'
    return t


def t_MEMBER(t): 
    r'in'
    return t


def t_NEGATION(t): 
    r'not'
    return t


def t_CONJUNCTION(t): 
    r'andalso'
    return t


def t_DISJUNCTION(t):
    r'orelse'
    return t


def t_PRINT(t):
    r'print'
    return t


def t_STRING(t):
    r'(\"[^"]*\")|(\'[^\']*\')'
    t.value = t.value[1:-1]
    return t


def t_REAL_VAL(t):
    r'(?=\.\d|\d)(?:0|[1-9]\d*)?(?:\.\d*)?(?:\d[eE][+\-]?\d+)|(\d*(\.\d|\d\.)\d*)'
    t.value = float(t.value)
    return t


def t_INT_VAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r'True|False'
    t.value = t.value == 'True'
    return t


def t_NAME(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("SYNTAX ERROR: %s at %d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)


lexer = lex.lex()

precedence = (
    ('left', 'DISJUNCTION'),
    ('left', 'CONJUNCTION'),
    ('left', 'GT', 'GTE', 'EQUAL', 'NEQUAL', 'LTE', 'LT'),
    ('left', 'NEGATION'),
    ('left', 'MEMBER'),
    ('left', 'SUBTRACTION', 'ADDITION'),
    ('left', 'MODULUS', 'INTDIVISION', 'DIVISION', 'MULTIPLICATION'),
    ('right', 'CONS'),
    ('right', 'EXPONENTIATION'),
    ('right', 'INDEXTUPES'),
    ('left', 'LBRACKET'),
    ('left', 'LPAREN'),
    ('right', 'UMINUS'),
)


def p_start(t):
    '''
    start : statement-list
          | block
    '''
    run(t[1])


def p_block(t):
    'block : LBRACE statement-list RBRACE'
    t[0] = t[2]


def p_statement_list(t):
    '''
    statement-list : statement statement-list
    '''
    t[0] = Statement(None, t.lineno, t.lexpos, t[1], t[2])
    t[1].parent = t[0]
    t[2].parent = t[0]


def p_statement_list_empty(t):
    'statement-list : empty'
    t[0] = t[1]


def p_statement_expression(t):
    '''
    statement : expression SEMICOLON
              | var_assign SEMICOLON
    '''
    t[0] = t[1]


def p_statement_while(t):
    'statement : WHILE LPAREN expression RPAREN block'
    t[0] = While_Loop(None, t.lineno, t.lexpos, t[3], t[5])
    t[3].parent = t[0]
    t[5].parent = t[0]


def p_statement_else(t):
    'statement : IF LPAREN expression RPAREN block ELSE block'
    t[0] = If_Else_Statement(None, t.lineno, t.lexpos, t[3], t[5], t[7])
    t[3].parent = t[0]
    t[5].parent = t[0]
    t[7].parent = t[0]


def p_statement_if(t):
    'statement : IF LPAREN expression RPAREN block'
    t[0] = If_Statement(None, t.lineno, t.lexpos, t[3], t[5])
    t[3].parent = t[0]
    t[5].parent = t[0]


def p_print_call(t):
    'expression : PRINT LPAREN expression RPAREN'
    t[0] = Print_Statement(None, t.lineno, t.lexpos, t[3])
    t[3].parent = t[0]


def p_var_assign_expression(t):
    'var_assign : expression ASSIGN expression'
    t[0] = Assignment(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_tuple_indexing(t):
    'expression : INDEXTUPES expression LPAREN tuple RPAREN'
    t[0] = Tuple_Indexing(None, t.lineno, t.lexpos, t[2], t[4])
    t[2].parent = t[0]
    t[4].parent = t[0]


def p_expression_tuple(t):
    'expression : LPAREN tuple RPAREN'
    t[0] = t[2]


def p_tuple(t):
    '''
    tuple : expression COMMA tuple
    '''
    t[0] = Tuple_Node(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_tuple_none(t):
    '''
    tuple : empty
    '''
    t[0] = t[1]


def p_list_indexing(t):
    'expression : expression LBRACKET expression RBRACKET'
    t[0] = List_Indexing(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_list(t):
    'expression : LBRACKET list RBRACKET'
    t[0] = t[2]


def p_list(t):
    '''
    list : expression list_tail
    '''
    t[0] = List_Node(None, t.lineno, t.lexpos, t[1], t[2])
    t[1].parent = t[0]
    t[2].parent = t[0]


def p_list_none(t):
    '''
    list : empty
    '''
    t[0] = t[1]


def p_list_tail(t):
    '''
    list_tail : COMMA expression list_tail
    '''
    t[0] = List_Node(None, t.lineno, t.lexpos, t[2], t[3])
    t[2].parent = t[0]
    t[3].parent = t[0]


def p_list_tail_none(t):
    '''
    list_tail : empty
    '''
    t[0] = t[1]


def p_empty(t):
    '''
    empty :
    '''
    t[0] = My_None(None, t.lineno, t.lexpos)


def p_expression_int(t):
    '''
    expression : INT_VAL
    '''
    t[0] = Integer(None, t.lineno, t.lexpos, t[1])


def p_expression_real(t):
    '''
    expression : REAL_VAL
    '''
    t[0] = Real(None, t.lineno, t.lexpos, t[1])


def p_expression_string(t):
    '''
    expression : STRING
    '''
    t[0] = String(None, t.lineno, t.lexpos, t[1])


def p_expression_boolean(t):
    '''
    expression : BOOLEAN
    '''
    t[0] = Boolean(None, t.lineno, t.lexpos, t[1])


def p_expression_name(t):
    'expression : NAME'
    t[0] = Name(None, t.lineno, t.lexpos, t[1])


def p_expression_addition(t):
    'expression : expression ADDITION expression'
    t[0] = Addition(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_subtraction(t):
    'expression : expression SUBTRACTION expression'
    t[0] = Subtraction(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_uminus(t):
    'expression : SUBTRACTION expression %prec UMINUS'
    t[2].child = -t[2].child
    t[0] = t[2]


def p_expression_multiplication(t):
    'expression : expression MULTIPLICATION expression'
    t[0] = Multiplication(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_division(t):
    'expression : expression DIVISION expression'
    t[0] = Division(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_exponentiation(t):
    'expression : expression EXPONENTIATION expression'
    t[0] = Exponentiation(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_modulus(t):
    'expression : expression MODULUS expression'
    t[0] = Modulus(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_intdivision(t):
    'expression : expression INTDIVISION expression'
    t[0] = Intdivision(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_member(t):
    'expression : expression MEMBER expression'
    t[0] = Member(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_cons(t):
    'expression : expression CONS expression'
    t[0] = Cons(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_conjunction(t):
    'expression : expression CONJUNCTION expression'
    t[0] = Conjunction(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_disjunction(t):
    'expression : expression DISJUNCTION expression'
    t[0] = Disjunction(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_equal(t):
    'expression : expression EQUAL expression'
    t[0] = Equal(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_nequal(t):
    'expression : expression NEQUAL expression'
    t[0] = Nequal(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_gte(t):
    'expression : expression GTE expression'
    t[0] = Gte(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_gt(t):
    'expression : expression GT expression'
    t[0] = Gt(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_lte(t):
    'expression : expression LTE expression'
    t[0] = Lte(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_lt(t):
    'expression : expression LT expression'
    t[0] = Lt(None, t.lineno, t.lexpos, t[1], t[3])
    t[1].parent = t[0]
    t[3].parent = t[0]


def p_expression_negation(t):
    'expression : NEGATION expression'
    t[0] = Negation(None, t.lineno, t.lexpos, t[2])
    t[2].parent = t[0]


def p_expression_parenthetical(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]


def p_error(t):
    print("SYNTAX ERROR")


parser = yacc.yacc()
env = {}


def run(p):
    global env
    try:
        if type(p) == Statement:
            run(p.statement)
            if (type(p.next_statement) != My_None):
                run(p.next_statement)
        if type(p) == While_Loop:
            while (run(p.condition)):
                run(p.true_statement)
        if type(p) == If_Else_Statement:
            if (run(p.condition)):
                run(p.true_statement)
            else:
                run(p.false_statement)
        if type(p) == If_Statement:
            if (run(p.condition)):
                run(p.true_statement)
        if type(p) == Print_Statement:
            print(run(p.parameter))
        if type(p) == Name:
            return env[p.called]
        if type(p) == Assignment:
            if (type(p.name) == List_Indexing):
                (run(p.name.list_node))[run(p.name.index)] = run(p.assigned)
            else:
                env[p.name.called] = run(p.assigned)
        if type(p) == Integer or \
           type(p) == Real or \
           type(p) == String or \
           type(p) == Boolean:
            return p.child
        if type(p) == Tuple_Node:
            if type(p.tuple_tail) == My_None:
                return (run(p.element),)
            else:
                return (run(p.element),) + run(p.tuple_tail)
        if type(p) == List_Node:
            if type(p.list_tail) == My_None:
                return [run(p.element)]
            else:
                return [run(p.element)] + run(p.list_tail)
        if type(p) == Equal:
            return run(p.left) == run(p.right)
        if type(p) == Nequal:
            return run(p.left) != run(p.right)
        if type(p) == Lt:
            return run(p.left) < run(p.right)
        if type(p) == Lte:
            return run(p.left) <= run(p.right)
        if type(p) == Gt:
            return run(p.left) > run(p.right)
        if type(p) == Gte:
            return run(p.left) >= run(p.right)
        if type(p) == List_Indexing:
            return (run(p.list_node))[run(p.index)]
        if type(p) == Tuple_Indexing:
            return (run(p.tuple_node))[run(p.index)]
        if type(p) == Cons:
            return [run(p.element)] + run(p.list_node)
        if type(p) == Conjunction:
            return run(p.left) and run(p.right)
        if type(p) == Disjunction:
            return run(p.left) or run(p.right)
        if type(p) == Member:
            return run(p.left) in run(p.right)
        if type(p) == Addition:
            if (type(run(p.left)) == bool or type(run(p.left)) == bool):
                raise Exception("SEMANTIC ERROR")
            else:
                return run(p.left) + run(p.right)
        if type(p) == Subtraction:
            if (type(run(p.left)) == int or type(run(p.left)) == float) and \
               (type(run(p.right)) == int or type(run(p.right)) == float):
                return run(p.left) - run(p.right)
            else:
                raise Exception("SEMANTIC ERROR")
        if type(p) == Multiplication:
            if (type(run(p.left)) == int or type(run(p.left)) == float) and \
               (type(run(p.right)) == int or type(run(p.right)) == float):
                return run(p.left) * run(p.right)
            else:
                raise Exception("SEMANTIC ERROR")
        if type(p) == Intdivision:
            if (type(run(p.left)) == int or type(run(p.left)) == float) and \
               (type(run(p.right)) == int or type(run(p.right)) == float):
                return run(p.left) // run(p.right)
            else:
                raise Exception("SEMANTIC ERROR")
        if type(p) == Division:
            if (type(run(p.left)) == int or type(run(p.left)) == float) and \
               (type(run(p.right)) == int or type(run(p.right)) == float):
                return run(p.left) / run(p.right)
            else:
                raise Exception("SEMANTIC ERROR")
        if type(p) == Exponentiation:
            return run(p.left) ** run(p.right)
        if type(p) == Negation:
            return not run(p.child)
        if type(p) == Modulus:
            return run(p.left) % run(p.right)
    except Exception as e:
        print("SEMANTIC ERROR")
        exit()


def tmp_run(p):
    print(type(p))
    return p


with open(sys.argv[1], 'r') as f:
    contents = f.read()
parser.parse(contents)
'''

while True:
    try:
        s = input('')
    except EOFError:
        break
    parser.parse(s)
'''