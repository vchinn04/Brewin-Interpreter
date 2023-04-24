from bparser import BParser
from intbase import InterpreterBase, ErrorType



class Statement():
    def __init__(self, val):
        expression_list = []
        expression_list.append(val[0])
        for i in range(1, len(val)):
            print(val[i])
            if (isinstance(val[i], list)):
                if (val[i][0] == "begin"):
                    expression_list.append(StatementBlock(val[i]))
                else:
                    expression_list.append(Statement(val[i]))
            else:
                expression_list.append(Value(val[i]))
                
        self.expression = expression_list
        self.type = None
    def create_statement(expression):
        if (expression[0] != 'begin'):
            return Statement(expression)
        else:
            return StatementBlock(expression)
    def process_expression(self, vars, classDef):
        print("Processing Expression!")
        curExpr = self.expression
        command = curExpr[0]
        if (command == "print"):
            if (not isinstance(curExpr[1], Value)):
                curVal = curExpr[1].process_expression(vars, classDef)
            else:
                curVal = curExpr[1].value
            classDef.print(curVal)
        elif (command == "return"):
            if (not isinstance(curExpr[1], Value)):
                curVal = curExpr[1].process_expression(vars, classDef)
            else:
                curVal = curExpr[1].value
        elif(command == "+"):
            vals = [] 
            for i in range(1, len(curExpr)):
                if (not isinstance(curExpr[i], Value)):
                    vals.append(curExpr[i].process_expression(vars, classDef))
                else:
                   vals.append(curExpr[i].value)
            curVal = 0
            for i in vals:
                curVal += i

        elif(command == "-"):
            vals = [] 
            if (not isinstance(curExpr[1], Value)):
                startExpr = curExpr[1].process_expression(vars, classDef)
            else:
                startExpr = curExpr[1].value

            for i in range(2, len(curExpr)):
                if (not isinstance(curExpr[i], Value)):
                    vals.append(curExpr[i].process_expression(vars, classDef))
                else:
                   vals.append(curExpr[i].value)
            curVal = startExpr
            for i in vals:
                curVal -= i

        elif(command == "*"):
            vals = [] 
            if (not isinstance(curExpr[1], Value)):
                startExpr = curExpr[1].process_expression(vars, classDef)
            else:
                startExpr = curExpr[1].value

            for i in range(2, len(curExpr)):
                if (not isinstance(curExpr[i], Value)):
                    vals.append(curExpr[i].process_expression(vars, classDef))
                else:
                   vals.append(curExpr[i].value)
            curVal = startExpr
            for i in vals:
                curVal *= i

        elif(command == "/"):
            vals = [] 
            if (not isinstance(curExpr[1], Value)):
                startExpr = curExpr[1].process_expression(vars, classDef)
            else:
                startExpr = curExpr[1].value

            for i in range(2, len(curExpr)):
                if (not isinstance(curExpr[i], Value)):
                    vals.append(curExpr[i].process_expression(vars, classDef))
                else:
                   vals.append(curExpr[i].value)

            curVal = startExpr
            for i in vals:
                curVal /= i
        #TODO: IMPLEMENT FIELDS AND VARS! IMPELMENT FUNCTIONS: %, >, <, >=, <=, !=, ==, &, |, !, call, new, set
        
        return curVal

        

class StatementBlock():
    def __init__(self, val):
        self.expression = val[1]
        self.expr = [Statement.create_statement(val[x]) for x in range(1,len(val))]
    
    def process_expression(self, vars, classDef):
        print("Processing Begin Block!")
        for expr in self.expr:
            print(expr.expression)
            if (expr.expression[0] == "return"):
                return expr.process_expression(vars, classDef)
            else:
                expr.process_expression(vars, classDef)



classDict = {}

class Class():
    def __init__(self, class_name):
        self.name = class_name
        self.fields = classDict[class_name]["Fields"]
        self.methods = {x : Method(val, self) for x, val in classDict[class_name]["Methods"].items()}
        print("Class!")

    def process_class(class_info):
        class_name = class_info[1]
        classDict[class_name] = {
            "Name" : class_name,
            "Methods" : {},
            "Fields" : {}
        }
        for entry in class_info:
            if (entry[0] == 'method'):
                classDict[class_name]["Methods"][entry[1]] = {
                    "Name" : entry[1],
                    "Parameters" : entry[2],
                    "Expression" : entry[3]
                }
            elif (entry[0] == 'field'):
                classDict[class_name]["Fields"][entry[1]] = entry[2]

    def method_call(self, method_name, params):
        return self.methods[method_name].process_method(self.fields, params) 
    
    def print(self, val):
        print(val)


class Method():
    def __init__(self, method_info, classDef):
        self.name = method_info["Name"]
        self.params = method_info["Parameters"]
        self.expression = Statement.create_statement(method_info["Expression"]) 
        self.classDef = classDef
        print("Method!")
    
    def process_method(self, class_fields, params):
        if (self.params):
            vars = {x: val for x,val in zip(self.params, params)}
            for i in self.params:
                if (i not in vars):
                    vars[i] = None 
        else:
            vars = {}
        print("Processing Method!")
        return self.expression.process_expression(vars, self.classDef)
        

class Variable():
    def __init__(self):
        print("Variable!")

class Value():
    def __init__(self, val):
        self.value = val 
        if (val[0] == '"'):
            self.type = "String"
        elif (val == "null"):
            self.type = "None"
        elif (val == "true"):
            self.value = True
            self.type = "Boolean"
        elif (val == "false"):
            self.value = False
            self.type = "Boolean"
        else:
            self.value = int(val)
            self.type = "Number"

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase’s constructor

    def run(self, program):
        print(program)

class Environment():
    methodDict = {}
    #classDict = {}


def main():
  # all programs will be provided to your interpreter as a list of 
  # python strings, just as shown here.
    program_source = ['(class main',
                    ' (method main ()',
                    ' (begin ',
                    '   (print (return (- 1 2)))',
                    ' ) ',
                    ' ) # end of method',
                    ') # end of class',
                    '(class coolio',
                    ' (field num 2)',
                    ' (method main2 ()',
                    '   (print "hello world!")',
                    ' ) # end of method',
                    ') # end of class']
 
    # this is how you use our BParser class to parse a valid 
    # Brewin program into python list format.
    result, parsed_program = BParser.parse(program_source)
    print(parsed_program)
    if result == False:
        print('Parsing failed. There must have been a mismatched parenthesis.')
        return 1

    for class_def in parsed_program:
        Class.process_class(class_def)

    main_object = Class("main")
    print(classDict)
    main_object.method_call("main", [])
if __name__ == "__main__":
    main()

