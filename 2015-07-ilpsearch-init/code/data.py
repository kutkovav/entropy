__author__ = 'Jakub Danek'

import ConfigParser as cp

DATA_PATH='./data/'

"""
Reads functionality provider (library) information from data file
based on the provider name (expects to find provider_name.properties file in
the ./data folder.

Reads list of different versions and their sizes in kB.

Each item from the file may be loaded multiple times based on the magnification argument value.
"""
def readProviders(provider_names, magnification = 1):
    providers = []
    for name in provider_names:
        parser = cp.ConfigParser()
        parser.read(DATA_PATH + name + ".properties")
        for version,cost in parser.items('versions'):
            for i in range(magnification):
                providers.append(Provider(name, version, float(cost)))

    return providers


"""
Reads functionality provider (library) information from data file
based on the provider name (expects to find provider_name.properties file in
the ./data folder.

Reads number references of the provider from other libraries/applications

Amount of references can be increased based on the magnification argument value.
"""
def readDeps(provider_names, magnification = 1):
    deps = []
    for name in provider_names:
        parser = cp.ConfigParser()
        parser.read(DATA_PATH + name + ".properties")
        for caller,count in parser.items('refs'):
            deps.append((name , int(count) * magnification))

    return deps

"""
Convenience class for managing (name, version, cost) triplets.
"""
class Provider:
    def __init__(self, name, version, cost):
        self.name = name
        self.version = version
        self.cost = cost