import download as dl

# Download cifar 10
url1 = 'https://www.cs.toronto.edu/~kriz/cifar-10-matlab.tar.gz'
dataset = 'cifar10'
save_path = '/home/mf/Toolkits/Codigo/git/dbclt_teste/data/' + dataset + '/'
fname_save = 'cifar-10-matlab.tar.gz'

# download file
dl.download_file(url1, save_path, fname_save, True)
#print('download file')
#dl.download_file_v1(url1, save_path, fname_save, True)

# extract file
dl.extract_file(save_path, fname_save,True)

print('Done.')