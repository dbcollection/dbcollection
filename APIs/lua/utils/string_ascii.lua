--[[
    String-to-ascii and ascii-to-string convertion functions.
--]]

local ffi = require 'ffi'

------------------------------------------------------------------------------------------------------------

local function get_str_maxmimum_lenght(input_table)
    local max_l = 0
    for k, v in pairs(input_table) do
        assert(type(v)=='string')
        max_l = math.max(max_l, #v)
    end
    return max_l
end

------------------------------------------------------------------------------------------------------------

local function convert_str_to_ascii(input)
-- Convert a string to a torch.CharTensor
    assert(input)

    local input_type = type(input)
    assert(input_type == 'table' or input_type == 'string')

    if input_type == 'string' then
        input = {input}
    end

    -- get string maximum length of the table
    local maximum_lenght = get_str_maxmimum_lenght(input) + 1

    -- allocate tensor
    local ascii_tensor = torch.CharTensor(#input, maximum_lenght):fill(0)

    -- copy data to the tensor
    local s_data = ascii_tensor:data()
    for k, v in ipairs(input) do
        ffi.copy(s_data, v)
        s_data = s_data + maximum_lenght
    end
    return ascii_tensor
end

------------------------------------------------------------------------------------------------------------

local function convert_ascii_to_str(input)
-- convert torch.CharTensor to a table of strings
    local out = {}
    local input = input:char()
    for i=1, input:size(1) do
        table.insert(out, ffi.string(input[i]:data()))
    end
    return out
end

------------------------------------------------------------------------------------------------------------

return {
    convert_str_to_ascii = convert_str_to_ascii,
    convert_ascii_to_str = convert_ascii_to_str,
}