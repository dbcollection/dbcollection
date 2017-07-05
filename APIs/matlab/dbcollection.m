classdef dbcollection
    % dbcollection wrapper for Matlab.
    %
    % dbcollection.m is an API for loading/managing
    % datasets. It contains simple methods for loading,
    % downloading, processing, configurating and listing
    % datasets from a varied list of available datasets.
    % Also, it contains useful utility methods like ASCII
    % to string conversions at the disposal of the user.
    %
    % This code follows closely the main package
    % written in Python. For more information, please
    % check out the DOCUMENTATION.md file.
    %
    % The following API function are defined:
    %   load          - Returns a data loader of a dataset.
    %   download      - Download a dataset data to disk.
    %   process       - Process a dataset's metadata and stores it to file.
    %   add           - Add a dataset/task to the list of available datasets for loading.
    %   remove        - Remove/delete a dataset from the cache.
    %   config_cache  - Configure the cache file.
    %   query         - Do simple queries to the cache.
    %   info          - Prints the cache contents.
    %
    % For more information about the methods, check out
    % the dbcollection package documentation.

    properties
        utils
    end

    methods
        function obj = dbcollection()
            obj.utils = dbcollection_utils;
        end

        function loader = load(obj, varargin)
            % Returns a data loader of a dataset.
            %
            % Returns a loader with the necessary functions to manage the selected dataset.
            %
            % Parameters
            % ----------
            % name : str
            %     Name of the dataset.
            % task : str
            %     Name of the task to load.
            %     (optional, default='default')
            % data_dir : str
            %     Directory path to store the downloaded data.
            %     (optional, default='')
            % verbose : bool
            %     Displays text information (if true).
            %     (optional, default=true)
            % is_test : bool
            %     Flag used for tests.
            %     (optional, default=false)
            %
            % Returns
            % -------
            % dbcollection_DatasetLoader
            %     Data loader class.

            % default options
            config = struct('name', 'REQUIRED', ...
                            'task', 'default', ...
                            'data_dir', '', ...
                            'verbose', true, ...
                            'is_test', false);

            % parse input options
            opt = parse_options(varargin, config);

            % cache file name + path in disk
            home_path = get_cache_file_path(opt.is_test);

            % check if the .json cache has been initialized
            if exist(home_path, 'file') ~= 2
                config_cache(obj, [], [], [], [], [], [], opt.is_test);  % creates the cache file on disk if it doesn't exist
            end

            % read the cache file (dbcollection.json)
            cache = loadjson(home_path);

            % check if the dataset exists in the cache
            if ~isfield(cache.dataset, 'name')
                download(obj, opt.name, opt.data_dir, true, opt.verbose, opt.is_test)
                cache = loadjson(home_path);  % reload the cache file
            end

            % check if the task exists in the cache
            if ~exists_task(cache, opt.name, opt.task)
                process(obj, opt.name, opt.task, opt.verbose, opt.is_test)
                cache = loadjson(home_path);  % reload the cache file
            end

            % load check if task exists
            if ~exists_task(cache, opt.name, opt.task)
                error('Dataset name/task not available in cache for load.')
            end

            % get dataset paths (data + cache)
            [data_dir, cache_path] = get_dataset_paths(cache, opt.name, opt.task);

            % Get dataset loader
            loader = dbcollection_DatasetLoader(opt.name, opt.task, data_dir, cache_path);
        end

        function download(obj, varargin)
            % Download a dataset data to disk.
            %
            % This method will download a dataset's data files to disk. After download,
            % it updates the cache file with the  dataset's name and path where the data
            % is stored.
            %
            % Parameters
            % ----------
            % name : str
            %     Name of the dataset.
            % data_dir : str
            %     Directory path to store the downloaded data.
            %     (optional, default='None')
            % extract_data : bool
            %     Extracts/unpacks the data files (if true).
            %     (optional, default=true)
            % verbose : bool
            %     Displays text information (if true).
            %     (optional, default=true)
            % is_test : bool
            %     Flag used for tests.
            %     (optional, default=false)
            %
            % Returns
            % -------
            %     None

            % default options
            config = struct('name', 'REQUIRED', ...
                            'data_dir', 'None', ...
                            'extract_data', true, ...
                            'verbose', true, ...
                            'is_test', false);

            % parse input options
            opt = parse_options(varargin, config);

            command = sprintf(strcat('import dbcollection.manager as dbc;', ...
                              'dbc.download(name=''%s'',data_dir=''%s'',extract_data=%s,verbose=%s,is_test=%s)'), ...
                              opt.name, opt.data_dir, ...
                              logical2str(opt.extract_data), ...
                              logical2str(opt.verbose), ...
                              logical2str(opt.is_test));

            run_command(command);
        end

        function process(obj, varargin)
            % Process a dataset's metadata and stores it to file.
            %
            % The data is stored in a HDF5 file for each task composing the dataset's tasks.
            %
            % Parameters
            % ----------
            % name : str
            %     Name of the dataset.
            % task : str
            %     Name of the task to process.
            %     (optional, default='all')
            % verbose : bool
            %     Displays text information (if true).
            %     (optional, default=true)
            % is_test : bool
            %     Flag used for tests.
            %     (optional, default=false)
            %
            % Returns
            % -------
            %     None

            % default options
            config = struct('name', 'REQUIRED', ...
                            'task', 'all', ...
                            'verbose', true, ...
                            'is_test', false);

            % parse input options
            opt = parse_options(varargin, config);

            command = sprintf(strcat('import dbcollection.manager as dbc;', ...
                              'dbc.process(name=''%s'',task=''%s'',verbose=%s,is_test=%s)'), ...
                              opt.name, opt.task, ...
                              logical2str(opt.verbose), ...
                              logical2str(opt.is_test));

            run_command(command);
        end

        function add(obj, varargin)
            % Add a dataset/task to the list of available datasets for loading.
            %
            % Parameters
            % ----------
            % name : str
            %     Name of the dataset.
            % task : str
            %     Name of the task to load.
            % data_dir : str
            %     Path of the stored data on disk.
            % file_path : str
            %     Path to the metadata HDF5 file.
            % keywords : list
            %     List of strings of keywords that categorize the dataset.
            %     (optional, default={})
            % is_test : bool
            %     Flag used for tests.
            %     (optional, default=false)
            %
            % Returns
            % -------
            %     None

            % default options
            config = struct('name', 'REQUIRED', ...
                            'task', 'REQUIRED', ...
                            'data_dir', 'REQUIRED', ...
                            'file_path', 'REQUIRED', ...
                            'keywords', '[]', ...
                            'is_test', false);

            % parse input options
            opt = parse_options(varargin, config);

            if ~isempty(opt.keywords)
                if ischar(opt.keywords)
                    opt.keywords = sprintf('[''%s'']', opt.keywords);
                elseif iscell(opt.keywords)
                    tmp_str = '';
                    for i=1:1:size(opt.keywords,2)
                        tmp_str = strcat(tmp_str, ['' opt.keywords{i} '']);
                        if i < size(opt.keywords,2)
                            tmp_str = strcat(tmp_str, ',');
                        end
                    end
                    opt.keywords = sprintf('[%s]', tmp_str);
                else
                    error('keywords input must be either a string or a cell of strings')
                end
            else
                opt.keywords = '[]';
            end

            command = sprintf(strcat('import dbcollection.manager as dbc;', ...
                              'dbc.add(name=''%s'',task=''%s'',data_dir=''%s'',', ...
                              'file_path=''%s'',keywords=%s,is_test=%s)'), ...
                              opt.name, opt.task, opt.data_dir, opt.file_path, opt.keywords, ...
                              logical2str(opt.is_test));

            run_command(command);
        end

        function remove(obj, varargin)
            % Remove/delete a dataset from the cache.
            %
            % Removes the datasets cache information from the dbcollection.json file.
            % The dataset's data files remain on disk if 'delete_data' is set to False,
            % otherwise it removes also the data files.
            %
            % Parameters
            % ----------
            % name : str
            %     Name of the dataset to delete.
            % task : str
            %     Name of the task to delete.
            %     (optional, default='None')
            % delete_data : bool
            %     Delete all data files from disk for this dataset if True.
            %     (optional, default=false)
            % is_test : bool
            %     Flag used for tests.
            %     (optional, default=false)
            %
            % Returns
            % -------
            %     None

            % default options
            config = struct('name', 'REQUIRED', ...
                            'task', 'None', ...
                            'delete_data', false, ...
                            'is_test', false);

            % parse input options
            opt = parse_options(varargin, config);

            command = sprintf(strcat('import dbcollection.manager as dbc;', ...
                              'dbc.remove(name=''%s'',task=%s,delete_data=%s,is_test=%s)'), ...
                              opt.name, opt.task, ...
                              logical2str(opt.delete_data), ...
                              logical2str(opt.is_test));

            run_command(command);
        end

        function config_cache(obj, varargin)
            % Configure the cache file.
            %
            % This method allows to configure the cache file directly by selecting
            % any data field/value. The user can also manually configure the file
            % if he/she desires.
            %
            % To modify any entry in the cache file, simply input the field name
            % you want to change along with the new data you want to insert. This
            % applies to any field/data in the file.
            %
            % Another thing available is to reset/clear the entire cache paths/configs
            % from the file by simply enabling the 'reset_cache' flag to true.
            %
            % Also, there is an option to completely remove the cache file+folder
            % from the disk by enabling 'delete_cache' to true. This will remove the
            % cache dbcollection.json and the dbcollection/ folder from disk.
            %
            % Parameters
            % ----------
            % field : str
            %     Name of the field to update/modify in the cache file.
            %     (optional, default='None')
            % value : str, list, table
            %     Value to update the field.
            %     (optional, default='None')
            % delete_cache : bool
            %     Delete/remove the dbcollection cache file + directory.
            %     (optional, default=false)
            % delete_cache_dir : bool
            %     Delete/remove the dbcollection cache directory.
            %     (optional, default=false)
            % delete_cache_file : bool
            %     Delete/remove the dbcollection.json cache file.
            %     (optional, default=false)
            % reset_cache : bool
            %     Reset the cache file.
            %     (optional, default=false)
            % is_test : bool
            %     Flag used for tests.
            %     (optional, default=false)
            %
            % Returns
            % -------
            %     None

            % default options
            config = struct('field', 'None', ...
                            'value', 'None', ...
                            'delete_cache', false, ...
                            'delete_cache_dir', false, ...
                            'delete_cache_file', false, ...
                            'reset_cache', false, ...
                            'is_test', false);

            % parse input options
            opt = parse_options(varargin, config);

            command = sprintf(strcat('import dbcollection.manager as dbc;', ...
                              'dbc.config_cache(field=''%s'',value=''%s'',delete_cache=%s, ', ...
                              'delete_cache_dir=%s,delete_cache_file=%s,reset_cache=%s, ', ...
                              'is_test=%s)'), ...
                              opt.field, opt.value, ...
                              logical2str(opt.delete_cache), ...
                              logical2str(opt.delete_cache_dir), ...
                              logical2str(opt.delete_cache_file), ...
                              logical2str(opt.reset_cache), ...
                              logical2str(opt.is_test));

            run_command(command);
        end

        function query(obj, varargin)
            % Do simple queries to the cache.
            %
            % list all available datasets for download/preprocess. (tenho que pensar melhor sobre este)
            %
            % Parameters:
            % -----------
            % pattern : str
            %     Field name used to search for a matching pattern in cache data.
            %     (optional, default='info')
            % is_test : bool
            %     Flag used for tests.
            %     (optional, default=false)
            %
            % Returns
            % -------
            %     None

            % default options
            config = struct('pattern', 'info', ...
                            'is_test', false);

            % parse input options
            opt = parse_options(varargin, config);

            command = sprintf(strcat('import dbcollection.manager as dbc;', ...
                              'print(dbc.query(pattern=''%s'',is_test=%s))'), ...
                              opt.pattern, logical2str(opt.is_test));

            run_command(command);
        end

        function info(obj, varargin)
            % Prints the cache contents.
            %
            % Prints the contents of the dbcollection.json cache file to the screen.
            %
            % Parameters
            % ----------
            % list_datasets : bool
            %     Print available datasets in the dbcollection package.
            %     (optional, default=false)
            % is_test : bool
            %     Flag used for tests.
            %     (optional, default=false)
            %
            % Returns
            % -------
            %     None

            % default options
            config = struct('list_datasets', false, ...
                            'is_test', false);

            % parse input options
            opt = parse_options(varargin, config);

            command = sprintf(strcat('import dbcollection.manager as dbc;', ...
                              'dbc.info(list_datasets=%s,is_test=%s)'), ...
                              logical2str(opt.list_datasets), ...
                              logical2str(opt.is_test));


            run_command(command);
        end
    end

end

% -------------------------- Utility functions --------------------------

function opt = parse_options(input, config)
    [num_req, names_req] = num_required_inputs(config);
    if isstruct(input{1})
        if size(fieldnames(input{1}), 1) < num_req
            error('Not enough input arguments were provided.')
        end
    else
        if size(input{1}, 2) < num_req
            error('Not enough input arguments were provided.')
        end
    end

    opt = config;

    if size(input, 2) > 0  % skip this if no inputs are available
        if size(input, 2) == 1 && isstruct(input{1})
            % copy struct to another
            f = fieldnames(input{1});
            for i = 1:length(f)
                field = f{i};
                if isfield(opt, field)
                    opt.(field) = input{1}.(field);
                else
                    error('Invalid input argument: %s', field)
                end
            end
        else
            f = fieldnames(config);
            for i=1:1:size(input,2)
                if ~isempty(input{1, i})
                    opt.(f{i}) = input{1, i};
                end
            end
        end
    end

    % check if all required fields were filled
    for i=1:size(names_req,2)
        if strcmp(opt.(names_req{i}), 'REQUIRED')
            error('Missing required input argument: %s', names_req{i})
        end
    end
end


function [total, names] = num_required_inputs(input)
    f = fieldnames(input);
    total = 0;
    names = {};
    for i = 1:length(f)
        val = input.(f{i});
        if ischar(val)
            if strcmp(val, 'REQUIRED')
                total = total + 1;
                names{total} = f{i};
            end
        end
    end
end


function str = logical2str(bool)
    % Convert a boolean to a string
    assert(~(~exist('bool', 'var') || isempty(bool)), 'Missing input arg: bool')
    if bool
        str = 'True';
    else
        str = 'False';
    end
end


function path = get_cache_file_path(is_test)
    % get the home directory
    assert(~(~exist('is_test', 'var') || isempty(is_test)), 'Missing input arg: is_test')

    if ispc
        home_dir = [getenv('HOMEDRIVE') getenv('HOMEPATH')];
    else
        home_dir = getenv('HOME');
    end

    if is_test
        path = fullfile(home_dir, 'tmp', 'dbcollection.json');
    else
        path = fullfile(home_dir, 'dbcollection.json');
    end
end


function is_task = exists_task(cache, name, task)
    % check if the task exists in the cache

    dset = extractfield(cache.dataset, name);
    if isfield(dset{1}, 'tasks')
        tasks = extractfield(dset{1}, 'tasks');
        if ~isempty(tasks)
            if isfield(tasks{1}, task)
                is_task = true;
            else
                is_task = false;
            end
        else
            is_task = false;
        end
    else
        is_task = false;
    end
end


function [data_dir, cache_path] = get_dataset_paths(cache, name, task)
    % get the dataset's data and cache paths
    dset = extractfield(cache.dataset, name);
    data_dir = extractfield(dset{1}, 'data_dir');
    data_dir = data_dir{1};
    tasks = extractfield(dset{1}, 'tasks');
    cache_path = extractfield(tasks{1}, task);
    cache_path = cache_path{1};
end


function [status,cmdout] = run_command(command)
    assert(~(~exist('command', 'var') || isempty(command)), 'Missing input arg: command')
    [status,cmdout] = system(sprintf('python -c "%s"', command),'-echo');
end