## Folder Lookup

### Como rodar:

Para rodar localmente, é necessário instalar as dependências:

```
pip install -r requirements.txt
```

E depois apenaas rodar o script **main.py**

```
python main.py
```

### Como gerar o executável

Primeiramente, deve ser instalado o pyinstaller:

```
pip install pyinstaller
```

Na pasta principal do projeto, rodar:

```
pyinstaller --onefile --paths myenv\Lib\site-packages main.py
```

**OBS**: Executável do windows só pode ser gerado em uma máquina windows, enquanto executável do linux só pode ser gerado em uma máquina linux. 
