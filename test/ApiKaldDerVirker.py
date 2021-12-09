from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat


with sessions.Session() as session:
    rocket = RocketChat('christian', 'SuperStrong123!', server_url='http://justa.chat:3000/', session=session)
    pprint(rocket.service_configurations().json())
    #pprint(rocket.channels_list().json())

####################################################################################################################################
# Lists Own User Info, pprint(rocket.me().json()) Ligger i MyUserClass
# Send Message IM/CHANNEL/DISCUSSION, pprint(rocket.chat_post_message('besked', channel='room_id').json()) Mangler
# Send No-Text Message, pprint(rocket.chat_post_message(None, 'room_name').json())
# Pin Message, pprint(rocket.chat_pin_message('message_id').json())
# Unpin Message, pprint(rocket.chat_unpin_message('message_id').json())
# Star a Message, pprint(rocket.chat_star_message('message_id').json())
# Unstar a Message, pprint(rocket.chat_unstar_message('message_id').json())
# Search Chat Message, pprint(rocket.chat_search('room_id', search_text='text').json())
# Report a Message, pprint(rocket.chat_report_message('room_id', description='text').json())
# Follow a Message, pprint(rocket.chat_follow_message('message_id').json())
# Delete a Message, pprint(rocket.chat_delete('room_id', 'message_id').json()) Mangler
# Get Message Read Receipts, pprint(rocket.chat_get_message_read_receipts('message_id').json())
# Create/Start Direct Message, pprint(rocket.im_create('recipient_username').json())
# Direct Message History, pprint(rocket.im_history('room_id').json()) Mangler i IM
# Lists Members in Direct Message, pprint(rocket.im_members('room_id').json()) Mangler i IM
# Lists All Direct Messages, pprint(rocket.im_list().json()) Mangler i IM
# Lists Direct Message Counters, pprint(rocket.im_counters('room_id', 'username').json()) Mangler i IM
# Lists Latest Direct Message in ALL DM Channels, pprint(rocket.im_list_everyone().json()) Mangler i IM
# "Delete" a Direct Message, pprint(rocket.im_close('room_id').json()) Mangler i IM
# "Reopen" a Direct Message, pprint(rocket.im_open('room_id').json()) Mangler i IM
# Create New Channel, pprint(rocket.channels_create('new_channel_name').json()) Lavet i Public 
# Invite User to channel, pprint(rocket.channels_invite('room_id', 'recipient_user_id').json())
# Lists All Channels, pprint(rocket.channels_list().json())
# Lists Channels Joined, pprint(rocket.channels_list_joined().json())
# Lists Channel Info, pprint(rocket.channels_info('room_id/room_name').json())
# Lists Channel History, pprint(rocket.channels_history('room_id', count=5).json())
# Lists Channel Moderators, pprint(rocket.channels_moderators('room_id/room_name').json())
# Add ALL Users to a Channel, pprint(rocket.channels_add_all('room_id').json())
# Add User as Channel Owner, pprint(rocket.channels_add_owner('room_id', 'new_owner_user_id', 'new_owner_username').json())
# Remove User as Channel Owner, pprint(rocket.channels_remove_owner('room_id', 'other_user_id').json())
# Add User as Channel Leader, pprint(rocket.channels_add_leader('room_id', 'new_leader_user_id').json())
# Remove User as Channel Leader, pprint(rocket.channels_remove_leader('room_id', 'other_user_id').json())
# Add User as Channel Moderator, pprint(rocket.channels_add_moderator('room_id', 'new_moderator_user_id').json())
# Remove User as Channel Moderator, pprint(rocket.channels_remove_moderator('room_id', 'other_user_id').json())
# Rename existing Channel, pprint(rocket.channels_rename('room_id', 'new_room_name').json())
# "Delete" a Channel, pprint(rocket.channel_close('room_id').json())
# "Reopen" a Channel, pprint(rocket.channel_open('room_id').json())
# Permanently Delete a Channel, pprint(rocket.channels_delete('room_id').json())
# Archive a Channel, pprint(rocket.channels_archive('room_id/room_name').json())
# Unarchive a Channel, pprint(rocket.channels_unarchive('room_id/room_name').json())
# Create a User. pprint(rocket.users_create('name@justa.chat', 'name', 'password', 'username').json())
# Delete a User, pprint(rocket.users_delete('user_id')
# List User info, pprint(rocket.users_info('user_id/username').json())
# Lists Users Presence, pprint(rocket.users_get_presence('user_id').json())
# Create User Token (needs permissions), pprint(rocket.users_create_token('user_id').json())
# Update User Info (totp-required), pprint(rocket.users_update('user_id', email='email@domain.com', name='new_name', password='user_password', username='new_username').json())
# Update User Active Status (Disable Account), pprint(rocket.users_set_active_status('dubHtZnsmDkST4Nay', True).json())
# Set User Status, pprint(rocket.users_set_status(message='status_to_display', status='online/away/offline/busy').json())
# Set User Preferences, pprint(rocket.users_set_preferences('user_id', data={"preference": True/False}).json())
# Get User Prefernces, pprint(rocket.users_get_preferences().json())
# Set User Avatar from URL, pprint(rocket.users_set_avatar('URL').json())
# Set User Avatar from file, pprint(rocket.users_set_avatar("filepath").json())
# List Permissions, pprint(rocket.permissions_list_all().json())
# List Permissions with Updated Since, pprint(rocket.permissions_list_all(updatedSince="YYYY-MM-DDTHH:MM:SS.248Z").json())