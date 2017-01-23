from clint.textui import progress
import requests

url = 'https://www.cs.toronto.edu/~kriz/cifar-10-matlab.tar.gz'
dataset = 'cifar10'
save_path = '/home/mf/Toolkits/Codigo/git/dbclt_teste/data/' + dataset + '/'
fname_save = 'cifar-10-matlab.tar.gz'
fname = save_path + fname_save

r = requests.get(url, stream=True)
with open(fname, 'wb') as f:
    total_length = int(r.headers.get('content-length'))
    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
        if chunk:
            f.write(chunk)
            f.flush()