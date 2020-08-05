# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types


class Events(CollectionService):
    """
    Gives access to all Ovirt Events
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.service = self.connection.system_service().events_service()
        self.entity_service = self.service.event_service
        self.entity_type = types.Event

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return EventEntity(connection=self.connection)


class EventEntity(CollectionEntity):
    """
    Put Event custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
