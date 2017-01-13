--[[
    Copyright (C) 2017, Farrajota @ https://github.com/farrajota
    All rights reserved.

    This source code is licensed under the MIT license found in the
    LICENSE file in the root directory of this source tree.
--]]


--
-- Unit tests script
--

local mytest = torch.TestSuite()

local tester = torch.Tester()


-----------------------------------------------------------
-- Unit testing of the general API
-----------------------------------------------------------

function mytest.BuildClassDataLoader()
--
-- Initialize class
--

    paths.dofile('../APIs/Lua/loader.lua')

    local loader = DatasetLoader()

    tester:assert(loader,'Failed to initialize the class "DatasetLoader"')
end



-----------------------------------------------------------
-- Unit testing of the class 'DatasetLoader'
-----------------------------------------------------------


-----------------------------------------------------------
-- Run tests
-----------------------------------------------------------

tester:add(mytest)
tester:run()