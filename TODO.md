# List of stuff to do

## dbcollection:
- ver flags de unix e windows (import sys; sys.platform == 'linux')
- fazer save das opcoes como tinha feito com um ficheiro .dbcollection.json para linux/mac primeiro
- organizar o codigo em pastas (criar pastas)
- fazer script de download+extract do cifar10
- fazer script para remover a pasta de dados extraidos


## API geral para gerir os datasets a partir de qualquer linguagem:

- dbclt.get('dataset','task', path)
	- retorna uma classe com as funcoes necessarias para obter os dados necessarios do ficheior de metadados
- dbclt.list()
	- list all available datasets 
- dbclt.delete('dataset') 
	- delete a dataset's data folder
- dbclt.config(options) 
	- configure the .dbcollection.json file directly
- dbclt.clearcache() 
	- deletes the .dbcollection.json file


## dataset processing format

- download_<task_name>.py - downloads the necessary files
- process_<task_name>.py - script that extracts the data into a hdf5 file