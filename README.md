Seizure Detection Python


Trello Para ver o que está sendo realizado:
https://trello.com/b/XdPQqffy/clarissa-lima

-------------------------------------------------------------
Para rodar a versão atual usar o Tela.py


Comando:

python Tela.py

-------------------------------------------------------------

Para gerar executável:

pip install pyinstaller


pyinstaller --onefile --name projetoIC --icon=cerebro_icono.ico Tela.py --additional-hooks-dir ./hooks/


Outra forma seria utilizando esta interface para facilitar: pip install auto-py-to-exe (ele gera uma interface gráfica para rodar)

Assim que estiver tudo certinho e tiver gerado o executável, é preciso enviar uma cópia da pasta "meu_modelo", "logos" e a imagem "cerebro_icono.ico para dentro da pasta onde foi gerado o executável.


