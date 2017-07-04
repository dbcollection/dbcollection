function test_suite=test_utils
    % Test dbcollection util functions

    try % assignment of 'localfunctions' is necessary in Matlab >= 2016
        test_functions=localfunctions();
    catch % no problem; early Matlab versions can use initTestSuite fine
    end
    initTestSuite;


function test_pad_list
    % TODO
    assertTrue(true);

function test_unpad_list
    % TODO
    assertTrue(true)

function test_convert_str_to_ascii_single
    sample_str = 'test_string';
    sample_res = padarray(double(sample_str), [0 1], 0, 'post');
    utils = dbcollection_utils();
    res = utils.string_ascii.convert_str_to_ascii(sample_str);
    assertEqual(sample_res, res)

function test_convert_str_to_ascii_matrix
    sample_str = ['test_string'; 'string_test'];
    sample_res = padarray(double(sample_str), [0 1], 0, 'post');
    utils = dbcollection_utils();
    res = utils.string_ascii.convert_str_to_ascii(sample_str);
    assertEqual(sample_res, res)

function test_convert_str_to_ascii_cell
    sample_str = {'test_string'; 'string_test'};
    sample_res = padarray(double(char(sample_str)), [0 1], 0, 'post');
    utils = dbcollection_utils();
    res = utils.string_ascii.convert_str_to_ascii(sample_str);
    assertEqual(sample_res, res)

function test_convert_ascii_to_str_single
    sample_str = 'test_string';
    sample_ascii = padarray(double(char(sample_str)), [0 1], 0, 'post');
    utils = dbcollection_utils();
    res = utils.string_ascii.convert_ascii_to_str(sample_ascii);
    assertEqual(sample_str, res)

function test_convert_ascii_to_str_matrix
    sample_str = ['test_string'; 'string_test'];
    sample_ascii = padarray(double(char(sample_str)), [0 1], 0, 'post');
    utils = dbcollection_utils();
    res = utils.string_ascii.convert_ascii_to_str(sample_ascii);
    assertEqual(sample_str, res)