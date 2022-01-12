import json,time
import PySimpleGUI as sg
from Classes.time import formater_clock

class arquivos():
    def __init__(self):
        try:
            with open('logs.dados') as arquivo:
                self.data = json.load(arquivo)
                if len(self.data[str(len(self.data)-1)]) < 2:
                    self.status = True
                else:
                    self.status = False
        except:
            print("Programa Ricardo Amado")
            self.data = {}
            self.status = False

    def deletar(self,id):
        del self.data[id]
        for i in range(int(id)+1,len(self.data)+1):
            self.data[str(i-1)] = self.data[str(i)]
        if len(self.data) > 1:
            del self.data[str(len(self.data)-1)]

        self.save(refres=True)

    def load(self,window):

        teste = []

        for i in self.data.keys():
            if self.status:
                if int(i) < len(self.data) - 1:
                    teste.append(i)
            else:
                teste.append(i)

        window.Element('lista_pontos').update(values=(teste))
        tot = 0
        if not self.status:
            for i in self.data:
                tot += self.data[i][1] - self.data[i][0]
        else:
            for i in self.data:
                if int(i) < len(self.data) - 1:
                    #print(int(i))
                    tot += self.data[i][1] - self.data[i][0]

        tempo_tot = [tot // 3600, (tot % 3600 // 60), tot % 60]

        window.Element('total').update('TOTAL : {:2d} Horas, {:2d} Minutos e {:2d} Segundos'.format(int(tempo_tot[0]),int(tempo_tot[1]),int(tempo_tot[2])))
        return self.data

    def load_unitario (self,id,window):

        inicio = self.data[id][0]
        inicio_formated = time.localtime(inicio)
        fim = self.data[id][1]
        fim_formated = time.localtime(fim)
        tempo = fim - inicio

        tempo_passado = [tempo // 3600, (tempo % 3600 // 60), tempo % 60]

        templas_tempo = '{:2d} Horas, {:2d} Minutos e {:2d} Segundos'.format(int(tempo_passado[0]),int(tempo_passado[1]),int(tempo_passado[2]))
        templas_inicio = 'Inicio : '+str(formater_clock(inicio_formated.tm_mday))+'/'+str(formater_clock(inicio_formated.tm_mon))+'/'+str(inicio_formated.tm_year)+' - '+str(formater_clock(inicio_formated.tm_hour))+':'+str(formater_clock(inicio_formated.tm_min))+':'+str(formater_clock(inicio_formated.tm_sec))
        templas_final = 'Final : '+str(formater_clock(fim_formated.tm_mday))+'/'+str(formater_clock(fim_formated.tm_mon))+'/'+str(fim_formated.tm_year)+' - '+str(formater_clock(fim_formated.tm_hour))+':'+str(formater_clock(fim_formated.tm_min))+':'+str(formater_clock(fim_formated.tm_sec))
        choice, _ = sg.Window('Ponto de Controle', [[sg.Text(templas_inicio)],[sg.Text(templas_final)],[sg.Text(templas_tempo)], [sg.Button('OK'), sg.Button('DELETE')]], disable_close=True).read(close=True)

        if choice == 'DELETE':
            self.deletar(id)
            self.load(window)

    def loadultimo(self):
        inicio = self.data[str(len(self.data)-1)][0]
        fim = self.data[str(len(self.data)-1)][1]
        tempo = fim - inicio

        return [tempo // 3600, (tempo % 3600 // 60), tempo % 60]

    def save(self, value=None, stop=False,refres=False):
        if not refres:
            lista = [value]
            if stop:
                self.data[str(len(self.data)-1)].append(value)
            else:
                self.data[str(len(self.data))] = lista

        with open('logs.dados','w') as arquivo:
            json.dump(self.data,arquivo)


