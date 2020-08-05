==============================
**Ovirtlib4 Project Overview**
==============================

  The **Ovirtlib4 Project** is a wrapper for the OvirtSdk4 project,
  It fully integrated with OvirtSdk4.
  You can use the benefits of this wrapper without losing
  any OvirtSdk4 abilities


**Requirements**
----------------
- Python 2.7, 3.6
- ovirtsdk4


**Installation**
----------------

 .. code-block:: bash

  $ export PYCURL_SSL_LIBRARY=openssl
  $ pip install git+https://github.com/roniezr/ovirtlib4.git

 PYCURL_SSL_LIBRARY is required to install "pycurl" that required by ovirtsdk4,
 If you encounter the following error while import ovirtsdk4 or ovirtlib4

 .. code-block:: bash

  ImportError: pycurl: libcurl link-time ssl backend (openssl) is different from compile-time ssl backend (nss)

 Then run the following commands to fix it:

 .. code-block:: bash

  $ export PYCURL_SSL_LIBRARY=openssl
  $ pip uninstall pycurl
  $ pip install pycurl --no-cache-dir


**Introduction**
----------------
  This lib design to simplify the use of OvirtSdk4.
  The main class is the root for all oVirt components/entities,
  by navigating the class-path you can **quickly** find and set/get
  any oVirt feature/information.


**Why this lib is required**
-----------------------------
  The main ovirtsdk4 include basic REST API commands, it still needs
  to create simple methods to execute complex operations.
  So instead of "inventing the wheel" again and again by different developer/teams,
  you can use this library and contribute to the community by extending it
  with your added methods


**Project Vision**
----------------------
1. Fully integrated with the parent ovirtsdk4
2. Quickly and simply use of oVirt REST commands


**Main Concept**
----------------
  It all starts with the OvirtLib() main class
  This class holds the oVirt Collections and it used as
  the root point accessing any oVirt entity, only by using
  class-path navigation.

  | Each collection return a list of **CollectionEntity()** classes
  | Each CollectionEntity() class include two fields

  - **CollectionEntity.entity** hold the Entity type, (e.g.: ovirtsdk4.types.Vm) include the Entity properties and 'links'.

  - **CollectionEntity.service** hold the Entity service, that holds the Entity 'actions'.

  |
  | ** **Collection** **
  | --------------------------------
  | Each collection must inherit from **CollectionService()**
  | The new inherit class must define 3 parameters at the __init__() method:
  | 1. **self.service**: the collection service from the SDK
  | 2. **self.entity_service**: the entity service usually exists under 'self.service' above
  | 3. **self.entity.type**: the entity type from the SDK
  |
  | The new inherit class must also overwrite the following method
  | 4. **_get_collection_entity()**:
  | This metod must return a link to a new clas inherit from **CollectionEntity()** class.
  | This class represent an individual entity inside the collection
  | This class is used to store custom functions related to the individual entity
  |
  | Optional:
  | 5. **self.follows**: If it defined, it will retrieve assigning links when calling get()
  |
  |
  | See the example below, how to define VMs collection that will return a list of VmEntitiy()'s

   .. code-block:: python

    class Vms(CollectionService):
    """
    Gives access to all Ovirt VMs
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().vms_service()  # 1 above
        self.entity_service = self.service.vm_service                  # 2 above
        self.entity_type = types.Vm                                    # 3 above
        self.follows = (                                               # 5 optional
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

        def _get_collection_entity(self):                # 4 above
        """ Overwrite abstract parent method """
        return VmEntity(connection=self.connection)

    class VmEntity(CollectionEntity):                    # 4 above
    """
    Put VM custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)

  |
  | ** **Sub-Collection** **
  | --------------------------------
  | Entity can include other collections, for example, VM can include collections of NICs or Disks, etc...
  |
  | At the example below, we define sub-collection for the VmEntitiy()

   .. code-block:: python

    class VmEntity(CollectionEntity):
    """
    Put VM custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)

    @property
    def nics(self):
        return VmNics(connection=self.service)  # self.service is the indevidual VM service

    class VmNics(CollectionService):
    """
    Gives access to all VM NICs
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.nics_service()   # here self.connection is the VM collection service
        self.entity_service = self.service.nic_service  # same as collection above
        self.entity_type = types.Nic                    # same as collection above
        self.follows = "networkfilterparameters,reporteddevices,statistics,vm" # VM nics links

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmNic(connection=self.connection)


    class VmNic(CollectionEntity):
    """
    Put VmNic custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)

  |
  | **follow_link()**
  | ------------------
  | There are some option to retrieve entity links
  | 1. Define the 'self.follows' for a collection, see example above
  | 2. Through get() e.g.: get(follow="link_name")
  | 3. Use the ovirtlib.folow_link() method
  | 4. Use the CollectionEntity.follow_link() method
  |
  | 1 to 3 will retrieve the entity links, but it will not include the entity service
  | Options 4 will include the entity service as well if given

- Functions starts with **'get*()'** or **list()** are retrieving data from the remote oVirt Engine.

***************************
**OvirtSdk vs. OvirtLib**
***************************
 *Retrieving VMs via OvirtSdk4*:

 .. code-block:: python

  ovirtsdk4.system_service().vms_service().list()


 *Is equivalent for the following OvirtLib4 command*:

 .. code-block:: python

  ovirtlib.vms.list()

get()
*****************
 | *get()* is fully integrated with OvirtSdk4 list() method
 | The SDK list() methods of some services support additional parameters.
 | For more information please refer to the OvirtSdk4 documentation
 |
 | For example you can use vms.get(search="name=VM_name") to retrieve a special VM
 | Or use the 'max' parameter to limit the retrieving events
 |
 | *e.g.: the following will return all VM except the HostedEngine VM*:

 .. code-block:: python

  engine.vms.list(search="name!=HostedEngine")

 | *e.g.: the following will return 10 events*:

 .. code-block:: python

  engine.events.get(max=10)


CollectionEntiry
****************
  .. code-block:: python

   vm = ovirtlib.vms.get()[0] # list() return list of CollectionEntiry() classes
   vm.entity                   # entity, hold the Entity fields and links
   vm.service                  # service, hold the Entity actions

  At the above commands **vm.entity** is equivalent to:

  .. code-block:: python

    vm = ovirtsdk4.system_service().vms_service().list()[0]

  And **vm.service** is equivalent to:

  .. code-block:: python

   vm_service = ovirtsdk4.system_service().vms_service().vm_service(id=vm.id)


**Examples**
------------------

 Initialize the OvirtLib class e.g.:

 .. code-block:: python

  from ovirtlib4 import ovirtlib
  engine = ovirtlib.OvirtLib(host="192.168.1.100", password="engine_admin_password")

 Get and start all VMs:

 .. code-block:: python

  vms = engine.vms.get()
  for vm in vms:
    print("Starting VM {name}".format(name=vm.entity.name))
    vm.service.start()

 Get all hosts:

 .. code-block:: python

  hosts = engine.hosts.get() or
  hosts = engine.hosts()

 You can use the get_names() CollectionService method to retrieve the names of all entities at the collection:

 .. code-block:: python

  engine.hosts.get_names()



**Contribute**
------------------
  - git clone https://github.com/roniezr/ovirtlib4.git

  - It is recommended to read ovirtsdk4 documentation before starting to contribute to this project https://access.redhat.com/documentation/en-us/red_hat_virtualization/4.3/pdf/python_sdk_guide/Red_Hat_Virtualization-4.3-Python_SDK_Guide-en-US.pdf