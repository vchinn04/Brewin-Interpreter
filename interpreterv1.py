#!/usr/bin/python3

from bparser import BParser
from intbase import InterpreterBase, ErrorType
#globalC = 10
def getObj(val):
    if (isinstance(val, Class) and val != None):
        return val
    if (isinstance(val, list)):
        if (val[0] == "begin"):
            return StatementBlock(val)
        else:
            return Statement(val)
    else:
        if (isinstance(val, bool) or val == None):
            return Value(val)
        else:
            return Value(str(val)) 

def getVal(val, vars, classDef, printV=False):
    if (isinstance(val, Class) and val is not None):
        return val
    if (not isinstance(val, Value)):
        return getVal(getObj(val),vars, classDef, printV)
    else:
        if (val.type == "Variable"):
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
        else:
            if (printV):
                return val.printVal
            return val.value

class Statement():
    def __init__(self, val):
        expression_list = []
        expression_list.append(val[0])
        for i in range(1, len(val)):
            #print(val[i])
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

    def process_expression(self, vars, classDef, bSett={}):
        #global globalC
        #print("Processing Expression!")
        curExpr = self.expression
        command = curExpr[0]
        curVal = None
###################################################################################
        if (command == "print"):
            printStr = ""
            for x in curExpr[1:]:
                if (not isinstance(x, Value)):
                    curVal = getVal(getObj(x.process_expression(vars, classDef)), vars, classDef, printV=True)
                else:
                    curVal = getVal(x, vars, classDef, printV=True)
                printStr += str(curVal)

            classDef.interpreter.output(printStr)

            #valList = [str(getVal(x, vars, classDef, printV=True)) for x in curExpr[1:]]
            #classDef.interpreter.output(valList)

###################################################################################
        elif (command == "return"):
            #print(bSett)
            if ("ret" in bSett):
                #print("RETURNING!")
                bSett["ret"] = True

            if (len(curExpr) >= 2):
                if (isinstance(curExpr[1], Class)):
                    return curExpr[1]
                elif (not isinstance(curExpr[1], Value)):
                    return curExpr[1].process_expression(vars, classDef)
                else:
                    return getVal(curExpr[1], vars, classDef)
            else:
                return

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

            if ((isinstance(firstExpr, str)) and isinstance(secondExpr, str)):
                return ('"' + firstExpr[1:-1] + secondExpr[1:-1] + '"')

            elif ((type(firstExpr) == type(0)) and (type(secondExpr) == type(0))):
                return (firstExpr + secondExpr)
            else:
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

###################################################################################
        elif(command == "-" or command == "*" or command == "/" or command == "%"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = getVal(curExpr[1].process_expression(vars, classDef), vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (not isinstance(curExpr[2], Value)):
                secondExpr = getVal(curExpr[2].process_expression(vars, classDef), vars, classDef)
            else:
                secondExpr = getVal(curExpr[2], vars, classDef)

            if ((type(firstExpr) != type(0)) and (type(secondExpr) != type(0))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)

            if (command == "-"):
                return (firstExpr - secondExpr)
            elif(command == "*"):
                return (firstExpr * secondExpr)
            elif(command == "/"):
                return firstExpr // secondExpr
            else:
                return (firstExpr % secondExpr)

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
            
            if ((not isinstance(firstExpr, str) and (type(firstExpr) != type(0))) or (type(secondExpr) != type(firstExpr))):
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

            if ((not isinstance(firstExpr, str) and (type(firstExpr) != type(0))) or (type(secondExpr) != type(firstExpr))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return firstExpr < secondExpr
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
            if ((not isinstance(firstExpr, str) and (type(firstExpr) != type(0))) or (type(secondExpr) != type(firstExpr))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return firstExpr >= secondExpr
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
            if ((not isinstance(firstExpr, str) and (type(firstExpr) != type(0))) or (type(secondExpr) != type(firstExpr))):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return  firstExpr <= secondExpr

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
           # print(type(firstExpr))
           # print(type(secondExpr))
            if (isinstance(firstExpr, str) and isinstance(secondExpr, str)):
                return firstExpr == secondExpr
            elif (type(firstExpr) == type(True) and type(secondExpr) == type(True)):
                return firstExpr == secondExpr
            elif ((type(firstExpr) == type(0)) and (type(secondExpr) == type(0))):
                return firstExpr == secondExpr
            elif (firstExpr is None and ((secondExpr is None) or isinstance(secondExpr, Class))):
                return firstExpr == secondExpr
            elif (secondExpr is None and ((firstExpr is None) or isinstance(firstExpr, Class))):
                return firstExpr == secondExpr
            else:
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

            #if (((not isinstance(firstExpr, str) and not isinstance(firstExpr, bool) and not isinstance(firstExpr, int)) and not isinstance(firstExpr, Class) or (type(secondExpr) != type(firstExpr))) and (firstExpr is not None and secondExpr is not None)):
             #       classDef.interpreter.error(ErrorType.TYPE_ERROR)
            #if (firstExpr is None  and not (secondExpr is None or isinstance(secondExpr, Class))):
            #        classDef.interpreter.error(ErrorType.TYPE_ERROR)
            #if (secondExpr is None  and not (firstExpr is None or isinstance(firstExpr, Class))):
            #        classDef.interpreter.error(ErrorType.TYPE_ERROR)
            #print(firstExpr == secondExpr)
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

            if (isinstance(firstExpr, str) and isinstance(secondExpr, str)):
                return firstExpr != secondExpr
            elif (type(firstExpr) == type(True) and type(secondExpr) == type(True)):
                return firstExpr != secondExpr
            elif ((type(firstExpr) == type(0)) and (type(secondExpr) == type(0))):
                return firstExpr != secondExpr
            elif (firstExpr is None and ((secondExpr is None) or isinstance(secondExpr, Class))):
                return firstExpr != secondExpr
            elif (secondExpr is None and ((firstExpr is None) or isinstance(firstExpr, Class))):
                return firstExpr != secondExpr
            else:
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
            if (type(firstExpr) != type(True) and type(secondExpr) != type(True)):
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
            if (type(firstExpr) != type(True) and type(secondExpr) != type(True)):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
            return firstExpr or secondExpr
###################################################################################
        elif(command == "!"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            if (type(firstExpr) != type(True)):
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
                if (isinstance(arg, Class)):
                    paramList.append(Class(arg.name, classDef.interpreter))
                elif (isinstance(arg, Method)):
                    v = getVal(getObj(arg.process_method(vars, classDef)), vars, classDef)
                    if (v == None):
                        paramList.append(v)
                    else:
                        paramList.append(str(v))

                elif (not isinstance(arg, Value)):
                    v = getVal(getObj(arg.process_expression(vars, classDef)), vars, classDef)
                    if (v == None):
                        paramList.append(v)
                    else:
                        paramList.append(str(v))
                else:
                    v = getVal(arg, vars, classDef)
                    if (isinstance(v, Class)):
                        paramList.append(Class(getVal(arg, vars, classDef).name, classDef.interpreter))
                    else:
                        v = getVal(arg, vars, classDef)
                        if (v == None):
                            paramList.append(v)
                        else:
                            paramList.append(str(v))
            #print(firstExpr)
            if (isinstance(firstExpr, Class)):
                curVal = firstExpr.method_call(methodName, paramList)
            elif (firstExpr == "me"):
                #print("Called me!")
                curVal = classDef.method_call(methodName, paramList)
            elif (firstExpr in vars):
                if (not isinstance(vars[firstExpr], Class)):
                    classDef.interpreter.error(ErrorType.FAULT_ERROR)
                curVal = vars[firstExpr].method_call(methodName, paramList)
            elif(firstExpr in classDef.fields):
                if (not isinstance(classDef.fields[firstExpr], Class)):
                    classDef.interpreter.error(ErrorType.FAULT_ERROR)
                curVal = classDef.fields[firstExpr].method_call(methodName, paramList)
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)
            return curVal

###################################################################################
        elif (command == "new"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr =  curExpr[1].value


            if (firstExpr in Environment.classDict):
                #print("Returning class!")
                return Class(firstExpr, classDef.interpreter)
            else:
                classDef.interpreter.error(ErrorType.TYPE_ERROR)

###################################################################################
        elif (command == "set"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value

            if (not isinstance(curExpr[2], Value)):
                secondExpr = curExpr[2].process_expression(vars, classDef)
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
            elif(firstExpr in classDef.fields):
                classDef.fields[firstExpr] = getObj(classDef.interpreter.get_input())
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)

###################################################################################
        elif (command == "inputs"):
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = curExpr[1].value

            inputStr = '"'
            inputStr += classDef.interpreter.get_input()
            inputStr += '"'
            if (firstExpr in vars):
                vars[firstExpr] = getObj(inputStr)
            elif (firstExpr in classDef.fields):
                classDef.fields[firstExpr] = getObj(inputStr)
            else:
                classDef.interpreter.error(ErrorType.NAME_ERROR)

            
###################################################################################
        elif (command == "if"):
            #globalC -= 1
            if (not isinstance(curExpr[1], Value)):
                firstExpr = curExpr[1].process_expression(vars, classDef)
            else:
                firstExpr = getVal(curExpr[1], vars, classDef)

            retVal = None
            if (type(firstExpr) != type(True)):
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
            if (not isinstance(curExpr[1], Value)):
                boolExp = curExpr[1].process_expression(vars, classDef)
            else:
                boolExp = getVal(curExpr[1], vars, classDef)

            loopRet = {"ret" : False}
            #print(boolExp)
           # if (not boolExp):
             #   return
            if (type(boolExp) != type(True)):
                classDef.interpreter.error(ErrorType.TYPE_ERROR)
            #print(boolExp)
            while (boolExp):  
                #print("RUNNIN!")
                if (not isinstance(curExpr[2], Value)):
                    curVal = curExpr[2].process_expression(vars, classDef, loopRet)
                else:
                    curVal = getVal(curExpr[2], vars, classDef, loopRet)
                if ((curExpr[2]).expression[0] == "return" or loopRet["ret"]):
                    #print("VAL: ")
                    #print(curVal)
                    if ("ret" in bSett):
                        bSett["ret"] = True
                    return curVal
                if (not isinstance(curExpr[1], Value)):
                    boolExp = curExpr[1].process_expression(vars, classDef)
                else:
                    boolExp = getVal(curExpr[1], vars, classDef)
                #print(type(boolExp))
                #if (not boolExp):
                 #   break
                if (type(boolExp) != type(True)):
                    classDef.interpreter.error(ErrorType.TYPE_ERROR)
       
        return curVal

        

class StatementBlock():
    def __init__(self, val):
        self.expression = val[1]
        self.expr = [Statement.create_statement(val[x]) for x in range(1,len(val))]
    
    def process_expression(self, vars, classDef, bSett={}):
        #print("Processing Begin Block!")
        bSet = {"ret": False}
        for expr in self.expr:
           # print(expr.expression)
            #print(expr.expression[0])
            if (expr.expression[0] == "return"):
                #print(classDef.fields)
                #print("RETURING BEGIN")
                v = expr.process_expression(vars, classDef)
                if(bSett):
                    bSett["ret"] = True
                return v
            else:
                v = expr.process_expression(vars, classDef, bSett=bSet)
                if (bSet["ret"]):
                    if(bSett):
                        bSett["ret"] = True
                    return v


#classDict = {}

class Class():
    def __init__(self, class_name, interpreter):
        self.name = class_name
        self.interpreter = interpreter
        self.fields = {x : (getObj(val)) for x, val in Environment.classDict[class_name]["Fields"].items()} #Environment.classDict[class_name]["Fields"]
        #print(Environment.classDict[class_name]["Fields"])
        #for x, val in Environment.classDict[class_name]["Fields"].items():
         #   if (x in self.fields.keys()):
          #      interpreter.error(ErrorType.NAME_ERROR)
           # self.fields[x] = getObj(val)
            #print(self.fields)
       # print(self.fields)
        self.methods =  {x : Method(val, self) for x, val in Environment.classDict[class_name]["Methods"].items()}
        #for x, val in Environment.classDict[class_name]["Methods"].items():
         #   if (x in self.methods.keys()):
          #      interpreter.error(ErrorType.NAME_ERROR)
           # self.methods[x] = Method(val, self)
       # print("Class!")

    def process_class(class_info, interpreter):
        class_name = class_info[1]
        if (class_name in Environment.classDict.keys()):
            interpreter.error(ErrorType.TYPE_ERROR)

        Environment.classDict[class_name] = {
            "Name" : class_name,
            "Methods" : {},
            "Fields" : {}
        }
        for entry in class_info:
            if (entry[0] == 'method'):
                if (entry[1] in Environment.classDict[class_name]["Methods"].keys()):
                    interpreter.error(ErrorType.NAME_ERROR)
                Environment.classDict[class_name]["Methods"][entry[1]] = {
                    "Name" : entry[1],
                    "Parameters" : entry[2],
                    "Expression" : entry[3]
                }
            elif (entry[0] == 'field'):
                if (entry[1] in Environment.classDict[class_name]["Fields"].keys()):
                    interpreter.error(ErrorType.NAME_ERROR)
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
        checkParams = []
        for i in method_info["Parameters"]:
            if (i in checkParams):
                classDef.interpreter.error(ErrorType.NAME_ERROR)
            else:
                checkParams.append(i)

        self.expression = Statement.create_statement(method_info["Expression"]) 
        self.classDef = classDef
        #print("Method!")
    
    def process_method(self, class_fields, params):
        if (self.params):
            if (len(self.params) != len(params)):
                self.classDef.interpreter.error(ErrorType.TYPE_ERROR)
            vars = {x: getObj(val) for x,val in zip(self.params, params)}
            for i in self.params:
                if (i not in vars):
                    vars[i] = "null" 
        else:
            vars = {}
       # print("Processing Method!")
        #v = self.expression.process_expression(vars, self.classDef)
        #print(self.expression.expression)
        #print(v)
       # print('----')
        return self.expression.process_expression(vars, self.classDef)
        

#class Variable():
 #   def __init__(self):
 #       print("Variable!")


class Value():
    def __init__(self, val):
        self.value = val 
        self.printVal = str(val)
        if (isinstance(val, Class)):
            self.type = "Class"
            self.value = Class(val.name, val.interpreter) 
            self.printVal = "class"
        elif (val == "true" or (isinstance(val, bool) and val)):
            self.value = True
            self.printVal = "true"
            self.type = "Boolean"
        elif (val == "false" or (isinstance(val, bool) and not val)):
            #print("Tis false!")
            self.value = False
            self.printVal = "false"
            self.type = "Boolean"
        elif (val == "null" or val == None):
            self.value = None
            self.printVal = "null"
            self.type = "None"
        elif (val[0] == '"'):
            self.type = "String"
            self.printVal = val[1:-1]

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
        Environment.classDict = {}
        for class_def in parsed_program:
            Class.process_class(class_def, super())

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
#                     '   (print  (== false 0))',
#                     ' ) # end of method',
#                     ') # end of class',
#                     '(class coolio',
#                     ' (field num 2)',
#                     ' (method main2 (n)',
#                     '   (call me main2 "hello world!")',
#                     ' ) # end of method',
#                     ') # end of class']

#     p2 = [
#         '(class main',
#       '(field x null)',
#         '(method main ()', 
#           '(begin',
#                 ' (set x (new mycool))',

#                ' (call x getObj)',
#            ')',
#   ')',
# ')',
#       '(class mycool',
#       '(field y 10)',
#         '(method myMethod ()', 
#           '(begin',
#                         ' (set y (new mycool))',

#                '(return "unga")',
#            ')',
#   ')',
#   '(method getObj ()', 
#           '(begin',
#                 '(while false',
#                 '(begin',
#                     '(print "yipee")',
#                         ' (set y (- y 1))',
#                         '(while false',
#                     '(begin',
#                     '(print "YIPOO")',
#                         ' (set y (+ y 1))',
#                         ')',
#                         ')',
#                ')',
#                ')',
#                '(print "yipaa")',
#            ')',
#   ')',
# ')',

#       '(class thirdc',
#       '(field y 10)',
#       '(field y 21)',

#         '(method myMethod (y)', 
#           '(begin',
#                '(return (> y 0))',
#            ')',
#   ')',
# ')']
 
#     # this is how you use our BParser class to parse a valid 
#     # Brewin program into python list format.
#     result, parsed_program = BParser.parse(p2)
#     print(parsed_program)
#     if result == False:
#         print('Parsing failed. There must have been a mismatched parenthesis.')
#         return 1
    
#     interpreterObj = Interpreter()
#     interpreterObj.run(program_source)

# if __name__ == "__main__":
#  main()


# CAN ONLY COMPARE null to OBJECTS