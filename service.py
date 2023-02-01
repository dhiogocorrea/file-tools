import os
import shutil
from datetime import datetime
import pandas as pd
import platform
try:
    import win32security
except:
    print('so is not windows')
try:
    from pwd import getpwuid
except:
    print('so is not linux')


def get_file_info_windows(file_path: str):
    sd = win32security.GetFileSecurity(
        file_path, win32security.OWNER_SECURITY_INFORMATION)
    owner_sid = sd.GetSecurityDescriptorOwner()
    name, domain, type = win32security.LookupAccountSid(None, owner_sid)
    return name, domain, type


def get_information_about_files(root_dir: str) -> pd.DataFrame:
    """
        loop through  the root directory an gather information about all files
    """
    result = []

    current_path = os.getcwd()

    errors = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # go to the directory to prevent error if entire path has more than 255 characters
            os.chdir(subdir)

            if os.path.exists(file) == False:
                fullpath = os.path.join(subdir, file)
                print(f'file not found: {fullpath}')
                errors.append(fullpath)
                continue

            extension = file.split('.')[-1]

            if len(extension) > 5:
                extension = ''

            size = os.path.getsize(file)
            modified_date = os.path.getmtime(file)
            modified_date = datetime.utcfromtimestamp(
                modified_date).strftime('%d/%m/%Y')
            creation_date = os.path.getctime(file)
            creation_date = datetime.utcfromtimestamp(
                creation_date).strftime('%d/%m/%Y')

            if platform.system() == 'Windows':
                author, _, _ = get_file_info_windows(file)
            else:
                author = getpwuid(os.stat(file).st_uid).pw_name

            result.append(
                [file, modified_date, creation_date, author, extension, size, subdir])
    os.chdir(current_path)

    df = pd.DataFrame(result, columns=['Nome do arquivo', 'Data de modificação',
                                       'Data de criação', 'Autor', 'Tipo do arquivo', 'Tamanho', 'Caminho'])
    return df, errors


def move_and_rename_files(filepath: str, action_type: str = 'move'):
    """
        filepath: arquivo de entrada com 3 colunas obrigatórias* e 1 opcional
        -> Caminho: pasta do arquivo a ser copiado/movido*
        -> Nome do Arquivo: nome do arquivo a ser copiado/movido*
        -> Caminho Destino: pasta que o arquivo será copiado/movido*
        -> Nome do arquivo destino: qual nome o arquivo terá em seu destino.  Caso vazio, mantém o nome original
        action_type: move ou copy
    """
    df = pd.read_excel(filepath, sheet_name=0)
    df.columns = [x.lower() for x in df.columns]

    if 'caminho' not in df.columns:
        raise Exception('Coluna "Caminho" não encontrada')
    if 'nome do arquivo' not in df.columns:
        raise Exception('Coluna "Nome do arquivo" não encontrada')
    if 'caminho destino' not in df.columns:
        raise Exception('Coluna "Caminho destino" não encontrada')
    if 'nome do arquivo destino' not in df.columns:
        df['nome do arquivo destino'] = ''

    log_error = []
    for _, row in df.iterrows():
        try:
            current_path = os.path.join(row['caminho'], row['nome do arquivo'])

            if row['nome do arquivo destino'] == '':
                target_path = os.path.join(
                    row['caminho destino'], row['nome do arquivo'])
            else:
                target_path = os.path.join(
                    row['caminho destino'], row['nome do arquivo destino'])

            if action_type == 'move':
                os.rename(current_path, target_path)
            elif action_type == 'copy':
                shutil.copy2(current_path, target_path)
        except Exception as e:
            error = row.values.tolist()
            error.append(str(e))
            log_error.append(error)

    cols = list(df.columns)
    cols.append('Mensagem de erro')

    return pd.DataFrame(log_error, columns=cols)


def save(path: str, df: pd.DataFrame):
    """
        saves the result in excel format (can be changed to to_csv if wanted)
    """
    df.to_excel(path, index=False)
