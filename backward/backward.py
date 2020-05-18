from lark import Lark, Transformer


# ----------------------------------------------------------------------


class XSysTransformer(Transformer):
    pass

xsys_grammar = Lark(r"""
%import common.WS
%ignore WS

stmt_expr: stmt_head -> stmt
    | expr_head -> expr

stmt_head: ( expr_head "=>" expr_head ) -> stmt_impl
    | ( "=" atom* ) -> stmt_init
    | ( "?" atom* ) -> stmt_look

expr_head: expr_and -> expr

expr_and: expr_or -> expr
    | ( expr_and "&" expr_or ) -> expr_and

expr_or: expr_xor -> expr
    | ( expr_or "|" expr_xor ) -> expr_or

expr_xor: expr_last -> expr
    | ( expr_xor "^" expr_last ) -> expr_xor

expr_last: atom -> expr
    | ( "!" atom ) -> expr_not
    | ( "!" "(" expr_head ")" ) -> expr_not
    | ( "(" expr_head ")" ) -> expr

atom: /[a-zA-Z]+/

""",
    start="stmt_expr",
    parser="lalr",
    transformer=XSysTransformer(),
)


class Interpreter(): 
    def __init__(self):
        self.context = {}
    
    def interpret(self, text):
        tree = xsys_grammar.parse(text)
        return tree