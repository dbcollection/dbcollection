classdef dbcollection_DatasetLoader
    % Dataset loader (HDF5 data loading) class
    %
    % dbcollection_DatasetLoader.m is a API for loading and
    % managing metadata of a parsed dataset on
    % disk in the HDF5 format. It contains information
    % about the dataset (name, task, dir_path,
    % cache_path)and simple methods for retrieving
    % data from disk.
    %
    % The following API function are defined:
    %   get             - Retrieve data from the dataset's
    %                     hdf5 metadata file.
    %   object          - Retrieves a list of all fields'
    %                     indexes/values of an object
    %                     composition.
    %   size            - Returns the size of a field.
    %   list            - Lists all fields' names.
    %   object_field_id - Retrieves the index position
    %                     of a field in the 'object_ids'
    %                     list
    %
    % For more information about the methods, check out
    % the dbcollection package documentation.


    properties
        name            % Name of the dataset
        task            % Name of the task
        data_dir        % Path of the data's files
        cache_path      % Filepath to the HDF5 file
        file            % Handler for the HDF5 file
        root_path       % HDF5 default group path
        sets            % Names of the dataset splits (e.g. train/val/test/etc.)
        object_fields   % List of field names per set
    end

    methods
        function loader = dbcollection_DatasetLoader(name, task, data_dir, cache_path)
            % dbcollection's data loading API class initialization.
            %
            % Parameters
            % ----------
            % name : str
            %     Name of the dataset.
            % task : str
            %     Name of the task.
            % data_dir : str
            %     Path of the dataset's data directory on disk.
            % cache_path : str
            %     Path of the metadata cache file stored on disk.

            assert(~(~exist('name', 'var') || isempty(name)), 'Missing input arg: name')
            assert(~(~exist('task', 'var') || isempty(task)), 'Missing input arg: task')
            assert(~(~exist('data_dir', 'var') || isempty(data_dir)), 'Missing input arg: data_dir')
            assert(~(~exist('cache_path', 'var') || isempty(cache_path)), 'Missing input arg: cache_path')
            
            % store information of the dataset
            loader.name = name;
            loader.task = task;
            loader.data_dir = data_dir;
            loader.cache_path = cache_path;
            
            hinfo = hdf5info(cache_path);

            loader.root_path = '/default';
            loader.sets = {};
            loader.object_fields = {};
                     
            for i=1:1:size(hinfo.GroupHierarchy.Groups, 2)
                if isequal(hinfo.GroupHierarchy.Groups(1,i),loader.root_path)
                    for j=1:1:size(hinfo.GroupHierarchy.Groups(1,i).Groups, 2)
                        loader.sets{j} = {hinfo.GroupHierarchy.Groups(1,i).Groups(1,j).Name};                       
                        num_fields = size(hinfo.GroupHierarchy.Groups(1,i).Groups(1,j).Datasets, 2);
                        field_names = cell(1, num_fields);
                        for s=1:1:num_fields
                            [~,field_name,~] = fileparts(hinfo.GroupHierarchy.Groups(1,i).Groups(1,j).Datasets(1,s).Name);                           
                            field_names{s} = field_name;
                        end                        
                    end
                    loader.object_fields{j} = field_names;                    
                end
            end
        end

        function out = get (obj, set_name, field_name, idx)
            % Retrieve data from the dataset's hdf5 metadata file.
            %
            % Retrieve the i'th data from the field 'field_name'.
            %
            % Parameters
            % ----------
            % set_name : string
            %     Name of the set.
            % field_name : string
            %    Name of the data field.
            % idx : number/table
            %     Index number of the field. If the input is a table, it uses it as a range
            %     of indexes and returns the data for that range.
            %
            % Returns
            % -------
            % Double array
            %     Value/list of a field from the metadata cache file.
            %
            % Raises
            % ------
            %     None

            %% TODO
        end

        function out = object(obj, set_name, idx, is_value)
            % Retrieves a list of all fields' indexes/values of an object composition.
            %
            % Retrieves the data's ids or contents of all fields of an object.
            % It works by calling :get() for each field individually and grouping
            % them into a list.
            %
            % Parameters
            % ----------
            % set_name : str
            %     Name of the set.
            % idx : int, long, list
            %     Index number of the field. If it is a list, returns the data
            %     for all the value indexes of that list
            % is_value : bool
            %    Outputs a tensor of indexes (if false)
            %    or a table of tensors/values (if true).
            %
            % Returns:
            % --------
            % table
            %     Returns a table of indexes (or values, i.e. tensors, if is_value=True).
            %
            % Raises
            % ------
            %     None

            %% TODO
        end

        function size = size(obj, set_name, field_name)
            % Size of a field.
            %
            % Returns the number of the elements of a field_name.
            %
            % Parameters
            % ----------
            % set_name : str
            %     Name of the set.
            % field_name : str
            %     Name of the data field.
            %
            % Returns:
            % --------
            % table
            %     Returns the the size of the object list.
            %
            % Raises
            % ------
            %     None

            %% TODO
        end

        function out = list(obj, set_name)
            % Lists all fields names.
            %
            % Parameters
            % ----------
            % set_name : str
            %     Name of the set.
            %
            % Returns
            % -------
            % table
            %     List of all data fields names of the dataset.
            %
            % Raises
            % ------
            %     None

            %% TODO
        end

        function out = object_field_id(obj, set_name, field_name)
            % Retrieves the index position of a field in the 'object_ids' list.
            %
            % Parameters
            % ----------
            % set_name : str
            %     Name of the set.
            % field_name : str
            %     Name of the data field.
            %
            % Returns
            % -------
            % number
            %     Index of the field_name on the list.
            %
            % Raises
            % ------
            % error
            %     If field_name does not exist on the 'object_fields' list.

            %% TODO
        end
    end

end