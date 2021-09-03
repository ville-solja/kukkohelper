# KukkoHelper

## General
This discord bot is created originally for Kylmät Kukot game groups server in order to implement key features for the community. 

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
Displays a general list of available commands and brief usage tips

## Installation
### Env variables
* token -> Your Discord bot token
* azure_key -> Your Azure key
* azure_url_ext -> Your Azure cloud URL, for example https://northeurope.api.cognitive.microsoft.com/vision/v3.2/analyze?visualFeatures=Adult&language=en&model-version=latest
* command_prefix -> Bot command prefix'

Currently only the discord bot token is mandatory. NSFW filter is ON by default. Turn it off in kukkobot.py if you don't plan on using it.

## Adding cogs / for devs
Bot loads all env variables to conf[] dictionary, so you can add your own easily. Add new cogs to default_conf["initial_extensions"] in kukkobot.py.
