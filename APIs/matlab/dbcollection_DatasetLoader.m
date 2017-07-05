classdef dbcollection_DatasetLoader
    % Dataset loader (HDF5 data loading) class
    %
    % dbcollection_DatasetLoader.m is an API for loading and
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
            loader.object_fields = struct();
            for i=1:1:size(hinfo.GroupHierarchy.Groups, 2)
                if isequal(hinfo.GroupHierarchy.Groups(1,i).Name, loader.root_path)
                    for j=1:1:size(hinfo.GroupHierarchy.Groups(1,i).Groups, 2)
                        set_name_path = hinfo.GroupHierarchy.Groups(1,i).Groups(1,j).Name;
                        [~,set_name,~] = fileparts(set_name_path);

                        % add set to a cell
                        loader.sets{j} = set_name;

                        % fetch list of field names that compose the object list.
                        data = h5read(cache_path, [set_name_path '/object_fields'])';
                        loader.object_fields.(set_name) = convert_ascii_to_string(data);
                    end
                end
            end
        end

        function out = get(obj, set_name, field_name, idx)
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
            % idx : number/array or numbers
            %     Index number of the field. If the input is a table, it uses it as a range
            %     of indexes and returns the data for that range.
            %     (optional, default=[])
            %
            % Returns
            % -------
            % Double array
            %     Value/list of a field from the metadata cache file.
            %
            % Raises
            % ------
            %     None

            assert(~(~exist('set_name', 'var') || isempty(set_name)), 'Missing input arg: set_name')
            assert(~(~exist('field_name', 'var') || isempty(field_name)), 'Missing input arg: field_name')

            if ~exist('idx', 'var') || isempty(idx)
                idx = [];
            end

            % read data from file
            h5_path = sprintf('%s/%s/%s', obj.root_path, set_name,field_name);
            data = h5read(obj.cache_path, h5_path);

            % reshape the matrix to the correct shape
            data = flipH_array(data);

            % slice data
            if ~isempty(idx)
                out = slice_(data, idx, 1);
            else
                out = data;
            end
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
            %    (optional, default=false)
            %
            % Returns:
            % --------
            % cell
            %     Returns a list of indexes (or values, i.e. tensors, if is_value=True).
            %
            % Raises
            % ------
            %     None

            assert(~(~exist('set_name', 'var') || isempty(set_name)), 'Missing input arg: set_name')
            if ~exist('idx', 'var') || isempty(idx)
                idx = [];
            end
            if ~exist('is_value', 'var') || isempty(is_value)
                is_value = false;
            end

            indexes = get(obj, set_name, 'object_ids', idx);
            if is_value
                idx_size = size(indexes,2);
                field_names = obj.object_fields.(set_name);
                out = cell(1, idx_size);
                for i=1:1:idx_size
                    newdata = cell(1, size(field_names,2));
                    for k=1:1:size(field_names,2)
                        if indexes(i,k) > 0
                            newdata{k} = get(obj, set_name, field_names(k), indexes(i,k));
                        else
                            newdata{k} = [];
                        end
                    end
                    out{i} = newdata;
                end
            else
                out = indexes;
            end
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
            %     (optional, default='object_ids')
            %
            % Returns:
            % --------
            % Double Array
            %     Returns the the size of the field.
            %
            % Raises
            % ------
            %     None

            assert(~(~exist('set_name', 'var') || isempty(set_name)), 'Missing input arg: set_name')
            if ~exist('field_name', 'var') || isempty(field_name)
                field_name = 'object_ids';
            end

            h5_path = sprintf('%s/%s/%s', obj.root_path, set_name, field_name);
            info = h5info(obj.cache_path, h5_path);
            size = flipH_array(info.Dataspace.Size);
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

            assert(~(~exist('set_name', 'var') || isempty(set_name)), 'Missing input arg: set_name')

            hinfo = hdf5info(obj.cache_path);

            %% converter cell para struct
            for i=1:1:size(hinfo.GroupHierarchy.Groups, 2)
                if isequal(hinfo.GroupHierarchy.Groups(1,i).Name, obj.root_path)
                    for j=1:1:size(hinfo.GroupHierarchy.Groups(1,i).Groups, 2)
                        if strcmp(hinfo.GroupHierarchy.Groups(1,i).Groups(1,j).Name, [obj.root_path '/' set_name])
                            num_fields = size(hinfo.GroupHierarchy.Groups(1,i).Groups(1,j).Datasets, 2);
                            out = cell(1, num_fields);
                            for s=1:1:num_fields
                                [~,field_name,~] = fileparts(hinfo.GroupHierarchy.Groups(1,i).Groups(1,j).Datasets(1,s).Name);
                                out{s} = field_name;
                            end
                            return
                        end
                    end
                end
            end
        end

        function idx = object_field_id(obj, set_name, field_name)
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

            assert(~(~exist('set_name', 'var') || isempty(set_name)), 'Missing input arg: set_name')
            assert(~(~exist('field_name', 'var') || isempty(field_name)), 'Missing input arg: field_name')

            f = obj.object_fields.(set_name);
            for i=1:1:size(f, 1)
                field = f(i,:);
                if strcmp(field_name, field)
                    idx = i;
                    return
                end
            end
            error('Field name ''%s'' does not exist.', field_name)
        end
    end

end


% -------------------------- Utility functions --------------------------

function str = convert_ascii_to_string(array)
    utils = dbcollection_utils();
    str = utils.string_ascii.convert_ascii_to_str(array);
end


function out = slice_(A, ix, dim)
    subses = repmat({':'}, [1 ndims(A)]);
    subses{dim} = ix;
    out = A(subses{:});
end


function out = flipH_array(array)
    % Permute the array's dimensions
    % (centered around the array/matrix dimension)
    num_dims = ndims(array);
    if num_dims == 2 && size(array, 1) == 1
        out = flip(array);
    else
        out = permute(array, (ndims(array):-1:1));
    end
end