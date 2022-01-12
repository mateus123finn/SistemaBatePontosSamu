import PySimpleGUI as sg
import time
from Classes.files import arquivos
from Classes.time import clock_time,formater_clock
import pyperclip

USER = 'oFazax'

frame_layout = [[sg.Button('Iniciar Ponto',key = 'start'),sg.Button('Pausar/Resumir'),sg.Button('Parar Ponto',key = 'stop',disabled = True)]]

layout = [[sg.Text('RELOGIO',font=('Arial',20),key="clock",text_color = 'black')], [sg.Text('NÃO HÁ PONTOS EM ABERTO',font=('Arial',20),key="status")],[sg.Listbox(enable_events = True, values=(),key='lista_pontos',size=(25,18)),sg.Frame('Opções de Ponto',layout = frame_layout)],[sg.Text('',font=('Arial',15),key="total")]]

window = sg.Window('Pontos SAMU', layout,finalize=True)

files = arquivos()

files.load(window)

if files.status:
    window.Element('start').update(disabled = True)
    window.Element('stop').update(disabled = False)
    window.Element('status').update('PONTO EM ABERTO')

#clock = clock_time(window)
#clock.start()

while True:

    event, values = window.read()

    #print(event)

    if event == 'start':
        #print("uai")
        window.Element('start').update(disabled = True)
        window.Element('stop').update(disabled = False)
        window.Element('status').update('PONTO EM ABERTO')
        tempo = time.time()
        files.save(tempo)
        tempo_formated = time.localtime(tempo)
        clips = 'Seu Login: '+USER+'\nData: '+str(formater_clock(tempo_formated.tm_mday))+'/'+str(formater_clock(tempo_formated.tm_mon))+'/'+str(tempo_formated.tm_year)+'\nHorário de entrada: '+str(formater_clock(tempo_formated.tm_hour))+':'+str(formater_clock(tempo_formated.tm_min))
        pyperclip.copy(clips)
        pyperclip.paste()
        files.status = True
        files.load(window)

    elif event == 'stop':
        #print("uai")
        window.Element('start').update(disabled = False)
        window.Element('stop').update(disabled = True)
        window.Element('status').update('NÃO HÁ PONTOS EM ABERTO')
        tempo = time.time()
        tempo_formated = time.localtime(tempo)
        files.save(tempo,stop = True)
        valores = files.loadultimo()
        clips = 'Horário de saída: '+str(formater_clock(tempo_formated.tm_hour))+':'+str(formater_clock(tempo_formated.tm_min))+'\nTotalizando: {:2d} Horas e {:2d} Minutos'.format(int(valores[0]),int(valores[1]))
        pyperclip.copy(clips)
        pyperclip.paste()
        files.status = False
        files.load(window)

    if event == 'lista_pontos':
        if files.data:
            #print(files.data)
            files.load_unitario(str(values['lista_pontos'][0]),window)

    if event == sg.WINDOW_CLOSED:
        #clock.close_clock()
        break

window.close()

