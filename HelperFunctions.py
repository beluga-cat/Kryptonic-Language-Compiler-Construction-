from SemanticAnalyzer import DataTable, FunctionDataTable, MainTable, Stack

def insert_mt(name: str, type: str, type_modifier: str, ext: str, imp: str, main_table: list[MainTable]):
    if(not lookup_mt(name, main_table)):
        main_table_row = MainTable(name, type, type_modifier, ext, imp)
        main_table.append(main_table_row)
        return main_table_row
    print('Redeclaration Error')

def insert_dt(name: str, type: str, access_modifier: str, static: bool, final: bool, abstract: bool, current_class: MainTable):
    if((not lookup_dt(name, current_class)) or (not lookup_dt_pl(name, type, current_class))):
        current_class.add_data_table_row(DataTable(name, type, access_modifier, static, final, abstract))
    print('Redeclaration Error')

def insert_ft(name: str, type: str, scope: int, scope_stack: Stack, function_table: list[FunctionDataTable]):
    if(not lookup_ft(name, scope_stack, function_table)):
        function_table.append(FunctionDataTable(name, type, scope))
    print('Redeclaration Error')

def lookup_mt(name: str, main_table: list[MainTable]) -> MainTable|None:
    for i in range(len(main_table)):
        return main_table[i] if(main_table[i].name == name) else None

def lookup_ft(name: str, scope_stack: Stack, function_table: list[FunctionDataTable]) -> str|None:
    for function_data_row in function_table:
        if(function_data_row.scope in scope_stack.stack and function_data_row.name == name):
            return function_data_row.type
    return None

def lookup_dt(name: str, current_class: MainTable):
    for data_row in current_class.data_table:
        return data_row if(data_row.name == name) else None

def lookup_dt_pl(name: str, parameter_list: str, current_class: MainTable):
    for data_row in current_class.data_table:
        if(data_row.name == name and data_row.type == parameter_list):
            pList, return_list = parameter_list1(data_row.type)
            return data_row, pList, return_list
    return None


def parameter_list1(pl: str):
    plist = pl[0: pl.find("->")]
    return_list = pl[pl.find("->"):]
    return plist, return_list

def result_type_compatibility_binary(left_operand_type, right_operand_type, operator):
    if(operator == "=" and left_operand_type == right_operand_type):
        return left_operand_type

    elif(left_operand_type == right_operand_type and left_operand_type in ['int', 'float']):
        if(operator in ["/", "/=", "%", "%="]):
            return 'float'
        if(operator in ["+", "-", "*", "+=", "-=", "*="]):
            return left_operand_type
        if(operator in ["==", "!=", ">", "<", ">=", "<=", "AND", "OR", "not"]):
            return "bool"
        

    elif(left_operand_type in ['int', 'float'] and right_operand_type in ['int', 'float']):
        if(operator in ["/", "/=", "%", "%=", "+", "-", "*", "+=", "-=", "*="]):
            return 'float'
        if(operator in ["==", "!=", ">", "<", ">=", "<=", "AND", "OR", "not"]):
            return "bool"
    
    # string string (+) -> String
    elif(left_operand_type == right_operand_type == 'string'):
        if(operator in ["+", "="]):
            return 'string'
        if(operator in ["==", "!="]): 
            return 'bool'
        
    # string int (+ *)-> String
    elif((left_operand_type == 'string' and right_operand_type == 'int') or (left_operand_type == 'int' and right_operand_type == 'string')):
        if(operator in ['+', '*']):
            return 'string'
    # bool boolean
    elif(left_operand_type == 'bool' and right_operand_type == left_operand_type):
        if(operator in ["==", "!=", "AND", "OR", "<", ">", "<=", ">="]):
            return 'bool'
    return False

def result_type_compatibility_unary(operand_type, operator):
    if(operator in ['++', '--'] and operand_type in ['int', 'float']):
        return operand_type
    elif(operator in ["not"] and operand_type in ['bool']):
        return 'bool'
    return False