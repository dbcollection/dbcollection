--[[
    Test download a dataset using the dbcollection API.
]]

require 'paths'
local dbc = require 'dbcollection.manager'

local data_dir = paths.concat(os.getenv('HOME'), 'tmp','download_data')

local cmd = torch.CmdLine()
cmd:text()
cmd:text(' ----------- Download script options ----------- ')
cmd:text()
cmd:option('-name',  'cifar10', 'Dataset name.')
cmd:option('-data_dir',  data_dir, 'Directory where the dataset\'s files are stored.')

local opt = cmd:parse(arg or {})

-- delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache({delete_cache=true, is_test=true})

-- download/setup dataset
print('\n==> dbcollection: download()')
dbc.download({name=opt.name, data_dir=opt.data_dir, verbose=true, is_test=true})

-- print data from the loader
print('\n==> dbcollection: info()')
dbc.info({is_test=true})

-- delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache({delete_cache=true, is_test=true})