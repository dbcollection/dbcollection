--[[
    dbcollection wrapper for Lua/Torch7.
--]]


local dbcollection = require 'dbcollection.env'
local doc = require 'argcheck.doc'

doc[[
# dbcollection
dbcollection is a cross-platform (Windows, MacOS, Linux),
cross-language (Python, Lua/Torch7, Matlab) API to easily manage datasets'
metadata by using the standard HDF5 file format.

This is a simple Lua wrapper for the Python's dbcollection module.
The functionality is almost the same, appart with a few minor
differences regarding setting up ranges when fetching data.
Internally it uses the Python's dbcollection module for data
download/process/management.
]]

require 'dbcollection.manager'
require 'dbcollection.utils'

return dbcollection