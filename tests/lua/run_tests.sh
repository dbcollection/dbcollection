echo 'Run tests: manager API'
th $PWD/tests/APIs/lua/test_manager.lua

echo 'Run tests: loader API'
th $PWD/tests/APIs/lua/test_loader.lua

echo 'Run tests: string_ascii'
th $PWD/tests/APIs/lua/test_string_ascii.lua