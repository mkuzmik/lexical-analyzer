from nolang.lexer.tokenz import *


class Analyzer:

    def __init__(self, input):
        self.input = input
        self.position = 0
        self.line = 0
        self.column = 0

    def next_token(self):
        if self.position >= len(self.input):
            return Token(TokenType.END_OF_INPUT, '', self.line, self.column)

        char = self.input[self.position]

        if char.isalpha():
            return self.recognize_identifier()

        if char.isdigit():
            return self.recognize_number()

        if is_operator(char):
            return self.recognize_operator()

        if is_parenthesis(char):
            return self.recognize_parenthesis()

        if is_bracket(char):
            return self.recognize_brackets()

        if char == "'":
            return self.recognize_string()

        if (char == '\n'):
            self.position += 1
            self.line += 1
            self.column = 0
            return self.next_token()

        if (char == ' '):
            self.position += 1
            self.column += 1
            return self.next_token()

        return Token(TokenType.UNKNOWN, '', self.line, self.position)

    def recognize_string(self):
        position = self.position + 1
        line = self.line
        column = self.column + 1
        string = ''

        while self.input[position] != "'":
            string += self.input[position]
            position += 1

        self.position += len(string) + 2
        self.column += len(string) + 2

        return Token(TokenType.STRING, string, line, column)

    def recognize_identifier(self):

        position = self.position
        line = self.line
        column = self.column
        identifier = ''

        while position < len(self.input):
            character = self.input[position]
            if not(character.isalpha() | character.isdigit() | (character == '_')):
                break
            identifier += character
            position += 1

        self.position += len(identifier)
        self.column += len(identifier)

        if (identifier == 'function'):
            return Token(TokenType.FUNCTION, identifier, line, column)

        if (identifier == 'var'):
            return Token(TokenType.VARIABLE, identifier, line, column)

        if (identifier == 'while'):
            return Token(TokenType.WHILE, identifier, line, column)

        return Token(TokenType.IDENTIFIER, identifier, line, column)

    def recognize_number(self):

        position = self.position
        line = self.line
        column = self.column
        number = ''
        isFloat = False

        character = self.input[position]

        position +=1
        column +=1

        if character.isdigit():
            if (position < len(self.input)) & (character == '0'):
                if self.input[position] == '.':
                    number += '0.'
                    isFloat = True
                    position += 1
                    column += 1
                else:
                    return Token(TokenType.NUMBER, character, line, column)
            else:
                number += character

        while position < len(self.input):
            character = self.input[position]
            if not character.isdigit():
                if (character == '.') & (isFloat == False):
                    isFloat = True
                else:
                    break
            number += character
            position += 1

        self.position += len(number)
        self.column += len(number)

        return Token(TokenType.NUMBER, number, line, column)

    def recognize_operator(self):
        position = self.position
        line = self.line
        column = self.column
        character = self.input[position]
        nextchar = ''

        if position + 1 < len(self.input):
            nextchar = self.input[position + 1]

        self.position += 1
        self.column += 1

        if character == '+':
            return Token(TokenType.PLUS, character, line, column)

        if character == '-':
            return Token(TokenType.MINUS, character, line, column)

        if character == '*':
            return Token(TokenType.TIMES, character, line, column)

        if character == '/':
            return Token(TokenType.DIV, character, line, column)

        if character == ';':
            return Token(TokenType.END_OF_STATEMENT, character, line, column)

        if character == '=':
            if nextchar == '=':
                return Token(TokenType.EQUAL, character + nextchar, line + 1, column + 1)
            else:
                return Token(TokenType.ASSIGN, character, line, column)

        if character == '>':
            if nextchar == '=':
                return Token(TokenType.GREATER_EQUAL, character + nextchar, line + 1, column + 1)
            else:
                return Token(TokenType.GREATER, character, line, column)

        if character == '<':
            if nextchar == '=':
                return Token(TokenType.LESS_EQUAL, character + nextchar, line + 1, column + 1)
            else:
                return Token(TokenType.LESS, character, line, column)

    def recognize_parenthesis(self):
        line = self.line
        column = self.column
        character = self.input[self.position]

        self.position += 1
        self.column += 1

        return Token(TokenType.PAREN, character, line, column)

    def recognize_brackets(self):
        line = self.line
        column = self.column
        character = self.input[self.position]

        self.position += 1
        self.column += 1

        return Token(TokenType.BRACKET, character, line, column)

    def gather_tokens(self):
        token = self.next_token()
        if token.token_type == TokenType.END_OF_INPUT:
            return [token]
        return [token] + self.gather_tokens()


def is_operator(character):
    return character in "=+-<>*/;"


def is_parenthesis(character):
    return character in "()"


def is_bracket(character):
    return character in "{}"
