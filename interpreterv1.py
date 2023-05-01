#!/usr/bin/python3

from bparser import BParser
from intbase import InterpreterBase, ErrorType
#globalC = 10
def getObj(val):
    if (isinstance(val, list)):
        if (val[0] == "begin"):
            return StatementBlock(val)
        else:
            return Statement(val)
    else:
        if (isinstance(val, bool)):
            return Value(val)
        else:
            return Value(str(val)) 

def getVal(val, vars, classDef, printV=False):
    if (not isinstance(val, Value)):
        return val
    else:
        if (val.type == "Variable"):
            if (val.value in vars):
                if (printV):
                    return vars[val.value].printVal
                return vars[val.value].value
            elif(val.value in classDef.fields):
                if (printV):
                    return classDef.fields[val.value].printVal
                return classDef.fields[val.value].value
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)
        else:
            if (printV):
                return val.printVal
            return val.value

class Statement():
    def __init__(self, val):
        expression_list = []
        expression_list.append(val[0])
        for i in range(1, len(val)):
            expression_list.append(getObj(val[i]))
                
        self.expression = expression_list
        self.type = None
    def create_statement(expression):
        if (expression[0] != 'begin'):
            return Statement(expression)
        else:
            return StatementBlock(expression)
    def get_var(self, vars, classDef, ind):
        if (ind in vars):
            return vars[ind]
        else:
            return classDef.fields[ind]

    def process_expression(self, vars, classDef):
        #global globalC
        #print("Processing Expression!")
        curExpr = self.expression
        command = curExpr[0]
        curVal = None
###################################################################################
        if (command == "print"):
            if (not isinstance(curExpr[1], Value)):
                curVal = curExpr[1].process_expression(vars, classDef)
            else:
                curVal = getVal(curExpr[1], vars, classDef, printV=True)

            #classDef.print(curVal)
            classDef.interpreter.output(str(curVal))

###################################################################################
        elif (command == "return"):
            if (not isinstance(curExpr[1], Value)):
               return curExpr[1].process_expression(vars, classDef)
            else:
               return getVal(curExpr[1], vars, classDef)

###################################################################################
        elif(command == "+"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)

            if ((not isinstance(firstExpr, str) and not isinstance(firstExpr, int)) or (type(secondExpr) != type(firstExpr))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)

            curVal = firstExpr + secondExpr
###################################################################################
        elif(command == "-"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)

            if ((not isinstance(firstExpr, int)) or (not isinstance(secondExpr, int))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return (firstExpr - secondExpr)
###################################################################################
        elif(command == "*"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)
   
            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)

            if ((not isinstance(firstExpr, int)) or (not isinstance(secondExpr, int))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return firstExpr * secondExpr
###################################################################################
        elif(command == "/"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)
   
            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)

            if ((not isinstance(firstExpr, int)) or (not isinstance(secondExpr, int))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            
            curVal = firstExpr / secondExpr
###################################################################################
        elif(command == "%"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)
            
            if ((not isinstance(firstExpr, int)) or (not isinstance(secondExpr, int))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)

            curVal = firstExpr % secondExpr
###################################################################################
        elif(command == ">"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)
            
            if ((not isinstance(firstExpr, str) and not isinstance(firstExpr, int)) or (type(secondExpr) != type(firstExpr))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)

            curVal = firstExpr > secondExpr
###################################################################################
        elif(command == "<"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)

            if ((not isinstance(firstExpr, str) and not isinstance(firstExpr, int)) or (type(secondExpr) != type(firstExpr))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            curVal = firstExpr < secondExpr
###################################################################################
        elif(command == ">="):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)
            if ((not isinstance(firstExpr, str) and not isinstance(firstExpr, int)) or (type(secondExpr) != type(firstExpr))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            curVal = firstExpr >= secondExpr
###################################################################################
        elif(command == "<="):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)
            if ((not isinstance(firstExpr, str) and not isinstance(firstExpr, int)) or (type(secondExpr) != type(firstExpr))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            curVal = firstExpr <= secondExpr

###################################################################################
        elif(command == "=="):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)
            if (((   not isinstance(firstExpr, str) and not isinstance(firstExpr, bool) and not isinstance(firstExpr, int)) or (type(secondExpr) != type(firstExpr))) and ((not isinstance(firstExpr, Class) and not isinstance(secondExpr, None)) or (not isinstance(secondExpr, Class) and not isinstance(firstExpr, None)))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return firstExpr == secondExpr

###################################################################################
        elif(command == "!="):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)
            if (((   not isinstance(firstExpr, str) and not isinstance(firstExpr, bool) and not isinstance(firstExpr, int)) or (type(secondExpr) != type(firstExpr))) and ((not isinstance(firstExpr, Class) and not isinstance(secondExpr, None)) or (not isinstance(secondExpr, Class) and not isinstance(firstExpr, None)))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return firstExpr != secondExpr
###################################################################################
        elif(command == "&"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)
            if ((not isinstance(firstExpr, bool)) or (not isinstance(secondExpr, bool))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return firstExpr and secondExpr
###################################################################################
        elif(command == "|"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)
            if ((not isinstance(firstExpr, bool)) or (not isinstance(secondExpr, bool))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return firstExpr or secondExpr
###################################################################################
        elif(command == "!"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if ((not isinstance(firstExpr, bool))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return not firstExpr
###################################################################################
        elif(command == "call"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value

            if (not isinstance(curExpr[2], Value)):
                methodName = curExpr[2].process_expression(vars, classDef)
            else:
                methodName = curExpr[2].value

            #if (not isinstance(curExpr[3], Value)):
              #  methodName = curExpr[3].process_expression(vars, classDef)
           # else:
              #  methodName = getVal(curExpr[3], vars, classDef)
            paramList = []
            for arg in curExpr[3:]:
                if (not isinstance(arg, Value)):
                    paramList.append(str(arg.process_expression(vars, classDef)))
                else:
                    paramList.append(str(getVal(arg, vars, classDef)))

            if (firstExpr == "me"):
                curVal = classDef.method_call(methodName, paramList)
            elif (firstExpr in vars):
                if (not isinstance(firstExpr[vars], Class)):
                    classDef.interpreter.error(ErrorType.FAULT_ERROR)
                curVal = vars[firstExpr].method_call(methodName, paramList)
            elif(firstExpr in classDef.fields):
                if (not isinstance(firstExpr[vars], Class)):
                    classDef.interpreter.error(ErrorType.FAULT_ERROR)
                curVal = classDef.fields[firstExpr].method_call(methodName, paramList)
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)

###################################################################################
        elif (command == "new"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value


            if (firstExpr in Environment.classDict):
                curVal = Environment.classDict[firstExpr](firstExpr, classDef.interpreter)
            else:
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

###################################################################################
        elif (command == "set"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[1].process_expression(vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)

            if (firstExpr in vars):
                vars[firstExpr] = getObj(secondExpr)
                #print(vars[firstExpr].printVal)
            elif(firstExpr in classDef.fields):
                classDef.fields[firstExpr] = getObj(secondExpr)
                #print( classDef.fields[firstExpr].printVal)
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)
 
            return
###################################################################################
        elif (command == "inputi"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value

            if (firstExpr in vars):
                vars[firstExpr] = getObj(classDef.interpreter.get_input())
            else:
                classDef.fields[firstExpr] = getObj(classDef.interpreter.get_input())
            return
###################################################################################
        elif (command == "if"):
            #globalC -= 1
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            retVal = None
            if (not isinstance(firstExpr, bool)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)
                
            if (firstExpr):
                if (2 < len(curExpr) and not isinstance(curExpr[2], Value)):
                    retVal = curExpr[2].process_expression(vars, classDef)
                elif (2 < len(curExpr)):
                    retVal = getVal(curExpr[2], vars, classDef)

            else:
                if (3 < len(curExpr) and not isinstance(curExpr[3], Value)):
                    retVal = curExpr[3].process_expression(vars, classDef)
                elif (3 < len(curExpr)):
                    retVal = getVal(curExpr[3], vars, classDef)

            return retVal


###################################################################################
        elif (command == "while"):
            boolExp = curExpr[1].process_expression(vars, classDef)
            if (not isinstance(boolExp, bool)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)
            while (curExpr[1] and curExpr[1].process_expression(vars, classDef)):         
                if (not isinstance(curExpr[2], Value)):
                    secondExpr = curExpr[1].process_expression(vars, classDef)
                else:
                    secondExpr = getVal(curExpr[1], vars, classDef)


        #TODO: IMPLEMENT FIELDS AND VARS! IMPELMENT FUNCTIONS:  
        
        return curVal

        

class StatementBlock():
    def __init__(self, val):
        self.expression = val[1]
        self.expr = [Statement.create_statement(val[x]) for x in range(1,len(val))]
    
    def process_expression(self, vars, classDef):
       # print("Processing Begin Block!")
        for expr in self.expr:
            #print(expr.expression)
            if (expr.expression[0] == "return"):
                return expr.process_expression(vars, classDef)
            else:
                expr.process_expression(vars, classDef)



#classDict = {}

class Class():
    def __init__(self, class_name, interpreter):
        self.name = class_name
        self.interpreter = interpreter
        self.fields = {x : (getObj(val)) for x, val in Environment.classDict[class_name]["Fields"].items()} #Environment.classDict[class_name]["Fields"]
       # print(self.fields)
        self.methods = {x : Method(val, self) for x, val in Environment.classDict[class_name]["Methods"].items()}
       # print("Class!")

    def process_class(class_info):
        class_name = class_info[1]
        Environment.classDict[class_name] = {
            "Name" : class_name,
            "Methods" : {},
            "Fields" : {}
        }
        for entry in class_info:
            if (entry[0] == 'method'):
                Environment.classDict[class_name]["Methods"][entry[1]] = {
                    "Name" : entry[1],
                    "Parameters" : entry[2],
                    "Expression" : entry[3]
                }
            elif (entry[0] == 'field'):
                Environment.classDict[class_name]["Fields"][entry[1]] = entry[2]

    def method_call(self, method_name, params):
        if (not method_name in self.methods):
            self.interpreter.error(ErrorType.NAME_ERROR)
        return self.methods[method_name].process_method(self.fields, params) 
    
    #def print(self, val):
     #   print(val)


class Method():
    def __init__(self, method_info, classDef):
        self.name = method_info["Name"]
        self.params = method_info["Parameters"]
        self.expression = Statement.create_statement(method_info["Expression"]) 
        self.classDef = classDef
        #print("Method!")
    
    def process_method(self, class_fields, params):
        if (self.params):
            if (len(self.params) != len(params)):
                self.interpreter.error(ErrorType.TYPE_ERROR)
            vars = {x: getObj(val) for x,val in zip(self.params, params)}
            for i in self.params:
                if (i not in vars):
                    vars[i] = "null" 
        else:
            vars = {}
       # print("Processing Method!")
        return self.expression.process_expression(vars, self.classDef)
        

#class Variable():
 #   def __init__(self):
 #       print("Variable!")

class Value():
    def __init__(self, val):
        self.value = val 
        self.printVal = str(val)
        if (val == "true" or (isinstance(val, bool) and val)):
            self.value = True
            self.printVal = "true"
            self.type = "Boolean"
        elif (val == "false" or (isinstance(val, bool) and val)):
            self.value = False
            self.printVal = "false"
            self.type = "Boolean"
        elif (val[0] == '"'):
            self.type = "String"
            self.printVal = val[1:-1]
        elif (val == "null"):
            self.value = None
            self.printVal = "null"
            self.type = "None"
        else:
            try:
                self.value = int(val)
                self.type = "Number"
            except:
                self.value = val 
                self.type = 'Variable'

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase’s constructor

    def run(self, program):
        result, parsed_program = BParser.parse(program)
        if result == False:
            #print('Parsing failed. There must have been a mismatched parenthesis.')
            return 1
    
        for class_def in parsed_program:
            Class.process_class(class_def)

        main_object = Class("main", super())
        #print(Environment.classDict)
        main_object.method_call("main", [])
        return 0

class Environment():
    classDict = {}

# def main():
#   # all programs will be provided to your interpreter as a list of 
#   # python strings, just as shown here.
#     program_source = ['(class main',
#                     ' (method main ()',
#                     '   (print  (- 1 2))',
#                     ' ) # end of method',
#                     ') # end of class',
#                     '(class coolio',
#                     ' (field num 2)',
#                     ' (method main2 (n)',
#                     '   (call me main2 "hello world!")',
#                     ' ) # end of method',
#                     ') # end of class']
 
#     # this is how you use our BParser class to parse a valid 
#     # Brewin program into python list format.
#     result, parsed_program = BParser.parse(program_source)
#     print(parsed_program)
#     if result == False:
#         print('Parsing failed. There must have been a mismatched parenthesis.')
#         return 1
    
#     interpreterObj = Interpreter()
#     interpreterObj.run(program_source)

#if __name__ == "__main__":
#  main()
