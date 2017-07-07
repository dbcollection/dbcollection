--[[
    loader.lua unit tests.

    Warning: Requires Torch7 to be installed.
--]]


-- initializations
local dbc = require 'dbcollection'
local hdf5 = require 'hdf5'
local string_ascii = require 'dbcollection.utils.string_ascii'

local mytest = torch.TestSuite()
local tester = torch.Tester()
local precision = 1e-6
torch.manualSeed(4)


-- initlize data var
local toascii = string_ascii.convert_str_to_ascii
local tostring_ = string_ascii.convert_ascii_to_str
data = {}


------------
-- Tests
------------

function setUp()
    -- setup custom dataset data
    data.name = 'custom1'
    data.task = 'default'
    data.data_dir = '/tmp/dir'
    data.file_path = paths.concat(paths.cwd(), 'tests', 'APIs', 'data', 'test_data.h5')

    -- delete temporary cache data + dir
    dbc.config_cache({delete_cache=true, is_test=true})

    -- add dataset to dbcollection
    dbc.add({name=data.name, task=data.task, data_dir=data.data_dir, file_path=data.file_path, is_test=true})

    -- load custom dataset
    data.dataset = dbc.load({name=data.name, is_test=true})
end

function tearDown()
    -- delete temporary cache data + dir
    dbc.config_cache({delete_cache=true, is_test=true})
end


function mytest.test_get__fetch_single_idx()
    local filename = 'file1'
    local data = tostring_(data.dataset:get('train', 'filenames', 1))
    tester:eq(filename, data[1])
end

function mytest.test_get__fetch_range_idx()
    local filename = {'file1', 'file2', 'file3'}
    local data = tostring_(data.dataset:get('train', 'filenames', {1, 3}))
    tester:eq(filename, data)
end

function mytest.test_get__fetch_all_idx()
    local filename = { 'file1', 'file2', 'file3', 'file4', 'file5',
                       'file6', 'file7', 'file8', 'file9', 'file10'}
    local data = tostring_(data.dataset:get('train', 'filenames'))
    tester:eq(filename, data)
end

function mytest.test_get__fetch_single_idx__invalid_range()
    --tester:assertError(data.dataset:get('train', 'filenames','0'))
end

function mytest.test_get__fetch_all_idx__invalid_field()
    --tester:assert(false)
end

function mytest.test_get__invalid_inputs()
    --tester:assert(false)
end


function mytest.test_object__fetch_single_idx()
    local objlist = torch.ByteTensor({{1,1,1}})
    local data = data.dataset:object('train', 1)
    tester:eq(objlist, data)
end

function mytest.test_object__fetch_all_idx()
    local objlist = torch.range(1,10):view(10,1):repeatTensor(1,3):byte()
    local data = data.dataset:object('train')
    tester:eq(objlist, data)
end

function mytest.test_object__fetch_single_idx__invalid_range()
    --tester:assert(false)
end

function mytest.test_object__fetch_all_idx__invalid_field()
    --tester:assert(false)
end

function mytest.test_object__invalid_inputs()
    --tester:assert(false)
end


function mytest.test_size__succeed()
    local data = data.dataset:size('train', 'labels')
    tester:eq({10}, data)
end

function mytest.test_size__invalid_inputs()
    --tester:assert(false)
end


function mytest.test_list__succeed()
    local list = {'filenames', 'labels', 'data', 'object_ids', 'object_fields'}
    local data = data.dataset:list('train')
    table.sort(list)
    table.sort(data)
    tester:eq(list, data)
end

function mytest.test_list__invalid_inputs()
    --tester:assert(false)
end


function mytest.test_object_field_id__succeed()
    local data = data.dataset:object_field_id('train', 'filenames')
    tester:eq(1, data)
end

function mytest.test_object_field_id__invalid_field_name()
    --tester:assert(false)
end


------------------
-- Run Test Suite
------------------

setUp()
tester:add(mytest)
tester:run()
tearDown()
