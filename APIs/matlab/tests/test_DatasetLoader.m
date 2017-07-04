function test_suite=test_DatasetLoader
    % Test dbcollection's dataset loader API

    try % assignment of 'localfunctions' is necessary in Matlab >= 2016
        test_functions=localfunctions();
    catch % no problem; early Matlab versions can use initTestSuite fine
    end
    initTestSuite;

function [loader, utils] = setup_ini()
    name = 'mnist';
    task = 'classification';
    data_dir = [getenv('HOME') '/dbcollection/mnist/data'];
    cache_path = [getenv('HOME') '/dbcollection/mnist/classification.h5'];

    % initialize object
    loader = dbcollection_DatasetLoader(name, task, data_dir, cache_path);
    utils = dbcollection_utils();

function test_get
    sample_classes = ['0'; '1'; '2'; '3'; '4'; '5'; '6'; '7'; '8'; '9'];

    % setup data loader + utils class
    [loader, utils] = setup_ini();

    % call get() method
    data = loader.get('train', 'classes');
    % convert double to char
    classes = utils.string_ascii.convert_ascii_to_str(data);

    assertEqual(sample_classes, classes);

function test_object
    sample_ids = [0, 5];

    % setup data loader + utils class
    [loader, ~] = setup_ini();

    % call object() method
    ids = loader.object('train', 1);

    assertEqual(sample_ids, double(ids));  % int32 -> double

function test_size_1
    sample_ids = [10, 2];

    % setup data loader + utils class
    [loader, ~] = setup_ini();

    % call object() method
    cls_size = loader.size('train', 'classes');

    assertEqual(sample_ids, cls_size);

function test_size_2
    sample_ids = [60000, 2];

    % setup data loader + utils class
    [loader, ~] = setup_ini();

    % call object() method
    cls_size = loader.size('train');

    assertEqual(sample_ids, cls_size);

function test_list
    sample_field_names = {'classes', ...
                          'images', ...
                          'labels', ...
                          'list_images_per_class', ...
                          'object_fields', ...
                          'object_ids'};

    % setup data loader + utils class
    [loader, ~] = setup_ini();

    % call object() method
    field_names = loader.list('train');

    assertEqual(sample_field_names, field_names);

function test_object_field_id_1
    sample_idx = 1;

    % setup data loader + utils class
    [loader, ~] = setup_ini();

    % call object() method
    res = loader.object_field_id('train', 'images');

    assertEqual(sample_idx, res);

function test_object_field_id_2
    sample_idx = 2;

    % setup data loader + utils class
    [loader, ~] = setup_ini();

    % call object() method
    res = loader.object_field_id('train', 'labels');

    assertEqual(sample_idx, res);