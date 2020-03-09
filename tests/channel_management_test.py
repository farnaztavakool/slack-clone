# Feature 4: Ability to create a channel, join a channel, invite someone else to a channel, and leave a channel
import pytest
import auth
import channels
import channel
from error import InputError
from error import AccessError

@pytest.fixture
def get_new_user_1():
    user = auth.auth_register('bullshit@gmail.com', '1248901ha', 'Tim', 'Fan')
    return (user['u_id'], user['token'])

@pytest.fixture
def get_new_user_2():
    user = auth.auth_register('corbyQS@gmail.com', 'KACKACKACKAC', 'Beomjun', 'Kim')
    return (user['u_id'], user['token'])

valid_channel_name_1 = 'channel1'
valid_channel_name_2 = 'channel2'
invalid_channel_name_1 = 'ThisIsAnInvalidChannelNameAsItIsTooLong'

'''
testing channels_create()
'''

def test_channels_create_no_channels(get_new_user_1):
    # dummy users.
    u_id_1, token_1 = get_new_user_1
    my_channel_list_1 = channels.channelslistall(token_1)
    assert len(my_channel_list_1) == 0

def test_channels_create_one_valid_public_channel(get_new_user_1):
    # dummy users.
    u_id_1, token_1 = get_new_user_1
    channel1 = channels.channels_create(token_1,valid_channel_name_1,True)
    my_channel_list_1 = channels.channelslistall(token_1)
    assert len(my_channel_list_1) == 1

def test_channels_create_one_invalid_public_channel(get_new_user_1):
    # dummy users.
    u_id_1, token_1 = get_new_user_1
    with pytest.raises(InputError) as e:
        channel1 = channels.channels_create(token_1,invalid_channel_name_1,True)

def test_channels_create_one_valid_private_channel(get_new_user_1, get_new_user_2):
    # dummy users.
    u_id_1, token_1 = get_new_user_1
    u_id_2, token_2 = get_new_user_2
    # user_1 creates private channel, user_2 does not have access to this channel.
    channel1 = channels.channels_create(token_1,valid_channel_name_1,False)
    my_channel_list_2 = channels.channelslistall(token_2)
    assert len(my_channel_list_2) == 0

def test_channels_create_one_valid_public_one_valid_private_channel(get_new_user_1, get_new_user_2):
    # dummy users.
    u_id_1, token_1 = get_new_user_1
    u_id_2, token_2 = get_new_user_2
    # user_1 creates public channel, user_2 has access to this channel.
    channel1 = channels.channels_create(token_1,valid_channel_name_1,True)
    # user_1 creates private channel, user_2 does not have access to this channel.
    channel2 = channels.channels_create(token_1,valid_channel_name_2,False)
    my_channel_list_2 = channels.channelslistall(token_2)
    assert len(my_channel_list_2) == 1

'''
testing channel_join()
positive testing for this function in channels_list().
'''

def test_channel_join_invalid_channel(get_new_user_1, get_new_user_2):
    # dummy users.
    u_id_1, token_1 = get_new_user_1
    u_id_2, token_2 = get_new_user_2
    # user_1 creates public channel, user_2 has access to this channel.
    channel1 = channels.channels_create(token_1,valid_channel_name_1,True)
    # note that below is based on assumption.
    # user_1 leaves this channel, which causes the channel to be removed, making its channel_id invalid.
    # so when user_2 attempts to join channel, throw InputError.
    invalid_channel_id = channel1['channel_id']
    channel.channel_leave(token_1,channel1['channel_id'])
    with pytest.raises(InputError) as e:
        channel.channel_join(token_2,invalid_channel_id)

