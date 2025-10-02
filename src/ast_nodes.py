from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class VarDeclaration(ASTNode):
    var_type: str
    name: str
    value: Optional[ASTNode] = None

@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class Number(ASTNode):
    value: str

@dataclass
class String(ASTNode):
    value: str

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_block: List[ASTNode]
    else_block: Optional[List[ASTNode]] = None

@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class ForLoop(ASTNode):
    init: Optional[ASTNode]
    condition: Optional[ASTNode]
    update: Optional[ASTNode]
    body: List[ASTNode]

@dataclass
class FunctionCall(ASTNode):
    name: str
    arguments: List[ASTNode]

@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class PrintStatement(ASTNode):
    expression: ASTNode
