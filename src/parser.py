from typing import List, Optional
from src.lexer import Token, TokenType
from src.ast_nodes import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
    
    def expect(self, token_type: TokenType, value: str = None) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type} at line {token.line}")
        if value and token.value != value:
            raise SyntaxError(f"Expected '{value}', got '{token.value}' at line {token.line}")
        self.advance()
        return token
    
    def parse(self) -> Program:
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Program(statements)
    
    def parse_statement(self) -> ASTNode:
        token = self.current_token()
        
        if token.type == TokenType.KEYWORD:
            if token.value in ['int', 'float', 'string', 'bool', 'void']:
                return self.parse_var_declaration()
            elif token.value == 'if':
                return self.parse_if_statement()
            elif token.value == 'while':
                return self.parse_while_loop()
            elif token.value == 'for':
                return self.parse_for_loop()
            elif token.value == 'return':
                return self.parse_return_statement()
            elif token.value == 'print':
                return self.parse_print_statement()
        
        if token.type == TokenType.IDENTIFIER:
            if self.peek_token().type == TokenType.ASSIGN:
                return self.parse_assignment()
            elif self.peek_token().type == TokenType.LPAREN:
                stmt = self.parse_function_call()
                self.expect(TokenType.SEMICOLON)
                return stmt
        
        raise SyntaxError(f"Unexpected token {token.value} at line {token.line}")
    
    def parse_var_declaration(self) -> VarDeclaration:
        var_type = self.current_token().value
        self.advance()
        
        name = self.expect(TokenType.IDENTIFIER).value
        
        value = None
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_expression()
        
        self.expect(TokenType.SEMICOLON)
        return VarDeclaration(var_type, name, value)
    
    def parse_assignment(self) -> Assignment:
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return Assignment(name, value)
    
    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.KEYWORD, 'if')
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        then_block = self.parse_block()
        
        else_block = None
        if self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'else':
            self.advance()
            else_block = self.parse_block()
        
        return IfStatement(condition, then_block, else_block)
    
    def parse_while_loop(self) -> WhileLoop:
        self.expect(TokenType.KEYWORD, 'while')
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return WhileLoop(condition, body)
    
    def parse_for_loop(self) -> ForLoop:
        self.expect(TokenType.KEYWORD, 'for')
        self.expect(TokenType.LPAREN)
        
        init = None
        if self.current_token().type != TokenType.SEMICOLON:
            if self.current_token().value in ['int', 'float', 'string', 'bool']:
                init = self.parse_var_declaration()
                self.pos -= 1
            else:
                init = self.parse_assignment()
                self.pos -= 1
        self.expect(TokenType.SEMICOLON)
        
        condition = None
        if self.current_token().type != TokenType.SEMICOLON:
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        update = None
        if self.current_token().type != TokenType.RPAREN:
            name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.ASSIGN)
            value = self.parse_expression()
            update = Assignment(name, value)
        
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return ForLoop(init, condition, update, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.expect(TokenType.KEYWORD, 'return')
        value = None
        if self.current_token().type != TokenType.SEMICOLON:
            value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(value)
    
    def parse_print_statement(self) -> PrintStatement:
        self.expect(TokenType.KEYWORD, 'print')
        self.expect(TokenType.LPAREN)
        expr = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return PrintStatement(expr)
    
    def parse_block(self) -> List[ASTNode]:
        self.expect(TokenType.LBRACE)
        statements = []
        while self.current_token().type != TokenType.RBRACE:
            statements.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        return statements
    
    def parse_function_call(self) -> FunctionCall:
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        
        arguments = []
        if self.current_token().type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                arguments.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        return FunctionCall(name, arguments)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value == '||':
            op = self.current_token().value
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_logical_and(self) -> ASTNode:
        left = self.parse_equality()
        
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value == '&&':
            op = self.current_token().value
            self.advance()
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        left = self.parse_comparison()
        
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['==', '!=']:
            op = self.current_token().value
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_term()
        
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['<', '>', '<=', '>=']:
            op = self.current_token().value
            self.advance()
            right = self.parse_term()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_term(self) -> ASTNode:
        left = self.parse_factor()
        
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['+', '-']:
            op = self.current_token().value
            self.advance()
            right = self.parse_factor()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_factor(self) -> ASTNode:
        left = self.parse_unary()
        
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['*', '/', '%']:
            op = self.current_token().value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.current_token().type == TokenType.OPERATOR and self.current_token().value in ['-', '!']:
            op = self.current_token().value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value)
        
        if token.type == TokenType.STRING:
            self.advance()
            return String(token.value)
        
        if token.type == TokenType.IDENTIFIER:
            if self.peek_token().type == TokenType.LPAREN:
                return self.parse_function_call()
            self.advance()
            return Identifier(token.value)
        
        if token.type == TokenType.KEYWORD and token.value in ['true', 'false']:
            self.advance()
            return Identifier(token.value)
        
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        raise SyntaxError(f"Unexpected token {token.value} at line {token.line}")
