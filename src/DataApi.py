from email import header
import pandas as pd
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hola mundo!"

@app.route("/recomendaciones")
def getRecomendaciones():
        medicos = pd.read_csv('../DataSets/DatasetMedicos.csv')
        rating = pd.read_csv('../DataSets/MedicosRating.csv')

        print('Medicos: \n', medicos.head())

        medicos['Especialidad'] = medicos.Especialidad.str.split(',')

        medicos_copy = medicos.copy()
        for index, row in medicos.iterrows():
            for esp in row['Especialidad']:
                medicos_copy.at[index, esp] = 1
        
        medicos_copy = medicos_copy.fillna(0)
        print('Medicos codificados: \n', medicos_copy)

        print('Rating de medicos: \n', rating.head())

        usuario_perfil = [
            {'Tipo':'Especialista', 'Puntuacion':1},
            {'Tipo':'Medico', 'Puntuacion':3},
            {'Tipo':'Hospital', 'Puntuacion': 6}
        ]

        entrada_med = pd.DataFrame(usuario_perfil)
        print('Medicos del usuario: \n', entrada_med)

        id = medicos[medicos['Tipo'].isin(entrada_med['Tipo'].tolist())]
        entrada_med = pd.merge(id, entrada_med)

        medico_usuario = medicos_copy[medicos_copy['Id'].isin(entrada_med['Id'].tolist())]
        print('Medicos codificados: \n', medico_usuario)

        medico_usuario = medico_usuario.reset_index(drop=True)
        tabla_especialidades = medico_usuario.drop('Id', axis=1).drop('Tipo', axis=1).drop('Edad', axis=1).drop('Sexo', axis=1).drop('Especialidad', axis=1).drop('Pacientes', axis=1).drop('Casos', axis=1)
        print('Tabla de especialidades: \n', tabla_especialidades)

        perfil_usu = tabla_especialidades.transpose().dot(entrada_med['Puntuacion'])
        print('Medicos que el usuario prefiere: \n', perfil_usu)

        especialidades = medicos_copy.set_index(medicos_copy['Id'])
        especialidades = especialidades.drop('Id', axis=1).drop('Tipo', axis=1).drop('Edad', axis=1).drop('Sexo', axis=1).drop('Especialidad', axis=1).drop('Pacientes', axis=1).drop('Casos', axis=1)
        print('Especialidades: \n', especialidades.head())
        especialidades.shape

        recomendaciones = ((especialidades*perfil_usu).sum(axis=1))/(perfil_usu.sum())
        print('Recomendaciones: \n', recomendaciones.head())

        recomendaciones = recomendaciones.sort_values(ascending=False)
        print('Recomendaciones organizadas: \n', recomendaciones.head())

        final = medicos.loc[medicos['Id'].isin(recomendaciones.head(5).keys())]
        nfinal = final[['Tipo'] + ['Especialidad']]
        print('Medicos recomendados: \n', final)

        data = json.loads(final.to_json(orient='records'))

        resData = {
            "Recomendaciones" : data
        }

        return jsonify(resData)

if __name__ == "__main__":
    app.run(debug=True, host='172.16.15.77')
