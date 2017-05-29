--[[
    Test process a dataset using the dbcollection API.
]]

require 'paths'
local dbc = require 'dbcollection.manager'

local cmd = torch.CmdLine()
cmd:text()
cmd:text(' ----------- Process script options ----------- ')
cmd:text()
cmd:option('-name',  'cifar10', 'Dataset name.')

local opt = cmd:parse(arg or {})

-- delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache({delete_cache=true, is_test=true})

-- download/setup dataset
print('\n==> dbcollection: download()')
dbc.process({name=opt.name, verbose=true, is_test=true})

-- print data from the loader
print('\n==> dbcollection: info()')
dbc.info({is_test=true})

-- delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache({delete_cache=true, is_test=true})