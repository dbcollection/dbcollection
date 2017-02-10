"""
Select data from the metadata file.

Whenever an user requires to select only a set of the available data
from a specific task, it can use the selection property in the load()
API. 

This enables the user to select, for example, only a specific set of 
classes from the available class list. The resulting metadata removes
all data objects that do not contain the specified set of classes 
automatically. 
"""