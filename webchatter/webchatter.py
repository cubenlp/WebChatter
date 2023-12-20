"""Main module."""

from typing import Union
import os, uuid
import webchatter
from .request import (
    get_account_status, get_models, get_beta_features,
    get_chat_list, get_chat_by_id, 
    chat_completion, delete_chat,
)

class Node():
    def __init__(self, node:dict, name:str="", depth:int=0):
        """Initialize the class.
        
        Args:
            node (dict): The node.
        """
        self._node = self.simplify(node)
        self._message, self._parent, self._children, self._node_id = (
            self.node['message'], self.node['parent'], self.node['children'], self.node['id'])
        self.name, self.depth = name, depth
    
    @property
    def node(self):
        """Get the node."""
        return self._node
    
    @property
    def message(self):
        """Get the message."""
        return self._message
    
    @property
    def parent(self):
        """Get the parent."""
        return self._parent
    
    @property
    def children(self):
        """Get the children."""
        return self._children
    
    @property
    def node_id(self):
        """Get the node id."""
        return self._node_id
    
    @staticmethod
    def simplify(node:dict):
        """Simplify the node."""
        # message
        msg = node.get("message")
        if isinstance(msg, dict): msg = msg['content']['parts'][0]
        # parent id
        parent = node.get('parent')
        # children id
        children = node.get("children")
        if not children:children = []
        # node id
        node_id = node.get("id") or node['message']['id']
        return {
            "id": node_id,
            "message": msg,
            "parent": parent,
            "children": children}
    
    def __repr__(self):
        """Representation."""
        children = [child[:8] for child in self.children]
        parent = self.parent[:8] if self.parent else "tree"
        name = self.name + "-" if self.name else ""
        return f"<Node: {name}{parent} -|- {children}"
    
    def __str__(self):
        """String."""
        return self.__repr__()
    
    def __eq__(self, other):
        """Equal."""
        return self.node == other.node

class WebChat():
    """WebChat class."""
    def __init__( self
                , base_url: Union[str, None] = None
                , backend_url: Union[str, None] = None
                , access_token: Union[str, None] = None
                , chat_id: Union[str, None] = None
                , node_id: Union[str, None] = None):
        """Initialize the class.

        Args:
            base_url (Union[str, None], optional): The base url for the API. Defaults to None.
            backend_url (Union[str, None], optional): The backend url for the API. Defaults to None.
            access_token (Union[str, None], optional): The access token for the API. Defaults to None.
            chat_id (Union[str, None], optional): The conversation id for the API. Defaults to None.
            node_id (Union[str, None], optional): The parrent message id for the API. Defaults to None.
        """
        self._base_url = base_url or webchatter.base_url
        self._access_token = access_token or webchatter.access_token
        self.backend_url = backend_url or webchatter.backend_url or os.path.join(self.base_url, "backend-api")
        assert self.backend_url is not None, "The backend url and base url are not set!"
        assert self.access_token is not None, "The access token is not set!"
        self._chat_id = chat_id
        # Tree structure
        self._node_id = node_id # the answer node
        self._root_id, self._tree_id, self._que_id = None, None, None
        self._mapping = {}
    
    @property
    def chat_log(self):
        """Get the chat log."""
        node_id, mapping = self.node_id, self.mapping
        if node_id is None: return []
        # TODO
        
    def account_status(self):
        """Get the account status."""
        url, token = self.backend_url, self.access_token
        resp = get_account_status(url, token)
        return resp['account_plan']
    
    def valid_models(self):
        """Get the models."""
        url, token = self.backend_url, self.access_token
        resp = get_models(url, token)
        return [model['category'] for model in resp["categories"]]
    
    def beta_features(self):
        """Get the beta features."""
        url, token = self.backend_url, self.access_token
        return get_beta_features(url, token)
    
    def chat_list(self, offset:int=0, limit:int=3, order:str="updated"):
        """Get the chat list."""
        url, token = self.backend_url, self.access_token
        resp = get_chat_list(url, token, offset=offset, limit=limit, order=order)
        return [{'conversation_id':item['id'],'title': item['title']} for item in resp['items']]
    
    def num_of_chats(self):
        """Get the number of chats."""
        url, token = self.backend_url, self.access_token
        resp = get_chat_list(url, token)
        return resp['total']
    
    def ask( self, message:str
           , keep:bool=True):
        """Continue the chat."""
        url, token = self.backend_url, self.access_token
        # first call: create a conversation
        if self.chat_id is None:
            # create four nodes
            tree_id, que_id = str(uuid.uuid4()), str(uuid.uuid4())
            root_resp, ans_resp = chat_completion(url, token, message, que_id, tree_id)
            # update parent and children for these nodes
            root_resp['children'], root_resp['parent'] = [que_id], tree_id
            ans_resp['children'], ans_resp['parent'] = [], que_id
            root_node = Node(root_resp, name="root")
            tree_node = Node({
                "id": tree_id, "message": None,
                "children": [root_node.node_id], "parent":None})
            ans_node = Node(ans_resp, name="A1")
            que_node = Node({
                "id": que_id, "message": message,
                "children": [ans_node.node_id], "parent": root_node.node_id}
                , name="Q1")
            # update conversation id
            self._chat_id = ans_resp['conversation_id']
            # update mapping and tree ids
            self._tree_id, self._root_id = tree_id, root_node.node_id
            self._node_id, self._que_id = ans_node.node_id, que_node.node_id
            self._mapping = {
                tree_id: tree_node, root_node.node_id: root_node,
                ans_node.node_id: ans_node, que_node.node_id: que_node
            }
        else: # update ans_node and que_node
            que_id = str(uuid.uuid4())
            _, ans_resp = chat_completion(url, token, message, que_id, self.node_id, self.chat_id)
            ans_resp['parent'] = que_id
            ans_node = Node(ans_resp)
            que_node = Node({
                "id": que_id, "message": message,
                "children": [ans_node.node_id], "parent": self.node_id})
            # add children to the previous node
            self._mapping[self.node_id].children.append(que_id)
            # update node id and que id
            self._node_id, self._que_id = ans_node.node_id, que_node.node_id
            # update mapping
            self._mapping[ans_node.node_id] = ans_node
            self._mapping[que_node.node_id] = que_node
        # return the answer
        return ans_node.message

    def mapping_by_id(self, chat_id:Union[str, None]=None):
        """Get the mapping by id."""
        url, token = self.backend_url, self.access_token
        chat_id = chat_id or self.chat_id
        assert chat_id is not None, "The chat id is not set!"
        resp = get_chat_by_id(url, token, chat_id)
        return {key: Node(node) for key, node in resp['mapping'].items()}
    
    def newchat_by_id(self, conversation_id:Union[str, None]=None):
        """Get the chat by id."""
        url, token = self.backend_url, self.access_token
        conversation_id = conversation_id or self.conversation_id
        resp = get_chat_by_id(url, token, conversation_id)
        # TODO: extract the chat history
        return WebChat(base_url=url, access_token=token, conversation_id=conversation_id)

    def regenerate(self, message:Union[str, None]=None):
        """Regenerate the chat."""
        # TODO
    
    def goback(self):
        """Go back to the parrent node."""
        # TODO
    
    def goto(self, node_id:str):
        """Go to the parrent node."""
        # TODO

    def save(self, filename:str):
        """Save the chat."""
        # TODO
    
    def load(self, filename:str):
        """Load the chat."""
        # TODO
    
    def print_log(self):
        """Print the chat log."""
        # TODO
    
    def __repr__(self):
        """Representation."""
        return "<WebChat: {}>".format(self.chat_id or "None")
    
    def __str__(self):
        """String."""
        return self.__repr__()

    @property
    def base_url(self):
        """Get the base url."""
        return self._base_url
    
    @base_url.setter
    def base_url(self, new_url:str):
        """Set the base url."""
        self.backend_url = os.path.join(new_url, "backend-api")

    @property
    def access_token(self):
        """Get the access token."""
        return self._access_token
    
    @access_token.setter
    def access_token(self, _):
        """Set the access token."""
        raise AttributeError("The access token cannot be changed. Try to create another chat instead.")
    
    @property
    def chat_id(self):
        """Get the conversation id."""
        return self._chat_id
    
    @chat_id.setter
    def chat_id(self, _):
        """Set the conversation id."""
        raise AttributeError("The conversation id cannot be changed. Try to create another chat instead.")
    
    @property
    def node_id(self):
        """Get the node id."""
        return self._node_id
    
    @node_id.setter
    def node_id(self, _:str):
        """Set the node id."""
        raise AttributeError("The node id cannot be changed. Please use `self.goto` instead.")
    
    @property
    def root_id(self):
        """Get the root id."""
        return self._root_id
    
    @property
    def tree_id(self):
        """Get the tree id."""
        return self._tree_id

    @property
    def mapping(self):
        """Get the mapping."""
        return self._mapping