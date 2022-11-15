class DataTable:
    def __init__(self, name: str, type: str, access_modifier: str, static: bool, final: bool, abstract: bool):
        self.name = name
        self.type = type
        self.access_modifier = access_modifier
        self.static = static
        self.final = final
        self.abstract = abstract
    

class MainTable:
    def __init__(self, name: str, type: str, type_modifier: str, ext: str, imp: str):
        self.name = name
        self.type = type
        self.type_modifier = type_modifier
        self.ext = ext
        self.imp = imp
        self.data_table: list[DataTable] = []
    
    def add_data_table_row(self, data_table_row: DataTable):
        self.data_table.append(data_table_row)
    
    
    def __str__(self):
        return f'{self.name} | {self.type} | {self.type_modifier} | {self.ext} | { self.imp}'

    

class FunctionDataTable:
    def __init__(self, name: str, type: str, scope: int):
        self.name = name
        self.type = type
        self.scope = scope
    

class Stack:
    scope: int = 0
    scope_list: list[int] = []
    stack: list[int]

    def __init__(self):
        self.stack = [0]

    def push(self) -> int:
        Stack.scope += 1
        self.stack.append(Stack.scope)
        return Stack.scope

    def pop(self):
        self.stack.pop()
        

    def peek(self):
        return self.stack[len(self.stack) - 1]

class SemanticAnalyzer:
    main_type_table: list[MainTable]
    data_table: list[DataTable]
    function_data_table: list[FunctionDataTable]
    current_class: MainTable|None
    scope_stack = Stack()
    
    def __init__(self):
        self.main_type_table = []
        self.data_table = []
        self.function_data_table = []
        self.current_class = None
    
    def lookup_mt(self, name: str) -> MainTable|None:
        for main_table_row in self.main_type_table:
            if(main_table_row.name == name):
                return main_table_row
        return None
    
    def lookup_ft(self, name: str) -> str|None:
        for function_data_row in self.function_data_table:
            if(function_data_row.scope in self.scope_stack.stack and function_data_row.name == name):
                return function_data_row.type
        return None
    
    def lookup_dt(self, name: str):
        if(self.current_class is None): return # ! please handle it
        for data_row in self.current_class.data_table:
            if(data_row.name == name):
                return data_row
        return None
    
    def lookup_dt_pl(self, name: str, parameter_list: str):
        if(self.current_class is None): return # ! please handle it
        for data_row in self.current_class.data_table:
            if(data_row.name == name and data_row.type == parameter_list):
                return data_row
        return None
    
    def insert_mt(self, name: str, type: str, type_modifier: str, ext: str, imp: str):
        if(not self.lookup_mt(name)):
            main_table_row = MainTable(name, type, type_modifier, ext, imp)
            self.main_type_table.append(main_table_row)
            return
        print('Redeclaration Error')
    
    def create_scope(self):
        self.scope_stack.push()
    
    def destroy_scope(self):
        self.scope_stack.pop()