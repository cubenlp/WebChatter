# Ref: https://github.com/gngpp/ninja/blob/main/doc/rest.http

import requests
import os, uuid, json
from typing import Union

def get_account_status(base_url:str, access_token:str):
    """Get account status from backend-api

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
    
    Returns:
        dict: account status
    
    Rest API:
        ### check account status
        GET http://{{host}}/backend-api/accounts/check
        Authorization: {{bearer_token}}
    """
    url = os.path.join(base_url, "backend-api/accounts/check")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_models(base_url:str, access_token:str, history_and_training_disabled:bool=False):
    """Get models from backend-api

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        history_and_training_disabled (bool, optional): history and training disabled. Defaults to False.
    
    Returns:
        dict: models
    
    Rest API:
        ### get models
        GET http://{{host}}/backend-api/models?history_and_training_disabled=false
        Authorization: {{bearer_token}}
    """
    url = os.path.join(base_url, "backend-api/models")
    params = {
        "history_and_training_disabled": history_and_training_disabled
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def get_beta_features(base_url:str, access_token:str):
    """Get beta features from backend-api

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
    
    Returns:
        dict: beta features
    
    Rest API:
        ### get beta features
        GET http://{{host}}/backend-api/settings/beta_features
        Authorization: {{bearer_token}}
    """
    url = os.path.join(base_url, "backend-api/settings/beta_features")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

## dealing with chat

def get_chat_list( base_url:str, access_token:str
                 , offset:int=0, limit:Union[int, None]=None, order:str="updated"):
    """Get chat list from backend-api

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        offset (int, optional): start index. Defaults to 0.
        limit (int, optional): max number of chat. Defaults to 3.
        order (str, optional): order by. Defaults to "updated".
    
    Returns:
        dict: chat list
    
    Rest API:
        ### get conversation list
        GET http://{{host}}/backend-api/conversations?offset=0&limit=3&order=updated
        Authorization: {{bearer_token}}
    """
    url = os.path.join(base_url, "backend-api/conversations")
    params = {
        "offset": offset,
        "limit": limit,
        "order": order
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def get_chat_by_id(base_url:str, access_token:str, conversation_id:str):
    """Get chat by id from backend-api

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        conversation_id (str): conversation id
    
    Returns:
        dict: chat
    
    Rest API:
        ### get conversation by id
        GET http://{{host}}/backend-api/conversation/5ae8355a-82a8-4ded-b0e4-ea5dc11b4a9f
        Authorization: {{bearer_token}}
    """
    url = os.path.join(base_url, "backend-api/conversation", conversation_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_share_links(base_url:str, access_token:str, order:str="created"):
    """Get share links from backend-api

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        order (str, optional): order by. Defaults to "created".
    
    Returns:
        dict: share links
    
    Rest API:
        ### get share link
        GET http://{{host}}/backend-api/shared_conversations?order=created
        Authorization: {{bearer_token}}
    """
    url = os.path.join(base_url, "backend-api/shared_conversations")
    params = {
        "order": order
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def get_conversation_limit(base_url:str, access_token:str):
    """Get conversation limit of gpt-4

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
    
    Returns:
        dict: conversation limit
    
    Rest API:
        ### get conversation limit
        GET http://{{host}}/public-api/conversation_limit
        Authorization: {{bearer_token}}
    """
    url = os.path.join(base_url, "public-api/conversation_limit")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def send_data_to_email(base_url:str, access_token:str):
    """Send data to email

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
    
    Returns:
        dict: response
    
    Rest API:
        ### export data send to email
        POST http://{{host}}/backend-api/accounts/data_export
        Authorization: {{bearer_token}}
    """
    url = os.path.join(base_url, "backend-api/accounts/data_export")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, headers=headers)
    return response.json()

def edit_chat_title(base_url:str, access_token:str, conversation_id:str, title:str):
    """Edit chat title by id

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        conversation_id (str): conversation id
        title (str): title
    
    Returns:
        dict: response
    
    Rest API:
        ### change conversation title by id
        PATCH http://{{host}}/backend-api/conversation/5ae8355a-82a8-4ded-b0e4-ea5dc11b4a9f
        Authorization: {{bearer_token}}
        Content-Type: application/json

        {
            "title": "New Test"
        }
    """
    url = os.path.join(base_url, "backend-api/conversation", conversation_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "title": title
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.json()

def generate_chat_title(base_url:str, access_token:str, conversation_id:str, message_id:str):
    """Generate chat title by id and message id

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        conversation_id (str): conversation id
        message_id (str): message id
    
    Returns:
        dict: response
    
    Rest API:
        ### generate conversation title
        POST http://{{host}}/backend-api/conversation/gen_title/5ae8355a-82a8-4ded-b0e4-ea5dc11b4a9f
        Authorization: {{bearer_token}}
        Content-Type: application/json

        {
            "message_id": "1646facc-08a6-465f-ba08-58cec1e31ed6"
        }
    """
    url = os.path.join(base_url, "backend-api/conversation/gen_title", conversation_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "message_id": message_id
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def delete_chat(base_url:str, access_token:str, conversation_id:str):
    """Delete chat by id

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        conversation_id (str): conversation id
    
    Returns:
        dict: response
    
    Rest API:
        ### clear conversation by id
        PATCH http://{{host}}/backend-api/conversation/5ae8355a-82a8-4ded-b0e4-ea5dc11b4a9f
        Authorization: {{bearer_token}}
        Content-Type: application/json

        {
            "is_visible": false
        }
    """
    url = os.path.join(base_url, "backend-api/conversation", conversation_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "is_visible": False
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.json()

def continue_chat( base_url:str, access_token:str
                 , prompt:str
                 , parent_message_id:Union[str, None]=None
                 , conversation_id:Union[str, None]=None
                 , model:str="text-davinci-002-render-sha"
                 , history_and_training_disabled:bool=False):
    """chat completion(create or edit)

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        prompt (str): prompt
        parent_message_id (str, optional): parent message id. Defaults to None.
        conversation_id (str, optional): conversation id. Defaults to None.
        model (str, optional): model. Defaults to "text-davinci-002-render-sha".
        history_and_training_disabled (bool, optional): disable history record in the website. Defaults to False.
    
    Returns:
        dict: chat
    
    Rest API:
        ### new conversation
        POST http://{{host}}/backend-api/conversation
        Authorization: {{bearer_token}}
        Content-Type: application/json
        Accept: text/event-stream
    
    {
        "action": "next",
        "messages": [
            {
            "id": "{{$guid}}",
            "author": {
                "role": "user"
            },
            "content": {
                "content_type": "text",
                "parts": [
                "new conversation"
                ]
            },
            "metadata": {}
            }
        ],
        "model": "text-davinci-002-render-sha-mobile",
        "parent_message_id": "{{$guid}}",
        "timezone_offset_min": -480,
        "history_and_training_disabled": false
    }
    """
    url = os.path.join(base_url, "backend-api/conversation")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Accept': 'text/event-stream'
    }
    messages = [
        {
            "id": str(uuid.uuid4()),
            "author": {"role": "user"},
            "content": {"content_type": "text", "parts": [prompt]},
        },
    ]
    data = {
        "action": "next",
        "messages": messages,
        "conversation_id": conversation_id,
        "parent_message_id": parent_message_id,
        "model": model,
        "history_and_training_disabled": history_and_training_disabled,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    msg, info = response.text.split("data:")[-3:-1]
    return json.loads(msg), json.loads(info)

def create_chat( base_url:str, access_token:str
               , prompt:str, model:str="text-davinci-002-render-sha"
               , history_and_training_disabled:bool=False):
    """Create chat

    Args:
        base_url (str): base url
        access_token (str): access token at https://chat.openai.com/api/auth/session
        prompt (str): prompt
        model (str, optional): model. Defaults to "text-davinci-002-render-sha".
        history_and_training_disabled (bool, optional): history and training disabled. Defaults to False.

    Returns:
        dict: chat
    """
    parent_id = str(uuid.uuid4())
    return continue_chat( base_url, access_token
                        , prompt, model, history_and_training_disabled, parent_id)