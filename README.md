# KukkoHelper

## General
This discord bot is created originally for Kylmät Kukot game groups server in order to implement key features for the community. 

## Streamer features
#### Notification
Users that have role Role-Streamer will have bot announce when they start streaming.

## NSFW -filter
* User posts an image attachment
.gif is not currently supported and link previews are not checked either
* Attachment url is sent to Azure cognitive services
If it's NSFW process continues
* Channel is checked for nsfw status
If it safe for work (As in the status NSFW is not enabled) process continues
* Image is removed from the channel and it's NSFW rating is posted instead

## Commands
### !help 
Displays a general list of available commands and brief usage tips as DM

### !list
List roles available for users as DM. Crucial part of !add command 

Includes:
* Games (Based on current roles created)
* Members (Users who want to stick around and avoid prune)
* Streamers (Users who want to inform others when they go online)
* Developers (Users who are interested in viewing the test -channel and it's contents)

### !remove <role>
Command that allows user to remove chosen role

_!remove dota_
_!remove streamer_

### !add <role>
Command that allows user to add chosen role

_!add dota_
_!add streamer_

### !dota random
Picks random hero from opendota API and then displays relevant data about that pick to the chat.

### !wordcloud
Creates a wordcloud from the current channel. Links/emojis/commands/short messages will be excluded. Picture will be then posted to that channel.

## Installation
### Env variables for docker image
#### Azure Key
If you want to make use of the Azure cognitive services, you need to provide the access key for that as an environment variable

Example: "KEY=key with length of 32 characters"

Also make sure your cognitive services is using north europe URL:
"https://northeurope.api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures=adult"

#### Discord bot token
In order to provide access for the bot you need to provide it with the appropriate access token 

Example: "TOKEN=token with length of 59 characters"

Currently only the discord bot token is mandatory