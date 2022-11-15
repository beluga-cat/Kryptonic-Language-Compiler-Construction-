import re
from tokenize import Token


filepathi = "D:\\6th Semester\\CC\\Kryptonic Language\\Project\\output.txt"
fi = open (filepathi, "r", encoding="utf-8")
filepatho = "D:\\6th Semester\\CC\\Kryptonic Language\\Project\\Tokens.txt"
fo = open (filepatho, "w", encoding="utf-8")

KeyWords = [["int","double","String", "bool", "if","else", "elseif","for","while","switch","case","class","child_of","present","super","fixed", "new","interface","constructor","shared","own","$function", "return", "abstract", "void"],
            ["INT_DT","DOUBLE_DT","STRING_DT","BOOL_DT","COND_ST","COND_ST","COND_ST","ITER_ST","ITER_ST","ITER_ST","ITER_ST","class","child_of","present","super","fixed", "new","interface","constructor","shared","own","Func_dec", "return", "abstract", "void"]]
Operators = [["+", "-", "/", "*", "=", ">", "<", "!", "%", ">=","<=","==","+=","-=", "*=", "!=","++","--"],
             ["PM","PM","DM","DM","=","REL_OPERATOR","REL_OPERATOR","!","REMAINDER","CRO","CRO","CO","CO","CO","CO","CO","INC_DEC","INC_DEC"]]
Punctuators = [["[", "]", "{", "}", "(", ")", ",", ".", ";","[]","{}","()"]]
Tokens = []

retVal = False
for l in fi:
    i=0
    j=0
    k=0
    lineCounter0 = f"{l[-2:]}"
    lineCounter1 = lineCounter0.strip()

    strg = l[0:l.index("↓")]

    # KWs
    while i < 24:
        retVal = (KeyWords[0][i] == strg)
        if retVal == True:
            Tokens.append(f"({KeyWords[1][i]}, {strg}, Line #{lineCounter1})")
            # continue
        i += 1
    
    # isOperator
    while j < 18:
        retVal = (Operators[0][j] == strg)
        if retVal == True:
            Tokens.append(f"({Operators[1][j]}, {strg}, Line #{lineCounter1})")        
            # continue
        j += 1
    # isPunctuator
    while k < 12:
        retVal = (Punctuators[0][k] == strg)
        if retVal == True:
            Tokens.append(f"({Punctuators[0][k]}, {strg}, Line #{lineCounter1})")        
            # continue
        k += 1
    # isChar
    if strg[0] == "'" and strg[-1] == "'":
        Tokens.append(f"(CHAR_CONST, {strg}, Line #{lineCounter1})")
        # continue
    # isString
    pattern = re.compile(r'^\"((\\[\\\'\"\w])*|[A-Za-z0-9 \+\-\*/=@#\$%\^&_()\[\]\{\}:;,.?<>]*)*\"$')
    if bool(pattern.fullmatch(strg)):
        Tokens.append(f"(STRING_CONST, {strg}, Line #{lineCounter1})")
    
    # isFloat
    pattern = re.compile(r'(\+|\-)?(\d+|(\d*\.\d+))')
    if bool(pattern.fullmatch(strg)):
        Tokens.append(f"(ID, {strg}, Line #{lineCounter1})")

    # isID
    pattern = re.compile(r'^[A-Za-z_]*[A-Za-z0-9_]+$')
    if bool(pattern.fullmatch(strg)):
        Tokens.append(f"(ID, {strg}, Line #{lineCounter1})")
        

print(Tokens)
for tok in Tokens:
    fo.write(f"{tok}\n")