--[[
    dbcollection managing functions.
--]]

require 'paths'
local dbcollection = require 'dbcollection.env'
require 'dbcollection.loader'

local argcheck = require 'argcheck'
local doc = require 'argcheck.doc'
local json = require 'json'


-----------------------------------------------------------
-- utility functions
-----------------------------------------------------------

-- cache file path
local function get_cache_file_path(options)
    local home_dir = os.getenv('HOME')
    if options.is_test then
        return paths.concat(home_dir, 'tmp', 'dbcollection.json')
    else
        return paths.concat(home_dir, 'dbcollection.json')
    end
end


--[[ parse all booleans to strings in python format ]]
local function tostring_py(input)
    assert(type(input)=='boolean')
    if input then
        return 'True'
    else
        return 'False'
    end
end


--[[ convert to string if it does not match "None" ]]
local function tostring_none(input)
    if string.match(input, "None") then
        return input
    else
        return ('\'%s\''):format(input)
    end
end


--[[ get the dataset's data and cache paths ]]
local function get_dataset_paths(cache, name, task)
    local data_dir = cache['dataset'][name]['data_dir']
    local cache_path = cache['dataset'][name]['tasks'][task]
    return data_dir, cache_path
end


-- check if the task exists in the cache
local function exists_task(cache, name, task)
    if next(cache['dataset'][name]['tasks']) then
        if cache['dataset'][name]['tasks'][task] then
            return true
        else
            return false
        end
    else
        return false
    end
end


-----------------------------------------------------------
-- API functions
-----------------------------------------------------------

function dbcollection.load(options)
    local initcheck = argcheck{
        pack=true,
        help=[[
            Returns a data loader of a dataset.

            Returns a loader with the necessary functions to manage the selected dataset.

            Parameters
            ----------
            name : str
                Name of the dataset.
            task : str
                Name of the task to load.
                (optional, default='default')
            data_dir : str
                Directory path to store the downloaded data.
                (optional, default='')
            verbose : bool
                Displays text information (if true).
                (optional, default=true)
            is_test : bool
                Flag used for tests.
                (optional, default=false)

            Returns
            -------
            DatasetLoader
                Data loader class.

            Raises
            ------
                None
        ]],
        {name="name", type="string",
        help="Name of the dataset."},
        {name="task", type="string", default='default',
        help="Name of the task to load.",
        opt = true},
        {name="data_dir", type="string", default='',
        help="Path to store the data (if the data doesn't exist and the download flag is equal True).",
        opt = true},
        {name="verbose", type="boolean", default=true,
        help="Displays text information (if true).",
        opt = true},
        {name="is_test", type="boolean", default=false,
        help="Flag used for tests.",
        opt = true}
    }

    -- parse options
    local args = initcheck(options)

    local home_path = get_cache_file_path(args)

    -- check if the .json cache has been initialized
    if not paths.filep(home_path) then
        dbcollection.config_cache({is_test=args.is_test}) -- creates the cache file on disk if it doesn't exist
    end

    -- read the cache file (dbcollection.json)
    local cache = json.load(home_path)

    -- check if the dataset exists in the cache
    if not cache['dataset'][args.name] then
        dbcollection.download({name=args.name, data_dir=args.data_dir, extract_data=true,
                          verbose=args.verbose, is_test=args.is_test})
        cache = json.load(home_path) -- reload the cache file
    end

    -- check if the task exists in the cache
    if not exists_task(cache, args.name, args.task) then
        dbcollection.process({name=args.name, task=args.task, verbose=args.verbose,
                         is_test=args.is_test})
        cache = json.load(home_path) -- reload the cache file
    end

    -- load check if task exists
    if not cache['dataset'][args.name]["tasks"][args.task] then
        error('Dataset name/task not available in cache for load.')
    end

    -- get dataset paths (data + cache)
    local data_dir, cache_path = get_dataset_paths(cache, args.name, args.task)

    -- load HDF5 file
    local loader = dbcollection.DatasetLoader(args.name, args.task, data_dir, cache_path)

    return loader
end

------------------------------------------------------------------------------------------------------------

function dbcollection.download(options)
    local initcheck = argcheck{
        pack=true,
        help=[[
            Download a dataset data to disk.

            This method will download a dataset's data files to disk. After download,
            it updates the cache file with the  dataset's name and path where the data
            is stored.

            Parameters
            ----------
            name : str
                Name of the dataset.
            data_dir : str
                Directory path to store the downloaded data.
                (optional, default='None')
            extract_data : bool
                Extracts/unpacks the data files (if true).
                (optional, default=true)
            verbose : bool
                Displays text information (if true).
                (optional, default=true)
            is_test : bool
                Flag used for tests.
                (optional, default=false)

            Returns
            -------
                None

            Raises
            ------
                None
        ]],
        {name="name", type="string",
        help="Name of the dataset."},
        {name="data_dir", type="string", default='None',
        help="Path to store the data (if the data doesn't exist and the download flag is equal True).",
        opt = true},
        {name="extract_data", type="boolean", default=true,
        help="Extracts/unpacks the data files (if true).",
        opt = true},
        {name="verbose", type="boolean", default=true,
        help="Displays text information (if true).",
        opt = true},
        {name="is_test", type="boolean", default=false,
        help="Flag used for tests.",
        opt = true}
    }

    -- parse options
    local args = initcheck(options)

    assert(args.name, ('Must input a valid dataset name: %s'):format(args.name))

    local command = ('import dbcollection.manager as dbc;' ..
                    'dbc.download(name=\'%s\',data_dir=%s,extract_data=%s,verbose=%s,is_test=%s)')
                    :format(args.name, tostring_none(args.data_dir), tostring_py(args.extract_data),
                            tostring_py(args.verbose), tostring_py(args.is_test))

    os.execute(('python -c "%s"'):format(command))
end

------------------------------------------------------------------------------------------------------------

function dbcollection.process(options)
    local initcheck = argcheck{
        pack=true,
        help=[[
            Process a dataset's metadata and stores it to file.

            The data is stored in a HDF5 file for each task composing the dataset's tasks.

            Parameters
            ----------
            name : str
                Name of the dataset.
            task : str
                Name of the task to process.
                (optional, default='all')
            verbose : bool
                Displays text information (if true).
                (optional, default=true)
            is_test : bool
                Flag used for tests.
                (optional, default=false)

            Returns
            -------
                None

            Raises
            ------
                None
        ]],
        {name="name", type="string",
        help="Name of the dataset."},
        {name="task", type="string", default='all',
        help="Name of the dataset.",
        opt = true},
        {name="verbose", type="boolean", default=true,
        help="Displays text information (if true).",
        opt = true},
        {name="is_test", type="boolean", default=false,
        help="Flag used for tests.",
        opt = true}
    }

    -- parse options
    local args = initcheck(options)

    assert(args.name, ('Must input a valid dataset name: %s'):format(args.name))

    local command = ('import dbcollection.manager as dbc;' ..
                    'dbc.process(name=\'%s\',task=\'%s\',verbose=%s,is_test=%s)')
                    :format(args.name, args.task, tostring_py(args.verbose),
                            tostring_py(args.is_test))

    os.execute(('python -c "%s"'):format(command))
end

------------------------------------------------------------------------------------------------------------

function dbcollection.add(options)
    local initcheck = argcheck{
        pack=true,
        help=[[
            Add a dataset/task to the list of available datasets for loading.

            Parameters
            ----------
            name : str
                Name of the dataset.
            task : str
                Name of the task to load.
            data_dir : str
                Path of the stored data on disk.
            file_path : str
                Path to the metadata HDF5 file.
            keywords : table
                Table of strings of keywords that categorize the dataset.
                (optional, default={})
            is_test : bool
                Flag used for tests.
                (optional, default=false)

            Returns
            -------
                None

            Raises
            ------
                None
        ]],
        {name="name", type="string",
        help="Name of the dataset."},
        {name="task", type="string",
        help="Name of the task to load."},
        {name="data_dir", type="string",
        help="Path of the stored data on disk."},
        {name="file_path", type="string",
        help="Path to the metadata HDF5 file."},
        {name="keywords", type="table", default={},
        help="List of keywords to categorize the dataset.",
        opt = true},
        {name="is_test", type="boolean", default=false,
        help="Flag used for tests.",
        opt = true}
    }

    -- parse options
    local args = initcheck(options)

    assert(args.name, ('Must input a valid dataset name: %s'):format(args.name))
    assert(args.task, ('Must input a valid dataset name: %s'):format(args.task))
    assert(args.data_dir, ('Must input a valid dataset name: %s'):format(args.data_dir))
    assert(args.file_path, ('Must input a valid dataset name: %s'):format(args.file_path))

    -- parse the table into a string in python's format
    if next(args.keywords) then
        local str = ''
        for i=1, #args.keywords do
            str = str .. tostring(args.keywords[i])
            if i<=#args.keywords then str = str .. ',' end
        end
        args.keywords = ('[%s]'):format(str)
    else
        args.keywords = '[]'
    end

    local command = ('import dbcollection.manager as dbc;' ..
                    'dbc.add(name=\'%s\',task=\'%s\',data_dir=\'%s\',' ..
                    'file_path=\'%s\',keywords=%s,is_test=%s)')
                    :format(args.name, args.task, args.data_dir, args.file_path,
                            args.keywords, tostring_py(args.is_test))

    os.execute(('python -c "%s"'):format(command))
end

------------------------------------------------------------------------------------------------------------

function dbcollection.remove(options)
    local initcheck = argcheck{
        pack=true,
        help=[[
            Remove/delete a dataset from the cache.

            Removes the datasets cache information from the dbcollection.json file.
            The dataset's data files remain on disk if 'delete_data' is set to False,
            otherwise it removes also the data files.

            Parameters
            ----------
            name : str
                Name of the dataset to delete.
            delete_data : bool
                Delete all data files from disk for this dataset if True.
                (optional, default=false)
            is_test : bool
                Flag used for tests.
                (optional, default=false)

            Returns
            -------
                None

            Raises
            ------
                None
        ]],
        {name="name", type="string",
        help="Name of the dataset."},
        {name="delete_data", type="boolean", default=false,
        help="Delete all data files from disk for this dataset if True.",
        opt = true},
        {name="is_test", type="boolean", default=false,
        help="Flag used for tests.",
        opt = true}
    }

    -- parse options
    local args = initcheck(options)

    assert(args.name, ('Must input a valid dataset name: %s'):format(args.name))

    local command = ('import dbcollection.manager as dbc;' ..
                    'dbc.remove(name=\'%s\', delete_data=%s,is_test=%s)')
                    :format(args.name, tostring_py(args.delete_data), tostring_py(args.is_test))

    os.execute(('python -c "%s"'):format(command))
end

------------------------------------------------------------------------------------------------------------

function dbcollection.config_cache(options)
    local initcheck = argcheck{
        pack=true,
        help=[[
            Configure the cache file.

            This method allows to configure the cache file directly by selecting
            any data field/value. The user can also manually configure the file
            if he/she desires.

            To modify any entry in the cache file, simply input the field name
            you want to change along with the new data you want to insert. This
            applies to any field/data in the file.

            Another thing available is to reset/clear the entire cache paths/configs
            from the file by simply enabling the 'reset_cache' flag to true.

            Also, there is an option to completely remove the cache file+folder
            from the disk by enabling 'delete_cache' to true. This will remove the
            cache dbcollection.json and the dbcollection/ folder from disk.

            Parameters
            ----------
            field : str
                Name of the field to update/modify in the cache file.
                (optional, default='None')
            value : str, list, table
                Value to update the field.
                (optional, default='None')
            delete_cache : bool
                Delete/remove the dbcollection cache file + directory.
                (optional, default=false)
            delete_cache_dir : bool
                Delete/remove the dbcollection cache directory.
                (optional, default=false)
            delete_cache_file : bool
                Delete/remove the dbcollection.json cache file.
                (optional, default=false)
            reset_cache : bool
                Reset the cache file.
                (optional, default=false)
            is_test : bool
                Flag used for tests.
                (optional, default=false)

            Returns
            -------
                None

            Raises
            ------
                None
        ]],
        {name="field", type="string", default="None",
        help="Name of the field to update/modify in the cache file.",
        opt = true},
        {name="value", type="string", default="None",
        help="Value to update the field.",
        opt = true},
        {name="delete_cache", type="boolean", default=false,
        help="Delete/remove the dbcollection cache file + directory.",
        opt = true},
        {name="delete_cache_dir", type="boolean", default=false,
        help="Delete/remove the dbcollection cache directory.",
        opt = true},
        {name="delete_cache_file", type="boolean", default=false,
        help="Delete/remove the dbcollection.json cache file.",
        opt = true},
        {name="reset_cache", type="boolean", default=false,
        help="Reset the cache file.",
        opt = true},
        {name="is_test", type="boolean", default=false,
        help="Flag used for tests.",
        opt = true}
    }

    -- parse options
    local args = initcheck(options)

    local command = ('import dbcollection.manager as dbc;' ..
                    'dbc.config_cache(field=%s,value=%s,delete_cache=%s, ' ..
                    'delete_cache_dir=%s,delete_cache_file=%s,reset_cache=%s, ' ..
                    'is_test=%s)')
                    :format(tostring_none(args.field), tostring_none(args.value),
                            tostring_py(args.delete_cache), tostring_py(args.delete_cache_dir),
                            tostring_py(args.delete_cache_file), tostring_py(args.reset_cache),
                            tostring_py(args.is_test))

    os.execute(('python -c "%s"'):format(command))
end

------------------------------------------------------------------------------------------------------------

function dbcollection.query(options)
    local initcheck = argcheck{
        pack=true,
        help=[[
            Do simple queries to the cache.

            list all available datasets for download/preprocess. (tenho que pensar melhor sobre este)

            Parameters:
            -----------
            pattern : str
                Field name used to search for a matching pattern in cache data.
                (optional, default='info')
            is_test : bool
                Flag used for tests.
                (optional, default=false)

            Returns
            -------
                None

            Raises
            ------
                None
        ]],
        {name="pattern", type="string", default="info",
        help="Field name used to search for a matching pattern in cache data.",
        opt = true},
        {name="is_test", type="boolean", default=false,
        help="Flag used for tests.",
        opt = true}
    }

    -- parse options
    local args = initcheck(options)

    local command = ('import dbcollection.manager as dbc;' ..
                    'print(dbc.query(pattern=\'%s\',is_test=%s))')
                    :format(args.pattern, tostring_py(args.is_test))

    os.execute(('python -c "%s"'):format(command))
end

------------------------------------------------------------------------------------------------------------

function dbcollection.info(options)
    local initcheck = argcheck{
        pack=true,
        help=[[
            Prints the cache contents.

            Prints the contents of the dbcollection.json cache file to the screen.

            Parameters
            ----------
            list_datasets : bool
                Print available datasets in the dbcollection package.
                (optional, default=false)
            is_test : bool
                Flag used for tests.
                (optional, default=false)

            Returns
            -------
                None

            Raises
            ------
                None
        ]],
        {name="list_datasets", type="boolean", default=false,
        help="Print available datasets in the dbcollection package.",
        opt = true},
        {name="is_test", type="boolean", default=false,
        help="Flag used for tests.",
        opt = true},
        {name="t", type="boolean", default=false, -- without this it gives an error
        help="Flag used for tests.",
        opt = true}
    }

    -- parse options
    local args = initcheck(options)

    local command = ('import dbcollection.manager as dbc;' ..
                    'dbc.info(list_datasets=%s,is_test=%s)')
                    :format(tostring_py(args.list_datasets),
                            tostring_py(args.is_test or false))

    os.execute(('python -c "%s"'):format(command))
end