# fast_analysis

## data_analysis_risetimes
Esse arquivo é um notebook do jupyter que é utilizado para carlular os risetimes das formas de onda. Para utiliza-lo, é necessário utilizar arquivos H5 contendo a forma de onda a ser analisada e a forma de onda do sinal de trigger utilizado. 

## read_waveform
Esse arquivo deve ser utilizado para transformar o arquivo de texto contendo os dados da digitalização da forma de onde da interesse em um arquivo H5.
Para executar esse código, no prompt de comando, escreva:
```
python read_waveform.py arquivo.txt
```
Se quiser escolher o limite de eventos convertidos:
```
python read_waveform.py arquivo.txt -n (numero de eventos)
```
O default para o número máximo de eventos é 10000.

## read_trigger
Esse arquivo deve ser utilizado para transformar o arquivo de texto contendo os dados da digitalização do trigger em um arquivo H5.
Para executar esse código, no prompt de comando, escreva:
```
python read_waveform.py arquivo.txt
```
Se quiser escolher o limite de eventos convertidos:
```
python read_waveform.py arquivo.txt -n (numero de eventos)
```
O default para o número máximo de eventos é 10000.
