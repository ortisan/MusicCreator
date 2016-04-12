# Criador tosco de músicas
Projeto utiliza a biblioteca music21 pra criar músicas a partir de cadências e notas melódicas randomizadas.

## Instalação

Criar e exportar variável de ambiente $MUSIC_PROJECT_HOME

pip install -r requirements.txt
 
## Execução
python MusicGenerator.py

## Avaliação das cadências
python app_web.py

* [Link](http://localhost:5000)

## Inicio da análise para identificar padrões entre as distâncias das notas entre as cadências.

```
ipython notebook --notebook-dir=<PATH_PROJETO>
```

ou
 
```
/usr/bin/python2.7 /usr/local/bin/ipython notebook --ip 127.0.0.1 --port 8888
```

* Carregar o arquivo [analysis/AnaliseInicial.ipynb](http://127.0.0.1:8888/notebooks/analysis/CadencesPreferences.ipynb):


## TODO
Utilizar as cadências mais populares para um usuário e gerar uma música.

