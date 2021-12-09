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
# Send No-Text Message, pprint(rocket.chat_post_message(None, 'room_name').json()) Mangler
# Pin Message, pprint(rocket.chat_pin_message('message_id').json()) Skal ikke implementeres endnu
# Unpin Message, pprint(rocket.chat_unpin_message('message_id').json()) Skal ikke implementeres endnu
# Star a Message, pprint(rocket.chat_star_message('message_id').json()) Skal ikke implementeres endnu
# Unstar a Message, pprint(rocket.chat_unstar_message('message_id').json()) Skal ikke implementeres endnu
# Search Chat Message, pprint(rocket.chat_search('room_id', search_text='text').json()) Skal ikke implementeres endnu
# Report a Message, pprint(rocket.chat_report_message('room_id', description='text').json()) Skal ikke implementeres endnu
# Follow a Message, pprint(rocket.chat_follow_message('message_id').json()) Skal ikke implementeres endnu
# Delete a Message, pprint(rocket.chat_delete('room_id', 'message_id').json()) Mangler
# Get Message Read Receipts, pprint(rocket.chat_get_message_read_receipts('message_id').json()) 
# Create/Start Direct Message, pprint(rocket.im_create('recipient_username').json()) Mangler i IMClass
# Direct Message History, pprint(rocket.im_history('room_id').json()) Mangler i IMClass
# Lists Members in Direct Message, pprint(rocket.im_members('room_id').json()) Mangler i IMClass
# Lists All Direct Messages, pprint(rocket.im_list().json()) Mangler i IMClass
# Lists Direct Message Counters, pprint(rocket.im_counters('room_id', 'username').json()) Mangler i IMClass
# Lists Latest Direct Message in ALL DM Channels, pprint(rocket.im_list_everyone().json()) Mangler i IMClass
# "Delete" a Direct Message, pprint(rocket.im_close('room_id').json()) Mangler i IMClass
# "Reopen" a Direct Message, pprint(rocket.im_open('room_id').json()) Mangler i IMClass
# Create New Channel, pprint(rocket.channels_create('new_channel_name').json()) Lavet i ChannelClass
# Invite User to channel, pprint(rocket.channels_invite('room_id', 'recipient_user_id').json()) Lavet i ChannelClass
# Lists All Channels, pprint(rocket.channels_list().json()) Lavet i ChannelClass
# Lists Channels Joined, pprint(rocket.channels_list_joined().json()) Lavet i ChannelClass
# Lists Channel Info, pprint(rocket.channels_info('room_id/room_name').json()) Lavet i ChannelClass
# Lists Channel History, pprint(rocket.channels_history('room_id', count=5).json()) Lavet i ChannelClass
# Lists Channel Moderators, pprint(rocket.channels_moderators('room_id/room_name').json()) Mangler i ChannelClass
# Add ALL Users to a Channel, pprint(rocket.channels_add_all('room_id').json()) Mangler i ChannelClass
# Add User as Channel Owner, pprint(rocket.channels_add_owner('room_id', 'new_owner_user_id', 'new_owner_username').json()) Skal ikke implementeres endnu
# Remove User as Channel Owner, pprint(rocket.channels_remove_owner('room_id', 'other_user_id').json()) Skal ikke implementeres endnu
# Add User as Channel Leader, pprint(rocket.channels_add_leader('room_id', 'new_leader_user_id').json()) Skal ikke implementeres endnu
# Remove User as Channel Leader, pprint(rocket.channels_remove_leader('room_id', 'other_user_id').json()) Skal ikke implementeres endnu
# Add User as Channel Moderator, pprint(rocket.channels_add_moderator('room_id', 'new_moderator_user_id').json()) Skal ikke implementeres endnu
# Remove User as Channel Moderator, pprint(rocket.channels_remove_moderator('room_id', 'other_user_id').json()) Skal ikke implementeres endnu
# Rename existing Channel, pprint(rocket.channels_rename('room_id', 'new_room_name').json()) Mangler i Channel Rooms
# "Delete" a Channel, pprint(rocket.channel_close('room_id').json()) Skal ikke implementeres endnu
# "Reopen" a Channel, pprint(rocket.channel_open('room_id').json()) Skal ikke implementeres endnu
# Permanently Delete a Channel, pprint(rocket.channels_delete('room_id').json()) Lavet i ChannelClass
# Archive a Channel, pprint(rocket.channels_archive('room_id/room_name').json()) Skal ikke implementeres endnu
# Unarchive a Channel, pprint(rocket.channels_unarchive('room_id/room_name').json()) Skal ikke implementeres endnu
# Create a User. pprint(rocket.users_create('name@justa.chat', 'name', 'password', 'username').json()) Mangler
# Delete a User, pprint(rocket.users_delete('user_id') Mangler
# List User info, pprint(rocket.users_info('user_id/username').json()) Mangler
# Lists Users Presence, pprint(rocket.users_get_presence('user_id').json()) Mangler
# Create User Token (needs permissions), pprint(rocket.users_create_token('user_id').json()) Mangler
# Update User Info (totp-required), pprint(rocket.users_update('user_id', email='email@domain.com', name='new_name', password='user_password', username='new_username').json())
# Update User Active Status (Disable Account), pprint(rocket.users_set_active_status('dubHtZnsmDkST4Nay', True).json()) Skal ikke implementeres endnu
# Set User Status, pprint(rocket.users_set_status(message='status_to_display', status='online/away/offline/busy').json()) Lavet i MyUserClass
# Set User Preferences, pprint(rocket.users_set_preferences('user_id', data={"preference": True/False}).json()) Mangler
# Get User Prefernces, pprint(rocket.users_get_preferences().json()) Mangler
# Set User Avatar from URL, pprint(rocket.users_set_avatar('URL').json()) Mangler
# Set User Avatar from file, pprint(rocket.users_set_avatar("filepath").json()) Mangler
# List Permissions, pprint(rocket.permissions_list_all().json())
# List Permissions with Updated Since, pprint(rocket.permissions_list_all(updatedSince="YYYY-MM-DDTHH:MM:SS.248Z").json()) Skal ikke implementeres endnu