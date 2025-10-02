const examples = {
    hello: `int x = 10;
int y = 20;
int sum = x + y;

print(sum);
print("Hello from VoltScript!");`,
    
    loop: `int i = 0;

while(i < 5) {
    print(i);
    i = i + 1;
}

for(int j = 0; j < 3; j = j + 1) {
    print(j);
}`,
    
    conditional: `int age = 18;

if(age >= 18) {
    print("Adult");
} else {
    print("Minor");
}

int score = 85;

if(score >= 90) {
    print("A grade");
} else {
    if(score >= 80) {
        print("B grade");
    } else {
        print("C grade");
    }
}`
};

function loadExample(name) {
    const code = examples[name];
    if (code) {
        document.getElementById('voltscript-code').value = code;
        compileCode();
    }
}

async function compileCode() {
    const code = document.getElementById('voltscript-code').value;
    const outputElement = document.getElementById('cpp-output');
    const errorElement = document.getElementById('error-message');
    const compileBtn = document.getElementById('compile-btn');
    
    errorElement.classList.add('hidden');
    compileBtn.disabled = true;
    compileBtn.textContent = 'Compiling...';
    
    try {
        const response = await fetch('/compile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code })
        });
        
        const result = await response.json();
        
        if (result.success) {
            outputElement.textContent = result.cpp_code;
            errorElement.classList.add('hidden');
        } else {
            errorElement.textContent = result.error;
            errorElement.classList.remove('hidden');
            outputElement.textContent = '// Compilation failed. See error above.';
        }
    } catch (error) {
        errorElement.textContent = 'Error: Failed to connect to compiler';
        errorElement.classList.remove('hidden');
        outputElement.textContent = '// Compilation failed';
    } finally {
        compileBtn.disabled = false;
        compileBtn.textContent = 'Compile →';
    }
}

document.getElementById('voltscript-code').addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = e.target.selectionStart;
        const end = e.target.selectionEnd;
        e.target.value = e.target.value.substring(0, start) + '    ' + e.target.value.substring(end);
        e.target.selectionStart = e.target.selectionEnd = start + 4;
    }
    
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        compileCode();
    }
});

loadExample('hello');
