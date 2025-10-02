from src.ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.output = []
    
    def indent(self) -> str:
        return "    " * self.indent_level
    
    def generate(self, node: ASTNode) -> str:
        self.output = []
        self.output.append("#include <iostream>")
        self.output.append("#include <string>")
        self.output.append("")
        self.output.append("int main() {")
        self.indent_level += 1
        
        if isinstance(node, Program):
            for statement in node.statements:
                self.generate_statement(statement)
        
        self.output.append(self.indent() + "return 0;")
        self.indent_level -= 1
        self.output.append("}")
        
        return "\n".join(self.output)
    
    def generate_statement(self, node: ASTNode):
        if isinstance(node, VarDeclaration):
            self.generate_var_declaration(node)
        elif isinstance(node, Assignment):
            self.generate_assignment(node)
        elif isinstance(node, IfStatement):
            self.generate_if_statement(node)
        elif isinstance(node, WhileLoop):
            self.generate_while_loop(node)
        elif isinstance(node, ForLoop):
            self.generate_for_loop(node)
        elif isinstance(node, PrintStatement):
            self.generate_print_statement(node)
        elif isinstance(node, FunctionCall):
            self.output.append(self.indent() + self.generate_expression(node) + ";")
        elif isinstance(node, ReturnStatement):
            self.generate_return_statement(node)
    
    def generate_var_declaration(self, node: VarDeclaration):
        cpp_type = self.map_type(node.var_type)
        line = f"{self.indent()}{cpp_type} {node.name}"
        if node.value:
            line += f" = {self.generate_expression(node.value)}"
        line += ";"
        self.output.append(line)
    
    def generate_assignment(self, node: Assignment):
        line = f"{self.indent()}{node.name} = {self.generate_expression(node.value)};"
        self.output.append(line)
    
    def generate_if_statement(self, node: IfStatement):
        condition = self.generate_expression(node.condition)
        self.output.append(f"{self.indent()}if ({condition}) {{")
        self.indent_level += 1
        for stmt in node.then_block:
            self.generate_statement(stmt)
        self.indent_level -= 1
        self.output.append(f"{self.indent()}}}")
        
        if node.else_block:
            self.output.append(f"{self.indent()}else {{")
            self.indent_level += 1
            for stmt in node.else_block:
                self.generate_statement(stmt)
            self.indent_level -= 1
            self.output.append(f"{self.indent()}}}")
    
    def generate_while_loop(self, node: WhileLoop):
        condition = self.generate_expression(node.condition)
        self.output.append(f"{self.indent()}while ({condition}) {{")
        self.indent_level += 1
        for stmt in node.body:
            self.generate_statement(stmt)
        self.indent_level -= 1
        self.output.append(f"{self.indent()}}}")
    
    def generate_for_loop(self, node: ForLoop):
        init_str = ""
        if node.init:
            if isinstance(node.init, VarDeclaration):
                cpp_type = self.map_type(node.init.var_type)
                init_str = f"{cpp_type} {node.init.name}"
                if node.init.value:
                    init_str += f" = {self.generate_expression(node.init.value)}"
            elif isinstance(node.init, Assignment):
                init_str = f"{node.init.name} = {self.generate_expression(node.init.value)}"
        
        condition_str = self.generate_expression(node.condition) if node.condition else ""
        
        update_str = ""
        if node.update:
            if isinstance(node.update, Assignment):
                update_str = f"{node.update.name} = {self.generate_expression(node.update.value)}"
        
        self.output.append(f"{self.indent()}for ({init_str}; {condition_str}; {update_str}) {{")
        self.indent_level += 1
        for stmt in node.body:
            self.generate_statement(stmt)
        self.indent_level -= 1
        self.output.append(f"{self.indent()}}}")
    
    def generate_print_statement(self, node: PrintStatement):
        expr = self.generate_expression(node.expression)
        self.output.append(f'{self.indent()}std::cout << {expr} << std::endl;')
    
    def generate_return_statement(self, node: ReturnStatement):
        if node.value:
            expr = self.generate_expression(node.value)
            self.output.append(f"{self.indent()}return {expr};")
        else:
            self.output.append(f"{self.indent()}return;")
    
    def generate_expression(self, node: ASTNode) -> str:
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return f'"{node.value}"'
        elif isinstance(node, Identifier):
            if node.name == 'true':
                return 'true'
            elif node.name == 'false':
                return 'false'
            return node.name
        elif isinstance(node, BinaryOp):
            left = self.generate_expression(node.left)
            right = self.generate_expression(node.right)
            op = node.operator
            if op == '&&':
                op = '&&'
            elif op == '||':
                op = '||'
            return f"({left} {op} {right})"
        elif isinstance(node, UnaryOp):
            operand = self.generate_expression(node.operand)
            return f"({node.operator}{operand})"
        elif isinstance(node, FunctionCall):
            args = ", ".join(self.generate_expression(arg) for arg in node.arguments)
            return f"{node.name}({args})"
        
        return ""
    
    def map_type(self, volt_type: str) -> str:
        type_map = {
            'int': 'int',
            'float': 'double',
            'string': 'std::string',
            'bool': 'bool',
            'void': 'void'
        }
        return type_map.get(volt_type, volt_type)
