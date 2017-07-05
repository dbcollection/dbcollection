local dbcollection = require 'dbcollection.env'
local doc = require 'argcheck.doc'

doc[[
### dbcollection.utils
*dbcollection* provides a set of util functions which are useful for helping in parsing data.
]]

local utils = {
    string_ascii = require 'dbcollection.utils.string_ascii',
    pad = require 'dbcollection.utils.pad',
}
dbcollection.utils = utils

return utils