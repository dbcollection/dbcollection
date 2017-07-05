function test_suite=test_dbcollection
    % Test dbcollection API

    try % assignment of 'localfunctions' is necessary in Matlab >= 2016
        test_functions=localfunctions();
    catch % no problem; early Matlab versions can use initTestSuite fine
    end
    initTestSuite;

function info = fetch_minst_info()
    info = struct();
    info.name = 'mnist';
    info.task = 'classification';
    info.data_dir = [getenv('HOME') '/tmp/download_data'];
    info.is_test = true;

function test_load_mnist_1
    dbc = dbcollection();
    info = fetch_minst_info();
    loader = dbc.load(info);
    assertEqual(info.name, loader.name)
    assertEqual(info.task, loader.task)
    assertEqual([info.data_dir '/mnist'], loader.data_dir)

function test_load_mnist_2
    dbc = dbcollection();
    info = fetch_minst_info();
    loader = dbc.load(info.name, ...
                      info.task, ...
                      info.data_dir, ...
                      true, ...
                      info.is_test);
    assertEqual(info.name, loader.name)
    assertEqual(info.task, loader.task)
    assertEqual([info.data_dir '/mnist'], loader.data_dir)    

function test_download_mnist
    dbc = dbcollection();
    info = fetch_minst_info();
    info = rmfield(info,'task');
    dbc.download(info);
    assertTrue(true);

function test_process_mnist
    dbc = dbcollection();
    info = fetch_minst_info();
    info = rmfield(info,'data_dir');
    dbc.process(info);
    assertTrue(true);

function test_add_dataset
    dbc = dbcollection();
    new_info = struct('name', 'newdataset', ...
                      'task', 'newtask', ...
                      'data_dir', 'new/data/dir', ...
                      'file_path', 'file/path/disk.h5', ...
                      'keywords', {'new_kw'}, ...
                      'is_test', true);
    dbc.add(new_info);
    assertTrue(true);

function test_remove_dataset
    dbc = dbcollection();
    opts = struct('name', 'newdataset', ...
                  'is_test', true);
    dbc.remove(opts);
    assertTrue(true);

function test_config_cache
    dbc = dbcollection();
    opts = struct('delete_cache', true, ...
                  'is_test', true);
    dbc.config_cache(opts);
    assertTrue(true);

function test_query_cache
    dbc = dbcollection();
    opts = struct('pattern', 'mnist', ...
                  'is_test', true);
    dbc.query(opts);
    assertTrue(true);

function test_info_print_cache_contents
    dbc = dbcollection();
    dbc.info(struct('is_test', true))
    assertTrue(true);