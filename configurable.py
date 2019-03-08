"""
Created 06-17-18 by Matt C. McCallum
"""


# Local imports
# None.

# Third party module imports
# None.

# Python standard library imports
import copy


class InvalidConfigError(Exception):
    """
    An error that is raised when the required configuration fields are not provided.
    """
    pass


class Configurable(object):
    """
    A Base class for any object that has a given configuration, i.e., requires a certain set of parameters.

    The configuration may include a heirarchy. That is, in the list of required fields may be a dictionary
    with each key corresponding to a name of a sublist of feilds and each key being a list corresponding to 
    that sublist of field names.

    Note that anything below the top level of the heirarchy will not be assigned as an attribute.
    It is assumed that values further down the heirarchy are for configuration of other objects and it is
    up to the derived class to use these values.
    """
    
    _REQUIRED_CONFIG = []

    _CONFIG_DEFAULTS = {}

    def __init__(self, cfg):
        """
        Constructor.

        Args:
            cfg: dict - An object providing the configuration parameters for this object.
        """
        # Populate defaults
        self._populateDefaults(cfg, self._CONFIG_DEFAULTS)

        # Verify configuration
        self._verifyConfig(cfg, self._REQUIRED_CONFIG)

        # Set properties
        self._cfg = cfg
        for name in self._REQUIRED_CONFIG:
            if type(name) is str:
                setattr(self, "_"+name, cfg[name])

    def _populateDefaults(self, cfg, defaults):
        """
        Iterates through all of the items in the defaults and transfers them over to the configuration
        if they are not already there.

        Args:
            cfg: dict() - An object to be used to configure a configurable class

            defaults: dict() - A set of defaults to configure in `cfg` if they do not already exist there.
        """
        for field, value in defaults.items():
            if field not in cfg.keys():
                cfg[field] = value
            elif isinstance(value, dict):
                # Check the sub fields
                self._populateDefaults(cfg[field], value)

    def _verifyConfig(self, cfg, template):
        """
        Checks that all the required fields in the object configuration are there.

        Args:
            cfg: dict() - An object providing the configuration parameters for this object.

            template: list() - A list of keys that describe the required fields to be configured for this object.
            This may includ dictionaries, allowing a heirarchy in the provided configuration.
        """
        for field in template:
            if isinstance(field, dict):
                for key in field.keys():
                    if key not in cfg.keys():
                        print(key + " value not found in " + self.__class__.__name__ + " object configuration")
                        raise InvalidConfigError
                    self._verifyConfig(cfg[key], field[key])
            elif field not in cfg.keys():
                print(field + " value not found in " + self.__class__.__name__ + " object configuration")
                raise InvalidConfigError

    @property
    def cfg(self):
        """
        Getter function for a copy of this objects configuration.

        Return:
            dict{str:value} : A hierarchical dictionary of this class's configuration and all classes therein.
        """
        return copy.copy(self._cfg)
