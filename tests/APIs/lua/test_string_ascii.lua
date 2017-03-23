--[[
    string_ascii.lua unit tests.

    Warning: Requires Torch7 to be installed.
--]]


-- initializations
local ffi = require 'ffi'
local string_ascii = require 'dbcollection.utils.string_ascii'
local toascii_ = string_ascii.convert_str_to_ascii
local tostring_ = string_ascii.convert_ascii_to_str

local mytest = torch.TestSuite()
local tester = torch.Tester()
local precision = 1e-6
torch.manualSeed(4)


------------
-- Tests
------------

function mytest.test_convert_str_to_ascii__string()
    local str = 'test_string'
    local str_tensor = torch.CharTensor(1,#str+1):fill(0)
    ffi.copy(str_tensor[1]:data(), str)
    tester:eq(str_tensor, toascii_(str))
end

function mytest.test_convert_str_to_ascii__table()
    local str = {'test_string1', 'test_string2', 'test_string3'}
    local max_length = #str[1] + 1
    local str_tensor = torch.CharTensor(#str, max_length):fill(0)
    local s_data = str_tensor:data()
    for i=1, #str do
        ffi.copy(s_data, str[i])
        s_data = s_data + max_length
    end
    tester:eq(str_tensor, toascii_(str))
end



function mytest.test_convert_ascii_to_str__CharTensor_1D()
    local str = 'test_string'
    local str_tensor = torch.CharTensor(1,#str+1):fill(0)
    ffi.copy(str_tensor[1]:data(), str)
    tester:eq(str, tostring_(str_tensor)[1])
end

function mytest.test_convert_ascii_to_str__CharTensor_2D()
    local str = {'test_string1', 'test_string2', 'test_string3'}
    local max_length = #str[1] + 1
    local str_tensor = torch.CharTensor(#str, max_length):fill(0)
    local s_data = str_tensor:data()
    for i=1, #str do
        ffi.copy(s_data, str[i])
        s_data = s_data + max_length
    end
    tester:eq(str, tostring_(str_tensor))
end

function mytest.test_convert_ascii_to_str__ByteTensor_2D()
    local str = {'test_string1', 'test_string2', 'test_string3'}
    local max_length = #str[1] + 1
    local str_tensor = torch.CharTensor(#str, max_length):fill(0)
    local s_data = str_tensor:data()
    for i=1, #str do
        ffi.copy(s_data, str[i])
        s_data = s_data + max_length
    end
    tester:eq(str, tostring_(str_tensor:byte()))
end

------------------
-- Run Test Suite
------------------


tester:add(mytest)
tester:run()
