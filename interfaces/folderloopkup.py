import os
import webbrowser
import PySimpleGUI as sg
from service import get_information_about_files, save
from interfaces.utils import popup

dir_path = os.path.dirname(os.path.realpath(__file__))

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

sg.theme('LightGrey4')

layout = [
    [sg.Text('Caminho do diretório que deseja varrer:')],
    [sg.InputText()],
    [sg.Text('Caminho onde será salvo o excel de saída:')],
    [sg.InputText(os.path.join(dir_path, 'resultado.xlsx'))],
    [sg.Submit('Processar')]
]


def open_window():
    window = sg.Window('Folder Lookup', layout)

    """
    this loop will constantly look for a new user input (button press, for example)
    """
    while True:
        event, values = window.read()

        if event == 'Processar':
            path = values[0]
            result_path = values[1]

            if path == '' or result_path == '':
                popup(
                    'Ops...',
                    'É necessário indicar o diretório de entrada e o caminho do arquivo de saída.',
                    None)
            else:
                if os.path.exists(path) == False:
                    popup(
                        'Ops...',
                        'Diretório de entrada não existe.',
                        None)
                else:
                    dataframe, errors = get_information_about_files(
                        root_dir=path)

                    if result_path is not None:
                        save(result_path, dataframe)

                    if len(errors) == 0:
                        final_popup = popup(
                            'Finalizado!',
                            f'Processo concluído com sucesso! Salvo em {result_path}.',
                            None)
                    else:
                        with open('errors.txt', 'w') as f:
                            f.write('\n'.join(errors))
                        final_popup = popup(
                            'Finalizado com erro!',
                            f'Processo concluído, porém com {str(len(errors))} erros. Erros salvos no arquivo errors.txt',
                            None)

                    event, values = final_popup.read()

                    if event == sg.WIN_CLOSED or event == 'Ok':
                        final_popup.close()

        else:
            break

    window.close()
