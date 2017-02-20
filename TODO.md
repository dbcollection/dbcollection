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


## Coding Style

This repo tries to follow the PEP8 style convention as close as possible.

### Dataset loader class

- :get('field_name', id_ini, id_end) - retrieve the 'i'th' data from the field 'field_name' into a table
- :obj(id_ini, id_end) - retrieve the data of all fields of an object: It works as calling :get() for each field individually and grouping them into a table.
- :size('field_name') - returns the size of the elements of a field_name
- :list() - lists all fields in order that compose an object element.

### Dataset Loader API

- **.get('field_name', id_ini, [id_end]) ** - retrieve the 'i'th' data from the field 'field_name' into a table
	options:
		- field_name: field name identifier [Type=String]
		- id_ini: starting id (if -1 then returns all data entries) [Type=Integer]
		- id_end: ending id (if empty it returns only the initial id) [Type=Integer]
- **.obj(id_ini, id_end)** - retrieve the data of all fields of an object: It works as calling :get() for each field individually and grouping them into a list.
	options:
		- id_ini: starting id (if -1 then returns all data entries) [Type=Integer]
		- id_end:  ending id (if empty it returns only the initial id) [Type=Integer]
- **.size('field_name') ** - returns the size of the elements of a field_name.
	options:
		- field_name: field name identifier [Type=String]
- **.list()** - lists all fields in order that compose an object element.
	options:
		(none)


### dbcollection (dataset managing) API

- **.load()** - returns a loader class with the necessary functions to manage the selected dataset.
	options:
		- name: name of the dataset [Type=String]
		- data_path: path to store the data (if the data doesn't exist and the download flag is equal True) [Type=String, (default=data_path_default)]
		- cache_path: path to store the cache metadata (if the cache file doesn't exist and the download flag is equal True) [Type=String, (default=cache_path_default)]
		- save_name: save the metadata file with a new name (usefull to create custom versions of the original) [Type=Boolean]
		- task: specify a specific task to load [Type=String, (default='default')]
		- download: [Type=Boolean, (default=True)]
		- verbose: [Type=Boolean, (default=True)]
		- make_list: organizes the data w.r.t. to other fields. The data must be organized in a dictionary with the following format: {"new_field_name":"field_name"}  [Type=Dictionary]
		- select: selects indexes from 'field_name' equal to the selected value(s) (removes objects ids without those 'field_name''s values) [Type=Dictionary]
		- filter: removes indexes from 'field_name' equal to the selected value(s) (removes objects ids with those 'field_name''s values) [Type=Dictionary]

	```
	Example 1:
		# Load the metadata Loader for the cifar10 dataset
		- .load(name='cifar10', data_path='~/tmp/dir', cache_path='~/tmp/cache',task='classification')
	```

	```
	Example 2:
		# Load the metadata loader for the cifar10 dataset, split the train set into 75% train, 25% val data points and save it with a new task name.
		- .load(name='cifar10', spit={"train": 0.75, "val":0.25}, save_name='cifar10_75_25') # **recitify this format latter**

		# Load the metadata loader for the custom cifar10 dataset (split).
		- .load(name='cifar10', task='cifar10_75_25')
	```

	```
	Example 3:
		# Load the metadata loader for the cifar10 dataset and organize the data w.r.t. the class name.
		- .load(name='cifar10', make_list={"class_list":'classes', "filename_list":"fname"})
	```

	```
	Example 4:
		# Select data from only two categories from the cifar10 dataset
		- .load(name='cifar10', select={"class":['cat', 'dog']})
	```

	```
	Example 5:
		# Filter/remove data of all animals classes from cifar10.
		- .load(name='cifar10', filter={"class":['bird', 'cat', 'deer', 'dog', 'frog', 'horse']})
	```

	################
	 organize_list
	################

	- field_name: (str ou lista de strs)
	Procura por 'ids' do 'campo' no vector 'object_id' e agrupa cada 'object_id' por ordem crescente que tenha um 'id' igual ao do 'campo'. 
	Isto é, procura-se (por ordem crescente do 'id' do 'campo') por qualquer objecto que possua o mesmo 'id' do 'campo' e constroi-se uma lista ordenada do 'id' do 'object_id'. Isto irá resultar em listas de 'ids' para cada 'id' do 'campo' designado. Estas listas serão guardadas no ficheiro de metadados.

	- Nota: esta funcao é executada após os filtros e selecções (ver abaixo).

	#########
	 select
	#########

	- select: dict (name_field: [value, condition])
	Procura no vector 'object_id' pelo 'campo' inserido, e seleciona so os 'object_id' que possuam o mesmo valor(es) que o campo possua. A condicao de entrada é igual às operacoes matematicas: eq, ne, lt, gt, le, ge. Isto permite que o utilizador escolha intervalos em vez de inserir varios campos manualmente. Resumindo, um utilizador escolhe um ou varios 'campos' para selecionar apenas a informação que pretende manter. Este especifica o(s) valor(es) do(s) campo(s) que pretende e pode ainda selecionar uma condicao de filtragem dos valores (o default será eq - equal). A lista de indices do 'object_id' resultantes desta selecção irão compor (substituir) o novo vector/matriz do 'object_id'.


	#########
	 filter
	#########

	- filter: dict (name_field: [value, condition])
	Semelhante ao select, este filtra apenas os campos seleccionados do 'object_id' e substitui esta lista pela nova lista de 'object_id'.


	#########
	 balance
	#########

	- balance: dict ({'sets':['name_set'], 'load':[value]}, 'ordered'=True/False, 'unique'='field_name')
	'Balanceia' os sets consoante os valores introduzidos. O utilizador seleciona uma combinação de sets de dados ('train', 'val', 'test', etc) e direcciona a quantidade de dados para um lado ou para outro (a quantidade que vai para cada set tem de totalizar 100 no final senao dá erro). Esta funcao permite ao utilizador, por exemplo, usar o dataset inteiro (train+val+test) ao simplesmente assignar ao set de 'train' todos os dados dos outros sets ({'sets': ['train', 'val', 'test'], 'values': [100, 0, 0]})
	A opção 'ordered' permite que se faça um shuffle dos dados antes de se assignar para que set armazenar. Para assignar a divisão, os indices do 'object_id' são todos aglomerados numa unica lista e depois são divididos de acordo com a percentagem de divisão. O que esta opcao permite fazer eh um shuffle dos indices antes de efectuar a divisao dos mesmos.
	A opcao 'unique' força que objectos com o mesmo indice que o(s) campo(s) selecionado(s) esteja(m) presente apenas num set de dados. Por exemplo, evita que varios sets tenham a mesma imagem.


	Exemplos1: balance = {'sets': ['train', 'val'], 'values': [75,25]}
	Exemplos2: balance = {'sets': ['test', 'val'], 'values': [100,0]}
	Exemplos3: balance = {'sets': ['test', 'test'], 'values': [100,0]} -- nothing happens
	Exemplos4: balance = {'sets': ['test', 'train', 'val'], 'values': [15,70,15]}
	Exemplos5: balance = {'sets': ['val', 'train', 'test'], 'values': [0,100,0]} -- everything goes to the set 'train'

	------
	NOTA
	------
	No final, tenho que remover todos os dados que nao tenham sido usados no object_id e libertar espaco.

- **.delete()** - deletes the data of a dataset.
	options:
		- name: name of the dataset to delete the data from disk [Type=String]
		- data: flag indicating if the data folder is to be deleted from disk [Type=Boolean, (default=False)]
		- cache: flag indicating if the metadata cache file is to be deleted from disk [Type=Boolean, (default=True)]

	```
	Example 1:
		# Remove the cifar10 data and metadata from disk
		- .delete(name='cifar10', data=True, cache=True)
	```

- **.set()/config()** - Manually setup the configurations of the cache file dbcollection.json
	options:
		- name: name of the dataset (Type=String)
		- fields: specifies which fields and values to update the dbcollection cache file (Type=Dictionary)
		- default_paths: updates the default cache/data paths (Type=Dictionary)
	```
	Example 1:
		# update the paths for the Pascal VOC 2007 dataset
		- .set(name='pASCAL voc 2007', fields={"data_path":"~/tmp/dir/data","cache_path":"~/tmp/dir/data"})
	```

	```
	Example 2:
		# update the default paths of the metadata cache file
		- .set(default_paths={"cache_path_default":"~/newcachedir/","data_path_default":"~/newdatadir/"})
	```
- **.download()** - Download the data for one (or several) listed dataset(s).
	options:
		- name: name(s) of the dataset (Type=List)
		- path: path(s) to store the data (Type=List)

	```
	Example 1:
		# Download the data for the Cifar10 dataset
		- .download(name=["cifar10"], path=["~/data"]) # it will create a folder named '{image_processing}/cifar10' in '~/data'
	```

	```
	Example 2:
		# Download the data for the Cifar10/Cifar100/MNIST datasets into three different folders
		- .download(name=["cifar10", "cifar100", "mnist"], path=["~/folder1/data", "~/folder2/data", "~/folder3/data"])
	```

- **.reset(cache=True, name='Dataset')** - resets the data of the dbcollection.json cache file for a specific dataset (it deletes the cache files for this dataset as well, if any).
	options:
		- cache: force the cache file of the preprocessed data to be deleted for the particular dataset (type=Boolean)
		- data: force the dataset's data files to be deleted for the particular dataset (type=Boolean)
		- name: name of the dataset to reset the cache (Type=String)

	```
	Example 1:
		# Reset (delete) the cache for the cifar10 dataset
		- .download(name=["cifar10"], path=["~/data"]) # it will create a folder named '{image_processing}/cifar10' in '~/data'
	```

- **.list()/:query()** - list all available datasets for download/preprocess. (tenho que pensar melhor sobre este)
	options:
		- info:  (Type=List)
		- search: (Type=Dictionary)

	```
	Example 1:
		# Do some queries to the dbcollection.json file about it's stored data.
		- .query(info=[{"name":"Pascal VOC 2007"}]) # returns all information about pascal voc 2007 dataset
		- .query(search={"categories":['image processing'], "tasks":["classification", "detection"]}) # returns all datasets belonging to that category + tasks
	```

- **.add()** - adds a custom dataset to the list.
	options:
		- name: dataset name [Type=String]
		- data_path: data's folder path on disk [Type=String]
		- cache_path: cache's metadata storage path [Type=String]
		- category: name of the category [Type=String]
		- task: name of the task [Type=String]

	```
	Example 1:
		# add a custom dataset to the list of available datasets.
		- .add(name="custom_dataset", data_path="~/tmp/dir", cache_path="~/tmp/dir", category="custom", task="default")
	```

### IPython notebooks

- fazer uns quantos notebooks como tutoriais para mostrar como funciona a API.

### Notes

- Images are in the format of CxHxW, being C=color, H=height, and W=width.

### Tests coverage

unit tests (so far):
- utils: test_utils (13/22)
- storage: test_storage (2/10)
- manager: test_manager (7/8)
- loader: test_loader (16/16)
- cache: test_cache (8/17)

### Requirements to go live

- Manager API:
	- selecionar campos
	- filtrar campos
	- organizar campos
	- data balancing (train/test/val)
- Fazer loader API (Done)
- unit tests (a fazer)
- testes do cifar10 (mostrar imagens random)
- system tests
- adicionar mais alguns datasets (voc2007, imagenet, coco)
- setup.py do pacote
- testes com python 2.7
- testes em windows
- LuaAPI (TODO)
- MatlabAPI
- readme + docs + notebooks


**** TODO: ****
- acabar select/filter - (DONE)
- fazer balance - (a fazer)
- remover a categoria do cache manager e meter como um campo separado no dicionario. Sempre que adicionar um dataset, este tem que fazer o update das keywords neste novo campo e adicionar o nome do dataset na categoria especifica.
- adicionar o object_field ao DatasetLoader para nao estar sempre a procurar pelo campo do field (faço sempre a convercao para str e ta feito)
- adicionar keywords ao cifar10
- reformular a funcao adicionar de um dataset (talvez usar a formula escrita para o metodo new() que vem a seguir)
- criar uma funcao de criar um dataset ao adicionar so o caminho da pasta root dos datasets que tenham os caminhos das pastas de teste, train, val, etc.
  Por exemplo: .new(name, data_dir, keywords)
- reformular a funcao de print de datasets (.list()) para englobar a nova lista de categorias como opcao para listar os datasets
- reformular a funcao de .query() para o novo formato
- fazer um codigo de exemplo de como retornar dados (imagens, etc) de um dataset usando o LoaderAPI. Fazer o plot de imagens usando matplotlib.