#!/usr/bin/python3

from bparser import BParser
from intbase import InterpreterBase, ErrorType

class Statement(): # In charge of holding and evaluating a single expression
    def __init__(self, val):
        expression_list = []
        expression_list.append(val[0])
        for i in range(1, len(val)):
            expression_list.append(Value.getObj(val[i])) # Process the operands of expression and store them in a list
                
        self.expression = expression_list
        self.type = None

    def create_statement(expression):
        if (expression[0] != InterpreterBase.BEGIN_DEF):
            return Statement(expression)
        else:
            return StatementBlock(expression)


    def process_expression(self, vars, classDef, call_dict={}):
        curExpr = self.expression
        command = curExpr[0]
        
        ret_val = None
###################################################################################
        if (command == InterpreterBase.PRINT_DEF): # Process the print command
            print_string = ""
            for x in curExpr[1:]: # Concatenate all the printed out values into one string
                if (not isinstance(x, Value)):
                    ret_val = Value.getVal(Value.getObj(x.process_expression(vars, classDef)), vars, classDef, printV=True)
                else:
                    ret_val = Value.getVal(x, vars, classDef, printV=True)
                print_string += str(ret_val)

            classDef.interpreter.output(print_string)
###################################################################################
        elif (command == InterpreterBase.RETURN_DEF): # Process the return comand and set the return flag to true if passed it
            if ("ret" in call_dict):
                call_dict["ret"] = True

            if (len(curExpr) >= 2):
                if (isinstance(curExpr[1], Class)):
                    return curExpr[1]
                elif (not isinstance(curExpr[1], Value)):
                    return curExpr[1].process_expression(vars, classDef)
                else:
                    return Value.getVal(curExpr[1], vars, classDef)
            else:
                return
###################################################################################
        elif(command == Interpreter.OPERATOR_ADDITION): # Process the concatenation and the integer addition operators
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = Value.getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = Value.getVal(curExpr[2], vars, classDef)

            if ((isinstance(firstExpr, str)) and isinstance(secondExpr, str)):
                return ('"' + firstExpr[1:-1] + secondExpr[1:-1] + '"')

            elif ((type(firstExpr) == type(0)) and (type(secondExpr) == type(0))):
                return (firstExpr + secondExpr)
            else:
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

###################################################################################
        elif(command == Interpreter.OPERATOR_SUBTRACTION or command == Interpreter.OPERATOR_MULT or command == Interpreter.OPERATOR_DIV or command == Interpreter.OPERATOR_MOD): # Process the arithmetic operators except +
            if (not isinstance(curExpr[1], Value)):
                firstExpr = Value.getVal(curExpr[1].process_expression(vars, classDef), vars, classDef)
            else:
                firstExpr = Value.getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = Value.getVal(curExpr[2].process_expression(vars, classDef), vars, classDef)
            else:
                secondExpr = Value.getVal(curExpr[2], vars, classDef)

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
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = Value.getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = Value.getVal(curExpr[2], vars, classDef)
            
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
        elif(command == Interpreter.OPERATOR_EQUAL or command == Interpreter.OPERATOR_NOT_EQUAL):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = Value.getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = Value.getVal(curExpr[2], vars, classDef)

            # Check if any of the possible combinations match
            if ((not (isinstance(firstExpr, str) and isinstance(secondExpr, str))) and (not (type(firstExpr) == type(True) and type(secondExpr) == type(True))) and (not ((type(firstExpr) == type(0)) and (type(secondExpr) == type(0)))) and (not (firstExpr is None and ((secondExpr is None) or isinstance(secondExpr, Class)))) and (not (secondExpr is None and ((firstExpr is None) or isinstance(firstExpr, Class))))):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            if (command == Interpreter.OPERATOR_EQUAL):
                ret_val = firstExpr == secondExpr
            else:
                ret_val = firstExpr != secondExpr
###################################################################################
        elif(command == Interpreter.OPERATOR_LOGIC_AND or command == Interpreter.OPERATOR_LOGIC_OR): # Logic and (&) and logic or (|) operators
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = Value.getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = Value.getVal(curExpr[2], vars, classDef)

            if (type(firstExpr) != type(True) and type(secondExpr) != type(True)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            if (command == Interpreter.OPERATOR_LOGIC_AND):
                ret_val = firstExpr and secondExpr
            else:
                ret_val = firstExpr or secondExpr
###################################################################################
        elif(command == Interpreter.OPERATOR_NOT): # Not operator that works only on vools
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = Value.getVal(curExpr[1], vars, classDef)

            if (type(firstExpr) != type(True)):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
                    
            return not firstExpr
###################################################################################
        elif(command == InterpreterBase.CALL_DEF): # Process call
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value

            if (not isinstance(curExpr[2], Value)):
                methodName = curExpr[2].process_expression(vars, classDef)
            else:
                methodName = curExpr[2].value

            paramList = []
            for arg in curExpr[3:]: # Generate a list of the values to be passed in to the called method
                if (isinstance(arg, Class)):
                    paramList.append(Class(arg.name, classDef.interpreter))
                elif (isinstance(arg, Method)):
                    v = Value.getVal(Value.getObj(arg.process_method(vars, classDef)), vars, classDef)
                    if (v == None):
                        paramList.append(v)
                    else:
                        paramList.append(str(v))

                elif (not isinstance(arg, Value)):
                    v = Value.getVal(Value.getObj(arg.process_expression(vars, classDef)), vars, classDef)
                    if (v == None):
                        paramList.append(v)
                    else:
                        paramList.append(str(v))
                else:
                    v = Value.getVal(arg, vars, classDef)
                    if (isinstance(v, Class)): # Copy of class since we are doing pass by value
                        paramList.append(Class(Value.getVal(arg, vars, classDef).name, classDef.interpreter))
                    else:
                        v = Value.getVal(arg, vars, classDef)
                        if (v == None):
                            paramList.append(v)
                        else:
                            paramList.append(str(v))

            if (isinstance(firstExpr, Class)): # Call the method from the provided class if both exist
                ret_val = firstExpr.method_call(methodName, paramList)
            elif (firstExpr == InterpreterBase.ME_DEF):
                ret_val = classDef.method_call(methodName, paramList)
            elif (firstExpr in vars):
                if (not isinstance(vars[firstExpr], Class)):
                    classDef.interpreter.error(ErrorType.FAULT_ERROR)
                ret_val = vars[firstExpr].method_call(methodName, paramList)
            elif(firstExpr in classDef.fields):
                if (not isinstance(classDef.fields[firstExpr], Class)):
                    classDef.interpreter.error(ErrorType.FAULT_ERROR)
                ret_val = classDef.fields[firstExpr].method_call(methodName, paramList)
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)

            return ret_val
###################################################################################
        elif (command == InterpreterBase.NEW_DEF): # Create an instance of a class if it exists
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr =  curExpr[1].value

            if (firstExpr in classDef.interpreter.classDict):
                return Class(firstExpr, classDef.interpreter)
            else:
                classDef.interpreter.error(ErrorType.TYPE_ERROR)
###################################################################################
        elif (command == InterpreterBase.SET_DEF):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = Value.getVal(curExpr[2], vars, classDef)
            
            if (firstExpr in vars): # If its a paramenter set the object to the parameter var
                vars[firstExpr] = Value.getObj(secondExpr)
            elif(firstExpr in classDef.fields): # check in class
                classDef.fields[firstExpr] = Value.getObj(secondExpr)
            else: # no such variable exists
                classDef.interpreter.error(ErrorType.NAME_ERROR)
 
            return
###################################################################################
        elif (command == InterpreterBase.INPUT_INT_DEF): # Process inputi
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value

            if (firstExpr in vars):
                vars[firstExpr] = Value.getObj(classDef.interpreter.get_input())
            elif(firstExpr in classDef.fields):
                classDef.fields[firstExpr] = Value.getObj(classDef.interpreter.get_input())
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)
###################################################################################
        elif (command == InterpreterBase.INPUT_STRING_DEF): # inputs evaluation
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value

            inputStr = '"' # add quotations around recieved input so it can be properly processed as string later.
            inputStr += classDef.interpreter.get_input()
            inputStr += '"'
            if (firstExpr in vars):
                vars[firstExpr] = Value.getObj(inputStr)
            elif (firstExpr in classDef.fields):
                classDef.fields[firstExpr] = Value.getObj(inputStr)
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)        
###################################################################################
        elif (command == InterpreterBase.IF_DEF): # IF statement evaluation
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = Value.getVal(curExpr[1], vars, classDef)

            ret_val = None
            if (type(firstExpr) != type(True)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)
                
            if (firstExpr):
                if (2 < len(curExpr) and not isinstance(curExpr[2], Value)):
                    ret_val = curExpr[2].process_expression(vars, classDef)
                elif (2 < len(curExpr)):
                    ret_val = Value.getVal(curExpr[2], vars, classDef)

            else:
                if (3 < len(curExpr) and not isinstance(curExpr[3], Value)):
                    ret_val = curExpr[3].process_expression(vars, classDef)
                elif (3 < len(curExpr)):
                    ret_val = Value.getVal(curExpr[3], vars, classDef)
###################################################################################
        elif (command == InterpreterBase.WHILE_DEF): # While loop evaluation
            if (not isinstance(curExpr[1], Value)):
                loop_eval_expr = curExpr[1].process_expression(vars, classDef)
            else:
                loop_eval_expr = Value.getVal(curExpr[1], vars, classDef)

            loop_call_dict = {"ret" : False} # Store a local return flag that if set to true will break out of loop early

            if (type(loop_eval_expr) != type(True)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            while (loop_eval_expr):  
                if (not isinstance(curExpr[2], Value)):
                    ret_val = curExpr[2].process_expression(vars, classDef, loop_call_dict)
                else:
                    ret_val = Value.getVal(curExpr[2], vars, classDef, loop_call_dict)

                if ((curExpr[2]).expression[0] == InterpreterBase.RETURN_DEF or loop_call_dict["ret"]):
                    if ("ret" in call_dict): # Set the passed in return flat to true if it was passed it 
                        call_dict["ret"] = True
                    return ret_val
                if (not isinstance(curExpr[1], Value)):
                    loop_eval_expr = curExpr[1].process_expression(vars, classDef)
                else:
                    loop_eval_expr = Value.getVal(curExpr[1], vars, classDef)

                if (type(loop_eval_expr) != type(True)):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
       
        return ret_val

class StatementBlock(): # Used to store begin blocks
    def __init__(self, val):
        self.expression = val[1]
        self.expr = [Statement.create_statement(val[x]) for x in range(1,len(val))] # Generate a statement instance for every statement in block
    
    def process_expression(self, vars, classDef, call_dict={}):
        local_call_dict = {"ret": False} # Store a flag that is set if return is called
        for expr in self.expr:
            if (expr.expression[0] == InterpreterBase.RETURN_DEF): # if its a return expression then set the return flag to true and return
                val = expr.process_expression(vars, classDef)
                if(call_dict):
                    call_dict["ret"] = True
                return val
            else:
                val = expr.process_expression(vars, classDef, call_dict=local_call_dict) # Process the next expression in block and pass in return flag
                if (local_call_dict["ret"]):
                    if(call_dict):
                        call_dict["ret"] = True
                    return val

class Class(): # Class object to create instances of classes
    def __init__(self, class_name, interpreter):
        self.name = class_name
        self.interpreter = interpreter
        self.fields = {x : (Value.getObj(val)) for x, val in interpreter.classDict[class_name]["Fields"].items()} # Generate a dictionary of fields in class each of which contain an object (expression, or value)
        self.methods =  {x : Method(val, self) for x, val in interpreter.classDict[class_name]["Methods"].items()} # Generate a dictionary of methods in class each of which contain a method object 

    def process_class(class_info, interpreter): # Generate a dictionary entry for the class using the parsed program input
        class_name = class_info[1]
        if (class_name in interpreter.classDict.keys()):
            interpreter.error(ErrorType.TYPE_ERROR)

        interpreter.classDict[class_name] = {
            "Name" : class_name,
            "Methods" : {},
            "Fields" : {}
        }
        for entry in class_info:
            if (entry[0] == InterpreterBase.METHOD_DEF): # Add a method entry to the methods list
                if (entry[1] in interpreter.classDict[class_name]["Methods"].keys()):
                    interpreter.error(ErrorType.NAME_ERROR)
                interpreter.classDict[class_name]["Methods"][entry[1]] = {
                    "Name" : entry[1],
                    "Parameters" : entry[2],
                    "Expression" : entry[3]
                }
            elif (entry[0] == InterpreterBase.FIELD_DEF): # add a field entry to the field list
                if (entry[1] in interpreter.classDict[class_name]["Fields"].keys()):
                    interpreter.error(ErrorType.NAME_ERROR)
                interpreter.classDict[class_name]["Fields"][entry[1]] = entry[2]

    def method_call(self, method_name, params): # Call the method if it exists
        if (not method_name in self.methods):
            self.interpreter.error(ErrorType.NAME_ERROR)
        return self.methods[method_name].process_method(self.fields, params) 
    
class Method(): # Handles class methods
    def __init__(self, method_info, classDef):
        self.name = method_info["Name"]
        self.params = method_info["Parameters"]
        checkParams = []
        for i in method_info["Parameters"]:
            if (i in checkParams):
                classDef.interpreter.error(ErrorType.NAME_ERROR)
            else:
                checkParams.append(i)

        self.expression = Statement.create_statement(method_info["Expression"]) 
        self.classDef = classDef
    
    def process_method(self, class_fields, params): # Map passed in values to parameters and throw error if incorrect amount passed in. 
        if (self.params):
            if (len(self.params) != len(params)):
                self.classDef.interpreter.error(ErrorType.TYPE_ERROR)
            vars = {x: Value.getObj(val) for x,val in zip(self.params, params)}
            for i in self.params:
                if (i not in vars):
                    vars[i] = InterpreterBase.NULL_DEF
        else:
            vars = {}

        return self.expression.process_expression(vars, self.classDef) # Return the called top expression of method

class Value():
    def getObj(val): # Returns the correct object for val depending on its type
        if (isinstance(val, Class) and val != None):
            return val # simply return if its a class object
        if (isinstance(val, list)):
            if (val[0] == InterpreterBase.BEGIN_DEF):
                return StatementBlock(val) # its a begin block!
            else:
                return Statement(val) # Its an expression!
        else:
            if (type(val) == type(True) or val == None):
                return Value(val) # If its a boolean pass in as is to the Value class
            else:
                return Value(str(val))  # Else make it a string to properly process

    def getVal(val, vars, classDef, printV=False): # get the valur of the passed in object, printV indicates whether or not to return the output version of value
        if (isinstance(val, Class) and val is not None):
            return val # If its a class instance, just return it 
        if (not isinstance(val, Value)):
            return Value.getVal(Value.getObj(val),vars, classDef, printV) # if it isnt a value object, process it using getObj and retry
        else:
            if (val.type == Interpreter.VARIABLE_DEF): # If its a variable attempt to get it, else throw error 
                if (val.value in vars):
                    if (printV):
                        return vars[val.value].printVal
                    if (isinstance(vars[val.value], Class)):
                        return vars[val.value]
                    return vars[val.value].value
                elif(val.value in classDef.fields):
                    if (printV):
                        return classDef.fields[val.value].printVal
                    if (isinstance(classDef.fields[val.value], Class)):
                        return classDef.fields[val.value]
                    return classDef.fields[val.value].value
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
        elif (val == InterpreterBase.TRUE_DEF or (isinstance(val, bool) and val)):
            self.value = True
            self.printVal = InterpreterBase.TRUE_DEF
            self.type = InterpreterBase.BOOL_DEF
        elif (val == InterpreterBase.FALSE_DEF or (isinstance(val, bool) and not val)):
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
           super().error(ErrorType.NAME_ERROR)

        main_object = Class(InterpreterBase.MAIN_CLASS_DEF, self) # Create main class instance
        main_object.method_call(InterpreterBase.MAIN_FUNC_DEF, []) # call the main method

        return 0