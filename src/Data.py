import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

class Data():
    def __init__(self) -> None:
        self.medicos = pd.read_csv('../DataSets/DatasetMedicos.csv')
        self.rating = pd.read_csv('../DataSets/MedicosRating.csv')

        print('Medicos: \n', self.medicos.head())

        self.medicos['Especialidad'] = self.medicos.Especialidad.str.split(',')

        self.medicos_copy = self.medicos.copy()
        for index, row in self.medicos.iterrows():
            for esp in row['Especialidad']:
                self.medicos_copy.at[index, esp] = 1
        
        self.medicos_copy = self.medicos_copy.fillna(0)
        print('Medicos codificados: \n', self.medicos_copy)

        print('Rating de medicos: \n', self.rating.head())

        self.usuario_perfil = [
            {'Tipo':'Especialista', 'Puntuacion':10},
            {'Tipo':'Medico', 'Puntuacion':9},
            {'Tipo':'Hospital', 'Puntuacion':6},
            {'Tipo':'Clinica', 'Puntuacion':2},
            {'Tipo':'ONG', 'Puntuacion':0}
        ]

        self.entrada_med = pd.DataFrame(self.usuario_perfil)
        print('Medicos del usuario: \n', self.entrada_med)

        self.id = self.medicos[self.medicos['Tipo'].isin(self.entrada_med['Tipo'].tolist())]
        self.entrada_med = pd.merge(self.id, self.entrada_med)

        self.medico_usuario = self.medicos_copy[self.medicos_copy['Id'].isin(self.entrada_med['Id'].tolist())]
        print('Medicos codificados: \n', self.medico_usuario)

        self.medico_usuario = self.medico_usuario.reset_index(drop=True)
        self.tabla_especialidades = self.medico_usuario.drop('Id', axis=1).drop('Tipo', axis=1).drop('Edad', axis=1).drop('Sexo', axis=1).drop('Especialidad', axis=1).drop('Pacientes', axis=1).drop('Casos', axis=1)
        print('Tabla de especialidades: \n', self.tabla_especialidades)

        self.perfil_usu = self.tabla_especialidades.transpose().dot(self.entrada_med['Puntuacion'])
        print('Medicos que el usuario prefiere: \n', self.perfil_usu)

        self.especialidades = self.medicos_copy.set_index(self.medicos_copy['Id'])
        self.especialidades = self.especialidades.drop('Id', axis=1).drop('Tipo', axis=1).drop('Edad', axis=1).drop('Sexo', axis=1).drop('Especialidad', axis=1).drop('Pacientes', axis=1).drop('Casos', axis=1)
        print('Especialidades: \n', self.especialidades.head())
        self.especialidades.shape

        self.recomendaciones = ((self.especialidades*self.perfil_usu).sum(axis=1))/(self.perfil_usu.sum())
        print('Recomendaciones: \n', self.recomendaciones.head())

        self.recomendaciones = self.recomendaciones.sort_values(ascending=False)
        print('Recomendaciones organizadas: \n', self.recomendaciones.head())

        self.final = self.medicos.loc[self.medicos['Id'].isin(self.recomendaciones.head(5).keys())]
        self.nfinal = self.final[['Tipo'] + ['Especialidad']]
        print('Medicos recomendados: \n', self.nfinal)

if __name__ == "__main__":
    d = Data()