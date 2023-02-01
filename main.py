import os
from datetime import datetime
import PySimpleGUI as sg
from interfaces.folderloopkup import open_window as open_window_folderlookup
from interfaces.movecopy import open_window as open_window_movecopy


# Alterar a data de expiração conforme necessidade e gerar novo executável
EXPIRATION_DATE = datetime.strptime('20/02/2023 00:00:00', '%d/%m/%Y %H:%M:%S')


dir_path = os.path.dirname(os.path.realpath(__file__))

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

sg.theme('LightGrey4')

if EXPIRATION_DATE <= datetime.now():
    layout = [
        [sg.Text('O seu tempo de uso da aplicação expirou!')],
        [sg.Text('Favor, entrar em contato com a administração do sistema.')],
        [sg.Submit('Sair')]
    ]
else:
    layout = [
        [sg.Text('Qual ação deseja realizar?')],
        [sg.Button('Mapeamento de diretório')],
        [sg.Button('Copiar ou Mover arquivos')],
        [sg.Button('Sair')]
    ]

window = sg.Window('Menu', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Sair':
        break
    elif event == 'Mapeamento de diretório':
        open_window_folderlookup()
    elif event == 'Copiar ou Mover arquivos':
        open_window_movecopy()

window.close()
