import time
from threading import Thread

def formater_clock(elemento):
    if elemento < 10:
        #print(teste)
        return '0'+str(elemento)
    else:
        return str(elemento) 

class clock_time(Thread):
    def __init__(self,window):
        Thread.__init__(self)
        self.tela = window
        self.controle = True

    def run(self):
        while self.controle:
            tempo_ms = time.time()
            converter = time.localtime(tempo_ms)
            self.tela.Element('clock').update(value=(formater_clock(converter.tm_hour)+":"+formater_clock(converter.tm_min)+":"+formater_clock(converter.tm_sec)))

    def close_clock(self):
        self.controle = False
