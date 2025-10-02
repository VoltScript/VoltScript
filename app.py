from flask import Flask, render_template, request, jsonify
from src.lexer import Lexer
from src.parser import Parser
from src.codegen import CodeGenerator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        data = request.get_json()
        source_code = data.get('code', '')
        
        if not source_code.strip():
            return jsonify({
                'success': False,
                'error': 'No code provided'
            })
        
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        codegen = CodeGenerator()
        cpp_code = codegen.generate(ast)
        
        return jsonify({
            'success': True,
            'cpp_code': cpp_code
        })
        
    except SyntaxError as e:
        return jsonify({
            'success': False,
            'error': f'Syntax Error: {str(e)}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
