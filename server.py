from flask import Flask, request, jsonify, render_template
import sympy as sp

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Lista para almacenar problemas anteriores
previous_problems = []

@app.route('/')
def index():
    # Renderiza la página principal
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    # Obtiene los datos de la solicitud JSON
    data = request.json
    func_str = data['function']
    x0 = data['initial']
    max_iter = data['iterations']
    
    # Define el símbolo y la función simbólica
    x = sp.symbols('x')
    func = sp.sympify(func_str)
    deriv_func = sp.diff(func, x)
    
    # Define las funciones lambda para evaluar la función y su derivada
    f = lambda x_val: float(func.evalf(subs={x: x_val}))
    df = lambda x_val: float(deriv_func.evalf(subs={x: x_val}))

    try:
        # Llama al método de Newton-Raphson y almacena el resultado
        iterations, error = newton_raphson(f, df, x0, max_iter)
        
        # Almacena el problema resuelto
        previous_problems.append({
            'function': func_str,
            'initial': x0,
            'iterations': max_iter
        })
        
        # Devuelve las iteraciones como JSON
        return jsonify({'iterations': iterations})
    except Exception as e:
        # Devuelve el error como JSON
        return jsonify({'error': str(e)})

@app.route('/previous')
def previous():
    # Renderiza la página de problemas anteriores
    return render_template('previous.html')

@app.route('/previous_problems', methods=['GET'])
def get_previous_problems():
    # Devuelve la lista de problemas anteriores como JSON
    return jsonify(previous_problems)

@app.route('/solution/<func>/<initial>/<iterations>', methods=['GET'])
def get_solution(func, initial, iterations):
    # Define el símbolo y la función simbólica
    x = sp.symbols('x')
    func_expr = sp.sympify(func)
    
    # Define las funciones lambda para evaluar la función y su derivada
    f = lambda x_val: float(func_expr.evalf(subs={x: x_val}))
    df = lambda x_val: float(sp.diff(func_expr, x).evalf(subs={x: x_val}))

    try:
        # Llama al método de Newton-Raphson y almacena el resultado
        iterations, _ = newton_raphson(f, df, float(initial), int(iterations))
        
        # Devuelve las iteraciones como JSON
        return jsonify({'iterations': iterations})
    except Exception as e:
        # Devuelve el error como JSON
        return jsonify({'error': str(e)})

def newton_raphson(f, df, x0, max_iter=100):
    # Método de Newton-Raphson para encontrar raíces
    x = x0
    iterations = []
    for _ in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise ValueError("La derivada es cero en x = {}".format(x))
        x_new = x - fx / dfx
        iterations.append(x_new)
        if abs(x_new - x) < 1e-6:
            break
        x = x_new
    return iterations, abs(f(x))

if __name__ == '__main__':
    # Ejecuta la aplicación en modo debug
    app.run(debug=True)
