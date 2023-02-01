import os
import PySimpleGUI as sg
from service import move_and_rename_files, save
from interfaces.utils import popup


dir_path = os.path.dirname(os.path.realpath(__file__))

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

sg.theme('LightGrey4')

event_types = [[sg.Radio('Mover', 'group 1', key='move', enable_events=True, default=True)],
               [sg.Radio('Copiar', 'group 1', key='copy', enable_events=True)]
               ]

layout = [
    [sg.Text('Indique o caminho do excel contendo o mapeamento de arquivos:')],
    [sg.Text('O arquivo deve estar no formato XLSX e  conter as colunas:')],
    [sg.Text(' "Caminho", "Nome do arquivo", "Caminho destino" e "Nome do arquivo destino" (não obrigatório).')],
    [sg.In(), sg.FileBrowse(file_types=(("Excel Files", "*.xlsx"),))],
    event_types,
    [sg.Submit('Processar')]
]


def open_window():
    window = sg.Window('Folder Lookup', layout)

    selected_value = 'move'

    """
    this loop will constantly look for a new user input (button press, for example)
    """
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'move' or event == 'copy':
            selected_value = event
        elif event == 'Processar':
            path = values[0]

            if path == '':
                popup(
                    'Ops...',
                    'É necessário indicar o arquivo de entrada.',
                    None)
            else:
                if os.path.exists(path) == False:
                    popup(
                        'Ops...',
                        'Arquivo de entrada não existe.',
                        None)
                else:
                    try:
                        error_df = move_and_rename_files(
                            filepath=path, action_type=selected_value)

                        if len(error_df) > 0:
                            save('error.xlsx', error_df)
                            final_popup = popup('Alguns erros aconteceram',
                                                f'Ocorreram {str(len(error_df))} erros durante o processo. O excel de saída pode foi salvo como error.xlsx.',
                                                None)

                            if event == sg.WIN_CLOSED or event == 'Ok':
                                final_popup.close()
                        else:
                            final_popup = popup('Sucesso',
                                                f'Processo finalizado sem erros!',
                                                None)

                            if event == sg.WIN_CLOSED or event == 'Ok':
                                final_popup.close()

                    except Exception as exp:
                        final_popup = popup('Erro!', str(exp), None)

                        if event == sg.WIN_CLOSED or event == 'Ok':
                            final_popup.close()

    window.close()
