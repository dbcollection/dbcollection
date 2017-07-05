--[[
    Dataset loader class.
--]]

local dbcollection = require 'dbcollection.env'
local hdf5 = require 'hdf5'
local string_ascii = require 'dbcollection.utils.string_ascii'

local DataLoader = torch.class('dbcollection.DatasetLoader', dbcollection)

------------------------------------------------------------------------------------------------------------

function DataLoader:__init(name, task, data_dir, cache_path)
--[[
    dbcollection's data loading API class.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task.
    data_dir : str
        Path of the dataset's data directory on disk.
    cache_path : str
        Path of the metadata cache file stored on disk.
]]
    assert(name, ('Must input a valid dataset name: %s'):format(name))
    assert(task, ('Must input a valid task name: %s'):format(task))
    assert(data_dir, ('Must input a valid path for the data directory: %s'):format(data_dir))
    assert(cache_path, ('Must input a valid path for the cache file: %s'):format(cache_path))

    -- store information of the dataset
    self.name = name
    self.task = task
    self.data_dir = data_dir
    self.cache_path = cache_path

    -- create a handler for the cache file
    self.file = hdf5.open(self.cache_path, 'r')
    self.root_path = '/default'

    -- make links for all groups (train/val/test/etc) for easier access
    self.sets = {}
    self.object_fields = {}
    local group_default = self.file:read(self.root_path)
    for k, v in pairs(group_default._children) do
        -- add set to the table
        table.insert(self.sets, k)

        -- fetch list of field names that compose the object list.
        local data = self.file:read(('%s/%s/object_fields'):format(self.root_path, k)):all()
        if data:dim()==1 then data = data:view(1,-1) end
        self.object_fields[k] = string_ascii.convert_ascii_to_str(data)
    end
end

------------------------------------------------------------------------------------------------------------

function DataLoader:get(set_name, field_name, idx)
--[[
    Retrieve data from the dataset's hdf5 metadata file.

    Retrieve the i'th data from the field 'field_name'.

    Parameters
    ----------
    set_name : string
        Name of the set.
    field_name : string
        Name of the data field.
	idx : number/table
        Index number of the field. If the input is a table, it uses it as a range
        of indexes and returns the data for that range.
        (optional, default=nil)

    Returns
    -------
    torch.Tensor
        Value/list of a field from the metadata cache file.

    Raises
    ------
        None
]]
    assert(set_name, 'Must input a valid set name')
    assert(field_name, 'Must input a valid field name')

    local field_path = ('%s/%s/%s'):format(self.root_path, set_name, field_name)
    local data = self.file:read(field_path)
    local out
    if idx then
        local size = data:dataspaceSize()
        if type(idx)=='table' then
            assert(#idx>=1 and #idx<=2, 'Invalid range. Must have at most one or two entries: (idx_ini, idx_end).')
            if #idx == 1 then idx[2]=idx[1] end
        elseif type(idx)=='number' then
            assert(idx>=1 and idx<=size[1], string.format('Invalid \'%s\' value: %d. Valid range: (1, %d);',
                                                          field_name, idx, size[1]))
            idx = {idx, idx}
        else
            error('Invalid index type: %s. Must be either a \'number\' or a \'table\'.')
        end
        local ranges = {idx}
        for i=2, #size do
            table.insert(ranges, {1, size[i]})
        end
        out = data:partial(unpack(ranges))
    else
        out = data:all()
    end

    -- check if the field is 'object_ids'.
    -- If so, add one in order to get the right idx (python uses 0-index)
    if field_name == 'object_ids' then
        return out:add(1)
    else
        return out
    end
end

------------------------------------------------------------------------------------------------------------

function DataLoader:object(set_name, idx, is_value)
--[[
    Retrieves a list of all fields' indexes/values of an object composition.

    Retrieves the data's ids or contents of all fields of an object.

    It works by calling :get() for each field individually and grouping
    them into a list.

    Parameters
    ----------
    set_name : str
        Name of the set.
    idx : int, long, list
        Index number of the field. If it is a list, returns the data
        for all the value indexes of that list
    is_value : bool
       Outputs a tensor of indexes (if false)
       or a table of tensors/values (if true).
       (optional, default=false)

    Returns:
    --------
    table
        Returns a table of indexes (or values, i.e. tensors, if is_value=True).

    Raises
    ------
        None
]]
    assert(set_name, 'Must input a valid set name')
    assert(idx, 'Must input a valid index')
    assert(idx>0, ('Must input a valid index range: %d (>0)'):format(idx))

    local is_value = is_value or false

    local set_path = ('%s/%s/'):format(self.root_path,set_name)

    local indexes = self:get(set_name, 'object_ids', idx)
    if is_value then
        local out = {}
        for i=1, indexes:size(1) do
            local data = {}
            for k, field in ipairs(self.object_fields[set_name]) do
                if indexes[i][k] > 0 then
                    table.insert(data, self:get(set_name, field, indexes[i][k]))
                else
                    table.insert(data, {})
                end
            end
            table.insert(out, data)
        end
        return out
    else
        return indexes
    end
end

------------------------------------------------------------------------------------------------------------

function DataLoader:size(set_name, field_name)
--[[
    Size of a field.

    Returns the number of the elements of a field_name.

    Parameters
    ----------
    set_name : str
        Name of the set.
    field_name : str
        Name of the data field.
        (optional, default='object_ids')

    Returns:
    --------
    table
        Returns the the size of the object list.

    Raises
    ------
        None
]]
    assert(set_name, ('Must input a valid set name: %s'):format(set_name))

    local field_name = field_name or 'object_ids'
    local field_path = ('%s/%s/%s'):format(self.root_path, set_name, field_name)
    local data = self.file:read(field_path)
    return data:dataspaceSize()
end

------------------------------------------------------------------------------------------------------------

function DataLoader:list(set_name)
--[[
    Lists all fields' names.

    Parameters
    ----------
    set_name : str
        Name of the set.

    Returns
    -------
    table
        List of all data fields names of the dataset.

    Raises
    ------
        None
]]
    assert(set_name, ('Must input a valid set name: %s'):format(set_name))

    local set_path = ('%s/%s'):format(self.root_path, set_name)
    local data = self.file:read(set_path)
    local list_fields = {}
    for k, _ in pairs(data._children) do
        table.insert(list_fields, k)
    end
    return list_fields
end

------------------------------------------------------------------------------------------------------------

function DataLoader:object_field_id(set_name, field_name)
--[[
    Retrieves the index position of a field in the 'object_ids' list.

    Parameters
    ----------
    set_name : str
        Name of the set.
    field_name : str
        Name of the data field.

    Returns
    -------
    number
        Index of the field_name on the list.

    Raises
    ------
    error
        If field_name does not exist on the 'object_fields' list.
]]
    assert(set_name, ('Must input a valid set name: %s'):format(set_name))
    assert(field_name, ('Must input a valid field_name name: %s'):format(field_name))

    for k, field in pairs(self.object_fields[set_name]) do
        if string.match(field_name, field) then
            return k
        end
    end
    error(('Field name \'%s\' does not exist.'):format(field_name))
end