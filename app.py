from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import holidays

app = Flask(__name__)

# Crear un objeto con los días festivos en Chile
chile_holidays = holidays.Chile()

def calcular_dias_inhabiles(fecha_inicio, dias_vacaciones):
    fecha_actual = fecha_inicio
    dias_inhabiles = 0
    fechas_inhabiles = []

    while dias_vacaciones > 0:
        fecha_actual += timedelta(days=1)
        if fecha_actual.weekday() in [5, 6] or fecha_actual in chile_holidays:
            dias_inhabiles += 1
            fechas_inhabiles.append(fecha_actual.strftime('%Y-%m-%d'))
        else:
            dias_vacaciones -= 1

    return dias_inhabiles, fechas_inhabiles, fecha_actual

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular_inhabiles', methods=['POST'])
def calcular_inhabiles():
    try:
        data = request.json

        dias_vacaciones = int(data['dias_vacaciones'])
        fecha_termino_str = data['fecha_termino']
        fecha_termino = datetime.strptime(fecha_termino_str, '%Y-%m-%d')

        dias_inhabiles, fechas_inhabiles, nueva_fecha_termino = calcular_dias_inhabiles(fecha_termino, dias_vacaciones)

        return jsonify({
            'dias_inhabiles': dias_inhabiles,
            'fechas_inhabiles': fechas_inhabiles,
            'nueva_fecha_termino': nueva_fecha_termino.strftime('%Y-%m-%d')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
