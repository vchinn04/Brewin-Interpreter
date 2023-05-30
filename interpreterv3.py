#!/usr/bin/python3

from bparser import BParser
from intbase import InterpreterBase, ErrorType

class Statement(): # In charge of holding and evaluating a single expression
    def __init__(self, val, classDef):
        expression_list = []
        expression_list.append(val[0])
        for i in range(1, len(val)):
            expression_list.append(Value.getObj(val[i], classDef)) # Process the operands of expression and store them in a list
                
        self.expression = expression_list
        self.type = None
        self.classDef = classDef
        #if (val[0] in classDef.TemplateVars.keys()):
            #self.type = classDef.TemplateVars[val[0]]

    def create_statement(expression, classDef):
        #print("EXPR: ", expression)
        if (not expression):
            return None
        if (expression[0] != InterpreterBase.BEGIN_DEF and expression[0] != InterpreterBase.LET_DEF):
            return Statement(expression, classDef)
        else:
            return StatementBlock(expression, classDef)

    def process_expression(self, vars, classDef, call_dict=None, local_vars=None, get_type=False, exception_stack=None):
        curExpr = self.expression
        command = curExpr[0]
        if (not local_vars):
            local_vars = []
        if (not call_dict):
            call_dict = {}
            call_dict["exc"] = False
        if (not exception_stack):
            exception_stack = []
        ret_val = None

###################################################################################
        if (command == InterpreterBase.PRINT_DEF): # Process the print command
            try_dict = {"ret" : False, "exc" : False}
            print_string = ""
            for x in curExpr[1:]: # Concatenate all the printed out values into one string
                if (not isinstance(x, Value)):
                    print_val = Value.getVal(Value.getObj(x.process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict), classDef), vars,local_vars, classDef, printV=True)
                else:
                    print_val = Value.getVal(x, vars, local_vars, classDef, printV=True)
                if (try_dict["exc"]):
                    call_dict["ret"] = True
                    call_dict["exc"] = True
                    return print_val

                print_string += str(print_val)
            classDef.interpreter.output(print_string)
###################################################################################
        elif (command == InterpreterBase.RETURN_DEF): # Process the return comand and set the return flag to true if passed it. Return a tuple of the value and its type
            if ("ret" in call_dict):
                call_dict["ret"] = True
            try_dict = {"ret" : False, "exc" : False}

            if (len(curExpr) >= 2):
                if (isinstance(curExpr[1], Class)):
                    return (curExpr[1], curExpr[1].name)
                elif (not isinstance(curExpr[1], Value)):
                    v = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
                    if (try_dict["exc"]):
                        call_dict["ret"] = True
                        call_dict["exc"] = True
                        return v
                    v = (v, curExpr[1].process_expression(vars, classDef, local_vars=local_vars, get_type=True)) # Return the value of the expression and its type
                    return v
                elif (curExpr[1].value == InterpreterBase.ME_DEF):
                    return (classDef.get_inst_class(), classDef.name)
                else:
                    return (Value.getVal(curExpr[1], vars, local_vars, classDef), Value.get_string_type(curExpr[1], vars, local_vars, classDef))
            else:
                return (None, InterpreterBase.VOID_DEF)
###################################################################################
        elif(command == Interpreter.OPERATOR_ADDITION): # Process the concatenation and the integer addition operators
            try_dict = {"ret" : False, "exc" : False}

            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                firstExpr = Value.getVal(curExpr[1], vars, local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr
            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                secondExpr = Value.getVal(curExpr[2], vars, local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return secondExpr
            if ((isinstance(firstExpr, str)) and isinstance(secondExpr, str)):
                if (get_type):
                    return InterpreterBase.STRING_DEF
                return ('"' + firstExpr[1:-1] + secondExpr[1:-1] + '"')

            elif ((type(firstExpr) == type(0)) and (type(secondExpr) == type(0))):
                if (get_type):
                    return InterpreterBase.INT_DEF
                return (firstExpr + secondExpr)
            else:
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

###################################################################################
        elif(command == Interpreter.OPERATOR_SUBTRACTION or command == Interpreter.OPERATOR_MULT or command == Interpreter.OPERATOR_DIV or command == Interpreter.OPERATOR_MOD): # Process the arithmetic operators except +
            if (get_type):
                return InterpreterBase.INT_DEF
            try_dict = {"ret" : False, "exc" : False}

            if (not isinstance(curExpr[1], Value)):
                firstExpr = Value.getVal(curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict), vars,local_vars, classDef)
            else:
                firstExpr = Value.getVal(curExpr[1], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr

            if (not isinstance(curExpr[2], Value)):
                secondExpr = Value.getVal(curExpr[2].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict), vars,local_vars, classDef)
            else:
                secondExpr = Value.getVal(curExpr[2], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return secondExpr

            if ((type(firstExpr) != type(0)) and (type(secondExpr) != type(0))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)

            if (command == Interpreter.OPERATOR_SUBTRACTION):
                return (firstExpr - secondExpr)
            elif(command == Interpreter.OPERATOR_MULT):
                return (firstExpr * secondExpr)
            elif(command == Interpreter.OPERATOR_DIV):
                return firstExpr // secondExpr
            else:
                return (firstExpr % secondExpr)
###################################################################################
        elif(command == Interpreter.OPERATOR_GREATER or command == Interpreter.OPERATOR_LESS or command == Interpreter.OPERATOR_GREQ or command == Interpreter.OPERATOR_LSEQ): # Process the equality operators
            if (get_type):
                return InterpreterBase.BOOL_DEF

            try_dict = {"ret" : False, "exc" : False}

            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                firstExpr = Value.getVal(curExpr[1], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr
            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                secondExpr = Value.getVal(curExpr[2], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return secondExpr
            if ((not isinstance(firstExpr, str) and (type(firstExpr) != type(0))) or (type(secondExpr) != type(firstExpr))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)

            if (command == Interpreter.OPERATOR_GREATER):
                ret_val = firstExpr > secondExpr
            elif (command == Interpreter.OPERATOR_LESS):
                ret_val = firstExpr < secondExpr
            elif (command == Interpreter.OPERATOR_GREQ):
                ret_val = firstExpr >= secondExpr
            else:
                ret_val = firstExpr <= secondExpr
###################################################################################
        elif(command == Interpreter.OPERATOR_EQUAL or command == Interpreter.OPERATOR_NOT_EQUAL): # (==) and (!=) operators
            if (get_type):
                return InterpreterBase.BOOL_DEF

            try_dict = {"ret" : False, "exc" : False}

            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                firstExpr = Value.getVal(curExpr[1], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr
            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                secondExpr = Value.getVal(curExpr[2], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return secondExpr        

            if  (isinstance(firstExpr, Class) and isinstance(secondExpr, Class) and (secondExpr.check_type(firstExpr.name) or firstExpr.check_type(secondExpr.name))): # If both of the compared objects are classes of compatible types
                if (command == Interpreter.OPERATOR_EQUAL):
                    return firstExpr is secondExpr
                else:
                    return firstExpr is not secondExpr
            elif(isinstance(firstExpr, Class) and isinstance(secondExpr, Class)): 
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            if  (((isinstance(firstExpr, Class) or (firstExpr is None)) and (isinstance(secondExpr, Class) or (secondExpr is None)))): # if one of the objects is a class and the other null

                #Get  the types of both objects (or their variable types)
                if (not isinstance(curExpr[1], Value)):
                    firs_type = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, get_type=True)
                else:
                    firs_type = Value.get_string_type(curExpr[1], vars, local_vars, classDef)
                
                if (not isinstance(curExpr[2], Value)):
                    second_type = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, get_type=True)
                else:
                    second_type = Value.get_string_type(curExpr[2], vars, local_vars, classDef)
                
                if (Class.compare_class_types(firs_type, second_type, classDef.interpreter, class1_obj=firstExpr, class2_obj=secondExpr)): # compare the two types
                    if (command == Interpreter.OPERATOR_EQUAL):
                        return firstExpr is secondExpr
                    else:
                        return firstExpr is not secondExpr
                else:
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)

            # Check if all of the possible combinations do not match
            if ((not (isinstance(firstExpr, str) and isinstance(secondExpr, str))) and (not (type(firstExpr) == type(True) and type(secondExpr) == type(True))) and (not ((type(firstExpr) == type(0)) and (type(secondExpr) == type(0)))) and (not (firstExpr is None and ((secondExpr is None) or isinstance(secondExpr, Class)))) and (not (secondExpr is None and ((firstExpr is None) or isinstance(firstExpr, Class))))):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            if (command == Interpreter.OPERATOR_EQUAL):
                ret_val = firstExpr == secondExpr
            else:
                ret_val = firstExpr != secondExpr
###################################################################################
        elif(command == Interpreter.OPERATOR_LOGIC_AND or command == Interpreter.OPERATOR_LOGIC_OR): # Logic and (&) and logic or (|) operators
            if (get_type):
                return InterpreterBase.BOOL_DEF
            try_dict = {"ret" : False, "exc" : False}

            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                firstExpr = Value.getVal(curExpr[1], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                secondExpr = Value.getVal(curExpr[2], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return secondExpr        

            if (type(firstExpr) != type(True) and type(secondExpr) != type(True)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            if (command == Interpreter.OPERATOR_LOGIC_AND):
                ret_val = firstExpr and secondExpr
            else:
                ret_val = firstExpr or secondExpr
###################################################################################
        elif(command == Interpreter.OPERATOR_NOT): # Not operator that works only on bools
            if (get_type):
                return InterpreterBase.BOOL_DEF

            try_dict = {"ret" : False, "exc" : False}

            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                firstExpr = Value.getVal(curExpr[1], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr

            if (type(firstExpr) != type(True)):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
                    
            return not firstExpr
###################################################################################
        elif(command == InterpreterBase.CALL_DEF): # Process call
            try_dict = {"ret" : False, "exc" : False}
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                firstExpr = curExpr[1].value
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr

            if (not isinstance(curExpr[2], Value)):
                methodName = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                methodName = curExpr[2].value
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return methodName

            paramList = []
            for arg in curExpr[3:]: # Generate a list of the values to be passed in to the called method
                if (isinstance(arg, Class)):
                    paramList.append(arg)
                elif (isinstance(arg, Method)):
                    v = arg.process_method(vars, classDef, try_dict=try_dict)
                    if (try_dict["exc"]):
                        call_dict["ret"] = True
                        call_dict["exc"] = True
                        return v
                    v = Value.getVal(Value.getObj(v, classDef), vars,local_vars, classDef)

                    if (v == None or type(v) == type(True)):
                        paramList.append(v)
                    else:
                        paramList.append(str(v))

                elif (not isinstance(arg, Value)):
                    v = arg.process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
                    if (try_dict["exc"]):
                        call_dict["ret"] = True
                        call_dict["exc"] = True
                        return v
                    v = Value.getVal(Value.getObj(v, classDef), vars,local_vars, classDef)

                    if (v == None or isinstance(v, Class) or type(v) == type(True)):
                        paramList.append(v)
                    else:
                        paramList.append(str(v))
                else:
                    v = Value.getVal(arg, vars,local_vars, classDef)
                    if (isinstance(v, Class)): # Just append the val if its a class
                        paramList.append(v)
                    else:
                        if (v == None or type(v) == type(True)):
                            paramList.append(v)
                        else:
                            paramList.append(str(v))

            if (isinstance(firstExpr, Class)): # Call the method from the provided class if both exist
                ret_val = firstExpr.method_call(methodName, paramList, isExpr=True, get_type=get_type, try_dict=call_dict)
                return ret_val
            elif (firstExpr == InterpreterBase.ME_DEF):
                ret_val = classDef.method_call(methodName, paramList, isExpr=True, get_type=get_type, try_dict=call_dict)
                return ret_val
            elif (firstExpr == InterpreterBase.SUPER_DEF):
                ret_val = classDef.method_call(methodName, paramList, callSuper=True, get_type=get_type, try_dict=call_dict)
                return ret_val               
                
            for entr in local_vars: # check if there are any let vars
                if (firstExpr in entr):
                    if (not isinstance(entr[firstExpr]["Value"], Class)):
                        classDef.interpreter.error(ErrorType.FAULT_ERROR)
                    ret_val = entr[firstExpr]["Value"].method_call(methodName, paramList, isExpr=True, get_type=get_type, try_dict=call_dict)   
                    return ret_val

            if (firstExpr in vars):
                if (not isinstance(vars[firstExpr]["Value"], Class)):
                    classDef.interpreter.error(ErrorType.FAULT_ERROR)
                ret_val = vars[firstExpr]["Value"].method_call(methodName, paramList, isExpr=True, get_type=get_type, try_dict=call_dict)
            elif(firstExpr in classDef.fields):
                if (not isinstance(classDef.fields[firstExpr]["Value"], Class)):
                    classDef.interpreter.error(ErrorType.FAULT_ERROR)
                ret_val = classDef.fields[firstExpr]["Value"].method_call(methodName, paramList, isExpr=True, get_type=get_type, try_dict=call_dict)
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)
            #print(call_dict)
            return ret_val
###################################################################################
        elif (command == InterpreterBase.NEW_DEF): # Create an instance of a class if it exists
            try_dict = {"ret" : False, "exc" : False}

            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                firstExpr =  curExpr[1].value

            if (firstExpr in classDef.TemplateVars.keys()):
                firstExpr = classDef.TemplateVars[firstExpr]

            if (get_type):
                finStr = (firstExpr.split('@'))[0]

                if (len(firstExpr.split('@')) > 1):
                    for t in (firstExpr.split('@')[1:]):
                        v = t
                        if (t in classDef.TemplateVars.keys()):
                            v = classDef.TemplateVars[t]
                        finStr = finStr + '@' + v
                return finStr
                
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr
            
            finStr = (firstExpr.split('@'))[0]

            if (len(firstExpr.split('@')) > 1):
                for t in (firstExpr.split('@')[1:]):
                    v = t
                    if (t in classDef.TemplateVars.keys()):
                        v = classDef.TemplateVars[t]
                    finStr = finStr + '@' + v

            if ((firstExpr.split('@'))[0] in classDef.interpreter.classDict):
                return Class(finStr, classDef.interpreter)
            else:
                classDef.interpreter.error(ErrorType.TYPE_ERROR)
###################################################################################
        elif (command == InterpreterBase.SET_DEF):
            try_dict = {"ret" : False, "exc" : False}

            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                firstExpr = curExpr[1].value
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, call_dict=try_dict)
            else:
                secondExpr = Value.getVal(curExpr[2], vars,local_vars, classDef)
            if (try_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return secondExpr   

            for entr in local_vars:
                if (firstExpr in entr):
                    try_val = Value.getObj(secondExpr, classDef)
                    if (entr[firstExpr]["Type"] not in Interpreter.prim_types): # make sure if its a class type that it is compatible
                        if (not isinstance(curExpr[2], Value)):
                            second_type = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, get_type=True)
                        else:
                            second_type = Value.get_string_type(curExpr[2], vars,local_vars, classDef)

                        if (not Class.compare_class_types(entr[firstExpr]["Type"], second_type, classDef.interpreter)):
                            classDef.interpreter.error(ErrorType.TYPE_ERROR)

                    entr[firstExpr]["Value"] = Value.getObj(secondExpr, classDef)

                    if (not entr[firstExpr]["Value"].check_type(entr[firstExpr]["Type"])):
                        classDef.interpreter.error(ErrorType.TYPE_ERROR)
                    return 

            if (firstExpr in vars): # If its a paramenter set the object to the parameter var
                if (vars[firstExpr]["Type"] not in Interpreter.prim_types): # make sure if its a class type that it is compatible
                    if (not isinstance(curExpr[2], Value)):
                        second_type = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, get_type=True)
                    else:
                        second_type = Value.get_string_type(curExpr[2], vars,local_vars, classDef)
                    if (not Class.compare_class_types(vars[firstExpr]["Type"], second_type, classDef.interpreter)):
                        classDef.interpreter.error(ErrorType.TYPE_ERROR)

                vars[firstExpr]["Value"] = Value.getObj(secondExpr, classDef)

                if (not vars[firstExpr]["Value"].check_type(vars[firstExpr]["Type"])):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            elif(firstExpr in classDef.fields): # check in class
                if (classDef.fields[firstExpr]["Type"] not in Interpreter.prim_types):# make sure if its a class type that it is compatible
                    if (not isinstance(curExpr[2], Value)):
                        second_type = curExpr[2].process_expression(vars, classDef, local_vars=local_vars, get_type=True)
                    else:
                        second_type = Value.get_string_type(curExpr[2], vars,local_vars, classDef)
                    if (not Class.compare_class_types( classDef.fields[firstExpr]["Type"], second_type, classDef.interpreter)):
                        classDef.interpreter.error(ErrorType.TYPE_ERROR)
                classDef.fields[firstExpr]["Value"] = Value.getObj(secondExpr, classDef)

                if (not classDef.fields[firstExpr]["Value"].check_type(classDef.fields[firstExpr]["Type"])):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            else: # no such variable exists
                classDef.interpreter.error(ErrorType.NAME_ERROR)
            return
###################################################################################
        elif (command == InterpreterBase.INPUT_INT_DEF): # Process inputi
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars)
            else:
                firstExpr = curExpr[1].value

            for entr in local_vars:
                if (firstExpr in entr):
                    if (entr[firstExpr]["Type"] != InterpreterBase.INT_DEF):
                        classDef.interpreter.error(ErrorType.TYPE_ERROR)
                    entr[firstExpr]["Value"] = Value.getObj(classDef.interpreter.get_input(), classDef)
                    return 

            if (firstExpr in vars):
                if (vars[firstExpr]["Type"] != InterpreterBase.INT_DEF):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
                vars[firstExpr]["Value"] = Value.getObj(classDef.interpreter.get_input(), classDef)
            elif(firstExpr in classDef.fields):
                if (classDef.fields[firstExpr]["Type"] != InterpreterBase.INT_DEF):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
                classDef.fields[firstExpr]["Value"] = Value.getObj(classDef.interpreter.get_input(), classDef)
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)
###################################################################################
        elif (command == InterpreterBase.INPUT_STRING_DEF): # inputs evaluation
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars)
            else:
                firstExpr = curExpr[1].value

            inputStr = '"' # add quotations around recieved input so it can be properly processed as string later.
            inputStr += classDef.interpreter.get_input()
            inputStr += '"'
            
            for entr in local_vars:
                if (firstExpr in entr):
                    if (entr[firstExpr]["Type"] != InterpreterBase.STRING_DEF):
                        classDef.interpreter.error(ErrorType.TYPE_ERROR)
                    entr[firstExpr]["Value"] = Value.getObj(inputStr, classDef)
                    return 

            if (firstExpr in vars):
                if (vars[firstExpr]["Type"] != InterpreterBase.STRING_DEF):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)

                vars[firstExpr]["Value"] = Value.getObj(inputStr,classDef )
            elif (firstExpr in classDef.fields):
                if (classDef.fields[firstExpr]["Type"] != InterpreterBase.STRING_DEF):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
                classDef.fields[firstExpr]["Value"] = Value.getObj(inputStr, classDef)
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)        
###################################################################################
        elif (command == InterpreterBase.IF_DEF): # IF statement evaluation
            loop_call_dict = {"ret" : False, "exc" : False} # Store a local return flag that if set to true will break out of loop early

            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef, local_vars=local_vars, call_dict=loop_call_dict)
            else:
                firstExpr = Value.getVal(curExpr[1], vars,local_vars, classDef)

            if (loop_call_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return firstExpr

            ret_val = None
            if (type(firstExpr) != type(True)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)
                
            if (firstExpr):
                if (2 < len(curExpr) and not isinstance(curExpr[2], Value)):
                    ret_val = curExpr[2].process_expression(vars, classDef, call_dict=loop_call_dict, local_vars=local_vars)
                elif (2 < len(curExpr)):
                    ret_val = Value.getVal(curExpr[2], vars,local_vars, classDef)
            else:
                if (3 < len(curExpr) and not isinstance(curExpr[3], Value)):
                    ret_val = curExpr[3].process_expression(vars, classDef, call_dict=loop_call_dict, local_vars=local_vars)
                elif (3 < len(curExpr)):
                    ret_val = Value.getVal(curExpr[3], vars,local_vars, classDef)

            if (loop_call_dict["exc"]):
                call_dict["ret"] = True
                call_dict["exc"] = True
                return ret_val

            if (loop_call_dict["ret"]):
                if ("ret" in call_dict): # Set the passed in return flat to true if it was passed it 
                    call_dict["ret"] = True
                return ret_val

###################################################################################
        elif (command == InterpreterBase.WHILE_DEF): # While loop evaluation
            loop_call_dict = {"ret" : False, "exc" : False} # Store a local return flag that if set to true will break out of loop early

            if (not isinstance(curExpr[1], Value)):
                loop_eval_expr = curExpr[1].process_expression(vars, classDef, call_dict=loop_call_dict, local_vars=local_vars)
            else:
                loop_eval_expr = Value.getVal(curExpr[1], vars,local_vars, classDef)
           
            if (loop_call_dict["exc"]):
                call_dict["exc"] = True
                call_dict["ret"] = True
                return loop_eval_expr

            if (type(loop_eval_expr) != type(True)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            while (loop_eval_expr):  
                if (not isinstance(curExpr[2], Value)):
                    ret_val = curExpr[2].process_expression(vars, classDef, call_dict=loop_call_dict, local_vars=local_vars)
                else:
                    ret_val = Value.getVal(curExpr[2], vars,local_vars, classDef)

                if ((curExpr[2]).expression[0] == InterpreterBase.RETURN_DEF or loop_call_dict["ret"] or loop_call_dict["exc"]):

                    if ("ret" in call_dict): # Set the passed in return flat to true if it was passed it 
                        call_dict["ret"] = True

                    if (loop_call_dict["exc"]):
                        call_dict["ret"] = True
                        call_dict["exc"] = True
                    return ret_val

                if (not isinstance(curExpr[1], Value)):
                    loop_eval_expr = curExpr[1].process_expression(vars, classDef, call_dict=loop_call_dict, local_vars=local_vars)
                else:
                    loop_eval_expr = Value.getVal(curExpr[1], vars,local_vars, classDef)
              
                if (loop_call_dict["exc"]):
                    call_dict["exc"] = True
                    call_dict["ret"] = True
                    return loop_eval_expr

                if (type(loop_eval_expr) != type(True)):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
###################################################################################  
        elif (command == InterpreterBase.TRY_DEF):
            try_dict = {"ret" : False, "exc" : False}
            ret_val = curExpr[1].process_expression(vars, classDef, try_dict, local_vars=local_vars)
            if (try_dict["exc"]):
                try_dict = {"ret" : False, "exc" : False}
                local_vars.insert(0, {"exception" : {"Type" : InterpreterBase.STRING_DEF, "Value" : (Value.getObj(ret_val, classDef))}})
                ret_val = curExpr[2].process_expression(vars, classDef, call_dict=try_dict, local_vars=local_vars)
                local_vars.pop(0)
                if (try_dict["exc"]):
                    call_dict["ret"] = True
                    call_dict["exc"] = True
                    return ret_val
            if (try_dict["ret"]):
                call_dict["ret"] = True
                return ret_val
###################################################################################
        elif (command == InterpreterBase.THROW_DEF):
            call_dict["exc"] = True
            if ("ret" in call_dict):
                call_dict["ret"] = True
            #print(call_dict)
    

            if (not isinstance(curExpr[1], Value)):
                throw_str = curExpr[1].process_expression(vars, classDef, local_vars=local_vars)
            else:
                throw_str = Value.getVal(curExpr[1], vars,local_vars, classDef)

            if (not Value.getObj(throw_str, classDef).check_type(InterpreterBase.STRING_DEF)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            return throw_str
    
        return ret_val
        
    def check_type(self, type_name): # Return the type of expression (under ideal circustances not called)
            if (not self.type):
                return False
            if (self.type == "Check"):
                if (self.expression[0] == Interpreter.OPERATOR_ADDITION):
                    if (type_name == InterpreterBase.STRING_DEF or type_name == InterpreterBase.INT_DEF):
                        return True
                    else:
                        return False 
            return type_name == self.type

class StatementBlock(): # Used to store begin blocks
    def __init__(self, val, classDef):
        self.expression = val[1]
        self.local_vars = {}
        self.expr = []
        self.classDef = classDef
        #print("YE: ", val)
        if (val[0] == InterpreterBase.LET_DEF): # if it is a let statement, generate the local variables 
            self.local_vars = {}
            for x in val[1]:
                if (x[1] in self.local_vars.keys()):
                    self.classDef.interpreter.error(ErrorType.NAME_ERROR)
                var_type = x[0]
                finStr = (var_type.split('@'))[0]

                if (len(var_type.split('@')) > 1):
                    for t in (var_type.split('@')[1:]):
                        v = t
                        if (t in classDef.TemplateVars.keys()):
                            v = classDef.TemplateVars[t]
                        finStr = finStr + '@' + v
                var_type = finStr
                if (var_type in classDef.TemplateVars.keys()):
                    var_type = classDef.TemplateVars[(var_type)]

                if len(x) < 3:
                    if (var_type == InterpreterBase.INT_DEF):
                        var_val = '0'
                    elif (var_type == InterpreterBase.BOOL_DEF):
                        var_val = InterpreterBase.FALSE_DEF
                    elif (var_type == InterpreterBase.STRING_DEF):
                        var_val = '""'
                    else:
                        var_val =  InterpreterBase.NULL_DEF
                else:
                    var_val = x[2]


                if ((var_type not in Interpreter.prim_types or var_type == InterpreterBase.VOID_DEF) and not Class.is_valid_template(var_type, self.classDef.interpreter) and var_type not in self.classDef.TemplateVars):
                    self.classDef.interpreter.error(ErrorType.TYPE_ERROR)
                
                self.local_vars[x[1]] = {"Type" : var_type, "Value" : Value.getObj(var_val, classDef)}

            for i in self.local_vars.keys(): # double check types
                if (not self.local_vars[i]["Value"].check_type(self.local_vars[i]["Type"])):
                    self.classDef.interpreter.error(ErrorType.TYPE_ERROR)

            self.expr = [Statement.create_statement(val[x], classDef) for x in range(2,len(val))] # Generate a statement instance for every statement in block
            self.expression = val[2]
        else:
            self.expr = [Statement.create_statement(val[x], classDef) for x in range(1,len(val))] # Generate a statement instance for every statement in block

    def process_expression(self, vars, classDef, call_dict=None, local_vars=None, exception_stack=None):
        if (not call_dict):
            call_dict = {}
            call_dict["exc"] = False

        local_call_dict = {"ret": False, "exc" : False} # Store a flag that is set if return is called
        if (not local_vars):
            local_vars = []
        if (not exception_stack):
            exception_stack = []
        local_vars.insert(0, self.local_vars)

        for expr in self.expr:
            if (expr.expression[0] == InterpreterBase.RETURN_DEF): # if its a return expression then set the return flag to true and return
                val = expr.process_expression(vars, classDef, call_dict=local_call_dict, local_vars=local_vars, exception_stack=exception_stack)

                #print("HEE HEE: ", val)
                if(call_dict):
                    call_dict["ret"] = True
                if(local_call_dict["exc"]):
                    call_dict["ret"] = True
                    call_dict["exc"] = True
                local_vars.pop(0)

                return val
            else:
                val = expr.process_expression(vars, classDef, call_dict=local_call_dict, local_vars=local_vars, exception_stack=exception_stack) # Process the next expression in block and pass in return flag
                if (local_call_dict["ret"]):
                    if(call_dict):
                        call_dict["ret"] = True
                        if(local_call_dict["exc"]):
                            call_dict["ret"] = True
                            call_dict["exc"] = True
                        local_vars.pop(0)
                        return val
                if(local_call_dict["exc"]):
                    call_dict["ret"] = True
                    call_dict["exc"] = True
                    local_vars.pop(0)
                    return val
        local_vars.pop(0)

class Class(): # Class object to create instances of classes
    def __init__(self, class_name, interpreter, sub_class=None):
        if ((class_name.split('@'))[0] not in interpreter.classDict.keys()):
            interpreter.error(ErrorType.TYPE_ERROR)

        self.name = class_name
        class_name = (class_name.split('@'))[0]
        self.interpreter = interpreter
        self.SubClass = sub_class
        self.BaseClass = None
        self.TemplateVars = {}
        self.class_type = interpreter.classDict[class_name]["ClassType"]

        if (self.class_type == InterpreterBase.TEMPLATE_CLASS_DEF):
            #if (len(self.name.split('@')) > 1):
            template_vars = interpreter.classDict[class_name]["TemplateVars"]
            if (len(template_vars) != (len(self.name.split('@'))-1)):
                self.interpreter.error(ErrorType.TYPE_ERROR)
            if (len(self.name.split('@')) > 1):  
                converted_vars = (self.name.split('@'))[1:]
                for x, y in zip(template_vars, converted_vars):
                    self.TemplateVars[x] = y
                #self.TemplateVars = {x : y for x, y in zip(template_vars, converted_vars)}
                for t_type in self.TemplateVars.values():
                    if ((t_type not in Interpreter.prim_types or t_type == InterpreterBase.VOID_DEF) and (t_type not in interpreter.classDict)):
                        #print(class_name)
                        self.interpreter.error(ErrorType.TYPE_ERROR)

        #print(self.name)
        #print(self.TemplateVars)
        if ("BaseClass" in interpreter.classDict[class_name].keys()):
            self.BaseClass = Class(interpreter.classDict[class_name]["BaseClass"], interpreter, sub_class=self)
        self.fields = {}
        for x, val in interpreter.classDict[class_name]["Fields"].items():
            var_type = val["Type"]

            finStr = (var_type.split('@'))[0]

            if (len(var_type.split('@')) > 1):
                for t in (var_type.split('@')[1:]):
                    v = t
                    if (t in self.TemplateVars.keys()):
                        v = self.TemplateVars[t]
                    finStr = finStr + '@' + v
            var_type = finStr
            if (var_type in self.TemplateVars.keys()):
                var_type = self.TemplateVars[(var_type)]

            if ((var_type not in Interpreter.prim_types or var_type == InterpreterBase.VOID_DEF) and not Class.is_valid_template(var_type, interpreter) and var_type not in self.TemplateVars):
                interpreter.error(ErrorType.TYPE_ERROR)

            if (x in self.fields.keys()):
                self.interpreter.error(ErrorType.NAME_ERROR)

            if (val["Value"] is None):
                if (var_type == InterpreterBase.INT_DEF):
                    var_val = '0'
                elif (var_type == InterpreterBase.BOOL_DEF):
                    var_val = InterpreterBase.FALSE_DEF
                elif (var_type == InterpreterBase.STRING_DEF):
                    var_val = '""'
                else:
                    var_val =  InterpreterBase.NULL_DEF
            else:
                var_val = val["Value"]
            self.fields[x] = {"Type" : var_type, "Value" : Value.getObj(var_val, self)}


       # self.fields = {x : {"Type" : val["Type"], "Value" : Value.getObj(val["Value"], self)}  for x, val in interpreter.classDict[class_name]["Fields"].items()} # Generate a dictionary of fields in class each of which contain an object (expression, or value)
        for i in self.fields.keys():
           # print(self.fields[i]["Type"])
         #   if (self.fields[i]["Type"] in self.TemplateVars.keys()):
              #  self.fields[i]["Type"] = self.TemplateVars[(self.fields[i]["Type"])]
            if (not self.fields[i]["Value"].check_type(self.fields[i]["Type"])):
                print(self.fields[i]["Value"].type, self.fields[i]["Type"])
                self.interpreter.error(ErrorType.TYPE_ERROR)
        #print(self.fields)
        self.methods =  {x : Method(val, self) for x, val in interpreter.classDict[class_name]["Methods"].items()} # Generate a dictionary of methods in class each of which contain a method object 

    def process_class(class_info, interpreter): # Generate a dictionary entry for the class using the parsed program input
        class_name = class_info[1]
        if (class_name in interpreter.classDict.keys()):
            interpreter.error(ErrorType.TYPE_ERROR)

        interpreter.classDict[class_name] = {
            "Name" : class_name,
            "ClassType" : class_info[0], 
            "Methods" : {},
            "Fields" : {}
        }
        if (class_info[0] == InterpreterBase.TEMPLATE_CLASS_DEF):
            interpreter.classDict[class_name]["TemplateVars"] = class_info[2]
            if (class_info[3] == InterpreterBase.INHERITS_DEF):
                interpreter.classDict[class_name]["BaseClass"] = class_info[4]

        if (class_info[2] == InterpreterBase.INHERITS_DEF):
            interpreter.classDict[class_name]["BaseClass"] = class_info[3]
        for entry in class_info:
            if (entry[0] == InterpreterBase.METHOD_DEF): # Add a method entry to the methods list
                if (entry[2] in interpreter.classDict[class_name]["Methods"].keys()):
                    interpreter.error(ErrorType.NAME_ERROR)
                interpreter.classDict[class_name]["Methods"][entry[2]] = {
                    "Name" : entry[2],
                    "ReturnType" : entry[1],
                    "Parameters" : entry[3],
                    "Expression" : entry[4]
                }
            elif (entry[0] == InterpreterBase.FIELD_DEF): # add a field entry to the field list
                if (entry[2] in interpreter.classDict[class_name]["Fields"].keys()):
                    interpreter.error(ErrorType.NAME_ERROR)
                interpreter.classDict[class_name]["Fields"][entry[2]] = {
                    "Type" : entry[1]
                }
                if len(entry) < 4:
                    var_val = None
                else:
                    var_val = entry[3]
                interpreter.classDict[class_name]["Fields"][entry[2]]["Value"] = var_val

    def check_type(self, type_name): # return if the class is correct type (either needed type or subclass of needed type)
        if (type_name == self.name):
            return True
        else:
            if (self.BaseClass): 
                return self.BaseClass.check_type(type_name)
            else:
                return False

    def is_valid_template(template_name, interpreter):
        class_name = (template_name.split('@'))[0]
        if (class_name in interpreter.classDict):
            if (interpreter.classDict[class_name]["ClassType"] == InterpreterBase.TEMPLATE_CLASS_DEF):
                return (len(template_name.split('@')) - 1) == len(interpreter.classDict[class_name]["TemplateVars"])
            else:
                return (len(template_name.split('@')) <= 1)
        else:
            return False

   
    def get_inst_class(self):  # Get the lowest level class (the class type that was instantiated)
        if (self.SubClass):
            return self.SubClass.get_inst_class()
        return self

    def compare_class_types(class1, class2, interpreter, class1_obj=None, class2_obj=None ): # Check if two class types are compatible
        if ((class1 == InterpreterBase.NULL_DEF or class1 == InterpreterBase.VOID_DEF) or (class2 == InterpreterBase.NULL_DEF or class2 == InterpreterBase.VOID_DEF)):
            return True
        if (not class1_obj):
            class1_obj = Class(class1, interpreter)
        if (not class2_obj):
            class2_obj  = Class(class2, interpreter)
        return (class1_obj.check_type(class2) or class2_obj.check_type(class1))

    def method_call(self, method_name, params, callSuper=False, isExpr=False, get_type=False, try_dict=None): # Call the method if it exists (get_type is used to get the return type)
        if (self.SubClass and isExpr): # call the subclass if isExpr is true
            return self.SubClass.method_call(method_name, params, isExpr=True, get_type=get_type, try_dict=try_dict)
        if (method_name not in self.methods or callSuper): # if method does not exist and a superclass exists, try it, else error
            if (self.BaseClass):
                return self.BaseClass.method_call(method_name, params, get_type=get_type, try_dict=try_dict)
            self.interpreter.error(ErrorType.NAME_ERROR)
        else:
            return self.methods[method_name].process_method(self.fields, params, get_type=get_type, try_dict=try_dict) 
    
class Method(): # Handles class methods
    def __init__(self, method_info, classDef):
        self.name = method_info["Name"]
        self.return_type = method_info["ReturnType"]

        finStr = (self.return_type.split('@'))[0]

        if (len(self.return_type.split('@')) > 1):
            for t in (self.return_type.split('@')[1:]):
                v = t
                if (t in classDef.TemplateVars.keys()):
                    v = classDef.TemplateVars[t]
                finStr = finStr + '@' + v
        self.return_type = finStr

        if (self.return_type in classDef.TemplateVars.keys()):
            self.return_type = classDef.TemplateVars[(self.return_type)]
        if ((self.return_type not in Interpreter.prim_types) and (self.return_type.split('@'))[0] not in classDef.interpreter.classDict): # check if it is a valid return type
            classDef.interpreter.error(ErrorType.TYPE_ERROR)

        self.params = method_info["Parameters"]
        checkParams = []
        self.classDef = classDef
        for i in method_info["Parameters"]:
            if ((i[0] not in Interpreter.prim_types or i[0] == InterpreterBase.VOID_DEF) and not Class.is_valid_template(i[0], self.classDef.interpreter) and i[0] not in self.classDef.TemplateVars):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            if (i[1] in checkParams):
                classDef.interpreter.error(ErrorType.NAME_ERROR)
            else:
                checkParams.append(i[1])


        self.expression = Statement.create_statement(method_info["Expression"], self.classDef) 
        self.classDef = classDef
    
    def process_method(self, class_fields, params, get_type=False, try_dict=None): # Map passed in values to parameters and throw error if incorrect amount passed in. 
        no_skip = True

        if (self.params):
            if (len(self.params) != len(params)): # if incorrect lengths try superclass else error
                if (self.classDef.BaseClass):
                    no_skip = False
                    ret_val = self.classDef.method_call(self.name, params, callSuper=True, get_type=get_type, try_dict=try_dict)
                else:
                    self.classDef.interpreter.error(ErrorType.NAME_ERROR)
            if (no_skip):
                vars = {} 
                for x, val in zip(self.params, params): 
                                                        #{x[1]: {"Type" : x[0], "Value" : Value.getObj(val, self.classDef)} for x,val in zip(self.params, params)}
                    val_type = x[0]
                    finStr = (val_type.split('@'))[0]

                    if (len(val_type.split('@')) > 1):
                        for t in (val_type.split('@')[1:]):
                            v = t
                            if (t in self.classDef.TemplateVars.keys()):
                                v = self.classDef.TemplateVars[t]
                            finStr = finStr + '@' + v
                    val_type = finStr
                    #vars[i]["Type"] = finStr


                    vars[x[1]] = {"Type" : val_type, "Value" : Value.getObj(val,self.classDef)}
                for i in vars.keys(): # check if types match, if they do not try to call a superclass if it exists, else throw an error
                    if (vars[i]["Type"] in self.classDef.TemplateVars.keys()):
                        vars[i]["Type"] = self.classDef.TemplateVars[(vars[i]["Type"])]
                    if (isinstance(vars[i]["Value"], Class)):
                        if (not vars[i]["Value"].check_type(vars[i]["Type"])):
                            if (self.classDef.BaseClass):
                                no_skip = False
                                ret_val = self.classDef.method_call(self.name, params, callSuper=True, get_type=get_type, try_dict=try_dict)
                                break
                            else:
                                self.classDef.interpreter.error(ErrorType.NAME_ERROR)
                    elif (vars[i]["Value"].type == InterpreterBase.NULL_DEF):
                        if (vars[i]["Type"] in Interpreter.prim_types):
                            if (self.classDef.BaseClass):
                                no_skip = False
                                ret_val = self.classDef.method_call(self.name, params, callSuper=True, get_type=get_type, try_dict=try_dict)
                                break
                            else:
                                self.classDef.interpreter.error(ErrorType.NAME_ERROR)
                    else:
                        if(vars[i]["Type"] != vars[i]["Value"].type):
                            if (self.classDef.BaseClass):
                                no_skip = False
                                ret_val = self.classDef.method_call(self.name, params, callSuper=True, get_type=get_type, try_dict=try_dict)
                                break
                            else:
                                self.classDef.interpreter.error(ErrorType.NAME_ERROR)
                if(try_dict and try_dict["exc"]):
                    try_dict["exc"] = True
                    try_dict["ret"] = True
                    return ret_val
        else:
            if (len(params) > 0): # if incorrect lengths try superclass else error
                if (self.classDef.BaseClass):
                    no_skip = False
                    ret_val = self.classDef.method_call(self.name, params, callSuper=True, get_type=get_type, try_dict=try_dict)
                else:
                    self.classDef.interpreter.error(ErrorType.NAME_ERROR)
            vars = {}
            if(try_dict and try_dict["exc"]):
                try_dict["exc"] = True
                try_dict["ret"] = True
                return ret_val

        if (no_skip):
            if (get_type): 
                return self.return_type
            method_call_dict = {"ret" : False, "exc" : False}
            if (self.expression):
                ret_val = self.expression.process_expression(vars, self.classDef, call_dict=method_call_dict) # Return the called top expression of method
            else:
                ret_val = None 
            #print(method_call_dict)
            if (method_call_dict["exc"]):
                if(try_dict):
                    try_dict["exc"] = True
                    try_dict["ret"] = True

                if(self.name == InterpreterBase.MAIN_FUNC_DEF):
                    self.classDef.interpreter.error(ErrorType.NAME_ERROR)

                return ret_val
            if (type(ret_val) is tuple): # If its a return from return statement unpack it
                ret_type = ret_val[1]
                ret_val = ret_val[0]
            else: # there was no return
                ret_val = None
                ret_type = InterpreterBase.VOID_DEF

            if (ret_val is None and ret_type != InterpreterBase.VOID_DEF): # if null is returned for an incompatible type
                if (self.return_type in Interpreter.prim_types):
                    self.classDef.interpreter.error(ErrorType.TYPE_ERROR)
                if (not Class.compare_class_types(self.return_type, ret_type, self.classDef.interpreter)):
                    self.classDef.interpreter.error(ErrorType.TYPE_ERROR)
            #print("VAL" , ret_val)
            if (not ret_val): # if not return type then return the default 
                if (self.return_type == InterpreterBase.VOID_DEF):
                    return
                if (self.return_type == InterpreterBase.INT_DEF):
                    return 0
                if (self.return_type == InterpreterBase.BOOL_DEF):
                    return False
                if (self.return_type == InterpreterBase.STRING_DEF):
                    return '""'
                return None

        if (not get_type):
            ret_val_obj = Value.getObj(ret_val, self.classDef)
            if (not ret_val_obj.check_type(self.return_type) and not (ret_val_obj.check_type(InterpreterBase.NULL_DEF) and self.return_type == InterpreterBase.VOID_DEF)): # double check if the return type matches the type of returned object
                self.classDef.interpreter.error(ErrorType.TYPE_ERROR)

        return ret_val

class Value():
    def getObj(val, classDef): # Returns the correct object for val depending on its type
        if (isinstance(val, Class) and val != None):
            return val # simply return if its a class object
        if (isinstance(val, list)):
            if (val[0] == InterpreterBase.BEGIN_DEF or val[0] == InterpreterBase.LET_DEF):
                return StatementBlock(val, classDef) # its a begin block!
            else:
                return Statement(val, classDef) # Its an expression!
        else:
            if (type(val) == type(True) or val == None):
                return Value(val) # If its a boolean pass in as is to the Value class
            else:
                return Value(str(val))  # Else make it a string to properly process

    def getVal(val, vars,local_vars, classDef, printV=False): # get the valur of the passed in object, printV indicates whether or not to return the output version of value
        if (isinstance(val, Class) and val is not None):
            return val # If its a class instance, just return it 
        if (not isinstance(val, Value)):
            return Value.getVal(Value.getObj(val,classDef),vars,local_vars, classDef, printV) # if it isnt a value object, process it using getObj and retry
        else:
            if (val.type == Interpreter.VARIABLE_DEF): # If its a variable attempt to get it, else throw error 

                for entr in local_vars:
                    if (val.value in entr):
                        if (printV):
                            return entr[val.value]["Value"].printVal
                        if (isinstance(entr[val.value]["Value"], Class)):
                            return entr[val.value]["Value"]
                        return entr[val.value]["Value"].value

                if (val.value in vars):
                    if (printV):
                        return vars[val.value]["Value"].printVal
                    if (isinstance(vars[val.value]["Value"], Class)):
                        return vars[val.value]["Value"]
                    return vars[val.value]["Value"].value
                elif(val.value in classDef.fields):
                    if (printV):
                        return classDef.fields[val.value]["Value"].printVal
                    if (isinstance(classDef.fields[val.value]["Value"], Class)):
                        return classDef.fields[val.value]["Value"]
                    return classDef.fields[val.value]["Value"].value
                else:
                    classDef.interpreter.error(ErrorType.NAME_ERROR)
            else: # Its just a normal value, simply return the stored value
                if (printV):
                    return val.printVal
                return val.value

    def __init__(self, val): # Process the passed in value and assign the needed values
        self.value = val 
        self.printVal = str(val)
        if (isinstance(val, Class)):
            self.type = Interpreter.CLASS_TYPE_DEF
            self.value = Class(val.name, val.interpreter) 
            self.printVal = Interpreter.CLASS_TYPE_DEF
        elif (val == InterpreterBase.TRUE_DEF or (type(val) == type(True) and val)):
            self.value = True
            self.printVal = InterpreterBase.TRUE_DEF
            self.type = InterpreterBase.BOOL_DEF
        elif (val == InterpreterBase.FALSE_DEF or (type(val) == type(True) and not val)):
            self.value = False
            self.printVal = InterpreterBase.FALSE_DEF
            self.type = InterpreterBase.BOOL_DEF
        elif (val == InterpreterBase.NULL_DEF or val == None):
            self.value = None
            self.printVal = InterpreterBase.NULL_DEF
            self.type = InterpreterBase.NULL_DEF
        elif (val[0] == '"'):
            self.type = InterpreterBase.STRING_DEF
            self.printVal = val[1:-1] # Remove the double quotes for output version
        else:
            try:
                self.value = int(val)
                self.type = InterpreterBase.INT_DEF
            except:
                self.value = val 
                self.type = Interpreter.VARIABLE_DEF

    def get_string_type(val, vars,local_vars, classDef): # return the type of the variable or the type of the value
        if (isinstance(val, Class) and val is not None):
            return val.name # If its a class instance, just return it 
        if (not isinstance(val, Value)):
            return Value.getObj(val,classDef).type # if it isnt a value object, process it using getObj and retry
        else:
            if (val.type == Interpreter.VARIABLE_DEF): # If its a variable attempt to get its type, else throw error 
                for entr in local_vars:
                    if (val.value in entr):
                        if (isinstance(entr[val.value]["Value"], Class)):
                            return entr[val.value]["Value"].name
                        return entr[val.value]["Type"]

                if (val.value in vars):
                    if (isinstance(vars[val.value]["Value"], Class)):
                        return vars[val.value]["Value"].name
                    return vars[val.value]["Type"]
                elif(val.value in classDef.fields):
                    if (isinstance(classDef.fields[val.value]["Value"], Class)):
                        return classDef.fields[val.value]["Value"].name
                    return classDef.fields[val.value]["Type"]
                else:
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            else: 
                return val.type

    def check_type(self, type_name): # Check if the values type matches the passed in type. Return True if it does else False
            if (type_name == self.type or (type_name not in Interpreter.prim_types and self.type == InterpreterBase.NULL_DEF)):
                return True
            else:
                return False

class Interpreter(InterpreterBase):
    # Constants
    VARIABLE_DEF = "Variable"
    CLASS_TYPE_DEF = "Class"

    OPERATOR_ADDITION = '+'
    OPERATOR_SUBTRACTION = '-'
    OPERATOR_MULT = '*'
    OPERATOR_DIV = '/'
    OPERATOR_MOD = '%'

    OPERATOR_GREATER = '>'
    OPERATOR_LESS = '<'
    OPERATOR_GREQ = '>='
    OPERATOR_LSEQ = '<='
    OPERATOR_EQUAL = '=='
    OPERATOR_NOT_EQUAL = '!='
    OPERATOR_LOGIC_AND = '&'
    OPERATOR_LOGIC_OR = '|'
    OPERATOR_NOT = '!'

    typeTable = {
        '+' : "Check",
        '-' : InterpreterBase.INT_DEF,
        '*' : InterpreterBase.INT_DEF,
        '/' : InterpreterBase.INT_DEF,
        '%' : InterpreterBase.INT_DEF,
        '>' : InterpreterBase.BOOL_DEF,
        '<'  : InterpreterBase.BOOL_DEF,
        '>='  : InterpreterBase.BOOL_DEF,
        '<='  : InterpreterBase.BOOL_DEF,
        '=='  : InterpreterBase.BOOL_DEF,
        '!=' : InterpreterBase.BOOL_DEF,
        '&' : InterpreterBase.BOOL_DEF,
        '|'  : InterpreterBase.BOOL_DEF,
        '!'  : InterpreterBase.BOOL_DEF
    }
    prim_types = [InterpreterBase.BOOL_DEF, InterpreterBase.INT_DEF, InterpreterBase.STRING_DEF, InterpreterBase.VOID_DEF]
    # Methods
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp) 
        self.classDict = {}

    def run(self, program):
        result, parsed_program = BParser.parse(program)
        if result == False:
            return 1

        for class_def in parsed_program:
            Class.process_class(class_def, self)

        if (InterpreterBase.MAIN_CLASS_DEF not in self.classDict): # No main class exists!
           super().error(ErrorType.TYPE_ERROR)

        main_object = Class(InterpreterBase.MAIN_CLASS_DEF, self) # Create main class instance
        main_object.method_call(InterpreterBase.MAIN_FUNC_DEF, []) # call the main method

        return 0
