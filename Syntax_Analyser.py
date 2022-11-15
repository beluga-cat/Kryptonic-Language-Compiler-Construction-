#doesnt handle interface
from SemanticAnalyzer import DataTable, FunctionDataTable, MainTable, Stack
from Token import Token

const = ['int', 'float', 'string', 'bool']


class SyntaxAnalyzer:
    current_index: int = 0
    end_index: int = 0
    token_set: list[Token] = []
    main_table: list[MainTable] = []
    main_data_table: list[DataTable] = []
    function_table: list[FunctionDataTable] = []
    scope_stack: Stack = Stack()
    current_class: MainTable

    @staticmethod
    def main(token_set: list[Token]):
        SyntaxAnalyzer.end_index = len(token_set) - 1
        SyntaxAnalyzer.token_set = token_set
        # print('dbaj')
        if(SyntaxAnalyzer.validate()):
            return "Syntax Valid"
        return f'Invalid Syntax @ line # {token_set[SyntaxAnalyzer.current_index].line_number}'


    @staticmethod
    def validate() -> bool:
        if(SyntaxAnalyzer.start()):
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "$"):
                return True
        return False

    @staticmethod
    def start() -> bool:
        # { fixed, abstract, class, $function, $mfunction, enum }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['fixed', 'abstract', 'class', '$function', '$mfunction', 'enum']):
            if(SyntaxAnalyzer.defs()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "$mfunction"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "main"):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "void"):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                                SyntaxAnalyzer.current_index += 1
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                                    SyntaxAnalyzer.current_index += 1
                                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                                        SyntaxAnalyzer.current_index += 1
                                        if(SyntaxAnalyzer.mst()):
                                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                                SyntaxAnalyzer.current_index += 1
                                                if(SyntaxAnalyzer.defs()):
                                                    return True
        return False

    @staticmethod
    def defs() -> bool:
        # { fixed, abstract, class } 
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['fixed', 'abstract', 'class']):
            if(SyntaxAnalyzer.class_dec()):
                if(SyntaxAnalyzer.defs()):
                    return True
        # { $fnction }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['$function']):
            if(SyntaxAnalyzer.fn_dec()):
                if(SyntaxAnalyzer.defs()):
                    return True
        # { enum }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['enum']):
            if(SyntaxAnalyzer.enum()):
                if(SyntaxAnalyzer.defs()):
                    return True
        # { $function, $ }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['$mfunction', '$']):
            return True

        return False

    @staticmethod
    def sst() -> bool:
        # { while }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ['while']):
            if(SyntaxAnalyzer.while_st()):
                return True
        # { for }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "for"):
            if(SyntaxAnalyzer.for_st()):
                return True
        # { return }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "return"):
            if(SyntaxAnalyzer.return_st()):
                return True
        # { switch }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "switch"):
            if(SyntaxAnalyzer.switch()):
                return True
        # { break }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "break"):
            if(SyntaxAnalyzer.break_st()):
                return True
        # { continue }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "continue"):
            if(SyntaxAnalyzer.continue_st()):
                return True
        # { if }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "if"):
            if(SyntaxAnalyzer.if_elif_else()):
                return True
        # { take }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "take"):
            if(SyntaxAnalyzer.dec()):
                return True
        # { ID }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.sst1()):
                return True
        # { ++, -- }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "inc_dec"):
            if(SyntaxAnalyzer.inc_dec_op()):            
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                    SyntaxAnalyzer.current_index += 1
                    return True
        return False

    @staticmethod
    def sst1() -> bool:
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["assignment", "compound_assignment"]):
            if(SyntaxAnalyzer.cb6()):
                return True
        # { ( }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.argu()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.sst2()):
                        return True
        # { ++, -- }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "inc_dec"):
            if(SyntaxAnalyzer.inc_dec_op()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
                    SyntaxAnalyzer.current_index += 1
                    return True
        #{ . }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.assign1()):
                    if(SyntaxAnalyzer.cb6()):
                        return True
        # { [ }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "["):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.exp()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "]"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.assign1()):
                        if(SyntaxAnalyzer.cb6()):
                            return True
        return False
                        

    @staticmethod
    def sst2() -> bool:
        # { ; }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
            SyntaxAnalyzer.current_index += 1
            return True
        # { . }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.assign1()):
                    if(SyntaxAnalyzer.cb6()):
                        return True
        return False

    @staticmethod
    def mst() -> bool:
        # {while, for, return, switch, break, continue, if, take, ID, ++, --}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["while", "for", "return", "switch", "break", "continue", "if", "take", "ID", "++", "--"]):
            if(SyntaxAnalyzer.sst()):
                if(SyntaxAnalyzer.mst()):
                    return True
        # { }, break }    
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["}", "break"]):
            return True

        return False
    
    @staticmethod
    def assign() -> bool:
        # { ID }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.assign1()):
                if(SyntaxAnalyzer.assign_operator()):
                    if(SyntaxAnalyzer.exp()):
                        if(SyntaxAnalyzer.assign_list()):
                            return True
        return False
    
    @staticmethod
    def assign_operator() -> bool:
        # { = }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "assignment"):
            SyntaxAnalyzer.current_index += 1
            return True
        # { CO }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "compound_assignment"):
            SyntaxAnalyzer.current_index += 1
            return True
        return False

    @staticmethod
    def assign1() -> bool:
        # { . }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.assign1()):
                    return True
        # { ( }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.argu()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.assign1()):
                                return True
        # { [ }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "["):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.exp()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "]"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.assign1()):
                        return True
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["assignment", "compound_assignment"]):
            return True
        return False

    @staticmethod
    def assign_list() -> bool:
        # { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ","):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.assign()):
                return True
        # { ; }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
            SyntaxAnalyzer.current_index += 1
            return True
        return False

    @staticmethod
    def dec() -> bool:
        # { take }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "take"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.dec0()):
                return True 
        return False

    @staticmethod
    def dec0() -> bool:
        # { dt, ID }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["data_type", "ID"]):
            if(SyntaxAnalyzer.f_dt()):
                if(SyntaxAnalyzer.arr()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ":"):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.dec1()):
                                return True

        return False

    @staticmethod
    def dec1() -> bool:
        # { ,, ; }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in [",", ";"]):
            if(SyntaxAnalyzer.dec_list()):
                return True
        # { = }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "assignment"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.dec2()):
                if(SyntaxAnalyzer.dec_list()):
                    return True
        return False
    
    @staticmethod
    def dec_list() -> bool:
        # { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ","):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.dec0()):
                return True
        #{ ; }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
            SyntaxAnalyzer.current_index += 1
            return True
        return False

    @staticmethod
    def dec2() -> bool:
        # { [ }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "["):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.argu()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "]"):
                    SyntaxAnalyzer.current_index += 1
                    return True
        #{ new }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "new"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.argu()):
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                            SyntaxAnalyzer.current_index += 1
                            return True
        # { present, super, ID, const, (, not }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["present", "super", "ID", *const, "(", "not_operator"]):
            if(SyntaxAnalyzer.exp()):
                return True
        return False


    @staticmethod
    def f_dt() -> bool:
        # { dt, ID }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["data_type", "ID"]):
            SyntaxAnalyzer.current_index += 1
            return True
        return False

    @staticmethod
    def f_dt1() -> bool:
        # { DT, ID }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["data_type", "ID"]):
            if(SyntaxAnalyzer.f_dt()):
                if(SyntaxAnalyzer.arr()):
                    return True
        # { void }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "void"):
            SyntaxAnalyzer.current_index += 1
            return True
        return False

    @staticmethod
    def arr() -> bool:
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "["):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "]"):
                SyntaxAnalyzer.current_index += 1
                return True
        # { :, ( }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in [":", "("]):
            return True
        return False

    @staticmethod
    def exp() -> bool:
        # { present, super, ID, const, (, not }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["present", "super", "ID", *const, "(", "not_operator"]):
            if(SyntaxAnalyzer.ae()):
                if(SyntaxAnalyzer.expc()):
                    return True
        return False

    @staticmethod
    def expc() -> bool:
        # { OR }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "or_operator"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.ae()):
                if(SyntaxAnalyzer.expc()):
                    return True
        # { ], ,, ), present, super, ID, const, (, not,  ;, while, for, return, switch, break, continue, if, take, ID, ++, --, }, break }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in [ "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break"]):
            return True
        return False

    @staticmethod
    def ae() -> bool:
        # { present, super, ID, const, (, not }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["present", "super", "ID", *const, "(", "not_operator"]):
            if(SyntaxAnalyzer.re()):
                if(SyntaxAnalyzer.aec()):
                    return True
        return False

    @staticmethod
    def aec() -> bool:
        # { AND }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "and_operator"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.re()):
                if(SyntaxAnalyzer.aec()):
                    return True
        # { OR,  ], ,, ), present, super, ID, const, (, not,  ;, while, for, return, switch, break, continue, if, take, ID, ++, --, }, break }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["or_operator","]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break"]):
            return True
        return False

    @staticmethod
    def re() -> bool:
        # {"present", "super", "ID", *const, "(", "not_operator"}
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["present", "super", "ID", *const, "(", "not_operator"]):
            if(SyntaxAnalyzer.e()):
                if(SyntaxAnalyzer.rec()):
                    return True
        return False

    @staticmethod
    def rec() -> bool:
        # { ROP }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "relational_operators"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.e()):
                if(SyntaxAnalyzer.rec()):
                    return True
        # {"AND", "OR", "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break" }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["and_operator", "or_operator", "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break"]):
            return True
        return False

    @staticmethod
    def e() -> bool:
        # { present, super, ID, const, (, not }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["present", "super", "ID", *const, "(", "not_operator"]):
            if(SyntaxAnalyzer.t()):
                if(SyntaxAnalyzer.ec()):
                    return True
        return False

    @staticmethod
    def ec() -> bool:
        # { PM }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "plus_minus"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.t()):
                if(SyntaxAnalyzer.ec()):
                    return True
        # { "ROP", "and_operator", "or_operator", "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break" }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["relational_operators", "and_operator", "or_operator", "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break"]):
            return True
        return False

    @staticmethod
    def t() -> bool:
        # { present, super, ID, const, (, not }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["present", "super", "ID", *const, "(", "not_operator"]):
            if(SyntaxAnalyzer.f()):
                if(SyntaxAnalyzer.tc()):
                    return True
        return False

    @staticmethod
    def tc() -> bool:
        # { MDM }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "multiply_divide_mod"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.f()):
                if(SyntaxAnalyzer.tc()):
                    return True
        # { "plus_minus" ,"relational_operators", "and_operator", "or_operator", "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break" }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["plus_minus" ,"relational_operators", "and_operator", "or_operator", "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break"]):
            return True
        return False

    @staticmethod
    def f() -> bool:
        # { present, super, ID }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["present", "super", "ID"]):
            if(SyntaxAnalyzer.ts()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.o()):    
                        return True
        # { const }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in [*const]):
            SyntaxAnalyzer.current_index += 1
            return True
        # { ( }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.exp()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                    SyntaxAnalyzer.current_index += 1
                    return True
        # { not }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "not_operator"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.f()):
                return True
        return False

    @staticmethod
    def o() -> bool:
        # { [ }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "["):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.argu()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "]"):
                    if(SyntaxAnalyzer.oc()):
                        return True
        # { ( }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.argu()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.oc()):
                        return True
        # { ".", "multiply_divide_mod", "plus_minus" ,"relational_operators", "and_operator", "or_operator", "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break" }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in [".", "multiply_divide_mod", "plus_minus" ,"relational_operators", "and_operator", "or_operator", "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break"]):
            if(SyntaxAnalyzer.oc()):
                return True
        return False

    @staticmethod
    def oc() -> bool:
        # { . }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                        if(SyntaxAnalyzer.o()):
                            return True
        # { MDM, PM, ROP, AND, OR,  ], ,, ), present, super, ID, const, (, not,  ;, while, for, return, switch, break, continue, if, take, ID, ++, --, }, break }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["multiply_divide_mod", "plus_minus" ,"relational_operators", "and_operator", "or_operator", "]", ",", ")", "present", "super", "ID", *const, "(", "not_operator",  ";", "while", "for", "return", 'switch', "break", "continue", "if", "take", "++", "--", "}", "break"]):
            return True
        return False

    @staticmethod
    def ts() -> bool:
        # { present }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "present"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
                SyntaxAnalyzer.current_index += 1
                return True
        # { super }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "super"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
                SyntaxAnalyzer.current_index += 1
                return True
        # { ID }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
            return True
        return False 

    @staticmethod
    def argu() -> bool:
        # { present, super, ID, const, (, not }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["present", "super", "ID", *const, "(", "not_operator"]):
            if(SyntaxAnalyzer.exp()):
                if(SyntaxAnalyzer.argu1()):
                    return True
        # { ")", "]" }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in [")", "]"]):
            return True
        return False

    @staticmethod
    def argu1() -> bool:
        # { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ","):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.exp()):
                if(SyntaxAnalyzer.argu1()):
                    return True
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in {")", "]"}):        
            return True
        return False

    @staticmethod
    def while_st() -> bool:
        # { while }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "while"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.exp()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.mst()):
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                    SyntaxAnalyzer.current_index += 1
                                    return True
        return False

    @staticmethod
    def for_st() -> bool:
        # { for }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "for"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.assign()):
                    if(SyntaxAnalyzer.exp()):                   
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.inc_dec_st()):
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                                    SyntaxAnalyzer.current_index += 1
                                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                                        SyntaxAnalyzer.current_index += 1
                                        if(SyntaxAnalyzer.mst()):
                                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                                SyntaxAnalyzer.current_index += 1
                                                return True
        return False

    @staticmethod
    def inc_dec_st() -> bool:
        # { ID }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.inc_dec_op()):
                return True
        # { ++, -- }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "inc_dec"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                return True
        return False
    
    @staticmethod
    def inc_dec_op() -> bool:
        # { ++ }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "inc_dec"):
            SyntaxAnalyzer.current_index += 1
            return True
        # { -- }
        # elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "--"):
        # SyntaxAnalyzer.current_index += 1
        #     return True
        return False

    @staticmethod
    def fixed() -> bool:
        # { fixed }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "fixed"):
            SyntaxAnalyzer.current_index += 1
            return True
        # { abstract, class, static, take, $function }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["abstract", "class", "static", "take", "$function"]):
            return True
        return False

    @staticmethod
    def abstract() -> bool:
        # { abstract }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "abstract"):
            SyntaxAnalyzer.current_index += 1
            return True
        # { class, static, take, abstract, $function }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["class", "static", "take", "abstract", "$function"]):
            return True
        return False

    @staticmethod
    def static() -> bool:
        # { static }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "static"):
            SyntaxAnalyzer.current_index += 1
            return True
        # {  take, abstract, $function }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["take", "abstract", "$function"]):
            return True
        return False

    @staticmethod
    def class_dec() -> bool:
        # { fixed, abstract, class }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["fixed", "abstract", "class"]):
            if(SyntaxAnalyzer.fixed()):
                if(SyntaxAnalyzer.abstract()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "class"):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.interface()):
                                if(SyntaxAnalyzer.inheritance()):
                                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                                        SyntaxAnalyzer.current_index += 1
                                        if(SyntaxAnalyzer.cb()):
                                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                                SyntaxAnalyzer.current_index += 1
                                                return True
        return False

    @staticmethod
    def inheritance() -> bool:
        # { child_of }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "child_of"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.multi_id()):
                    return True
        # { { }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
            return True
        return False

    @staticmethod
    def multi_id() -> bool:
        # { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ","):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.multi_id()):
                    return True
        # { { }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
            return True
        return False

    @staticmethod
    def interface() -> bool:
        # { implements }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "implements"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "class"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.interface1()):
                        return True
        # { child_of, { }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["child_of", "{"]):
            return True
        return False
        
    @staticmethod
    def interface1() -> bool:
        # { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ","):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.interface1()):
                    return True
        # { child_of, { }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["child_of", "{"]):
            return True
        return False 

    @staticmethod
    def cb() -> bool:
        # { shared, own, } }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["shared", "own", "}"]):
            if(SyntaxAnalyzer.cb0()):
                if(SyntaxAnalyzer.cb1()):
                    return True
        return False

    @staticmethod
    def cb0() -> bool:
        # { shared }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "shared"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.cb2()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                        SyntaxAnalyzer.current_index += 1
                        return True
        # { own, } }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["own", "}"]):
            return True
        return False
    
    @staticmethod
    def cb1() -> bool:
        # { own }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "own"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.cb2()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                        SyntaxAnalyzer.current_index += 1
                        return True
                    
        # { } }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
            return True
        return False

    @staticmethod
    def cb2() -> bool:
        # {fixed, static, abstract, $function, take }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["fixed", "static", "abstract", "$function", "take"]):
            if(SyntaxAnalyzer.fixed()):
                if(SyntaxAnalyzer.static()):
                    if(SyntaxAnalyzer.cb3()):
                        return True
        # { ID }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.cb4()):
                return True
        # { } }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
            return True
        return False

    @staticmethod
    def cb3() -> bool:
        # { take }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "take"):
            if(SyntaxAnalyzer.dec()):
                if(SyntaxAnalyzer.cb2()):
                    return True
        # { abstract, $function }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["abstract", "$function"]):
            if(SyntaxAnalyzer.abstract()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "$function"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.f_dt1()):
                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                                SyntaxAnalyzer.current_index += 1
                                if(SyntaxAnalyzer.paramerter()):
                                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                                        SyntaxAnalyzer.current_index += 1
                                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                                            SyntaxAnalyzer.current_index += 1
                                            if(SyntaxAnalyzer.c_f_body()):
                                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                                    SyntaxAnalyzer.current_index += 1
                                                    if(SyntaxAnalyzer.cb2()):
                                                        return True

        return False

    @staticmethod
    def cb4() -> bool:
        # { ( }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.argu()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.cb5()):
                        return True
        # { . }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.assign1()):
                    if(SyntaxAnalyzer.cb6()):
                        return True
        # { [ }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "["):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.exp()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "]"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.cb6()):
                        return True
        return False

    @staticmethod
    def cb5() -> bool:
        # { fixed, static, abstract, $function, take, ID, own }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["fixed", "static", "abstract", "$function", "take", "ID", "own"]):
            if(SyntaxAnalyzer.cb2()):
                return True
        # { . }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.assign1()):
                    if(SyntaxAnalyzer.cb6()):
                        return True
        return False

    @staticmethod
    def cb6() -> bool:
        # { =, CO }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["assignment", "compound_assignment"] ):
            if(SyntaxAnalyzer.assign_operator()):
                if(SyntaxAnalyzer.exp()):
                    if(SyntaxAnalyzer.assign_list()):
                        return True
        return False
        
    @staticmethod
    def c_f_body() -> bool:
        #{ present }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "present"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.c_f_body1()):
                    if(SyntaxAnalyzer.c_f_body()):
                        return True
        # { super } 
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "super"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.c_f_body1()):
                    if(SyntaxAnalyzer.c_f_body()):
                        return True
        # { while, for, return, switch, break, continue, if, take, ID, ++, -- }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["while", "for", "return", "switch", "break", "continue", "if", "take", "ID", "++", "--"]):
            if(SyntaxAnalyzer.sst()):
                if(SyntaxAnalyzer.c_f_body()):
                    return True
        # { } }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
            return True
        return False

    @staticmethod
    def c_f_body1() -> bool:
        #{ ID }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.c_f_body2()):
                return True
        return False

    @staticmethod
    def c_f_body2() -> bool:
        # { ( }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.argu()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.c_f_body3()):
                        return True
        # { . }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.assign1()):
                    if(SyntaxAnalyzer.cb6()):
                        return True
        # { [ }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "["):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.exp()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "]"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.assign1()):
                        if(SyntaxAnalyzer.cb6()):
                            return True
        # { ; }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
            SyntaxAnalyzer.current_index += 1
            return True
        # { = }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "assignment"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.exp()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
                    SyntaxAnalyzer.current_index += 1
                    return True

        return False

    @staticmethod
    def c_f_body3():
        # { . }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "."):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.assign1()):
                        if(SyntaxAnalyzer.cb6()):
                            return True
        # { ; }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
            SyntaxAnalyzer.current_index += 1
            return True
        return False

    @staticmethod
    def continue_st() -> bool:
        # { continue }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "continue"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
                SyntaxAnalyzer.current_index += 1
                return True
        return False

    @staticmethod
    def break_st() -> bool:
        # { break }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "break"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
                SyntaxAnalyzer.current_index += 1
                return True
        return False

    @staticmethod
    def return_st() -> bool:
        # { return }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "return"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.return1()):
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
                    SyntaxAnalyzer.current_index += 1
                    return True
        return False

    @staticmethod
    def return1() -> bool:
        # { True, False }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "bool"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.return2()):
                return True

        # { False }
        # elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "False"):
        #     SyntaxAnalyzer.current_index += 1
        #     if(SyntaxAnalyzer.return2()):
        #         return True
        # { present, super, ID, const, (, not }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["present", "super", "ID", *const, "(", "not_operator"]):
            if(SyntaxAnalyzer.exp()):
                if(SyntaxAnalyzer.return2()):
                    return True
        # { take }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "take"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.dec()):
                if(SyntaxAnalyzer.return2()):
                    return True
        return False

    @staticmethod
    def return2() -> bool:
        # { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ","):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.return1()):
                return True
        # { while, for, return, switch, break, continue, if, take, ID, ++, --,}, break, ; }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["while", "for", "return", "switch", "break", "continue", "if", "take", "ID", "++", "--", "break", ";"]):
            return True
        return False

    @staticmethod
    def paramerter() -> bool:
        # { DT }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "data_type"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.paramerter1()):
                    return True
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
            return True
        return False

    @staticmethod
    def paramerter1() -> bool:
        # { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ","):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "data_type"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.paramerter1()):
                        return True
        # { ) }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
            return True
        return False

    @staticmethod
    def fn_dec() -> bool:
        # { $function }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "$function"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.f_dt1()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.paramerter()):
                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                                SyntaxAnalyzer.current_index += 1
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                                    SyntaxAnalyzer.current_index += 1
                                    if(SyntaxAnalyzer.mst()):
                                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                            SyntaxAnalyzer.current_index += 1
                                            return True
            # ! bharwat hai yahan
        return False


    @staticmethod
    def enum() -> bool:
        # { enum }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "enum"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "assignment"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.list()):
                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                SyntaxAnalyzer.current_index += 1
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ";"):
                                    SyntaxAnalyzer.current_index += 1
                                    return True
        return False

    @staticmethod
    def list() -> bool:
        # { ID }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.list1()):
                return True
        # { } }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
            SyntaxAnalyzer.current_index += 1
            return True
        return False

    @staticmethod
    def list1() -> bool:
        # { , }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ","):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.list1()):
                    return True
        # { } }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
            # SyntaxAnalyzer.current_index += 1
            return True
        return False

    @staticmethod
    def fn_call() -> bool:
        # { ID }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "ID"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.argu()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                        SyntaxAnalyzer.current_index += 1
                        return True
        return False

    @staticmethod
    def if_elif_else() -> bool:
        # { if }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "if"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.exp()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.mst()):
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                    SyntaxAnalyzer.current_index += 1
                                    if(SyntaxAnalyzer.elif_st()):
                                        if(SyntaxAnalyzer.else_st()):
                                            return True
        return False

    @staticmethod
    def elif_st() -> bool:
        # { elif }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "elif"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.exp()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.mst()):
                                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                    SyntaxAnalyzer.current_index += 1
                                    if(SyntaxAnalyzer.elif_st()):
                                        return True
        # { else, while, for, return, switch, break, continue, if, take, ID, ++, --,}, break }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["else", "while", "for", "return", "switch", "break", "continue", "if", "take", "ID", "++", "--", "}", "break"]):
            return True
        return False

    @staticmethod
    def else_st() -> bool:
        # { else }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "else"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.mst()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                        SyntaxAnalyzer.current_index += 1
                        return True
        
        #{ while, for, return, switch, continue, if, take, ID, ++, --,}, break }
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in ["while", "for", "return", "switch", "continue", "if", "take", "ID", "++", "--", "}", "break"]):
            return True
        return False

    @staticmethod
    def switch() -> bool:
        # { switch }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "switch"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "("):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.exp()):
                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == ")"):
                        SyntaxAnalyzer.current_index += 1
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                            SyntaxAnalyzer.current_index += 1
                            if(SyntaxAnalyzer.case()):
                                if(SyntaxAnalyzer.default()):
                                    if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                        SyntaxAnalyzer.current_index += 1
                                        return True
        return False

    @staticmethod
    def case() -> bool:
        # { case }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "case"):
            SyntaxAnalyzer.current_index += 1
            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part in [*const]):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.mst()):
                        # if(SyntaxAnalyzer.break_st()):
                            if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                                SyntaxAnalyzer.current_index += 1
                                if(SyntaxAnalyzer.case()):
                                    return True
        elif(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "default"):
            return True
        return False
    @staticmethod
    def default() -> bool:
        # { default }
        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "default"):
                SyntaxAnalyzer.current_index += 1
                if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "{"):
                    SyntaxAnalyzer.current_index += 1
                    if(SyntaxAnalyzer.mst()):
                        if(SyntaxAnalyzer.token_set[SyntaxAnalyzer.current_index].class_part == "}"):
                            SyntaxAnalyzer.current_index += 1
                            return True
        return False