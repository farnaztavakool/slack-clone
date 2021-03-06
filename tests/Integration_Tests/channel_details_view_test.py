# Feature 5: Within a channel, ability to view all messages, view the members of the channel, and the details of the channel

import pytest
import pytest
import message
import auth
from error import AccessError
from error import InputError
from channel import channel_messages, channel_details
import channels

@pytest.fixture
def authUser():
    message_id = 0
    return auth.auth_register("somebody@gmail.com", "password", "firstName", "lastName")
    
@pytest.fixture
def unAuthUser():
    return auth.auth_register("somebody2@gmail.com", "password", "firstName", "lastName")
    
@pytest.fixture
def channel_id(authUser):
    channel_id = channels.channels_create(authUser['token'], 'channel1', True)['channel_id']
    return channel_id

        
# Test if the channel id is not valid  
def test_channel_id_valid(channel_id):
    with pytest.raises(InputError):
        assert(channel_id >= 1)
    
# test details function if user it not a member of the channel
def test_details_user_member(authUser, channel_id):
    for i in range(len(channel_details(authUser['token'], channel_id)['all_members'])):
        if (channel_details(authUser['token'], channel_id)['all_members'][i]['name_first'] == "firstName"):
            raise AccessError()

# test if index start is greater than total messages
def test_index_greater(authUser, channel_id):
    with pytest.raises(AccessError):
        assert(channel_messages(authUser['token'], channel_id, 0)['start'] > channel_messages(authUser['token'], channel_id, 0)['messages'][-1]['message_id'])
        
# test messages function if user is not member of channel
def test_messages_user_member(authUser, channel_id):
    for i in range(len(channel_messages(authUser['token'], channel_id, 0)['messages'])):
        if (channel_messages(authUser['token'], channel_id, 0)['messages'][i]['u_id'] == authUser['u_id']):
            raise AccessError()
        
# test messages function returns 3 elements
def test_messages_return(authUser, channel_id):
    assert(len(channel_messages(authUser['token'], channel_id, 0)) == 3)
    
# test messages function returns -1 in "end" after showing oldest messages
def test_messages_oldest(authUser, channel_id):
    if channel_messages(authUser['token'], channel_id, 0)['messages'][0]['message_id'] == channel_messages(authUser['token'], channel_id, 0)['end']:
        assert(channel_messages(authUser['token'], channel_id)['end'] == -1)
        
# test messages function only displays 50 messages at most
def test_messages_display(authUser, channel_id):
    assert((channel_messages(authUser['token'], channel_id, 0)['start']) + 50 == channel_messages(authUser['token'], channel_id, 0)['end'])
    



 

