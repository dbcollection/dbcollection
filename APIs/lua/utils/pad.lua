--[[
    Padding functions.
--]]


local function pad_list_table(tableA, val)
    -- get maximum size of all tables
    local max_lenght = 0
    for _, v in pairs(tableA) do
        max_lenght = math.max(max_lenght, #v)
    end

    -- pad table with 'val'
    local out = {}
    for _, v in ipairs(tableA) do
        -- copy contents into a new table
        local t = {}
        for _, value in ipairs(v) do
            table.insert(t, value)
        end
        -- pad table
        for i=1, max_lenght - #v do
            table.insert(t, val)
        end
        -- add padded table
        table.insert(out,t)
    end

    return out
end

local function pad_list_tensor(tableA, val)
    -- tableA: table of tensors
    local out = {}
    -- convert table of tensors into table of tables
    for k, v in ipairs(tableA) do
        table.insert(out, v:totable())
    end
    return torch.DoubleTensor(pad_list_table(out, val)):typeAs(tableA[1])
end


local function pad_list(inputA, val)
-- pad a table or tensor with a value
    assert(inputA)

    local val = val or -1

    if type(inputA) == 'userdata' then
        return pad_list_tensor(inputA, val)
    elseif type(inputA) == 'table' then
        return pad_list_table(inputA, val)
    else
        error(('Invalid input type for pad_list: \'%s\'. Must be either a table or a tensor.')
              :format(type(inputA)))
    end
end


local function unpad_list_tensor(tensorA, val)
    local size = tensorA:size(1)
    if size > 1 then
        -- table of tensors
        local out = {}
        for i=1, size do
            local tensor = tensorA[i]
            table.insert(out, tensor[tensor:ne(val)])
        end
        return out
    elseif size == 1 then
        return tensorA[tensorA:ne(val)]
    else
        error('Tensor size < 1.')
    end
end


local function unpad_list_table(tableA, val)
    local out = {}
    for k, v in ipairs(tableA) do
        if type(v) == 'table' then
            local t = {}
            for _, value in ipairs(v) do
                if value ~= val then
                    table.insert(t, value)
                end
            end
            table.insert(out, t)
        elseif type(v) == 'number' then
            if v ~= val then
                table.insert(out, v)
            end
        else
            error('Type must be either a \'table\' or \'number\'.')
        end
    end
    return out
end


local function unpad_list(inputA, val)
-- unpad a table or tensor with a certain value
    assert(inputA)

    local val = val or -1

    if type(inputA) == 'userdata' then
        return unpad_list_tensor(inputA, val)
    elseif type(inputA) == 'table' then
        return unpad_list_table(inputA, val)
    else
        error(('Invalid input type for unpad_list: \'%s\'. Must be either a table or a tensor.')
              :format(type(inputA)))
    end
end


return {
    pad_list = pad_list,
    unpad_list = unpad_list,
}