# -*- coding: utf-8 -*-
from string import letters, digits

dic = {}


class CuteType:
    INT = 1
    ID = 4
    MINUS = 2
    PLUS = 3
    L_PAREN = 5
    R_PAREN = 6
    TRUE = 8
    FALSE = 9
    TIMES = 10
    DIV = 11
    LT = 12
    GT = 13
    EQ = 14
    APOSTROPHE = 15
    DEFINE = 20
    LAMBDA = 21
    COND = 22
    QUOTE = 23
    NOT = 24
    CAR = 25
    CDR = 26
    CONS = 27
    ATOM_Q = 28
    NULL_Q = 29
    EQ_Q = 30

    KEYWORD_LIST = ('define', 'lambda', 'cond', 'quote', 'not', 'car', 'cdr', 'cons', 'atom?', 'null?', 'eq?')
    BINARYOP_LIST = (DIV, TIMES, MINUS, PLUS, LT, GT, EQ)
    BOOLEAN_LIST = (TRUE, FALSE)


def check_keyword(token):
    """
    :type token:str
    :param token:
    :return:
    """
    if token.lower() in CuteType.KEYWORD_LIST:
        return True
    return False


def is_type_keyword(token):
    if 20 <= token.type <= 30:
        return True
    return False


def _get_keyword_type(token):
    return {
        'define': CuteType.DEFINE,
        'lambda': CuteType.LAMBDA,
        'cond': CuteType.COND,
        'quote': CuteType.QUOTE,
        'not': CuteType.NOT,
        'car': CuteType.CAR,
        'cdr': CuteType.CDR,
        'cons': CuteType.CONS,
        'atom?': CuteType.ATOM_Q,
        'null?': CuteType.NULL_Q,
        'eq?': CuteType.EQ_Q
    }[token]


CUTETYPE_NAMES = dict((eval(attr, globals(), CuteType.__dict__), attr) for attr in dir(CuteType()) if
                      not callable(attr) and not attr.startswith("__"))


def is_type_binaryOp(token):
    """
    :type token:Token
    :param token:
    :return:
    """
    if token.type in CuteType.BINARYOP_LIST:
        return True
    return False


def is_type_boolean(token):
    """
    :type token:Token
    :param token:
    :return:
    """
    if token.type in CuteType.BOOLEAN_LIST:
        return True
    return False


class Token(object):
    def __init__(self, type, lexeme):
        """
        :type type:CuteType
        :type lexeme: str
        :param type:
        :param lexeme:
        :return:
        """
        self.type = type
        self.lexeme = lexeme
        # print type

    def __str__(self):
        # return self.lexeme
        if self is None: return None
        return "[" + CUTETYPE_NAMES[self.type] + ": " + self.lexeme + "]"

    def __repr__(self):
        return str(self)


class CuteScanner(object):
    """
    :type token_iter:iter
    """

    transM = {}

    def __init__(self, source):
        """
        :type source:str
        :param source:
        :return:
        """
        source = source.strip()
        token_list = source.split(" ")
        self.token_iter = iter(token_list)

    def get_state(self, old_state, trans_char):
        if trans_char in digits + letters + '?':
            return {
                0: {k: 1 if k in digits else 4 for k in digits + letters},
                1: {k: 1 for k in digits},
                2: {k: 1 for k in digits},
                3: {k: 1 for k in digits},
                4: {k: 4 if k is not '?' else 16 for k in digits + letters + '?'},
                7: {k: 8 if k is 'T' else 9 for k in ['T', 'F']}
            }[old_state][trans_char]
        if old_state is 0:
            return {
                '(': 5, ')': 6,
                '+': 3, '-': 2,
                '*': 10, '/': 11,
                '<': 12, '=': 14,
                '>': 13, "'": 15,
                '#': 7
            }[trans_char]

    def next_token(self):
        state_old = 0
        temp_token = next(self.token_iter, None)
        """:type :str"""
        if temp_token is None: return None
        for temp_char in temp_token:
            state_old = self.get_state(state_old, temp_char)

        if check_keyword(temp_token):
            result = Token(_get_keyword_type(temp_token), temp_token)
        else:
            result = Token(state_old, temp_token)
        return result

    def tokenize(self):
        tokens = []
        while True:
            t = self.next_token()
            if t is None: break
            tokens.append(t)
        return tokens


class TokenType():
    INT = 1
    ID = 4
    MINUS = 2
    PLUS = 3
    LIST = 5
    TRUE = 8
    FALSE = 9
    TIMES = 10
    DIV = 11
    LT = 12
    GT = 13
    EQ = 14
    APOSTROPHE = 15
    DEFINE = 20
    LAMBDA = 21
    COND = 22
    QUOTE = 23
    NOT = 24
    CAR = 25
    CDR = 26
    CONS = 27
    ATOM_Q = 28
    NULL_Q = 29
    EQ_Q = 30


NODETYPE_NAMES = dict((eval(attr, globals(), TokenType.__dict__), attr) for attr in dir(TokenType()) if
                      not callable(attr) and not attr.startswith("__"))


class Node(object):
    def __init__(self, type, value=None):
        self.next = None
        self.value = value
        self.type = type

    def set_last_next(self, next_node):
        if self.next is not None:
            self.next.set_last_next(next_node)

        else:
            self.next = next_node

    def get_tail(self):
        def get_list_tail(node):
            """
            :type node: Node
            """
            if node.type is TokenType.LIST:
                return get_list_tail(node.value)
            else:
                if node.next is None:
                    return node
                return get_list_tail(node.next)

        if self.type is TokenType.LIST:
            return get_list_tail(self)
        return self

    def __str__(self):
        result = ""

        if self.type is TokenType.ID:
            result = "[" + self.value + "]"
        elif self.type is TokenType.INT:
            result = str(self.value)
        elif self.type is TokenType.LIST:
            if self.value is not None and self.value.type is TokenType.QUOTE:
                result = str(self.value)
            else:
                result = "(" + str(self.value) + ")"
        elif self.type is TokenType.QUOTE:
            result = "'"
        else:
            result = "[" + NODETYPE_NAMES[self.type] + "]"

        if self.next is None:
            return result
        else:
            return result + " " + str(self.next)


class BasicPaser(object):
    def __init__(self, token_list):
        """
        :type token_list:list
        :param token_list:
        :return:
        """
        self.token_iter = iter(token_list)

    def _get_next_token(self):
        """
        :rtype: Token
        :return:
        """
        next_token = next(self.token_iter, None)
        if next_token is None: return None
        return next_token

    def parse_expr(self):
        """
        :rtype : Node
        :return:
        """
        token = self._get_next_token()
        """:type :Token"""
        if token == None: return None
        result = self._create_node(token)
        return result

    def _create_node(self, token):
        if token is None: return None

        if token.type is CuteType.INT:
            return Node(TokenType.INT, token.lexeme)
        elif token.type is CuteType.ID:
            return Node(TokenType.ID, token.lexeme)
        elif token.type is CuteType.L_PAREN:
            return Node(TokenType.LIST, self._parse_expr_list())
        elif token.type is CuteType.R_PAREN:
            return None
        elif token.type is CuteType.APOSTROPHE:
            q_node = Node(TokenType.QUOTE)
            q_node.next = self.parse_expr()
            new_list_node = Node(TokenType.LIST, q_node)
            return new_list_node

        elif token.type is CuteType.QUOTE:
            q_node = Node(TokenType.QUOTE)
            return q_node

        elif is_type_binaryOp(token) or \
                is_type_keyword(token) or \
                is_type_boolean(token):
            return Node(token.type)

        else:
            return None

    def _parse_expr_list(self):
        head = self.parse_expr()
        """:type :Node"""
        if head is not None:
            head.next = self._parse_expr_list()
        return head


class CuteInterpreter(object):
    TRUE_NODE = Node(TokenType.TRUE)
    FALSE_NODE = Node(TokenType.FALSE)

    def run_arith(self, arith_node):
        pass

    def run_func(self, func_node):
        rhs1 = func_node.next
        rhs2 = rhs1.next if rhs1.next is not None else None

        if rhs1.value in dic.keys():
            rhs1 = dic[rhs1.value]
        if rhs2 is not None and rhs2.value in dic.keys():
            rhs2 = dic[rhs2.value]

        def create_quote_node(node, list_flag=False):
            """
            "Quote ��带 ������ ��, node�� next�� �Ͽ� ��ȯ"
            "list_flag�� True�� ���, list node�� ������ ��, list�� value�� �Է¹��� node�� �����ϰ�"
            "Quote�� next�� ���⼭ ������ list�� ������"
            "���� ������ ���⼭ ������ quote��带 value�� ���� List"
            """
            q_node = Node(TokenType.QUOTE)
            if list_flag:
                inner_l_node = Node(TokenType.LIST, node)
                q_node.next = inner_l_node
            else:
                q_node.next = node
            l_node = Node(TokenType.LIST, q_node)
            return l_node

        def is_quote_list(node):
            "Quote�� next�� list���� Ȯ��"
            if node.type is TokenType.LIST:
                if node.value.type is TokenType.QUOTE:
                    if node.value.next.type is TokenType.LIST:
                        return True
            return False

        def pop_node_from_quote_list(node):
            "Quote list���� quote�� ����Ǿ� �ִ� list����� value�� ������"
            if not is_quote_list(node):
                return node
            return node.value.next.value

        def list_is_null(node):
            "�Է¹��� node�� null list���� Ȯ����"
            node = pop_node_from_quote_list(node)
            if node is None: return True
            return False

        def insertTable(id, value):
            dic[id] = value
            return None

        def look_up_Table(id):
            temp = dic.get(id)
            del dic[id]
            return temp

        if func_node.type is TokenType.CAR:
            rhs1 = self.run_expr(rhs1)
            if not is_quote_list(rhs1):
                print ("car error!")

            if rhs1 in dic.values():
                if rhs1.type is TokenType.QUOTE:
                    rhs1 = Node(TokenType.LIST, rhs1)
                # return create_quote_node(result)

            result = pop_node_from_quote_list(rhs1)
            if result.type is not TokenType.LIST:
                return result
            return create_quote_node(result)

        elif func_node.type is TokenType.CDR:
            # �ۼ�
            if not is_quote_list(rhs1):
                print ("cdr error!")
            tmp = rhs1.value.next.value.next
            if tmp is None:
                return create_quote_node(Node(TokenType.ID, ""), True)
            return create_quote_node(tmp, True)

        elif func_node.type is TokenType.CONS:
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)
            # �ۼ�
            # rhs2�� ������ list��� ����
            if is_quote_list(expr_rhs1):
                tmp = create_quote_node(pop_node_from_quote_list(expr_rhs1), True).value.next
            else:
                tmp = create_quote_node(pop_node_from_quote_list(expr_rhs1)).value.next
            if expr_rhs2 is not None:
                tmp.next = pop_node_from_quote_list(expr_rhs2)
            return create_quote_node(tmp, True)

        elif func_node.type is TokenType.ATOM_Q:
            if list_is_null(rhs1): return self.TRUE_NODE
            if rhs1.type is not TokenType.LIST: return self.TRUE_NODE
            if rhs1.type is TokenType.LIST:
                if rhs1.value.type is TokenType.QUOTE:
                    if rhs1.value.next is not TokenType.LIST:
                        return self.TRUE_NODE
            return self.FALSE_NODE

        elif func_node.type is TokenType.EQ_Q:
            # �ۼ�
            if rhs1.type is TokenType.INT:
                if rhs1.value == rhs1.next.value:
                    return self.TRUE_NODE
                else:
                    return self.FALSE_NODE
            else:
                return self.FALSE_NODE

        elif func_node.type is TokenType.NULL_Q:
            if list_is_null(rhs1): return self.TRUE_NODE
            return self.FALSE_NODE
        elif func_node.type is TokenType.NOT:
            if rhs1.type is TokenType.FALSE:
                return Node(TokenType.TRUE, self.TRUE_NODE)
            else:
                return Node(TokenType.FALSE, self.FALSE_NODE)

        elif func_node.type is TokenType.COND:
            while True:
                if rhs1.value.type is TokenType.LIST:
                    if calc(rhs1.value) == "#T":
                        rhs1.value.next.next = None
                        return Node(TokenType.INT, rhs1.value.next)
                    else:
                        rhs1 = rhs1.next
                elif rhs1.value.type is TokenType.TRUE:
                    return Node(rhs1.value.next.type, rhs1.value.next)
                else:
                    self.run_func(rhs1)

        elif func_node.type is TokenType.DEFINE:
            rhs1 = func_node.next
            rhs2 = rhs1.next if rhs1.next is not None else None
            expr_rhs2 = self.run_expr(rhs2)
            if expr_rhs2.type is TokenType.LIST and is_type_binaryOp(expr_rhs2.value):
                result_data = Test_method(print_node(expr_rhs2))
                if result_data == "#T":
                    expr_rhs2 = Node(TokenType.TRUE, result_data)
                elif result_data == "#F":
                    expr_rhs2 = Node(TokenType.FALSE, result_data)
                else:
                    expr_rhs2 = Node(TokenType.INT, result_data)
            if expr_rhs2.type is TokenType.LIST:
                if expr_rhs2.value.type is TokenType.QUOTE:
                    insertTable(rhs1.value, expr_rhs2)
                else:
                    insertTable(rhs1.value, Node(TokenType.INT, expr_rhs2.value))
            else:
                insertTable(rhs1.value, expr_rhs2)
            return None

    def run_expr(self, root_node):
        """
        :type root_node: Node
        """
        if root_node is None:
            return None

        if root_node.type is TokenType.ID:
            return root_node
        elif root_node.type is TokenType.INT:
            return root_node
        elif root_node.type is TokenType.TRUE:
            return root_node
        elif root_node.type is TokenType.FALSE:
            return root_node
        elif root_node.type is TokenType.LIST:
            return self.run_list(root_node)
        else:
            print "Run Expr Error"
        return None

    def run_list(self, l_node):
        """
        :type l_node:Node
        """
        op_code = l_node.value
        if op_code is None:
            return l_node
        if op_code.type in \
                [TokenType.CAR, TokenType.CDR, TokenType.CONS, TokenType.ATOM_Q, \
                 TokenType.EQ_Q, TokenType.NULL_Q, TokenType.NOT, TokenType.COND, TokenType.DEFINE]:
            return self.run_func(op_code)
        if op_code.type is TokenType.QUOTE:
            return l_node
        if op_code.type is TokenType.PLUS:
            return l_node
        if op_code.type is TokenType.MINUS:
            return l_node
        if op_code.type is TokenType.EQ:
            return l_node
        if op_code.type is TokenType.GT:
            return l_node
        if op_code.type is TokenType.LT:
            return l_node
        if op_code.type is TokenType.TIMES:
            return l_node
        if op_code.type is TokenType.DIV:
            return l_node
        else:
            print "application: not a procedure;"
            print "expected a procedure that can be applied to arguments"
            print "Token Type is " + op_code.value
            return None


def print_node(node):
    """
    "Evaluation �� ����� ����ϱ� ���� �Լ�"
    "�Է��� List Node �Ǵ� atom"
    :type node: Node
    """

    def print_list(node):
        """
        "List����� value�� ���ؼ� ���"
        "( 2 3 )�� �Է��̸� 2�� 3�� ���ؼ� ��� �����"
        :type node: Node
        """

        def print_list_val(node):
            if node.next is not None:
                return print_node(node) + " " + print_list_val(node.next)
            return print_node(node)

        if node.type is TokenType.LIST:
            if node.value.type is TokenType.QUOTE:
                return print_node(node.value)
            return "( " + print_list_val(node.value) + " )"

    if node is None:
        return ""
    if node.type in [TokenType.ID, TokenType.INT]:
        return node.value
    if node.type is TokenType.TRUE:
        return "#T"
    if node.type is TokenType.FALSE:
        return "#F"
    if node.type is TokenType.PLUS:
        return "+"
    if node.type is TokenType.MINUS:
        return "-"
    if node.type is TokenType.TIMES:
        return "*"
    if node.type is TokenType.DIV:
        return "/"
    if node.type is TokenType.GT:
        return ">"
    if node.type is TokenType.LT:
        return "<"
    if node.type is TokenType.EQ:
        return "="
    if node.type is TokenType.LIST:
        return print_list(node)
    if node.type is TokenType.ATOM_Q:
        return "atom?"
    if node.type is TokenType.CAR:
        return "car"
    if node.type is TokenType.CDR:
        return "cdr"
    if node.type is TokenType.COND:
        return "cond"
    if node.type is TokenType.CONS:
        return "cons"
    if node.type is TokenType.LAMBDA:
        return "lambda"
    if node.type is TokenType.NULL_Q:
        return "null?"
    if node.type is TokenType.EQ_Q:
        return "eq?"
    if node.type is TokenType.NOT:
        return "not"
    if node.type is TokenType.QUOTE:
        return "'" + print_node(node.next)


def Test_method(input):
    test_cute = CuteScanner(input)
    test_tokens = test_cute.tokenize()
    test_basic_paser = BasicPaser(test_tokens)
    node = test_basic_paser.parse_expr()
    cute_inter = CuteInterpreter()
    result = cute_inter.run_expr(node)

    if result is None:
        return ""  # print "result : "
    elif result.type is not TokenType.LIST:
        return result.value
    elif is_type_binaryOp(result.value):
        return run_binary(result)  # print "result : {0}".format(run_binary(result))
    else:
        return print_node(result)  # print "result : {0}".format(print_node(result))


def run_binary(result):
    rhs1 = result.value
    if rhs1.type is TokenType.PLUS:
        return calc(rhs1.next) + calc(rhs1.next.next)
    elif rhs1.type is TokenType.MINUS:
        return calc(rhs1.next) - calc(rhs1.next.next)
    elif rhs1.type is TokenType.GT:
        if calc(rhs1.next) > calc(rhs1.next.next):
            return "#T"
        elif calc(rhs1.next) < calc(rhs1.next.next):
            return "#F"
    elif rhs1.type is TokenType.LT:
        if calc(rhs1.next) < calc(rhs1.next.next):
            return "#T"
        elif calc(rhs1.next) > calc(rhs1.next.next):
            return "#F"
    elif rhs1.type is TokenType.TIMES:
        return calc(rhs1.next) * calc(rhs1.next.next)
    elif rhs1.type is TokenType.DIV:
        return calc(rhs1.next) / calc(rhs1.next.next)
    elif rhs1.type is TokenType.EQ:
        if calc(rhs1.next) == calc(rhs1.next.next):
            return "#T"
        else:
            return "#F"


def calc(node):
    if node.type is TokenType.LIST:
        return run_binary(node)
    elif node.value in dic.keys():
        return calc(dic[node.value])
    else:
        return int(node.value)


def Test_All():
    cmd = raw_input("> ")
    print "result : {0}".format(Test_method(cmd))


while True:
    Test_All()