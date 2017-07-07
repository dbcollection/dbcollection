echo 'Run tests: manager API'
th $PWD/APIs/lua/tests/test_manager.lua

echo 'Run tests: loader API'
th $PWD/APIs/lua/tests/test_loader.lua

echo 'Run tests: string_ascii'
th $PWD/APIs/lua/tests/test_string_ascii.lua