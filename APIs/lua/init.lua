--[[
    dbcollection wrapper for Lua/Torch7.
--]]

require 'paths'
require 'torch'

local dbcollection = require 'dbcollection.env'
dbcollection.manager = require 'dbcollection.manager'
dbcollection.utils = require 'dbcollection.utils'

return dbcollection