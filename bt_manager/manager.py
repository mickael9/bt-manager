from __future__ import unicode_literals

from interface import BTInterface


class BTManager(BTInterface):
    """
    Wrapper around dbus to encapsulate the org.bluez.manager interface
    which notionally is used to manage available bluetooth adapters.
    See also :py:class:`.BTAdapter`
    """

    SIGNAL_INTERFACES_ADDED = 'InterfacesAdded'
    SIGNAL_INTERFACES_REMOVED = 'InterfacesRemoved'

    def __init__(self):
        BTInterface.__init__(self, '/', 'org.freedesktop.DBus.ObjectManager')
        self._register_signal_name(BTManager.SIGNAL_INTERFACES_ADDED)
        self._register_signal_name(BTManager.SIGNAL_INTERFACES_REMOVED)

    def find_objects(self, interface, **filters):
        objects = self._interface.GetManagedObjects()

        for path, interfaces in objects.items():
            if interface in interfaces:
                all_match = True
                for prop, val in filters.items():
                    if (prop not in interfaces[interface] or
                        interfaces[interface][prop] != val):
                        all_match = False
                        break
                if all_match:
                    yield path

    def list_adapters(self, **filters):
        return self.find_objects('org.bluez.Adapter1', **filters)
    
    def list_devices(self, **filters):
        return self.find_objects('org.bluez.Device1', **filters)
