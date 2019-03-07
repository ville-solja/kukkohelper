# kukkohelper

## General
This discord bot is created originally for Kylmät Kukot game groups server in order to implement key features for the community.

### Streamer features
#### Notification
Users that have role Role-Streamer will have bot announce when they start streaming.

#### Invite link
Streamer receives DM from kukkohelper which contains a invite link to server. This invite link only grants temporary access to channels stream-chat & stream-voice. Original idea was that low view count streamers who aren't often looking at their twitch chat could invite the viewers to participate in VoIP chat. 

## Commands
### !help 
Displays a general list of available commands and brief usage tips as DM

### !list
List roles available for users as DM. Crucial part of !add command 

Includes commands for:
*Games
*Members
**Users who want to stick around and avoid prune
*Streamers
**Users who want to inform others when they go online
*Developers
**Users who are interested in viewing the test -channel and it's contents. Discuss with author regarding possibility of additional things to do.

### !remove <role>
Command that allows user to remove chosen role

_!remove dota_
_!remove streamer_

### !add <role>
Command that allows user to add chosen role
  
## Installation
For now just DM me as there's so many minor things that need adjusting in Discord's end before the bot actually functions correctly.

_!add dota_
_!add streamer_

### !dota random
Picks random hero from opendota API and then displays relevant data about that pick to the chat.

### !git
Displays link to the bots source in git
