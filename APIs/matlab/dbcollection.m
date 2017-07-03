classdef dbcollection
    % dbcollection wrapper for Matlab.

    properties
        utils
    end

    methods
        function obj = dbcollection()
            obj.utils = dbcollection_utils;
        end

        function loader = load(obj, name, task, data_dir, verbose, is_test)
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
            % data_dir : str
            %     Directory path to store the downloaded data.
            % verbose : bool
            %     Displays text information (if true).
            % is_test : bool
            %     Flag used for tests.
            %
            % Returns
            % -------
            % dbcollection_DatasetLoader
            %     Data loader class.

            assert(~(~exist('name', 'var') || isempty(name)), 'Missing input arg: name')
            
        end

        function download(obj, options)
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
            % extract_data : bool
            %     Extracts/unpacks the data files (if true).
            % verbose : bool
            %     Displays text information (if true).
            % is_test : bool
            %     Flag used for tests.
            %
            % Returns
            % -------
            %     None

            %% TODO
        end

        function process(obj, options)
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
            % verbose : bool
            %     Displays text information (if true).
            % is_test : bool
            %     Flag used for tests.
            %
            % Returns
            % -------
            %     None

            %% TODO
        end

        function add(obj, options)
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
            % keywords : table
            %     Table of strings of keywords that categorize the dataset.
            % is_test : bool
            %     Flag used for tests.
            %
            % Returns
            % -------
            %     None

            %% TODO
        end

        function remove(obj, options)
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
            % delete_data : bool
            %     Delete all data files from disk for this dataset if True.
            % is_test : bool
            %     Flag used for tests.
            %
            % Returns
            % -------
            %     None

            %% TODO
        end

        function config_cache(obj, options)
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
            % value : str, list, table
            %     Value to update the field.
            % delete_cache : bool
            %     Delete/remove the dbcollection cache file + directory.
            % delete_cache_dir : bool
            %     Delete/remove the dbcollection cache directory.
            % delete_cache_file : bool
            %     Delete/remove the dbcollection.json cache file.
            % reset_cache : bool
            %     Reset the cache file.
            % is_test : bool
            %     Flag used for tests.
            %
            % Returns
            % -------
            %     None

            %% TODO
        end

        function query(obj, options)
            % Do simple queries to the cache.
            %
            % list all available datasets for download/preprocess. (tenho que pensar melhor sobre este)
            %
            % Parameters:
            % -----------
            % pattern : str
            %     Field name used to search for a matching pattern in cache data.
            % is_test : bool
            %     Flag used for tests.
            %
            % Returns
            % -------
            %     None

            %% TODO
        end

        function info(obj, options)
            % Prints the cache contents.
            %
            % Prints the contents of the dbcollection.json cache file to the screen.
            %
            % Parameters
            % ----------
            % list_datasets : bool
            %     Print available datasets in the dbcollection package.
            % is_test : bool
            %     Flag used for tests.
            %
            % Returns
            % -------
            %     None

            %% TODO
        end
    end

end
