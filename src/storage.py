'''
# typical use case, say in auth.py (EXAMPLE!!!)
import storage
def auth_register(email,password,name_first,name_last):
    u_id = generate_u_id()                  # "unique" u_id.
    token = generate_token()                # "unique" token.
    handle = generate_handle()              # "unique" handle.
    permission_id = DEFAULT_PERM_ID         # check spec for this i guess.
    encrypted_password = encrypt(password)

    # storage.add_user() is what calls storage.load_user_all() and storage.save_user_all().
    storage.add_user(name_first,name_last,email,encrypted_password,token,u_id,handle,permission_id)
    return {
        'u_id': u_id,
        'token': token,
    }
'''

import json
import helper
################################################################################
# FUNCTIONS FOR CREATING, SAVING, AND LOADING DATABASES.
################################################################################

'''
database initialization.
'''
# creates new empty database, stored in json files.
def new_code_file():
    codes = {}
    save_code_file(codes)
def new_storage():
    user_all = {}
    channel_all = {}
    user_active = {}
    save_user_active(user_active)
    save_user_all(user_all)    
    save_channel_all(channel_all)

'''
database of all registered users.
'''
# loads and returns locally stored user_all database.
### user_all.json is a dictionary indexed by u_id.
### user_all['u_id1'] is a dictionary of information unique to the user with u_id 'u_id1'.
### the keys in a user dictionary are:
### 'name_first','name_last','email','encrypted_password','token','u_id'.
def load_code_file():
    with open("code_file.json","r") as FILE:
        code_all = json.load(FILE)
        return code_all
def save_code_file(code):
    with open("code_file.json", "w") as FILE:
        json.dump(code, FILE)
        return

def load_user_all():
    with open("user_all.json", "r") as FILE:
        user_all = json.load(FILE)
        return user_all

# saves to locally stored user_all database.
def save_user_all(user_all):
    with open("user_all.json", "w") as FILE:
        json.dump(user_all, FILE)
        return

'''
database that records which users are active (logged in).
'''
# load the file of the users who logged in 
### user_active.json is a dictionary indexed by token.
### user_active['token1'] is a boolean.
### if user_active['token1'] == True, then the user with token 'token1' is logged in.
def load_user_active():
    with open('user_active.json','r') as FILE:
        active = json.load(FILE)
        return active

def save_user_active(user_active):
    with open('user_active.json','w') as FILE:
        json.dump(user_active,FILE)

# would add the user who logged in 
### perhaps activate_user(token) makes more sense.
def active_user(token):
    user_active = load_user_active()
    user_active[token] = True
    save_user_active(user_active)

def unactivate(token):
    user_active = load_user_active()
    del user_active[token]
    save_user_active(user_active)

'''
database of all channels.
'''  
# loads and returns locally stored channel_all database.
### channel_all.json is a dictionary indexed by channel_id.
### channel_all['channel_id1'] is a dictionary of information unique to the user with channel_id 'channel_id1'.
### the keys in a channel dictionary are:
### 'channel_id','channel_name','owner_members_list','all_members_list','messages_list','standup'.a
def load_channel_all():
    with open("channel_all.json", "r") as FILE:
        channel_all = json.load(FILE)
        return channel_all

# saves to locally stored channel_all database.
def save_channel_all(channel_all):
    with open("channel_all.json", "w") as FILE:
        json.dump(channel_all, FILE)
        return

################################################################################
# FUNCTIONS FOR INTERACTING WITH DATABASES.
################################################################################

'''
functions for interacting with user_all
'''
# adds user to database given email, password, name_first, name_last.
def add_user(name_first, name_last, email, encrypted_password, token, u_id, handle_str, profile_img_url):
    user_all = load_user_all()
    # generate a user dictionary unique to the given user.
    user_data = {}
    user_data['name_first'] = name_first
    user_data['name_last'] = name_last
    user_data['email'] = email
    user_data['encrypted_password'] = encrypted_password
    user_data['token'] = token
    user_data['u_id'] = u_id
    user_data['handle'] = handle_str
    # user_data['permission_id'] = permission_id
    # recall that each u_id is unique.
    user_data['profile_img_url'] = profile_img_url
    user_all[u_id] = user_data
    save_user_all(user_all)
    return


def add_member(u_id, channel_id):
    member = {}
    data = load_user_all()
    member['u_id'] = u_id
    member['name_first'] = data[str(u_id)]['name_first']
    member['name_last'] = data[str(u_id)]['name_last']
    member['profile_img_url'] = data[str(u_id)]['profile_img_url']
    channel_all = load_channel_all()
    channel_all[channel_id]['member'].append(member)
    save_channel_all(channel_all)

def remove_member(u_id, channel_id):
    channel_all = load_channel_all()
    delete = [i for i in channel_all[channel_id]['member'] if i['u_id'] == u_id]
    channel_all[channel_id]['member'].remove(delete[0])
    save_channel_all(channel_all)

def add_channel(token, channel_id,name, is_public):
    channel = {}
    owner = {}
    data = load_user_all()
    u_id = helper.get_id(token,data)
    owner['u_id'] = u_id
    owner['name_first'] = data[str(u_id)]['name_first']
    owner['name_last'] = data[str(u_id)]['name_last']
    owner['profile_img_url'] = data[str(u_id)]['profile_img_url']
    channel_all = load_channel_all()
    channel['owner'] = []
    channel['owner'].append(owner)
    channel['name'] = name
    channel['access'] = is_public
    channel['member'] = []
    channel['messages'] = []
    # for use in standup.py
    channel['standup'] = {
        # if standup['is_active'] == False, 
        # then 'length' and 'time_finish' should never be accessed.
        'is_active': False, 
        'length': 0,
        'time_finish': 0,
        'message_queue': '',
    }
    channel_all[channel_id] = channel
    save_channel_all(channel_all)

def add_message(message_data,channel_id):
    channel_id = str(channel_id)
    data = load_channel_all()
    data[channel_id]['messages'].append(message_data)
    save_channel_all(data)

def add_owner(u_id, channel_id):
    owner = {}
    data = load_user_all()
    owner['u_id'] = u_id
    owner['name_first'] = data[u_id]['name_first']
    owner['name_last'] = data[u_id]['name_last']
    owner['profile_img_url'] = data[u_id]['profile_img_url']
    channel_all = load_channel_all()
    channel_all[channel_id]['owner'].append(owner)
    save_channel_all(channel_all)

def remove_owner(u_id, channel_id):
    channel_all = load_channel_all()
    delete = [i for i in channel_all[channel_id]['owner'] if i['u_id'] == u_id]
    channel_all[channel_id]['owner'].remove(delete[0])
    save_channel_all(channel_all)

def add_react(channel_id,message_id,react):
    u_id = react['u_ids'][0]
    channel_id = str(channel_id)
    channel_all = load_channel_all()
    message = channel_all[channel_id]['messages']
    for i in message:
        if i['message_id'] == message_id:
            if not i['reacts']:
               i['reacts'].append(react) 
            else:
                i['reacts'][0]['u_ids'].append(u_id)
    save_channel_all(channel_all)

def remove_react(channel_id,message_id,react):
    u_id = react['u_ids'][0]
    channel_id = str(channel_id)
    channel_all = load_channel_all()
    message = channel_all[channel_id]['messages']
    for i in message:
        if i['message_id'] == message_id:
                delete = [j for j in i['reacts'][0]['u_ids'] if j['u_id'] == u_id]
                i['reacts'][0]['u_ids'].remove(delete[0])
    save_channel_all(channel_all)
   