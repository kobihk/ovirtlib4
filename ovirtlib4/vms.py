# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types
from . import defaults, hosts


class Vms(CollectionService):
    """
    Gives access to all Ovirt VMs
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().vms_service()
        self.entity_service = self.service.vm_service
        self.entity_type = types.Vm
        self.follows = (
            "diskattachments.disk,"
            "katelloerrata,"
            "permissions,"
            "tags,"
            "affinitylabels,"
            "graphicsconsoles,"
            "cdroms,"
            "nics,"
            "watchdogs,"
            "snapshots,"
            "applications,"
            "hostdevices,"
            "reporteddevices,"
            "sessions,"
            "statistics"
        )

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmEntity(connection=self.connection)

    def get_vms(self, he_name=defaults.HOSTED_ENGINE_VM_NAME):
        """ Return all VMs beside the HostedEngine VM """
        return self.list(search="name!={name}".format(name=he_name))

    def get_hosted_engine_vm(self, he_name=defaults.HOSTED_ENGINE_VM_NAME):
        """ Return the hosted-engine VM: (VmEntity) """
        vms = self.list(search="name={name}".format(name=he_name))
        if vms:
            return vms[0]
        return None

    def get_hosted_engine_host(self):
        """
        Return the host Entity of the HostedEngine VM, or None if not found
        """
        vm = self.get_hosted_engine_vm()
        if vm:
            host_id = vm.entity.host.id
            if host_id:
                return hosts.Hosts(self.connection).get_entity_by_id(id=host_id)
        return None


class VmEntity(CollectionEntity):
    """
    Put VM custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)

    @property
    def nics(self):
        return VmNics(connection=self.service)

    @property
    def disks(self):
        return VmDisks(connection=self.service)


class VmNics(CollectionService):
    """
    Gives access to all VM NICs
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.nics_service()
        self.entity_service = self.service.nic_service
        self.entity_type = types.Nic
        self.follows = "networkfilterparameters,reporteddevices,statistics,vm"

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmNic(connection=self.connection)


class VmNic(CollectionEntity):
    """
    Put VmNic custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)


class VmDisks(CollectionService):
    """
    Gives access to all VM attached disks
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.disk_attachments_service()
        self.entity_service = self.service.attachment_service
        self.entity_type = types.DiskAttachment
        self.follows = "disk,vm"

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmDisk(connection=self.connection)


class VmDisk(CollectionEntity):
    """
    Put VmDisk custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
