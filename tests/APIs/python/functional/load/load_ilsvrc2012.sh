path=$PWD/tests/APIs/python/functional/load/_test_load.py
datadir='/media/HDD2/Datasets/Imagenet'
echo '**Load imagenet 2012 (ilsvrc2012)**'
python $path --name 'ilsvrc2012' --data_dir $datadir