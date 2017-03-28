package = "dbcollection"

version = "scm-1"

source = {
    url = "git://github.com/farrajota/dbcollection.git",
    tag = "master"
 }

description = {
    summary = "A Lua/Torch7 wrapper for dbcollection.",
    detailed = [[
       This package provides a list of scripts to load the most common datasets
       used in computer vision into memory. It comes along with several download
       scripts to ease the burden of finding all necessary files from a particular
       dataset and/or task.

       Warning: some datasets cannot be downloaded via scripts
       due to lincensing concerns, although this is highlighted by the downloading
       scripts for these datasets.

       The dataset's metada is stored in a HDF5 file which contains the processed/raw
       data provided by each dataset. This allows for fast access to the needed data
       with a small impact on both access time and system's RAM memory usage, meaning
       faster script intializations and optimization of the system's  resources.
    ]],
    homepage = "https://github.com/farrajota/dbcollection",
    license = "MIT",
    maintainer = "M. Farrajota"
 }

dependencies = {
    "lua >= 5.1",
    "torch >= 7.0",
    "json >= 1.0",
    "argcheck >= 1.0"
}

build = {
    type = "cmake",
    variables = {
        CMAKE_BUILD_TYPE="Release",
        LUA_PATH="$(LUADIR)",
        LUA_CPATH="$(LIBDIR)"
   }
}