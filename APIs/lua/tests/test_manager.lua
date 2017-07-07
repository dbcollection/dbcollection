--[[
    manager.lua unit tests.

    Warning: Requires Torch7 to be installed.
--]]


-- initializations
local dbc = require 'dbcollection'

local mytest = torch.TestSuite()
local tester = torch.Tester()
local precision = 1e-6
torch.manualSeed(4)


local data_dir = paths.concat(os.getenv('HOME'),'tmp','download_data', 'cifar10')


------------
-- Tests
------------

function mytest._setUp()
    dbc.config_cache({delete_cache=true, is_test=true})
end

function mytest._tearDown()
    dbc.config_cache({delete_cache=true, is_test=true})
end

function mytest.test_load__invalid_inputs()
    --tester:assert(false)
end

function mytest.test_load__succeed()
    dbc.load({name='cifar10', data_dir=data_dir, is_test=true})
end


function mytest.test_download__invalid_inputs()
    --tester:assert(false)
end

function mytest.test_download__succeed_cifar10()
    dbc.download({name='cifar10', data_dir=data_dir, is_test=true})
end


function mytest.test_process__invalid_inputs()
    --tester:assert(false)
end

function mytest.test_process__succeed_cifar10()
    dbc.download({name='cifar10', data_dir=data_dir, is_test=true})
    dbc.process({name='cifar10', is_test=true})
end


function mytest.test_add__invalid_inputs()
    --tester:assert(false)
end

function mytest.test_add__succeed()
    dbc.add({name='test', task='task1', data_dir='data/dir', file_path='path/file.h5', is_test=true})
end


function mytest.test_remove__invalid_inputs()
    --tester:assert(false)
end

function mytest.test_remove__invalid_dataset()
    --tester:assert(false)
end

function mytest.test_remove__succeed()
    dbc.add({name='test', task='task1', data_dir='data/dir', file_path='path/file.h5', is_test=true})
    dbc.remove({name='test', delete_data=true, is_test=true})
end


function mytest.test_config_cache__change_default_dir()
    dbc.config_cache({field='default_cache_dir', value='new/cache/path', is_test=true})
end

function mytest.test_config_cache__delete_cache()
    dbc.config_cache({delete_cache=true, is_test=true})
end

function mytest.test_config_cache__delete_data()
    dbc.config_cache({clear_cache=true, delete_cache=true, is_test=true})
end


function mytest.test_query()
    dbc.query({is_test=true})
end

function mytest.test_info()
    dbc.info({is_test=true})
end

------------------
-- Run Test Suite
------------------

tester:add(mytest)
tester:run()
