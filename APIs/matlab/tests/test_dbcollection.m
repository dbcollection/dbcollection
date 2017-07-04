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

function test_load_mnist
    dbc = dbcollection();
    info = fetch_minst_info();
    loader = dbc.load(info);
    assertEqual(info.name, loader.name)
    assertEqual(info.task, loader.task)
    assertEqual(info.data_dir, loader.data_dir)

function test_download_mnist
    % TODO
    dbc = dbcollection();
    assertTrue(true);

function test_process_mnist
    % TODO
    dbc = dbcollection();
    assertTrue(true);

function test_add_dataset
    % TODO
    dbc = dbcollection();
    assertTrue(true);

function test_remove_dataset
    % TODO
    dbc = dbcollection();
    assertTrue(true);

function test_config_cache
    % TODO
    dbc = dbcollection();
    assertTrue(true);

function test_query_cache
    % TODO
    dbc = dbcollection();
    assertTrue(true);

function test_info_print_cache_contents
    dbc = dbcollection();
    dbc.info(struct('is_test', true))
    assertTrue(true);