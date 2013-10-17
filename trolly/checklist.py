'''
Created on 13 Nov 2012

@author: plish
'''

from trelloobject import TrelloObject


class Checklist( TrelloObject ):
    """
    Class representing a Trello Checklist
    """
    def __init__( self, trello_client, card_id, checklist_id, name = '' ):
        super( Checklist, self ).__init__( trello_client )

        self.idCard = card_id
        self.id = checklist_id
        self.name = name

        self.base_uri = '/checklists/' + self.id


    def getChecklistInformation( self, query_params = {} ):
        """
        Get all information for this Checklist. Returns a dictionary of values.
        """
        return self.fetchJson( 
                uri_path = self.base_uri,
                query_params = query_params
            )


    def getItems( self, query_params = {} ):
        """
        Get all the items for this checklist. Returns a list of dictionaries.
        Each dictionary has the values for an item.
        """
        return self.fetchJson( 
                uri_path = self.base_uri + '/checkItems',
                query_params = query_params
            )


    def getItemObjects( self, query_params = {} ):
        """
        Get the items for this checklist. Returns a list of ChecklistItem objects.
        """
        checklistitems_list = []
        for checklistitem_json in self.getItems(query_params):
            checklistitems_list.append( self.createChecklistItem( self.idCard, self.id, checklistitem_json ) )

        return checklistitems_list


    def updateChecklist( self, name ):
        """
        Update the current checklist. Returns a new Checklist object.
        """
        checklist_json = self.fetchJson( 
                uri_path = self.base_uri,
                http_method = 'PUT',
                query_params = { 'name': name }
            )

        return self.createChecklist( checklist_json )


    def addItem( self, query_params = {} ):
        """
        Add an item to this checklist. Returns a dictionary of values of new item.
        """
        return self.fetchJson( 
                uri_path = self.base_uri + '/checkItems',
                http_method = 'POST',
                query_params = query_params
            )


    def removeItem( self, item_id ):
        """
        Deletes an item from this checklist.
        """
        return self.fetchJson( 
                uri_path = self.base_uri + '/checkItems/' + item_id,
                http_method = 'DELETE'
            )


class ChecklistItem( TrelloObject ):
    """
    Class representing a Trello Checklist Item
    """
    def __init__( self, trello_client, card_id, checklist_id, checklistitem_id, name = '', state = 'incomplete'):
        super( ChecklistItem, self ).__init__( trello_client )

        self.idCard = card_id
        self.idChecklist = checklist_id
        self.id = checklistitem_id
        self.name = name
        self.state = (state == 'complete')

        self.base_uri = '/cards/' + self.idCard + '/checklist/' + self.idChecklist + '/checkItem/' + self.id


    def updateName( self, name ):
        """
        Rename the current checklist item. Returns a new ChecklistItem object.
        """
        checklistitem_json = self.fetchJson(
                uri_path = self.base_uri + '/name',
                http_method = 'PUT',
                query_params = { 'value': name }
            )

        return self.createChecklistItem( self.idCard, self.idChecklist, checklistitem_json )


    def updateState( self, state ):
        """
        Set the state of the current checklist item. Returns a new ChecklistItem object.
        """
        checklistitem_json = self.fetchJson(
                uri_path = self.base_uri + '/state',
                http_method = 'PUT',
                query_params = { 'value': 'complete' if state else 'incomplete' }
            )

        return self.createChecklistItem( self.idCard, self.idChecklist, checklistitem_json )
