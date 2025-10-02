import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    ASSIGN = "ASSIGN"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        self.keywords = {
            'int', 'float', 'string', 'bool', 'void',
            'if', 'else', 'while', 'for', 'return',
            'true', 'false', 'print'
        }
        
        self.operators = {
            '+', '-', '*', '/', '%',
            '==', '!=', '<', '>', '<=', '>=',
            '&&', '||', '!'
        }
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\n\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            self.advance()
    
    def read_number(self) -> Token:
        start_line = self.line
        start_column = self.column
        num_str = ''
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            num_str += self.current_char()
            self.advance()
        
        return Token(TokenType.NUMBER, num_str, start_line, start_column)
    
    def read_string(self) -> Token:
        start_line = self.line
        start_column = self.column
        self.advance()
        
        string_val = ''
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\' and self.peek_char() == '"':
                string_val += '"'
                self.advance()
                self.advance()
            else:
                string_val += self.current_char()
                self.advance()
        
        self.advance()
        return Token(TokenType.STRING, string_val, start_line, start_column)
    
    def read_identifier(self) -> Token:
        start_line = self.line
        start_column = self.column
        ident = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            ident += self.current_char()
            self.advance()
        
        token_type = TokenType.KEYWORD if ident in self.keywords else TokenType.IDENTIFIER
        return Token(token_type, ident, start_line, start_column)
    
    def read_operator(self) -> Token:
        start_line = self.line
        start_column = self.column
        op = self.current_char()
        self.advance()
        
        if self.current_char() and op + self.current_char() in self.operators:
            op += self.current_char()
            self.advance()
        
        return Token(TokenType.OPERATOR, op, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            char = self.current_char()
            
            if char.isdigit():
                self.tokens.append(self.read_number())
            elif char == '"':
                self.tokens.append(self.read_string())
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, char, self.line, self.column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, char, self.line, self.column))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, char, self.line, self.column))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, char, self.line, self.column))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, char, self.line, self.column))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, char, self.line, self.column))
                self.advance()
            elif char == '=' and self.peek_char() != '=':
                self.tokens.append(Token(TokenType.ASSIGN, char, self.line, self.column))
                self.advance()
            elif char in '+-*/%<>!=&|':
                self.tokens.append(self.read_operator())
            else:
                raise SyntaxError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
