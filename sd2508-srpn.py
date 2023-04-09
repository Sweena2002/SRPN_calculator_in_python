
from queue import LifoQueue
import operator, re, random

# stack is the LIFO Queue which will hold the numbers to be operated upon, comming from the imput.
stack = LifoQueue()
# postfix is a list used to convert and Infix expression to a postfix expression.
postfix = []
# conversion_stack is a list used to hold the operators during the conversion of infix to postfix.
conversion_stack = []
MAX_INT = 2147483647
MIN_INT = -2147483648

# math_operator is a dictionary for identifying the operation to perform based on the operator found.
math_operators = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '%' : operator.mod,
    '^' : operator.pow,
}

# get_operator_priority function takes and operator as an input and return its priority as per BODMAS.
def get_operator_priority(operator_value):
    if operator_value == '^':
        return 3
    elif operator_value == '%' or operator_value == '/' or operator_value == '*':
        return 2
    elif operator_value == '+' or operator_value == '-':
        return 1
    return 0

# convert_to_postfix function takes infix expression and convert it into postfix expression.
# The created postfix expression is available in golbal list named postfix.
def convert_to_postfix(list_of_commands):
    lastItem = ''
    for item in list_of_commands:
        if lastItem == item == '-':
            item = '+'
            conversion_stack.pop(len(conversion_stack)-1)
        if item.lstrip('-+').isdigit() or item =='d' or item == '=':
            postfix.append(item)
        elif item == 'r':
            postfix.append(item)
        elif item in math_operators.keys():
            if len(conversion_stack) == 0 or get_operator_priority(item) > get_operator_priority(conversion_stack[len(conversion_stack)-1]):
                conversion_stack.append(item)
            elif get_operator_priority(item) <= get_operator_priority(conversion_stack[len(conversion_stack)-1]):
                pop_untill_lower_found(item)
        else:
            print("Unrecognised operator or operand \"{}\".".format(item))
          
        lastItem = item
    
    if len(conversion_stack) >0:
      for inside_operator in reversed(conversion_stack):
        postfix.append(inside_operator)

# pop_untill_lower_found function takes an operator as input and
# will pop the operators from conversion_stack and
# put them in postfix list until the latest element in conversion_stack
# has a lower priority that the input operator.             
def pop_untill_lower_found(item):
    count=len(conversion_stack)-1
    for inside_operator in reversed(conversion_stack):
        if get_operator_priority(inside_operator) >= get_operator_priority(item):
            postfix.append(conversion_stack.pop(count))
            count=count-1
        else:
            break
    conversion_stack.append(item)

# set_limit function controls the bounday for an integer
def set_limit(result):
  if result > MAX_INT :
    return MAX_INT
  elif result < MIN_INT:
    return MIN_INT
  else:
    return result

# handle_operator is used to perform the operator action on the stack of operands.
# This function will pop 2 operands from the stack and
# perform the input operation on them.
# The result of the operation is put back into the stack.
def handle_operator(cmd):
    pop1 = int(stack.get())
    if cmd == '/' and pop1 == 0:
        stack.put(pop1)
        print("Divide by 0.")
    elif cmd == '^' and pop1 < 0:
        stack.put(pop1)
        print("Negative power.")
    else:
        pop2 = int(stack.get())
        result = math_operators[cmd](int(pop2), int(pop1))
        stack.put(set_limit(int(result)))
    return 0

# handle_digit function will take a digit as an input and
# put it in the stack if the stack size is less than 22.
def handle_digit(cmd):
    if stack.qsize() > 22:
      print("Stack overflow.")
    else:
      stack.put(set_limit(int(cmd)))

# display_stack function is to print all the content of the stack.  
def display_stack():
    currentStackCopy = list(stack.queue)
    for item in currentStackCopy:
      print(item)
      
# process_each_command takes a single input like an operand or an operator and
# process them as per the SRPN functionality.
# A digit goes into the stack if under the stack limit.
# ^/*%+- are operators and act upon the poped elements from stack.
# = prints the top most element in the stack.
# r will put a random number in stack within the defined int limit.
# d will display the content of the stack
def process_each_command(cmd):
  
  if cmd.lstrip('-+').isdigit():
    handle_digit(cmd)
    
  elif cmd == "=":
    poped = stack.get()
    stack.put(poped)
    print(str(poped))
    
  elif cmd in math_operators.keys() and stack.qsize() < 2:
      print("Stack underflow.")
        
  elif cmd in math_operators.keys():
    handle_operator(cmd)

  elif cmd =='d':
    display_stack()

  elif cmd == 'r':
    stack.put(random.randint(MIN_INT, MAX_INT))
         
  else: # if none of the above conditions are matched we assume the input is not handled by the code.
    for item in cmd:
      print("Unrecognised operator or operand \"{}\".".format(item))

  return 0

     
# process_command function takes an input which can be
# 1. A single command, an operator or operand like '10' or '+', can be more than one separated by space like 1 2 +
# 2. it also handles an infix expression which can be like 10+2+3
# The input command is split based on space and sub commands are found
# Each sub command  is put under a regex (regex used to break a non space separated string)
# if  2 or less operands/operator found by regex, they are passed to process_each_command for processing
# if more than 2 operator/operands found its an infix expression.
# Infix expressions are converted to a postfix expression and 
# each element of the postfix expression is passed over to process_each_command for processing.
def process_command(cmd):
  multi_command = cmd.split()
  for sub_command in multi_command:
    list_of_commands = re.findall("(\d+|.)", sub_command)
    if len(list_of_commands) == 2 and list_of_commands[0] == '-':
      process_each_command(sub_command)
    elif len(list_of_commands) >= 2: 
      convert_to_postfix(list_of_commands)
      for item in postfix:
        process_each_command(item)
      postfix.clear()
      conversion_stack.clear()
    elif '#' in sub_command:
      return 0
    else:
      process_each_command(sub_command)
        
        


#This is the entry point for the program.
#It is suggested that you do not edit the below,
#to ensure your code runs with the marking script
if __name__ == "__main__": 
  while True:
    try:
      cmd = input()
      pc = process_command(cmd)
    except EOFError: 
      exit()