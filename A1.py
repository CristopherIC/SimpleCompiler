# Generar codigo basado en la pagina 40 del libro 
from lib2to3.pgen2 import token
from Tokens import Tokens

global content_index
global content
content_index = 0

def peek():
    global content_index
    global content  
    return content[content_index]

def advance():
    global content_index
    val = peek()
    content_index = content_index + 1
    return val

def eof():
    global content_index
    global content  
    return content_index >= len(content)

def scan_digits():
    ans = {
        'val': ''
    }
    while peek() in '0123456789':
        ans['val'] = ans['val'] + advance()
    if peek() != '.':
        ans['type'] = 'inum'
    else:
        ans['type'] = 'fnum'
        ans['val'] = ans['val'] + advance()
        while peek() in '0123456789':
            ans['val'] = ans['val'] + advance()
    return ans

def scanner():
    global content_index
    global content
    ans = {}
    while not eof() and (peek() == ' ' or peek() == '\n'):
        advance()
    if eof():
        ans["type"] = '$'
    else:
        if peek() in '0123456789':
            ans = scan_digits()
        else:
            ch = advance()
            if ch in 'abcdeghjklmnoqrstuvwxyz':
                ans['type'] = 'id'
                ans['val'] = ch
            elif ch == 'f':
                ans['type'] = 'floatdcl'
            elif ch == 'i':
                ans['type'] = 'intdcl'
            elif ch == 'p':
                ans['type'] = 'print'
            elif ch == '=':
                ans['type'] = 'assign'
            elif ch == '+':
                ans['type'] = 'plus'
            elif ch == '-':
                ans['type'] = 'minus'
            else:
                print('Error Lexico')
                exit()
    return ans
# ~~ NODE ~~

class Node:
    val = None
    type = None
    childs = None

    def __init__(self, type = None, val = None):
        self.type = type
        self.val = val
        self.childs = []

    def setVal(self, val):
        self.val = val

    def setType(self, type):
        self.type = type

    def addChilds(self, nodes):
        for node in nodes:
            self.childs.append(node)

    def __str__(self, level = 0):
        ret = "\t" * level + (self.type + ':' + str(self.val))+"\n"
        for child in self.childs:
            ret += child.__str__(level+1)
        return ret

# ~~ PARSER ~~

def prog(tokens):   
    root = Node("prog")
    root.addChilds(dcls(tokens))
    root.addChilds(stmts(tokens))
    return root

def dcls(tokens):
    if tokens.peek()['type'] == 'intdcl' or tokens.peek()['type'] == 'floatdcl':
        nodes = dcl(tokens)
        return nodes + dcls(tokens)
    return[]

def dcl(tokens):
    if tokens.peek()['type'] == 'intdcl' or tokens.peek()['type'] == 'floatdcl':
        node = Node(tokens.advance()['type'])
        if tokens.peek()['type'] == 'id':
            node.setVal(tokens.advance()['val'])
            return[node]
        else:
            print('Error Sintactico')
            exit()
    return[]

def stmt(tokens):
    if tokens.peek()['type'] == 'id':
        childNode1 = Node(tokens.peek()['type'])
        childNode1.setVal(tokens.advance()['val'])

        if tokens.peek()['type'] == 'assign':
            node = Node(tokens.advance()['type'])

            if tokens.peek()['type'] == 'fnum' or tokens.peek()['type'] == 'inum' or tokens.peek()['type'] == 'id':
                node.setVal(tokens.peek()['type'])
                childNode2 = Node(tokens.peek()['type'])
                childNode2.setVal(tokens.advance()['val'])
                node.addChilds([childNode1])

                if tokens.peek()['type'] == 'plus' or tokens.peek()['type'] == 'minus':           
                    subNodes = expr(tokens, childNode2) 
                    node.addChilds(subNodes)
                    return [node]
                else:
                    node.addChilds([childNode2])
                    return[node]

    elif tokens.peek()['type'] == 'print':
        node = Node(tokens.advance()['type'])
        node.setVal(tokens.advance()['val'])
        return[node]

    else:
        print('Error Sintactico')
        exit()

    return[]

def stmts(tokens):
    if tokens.peek()['type'] == 'id' or tokens.peek()['type'] == 'print':
        nodes = stmt(tokens)
        return nodes + stmts(tokens)
    return[]

def expr(tokens, childNode):
    if tokens.peek()['type'] == 'plus' or tokens.peek()['type'] == 'minus':
        node = Node(tokens.advance()['type'])
        if tokens.peek()['type'] == 'fnum' or tokens.peek()['type'] == 'inum' or tokens.peek()['type'] == 'id':
            node.setVal(tokens.peek()['type'])
            childNode1 = Node(tokens.peek()['type'])
            childNode1.setVal(tokens.advance()['val'])
            
            if tokens.peek()['type'] == 'plus' or tokens.peek()['type'] == 'minus':
                subNodes = expr(tokens, childNode1)
                node.addChilds(subNodes)
                return [node]
            else:
                node.addChilds([childNode])
                node.addChilds([childNode1])
                return [node]
        else:
            print('Error Sintactico')
            exit()       
    else:
        return []
    
with open('input.txt') as f: 
    content = f.read()
tokens = Tokens()
while not eof():
    tokens.append(scanner())
tokens.append(scanner())

print(prog(tokens))
