from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
import os

from plenum.common.config_util import getConfig as PlenumConfig


def getInstalledConfig(installDir, configFile):
    configPath = os.path.join(installDir, configFile)
    if os.path.exists(configPath):
        spec = spec_from_file_location(configFile, configPath)
        config = module_from_spec(spec)
        spec.loader.exec_module(config)
        return config
    else:
        raise FileNotFoundError("No file found at location {}".
                                format(configPath))


def getConfig(homeDir=None):
    plenumConfig = PlenumConfig(homeDir)
    sovrinConfig = import_module("sovrin.config")
    refConfig = plenumConfig
    refConfig.__dict__.update(sovrinConfig.__dict__)
    try:
        homeDir = os.path.expanduser(homeDir or "~")
        configDir = os.path.join(homeDir, ".sovrin")
        config = getInstalledConfig(configDir, "sovrin_config.py")
        refConfig.__dict__.update(config.__dict__)
    except FileNotFoundError:
        pass
    refConfig.baseDir = os.path.expanduser(refConfig.baseDir)
    return refConfig
