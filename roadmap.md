# Project's roadmap

This page lists the vision for this project and the roadmap of what needs to be added/changed in order to improve the package. The listed stuff to be added/considered is not, by any means, an exaustive list but it contains the core ideas of what this package should do and what types of users are targetted with this package.

## Vision of the project

TODO: describe the vision / goals for the project in terms of functionality and audience.

### Python

Things that would be nice to have:

- Hability to convert data fields (FieldLoader class) to a panda's Series
- Hability to convert an entire set (like train, test, val) to a panda's DataFrame
- Create a converter to convert a set or entire dataset in order to be able to work with sklearn in a seamless way
- Some methods from MS COCO so that the api is not needed anymore
- Wrappers for Java, Julia, R, Ruby, Scala (these seem enough for now, maybe one day even C/C++)
- Quarterly versioning scheme (bump the version at fixed periods of time)

Things that **definitely** should have:

- Better documentation for developers and users
- Tutorials on how to use dbcollection with everyone's favourite tools
- Add more different kinds of datasets for tasks like NLP, time series, reinforcement learning, audio, speech recognition

Things that should **NOT** have:

- Missing tests (datasets included)
- Missing docstrings of key functions
- Code that is hard to read

### Matlab

- Have feature parity with the python version

### Lua/Torch7

- Have feature parity with the python version

## Roadmap 2018

- Complete the Matlab wrapper and bring it to feature parity with the python package;
- Complete the Lua/Torch7 wrapper and bring it to feature parity with the python package;
- Improve the documentation for users;
- Create tutorials on how to use the packaged along with the most popular toolsfor data science / machine-learning like pandas, sklearn or tensorflow/pytorch;
