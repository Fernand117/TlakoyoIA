import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

class Data():
    def __init__(self) -> None:
        self.rutaCSV = "../DataSets/Final_Train_txt.txt"
        self.medicos = pd.read_csv(self.rutaCSV)

        print("Medicos\n", self.medicos.head())

        self.medicos['Especialidad'] = self.medicos.Especialidad.str.split(',')
        
        self.medicosCo = self.medicos.copy()
        for index, row in self.medicos.iterrows():
            for esp in row['Especialidad']:
                self.medicosCo.at[index, esp] = 1
        
        self.medicosCo = self.medicosCo.fillna(0)
        print("Especialidades calificadas\n", self.medicosCo)


if __name__ == "__main__":
    d = Data()