# KukkoHelper

## General
This discord bot is created originally for Kylmät Kukot -server (hence the name) in order to implement key features for the community. 

Functionalities are simple and you can quickly check the source code, before building the image and hosting it yourself. This way you'll have 100% control and understanding of what the bot does before adding it to your server.

## Commands
### General
* /ping
* /print_stats

### Club
* /list
* /join + /quit
* /create + /delete
* /archive + /respawn

### Dota
* /random

## Installation
* Create channel categories "CLUB" & "ARCHIVE" on discord server
* Create a bot for your discord server (see discord's documentation on this)
* Build the docker image
* Run the bot on docker with your token (environment variable "token")
* Create a server role that can manage the clubs (default is "club-admin")

## Adding cogs / for devs
Bot loads all env variables to conf[] dictionary, so you can add your own easily. Add new cogs to default_conf["initial_extensions"] in kukkobot.py.
