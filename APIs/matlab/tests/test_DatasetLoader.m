% Test dbcollection's dataset loader API

%% Load file

name = 'cifar10';
task = 'classification';
data_dir = '/home/mf/tmp/download_data/cifar10';
cache_path = '/home/mf/dbcollection/cifar10/classification.h5';

%% initialize object

loader = dbcollection_DatasetLoader(name, task, data_dir, cache_path);
utils = dbcollection_utils();

%% get()

data = loader.get('train', 'classes');
classes = utils.string_ascii.convert_ascii_to_str(data);
disp(classes)

%% object()

%% size()

%% list()

%% object_field_id()