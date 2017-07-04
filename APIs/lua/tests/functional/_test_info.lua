--[[
    Test manager API: info().
]]

require 'paths'
local dbc = require 'dbcollection.manager'

-- delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache({delete_cache=true, is_test=true})

-- print data from the loader
print('\n==> dbcollection: info():')
dbc.info({is_test=true})

-- delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache({delete_cache=true, is_test=true})