from __future__ import unicode_literals

from interface import BTInterface


class BTManager(BTInterface):
    """
    Wrapper around dbus to encapsulate the org.bluez.manager interface
    which notionally is used to manage available bluetooth adapters.

    :Properties:

    * **Adapters(list{str}) [readonly]**: List of adapter object paths.

    See also :py:class:`.BTAdapter`
    """

    SIGNAL_INTERFACES_ADDED = 'InterfacesAdded'
    SIGNAL_INTERFACES_REMOVED = 'InterfacesRemoved'

    def __init__(self):
        BTInterface.__init__(self, '/', 'org.freedesktop.DBus.ObjectManager')
        self._register_signal_name(BTManager.SIGNAL_INTERFACES_ADDED)
        self._register_signal_name(BTManager.SIGNAL_INTERFACES_REMOVED)

    def find_adapter(self, **kwargs):
        for adapter in self.list_adapters():
            all_match = True
            for prop, val in kwargs:
                if getattr(adapter, prop) != val:
                    all_match = False
                    break
            if all_match:
                return adapter

    def list_adapters(self):
        objects = self._interface.GetManagedObjects()

        for path, interfaces in objects.items():
            if 'org.bluez.Adapter1' in interfaces:
                yield path
