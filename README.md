# Trello Integration for Discord

## Aim

To write a program that is integrated into Discord, that allows users from within a text channel to perform functions on a Trello board, as well as receive DM notifications when specific events occur on Trello.

## Outcomes

Authoring this project would be great for my credentials as it would show:

- Deployment of server-less tech, specifically AWS Lambda functions.
- Ability to use a NOSQL database.
- Ability to integrate with 3rd party applications, through webhooks.
- Use of the SAM build tool, and Cloudformation transitively.

## Functionality

### Persisted Data

In order for the program to function, there are 2 entities which need to be persisted:

- Guilds: This entity maps a Discord Guild to a Trello Board, and contains Guild-wide settings.
- Users: This entity maps a Discord User to a Trello User, and contains User-specific settings.

### Guilds

- `guild_id` Snowflake ID of Discord Guild.
- `board_id` Trello board ID of tracked board.
- `create_list` Trello list ID of where created cards are placed.

### Users

- `discord_id` Snowflake ID of Discord User.
- `trello_id` Trello User ID
- `access_token` Access token for Trello User.
- `config` Object containing user settings such as whether notifications are turned on

### Trello Side

The Trello side of the application involves a single webhook, that gets called when an action occurs on a registered board. It will check to see if the event was `memberAddedToCard` event, and if present in the database, send a DM to the relevant user on Discord.

### Discord Side

This side of the application will allow a user to create a card on the linked Trello board, as well as manage the application settings. The app is completely controlled through slash commands.

The root command of the application is `trello` , which is in turn organized into a set of sub commands:

- `trello create name=string [description=string] [add-users]`: Creates a new card on the set Trello List. Name is required. If command is replying to a message, the body of the message will be used as the Card Description, but can optionally be provided. Add users will cause the bot to fetch the users from the Trello board and display them as a multi-select component back to the discord user, who can then add users to the card. The command fails if there is no board or list set, if the user hasn't authenticated with Trello, or the user doesn't have access to the set board.
- `trello login | logout`:  Privately links the user to an OAuth flow to integrate with Trello. If the user successfully completes the flow, then the Bot will DM the user. If the logout flag is provided, the user entry is deleted from the data store.
- `trello config board | list | subscribe`: Allows the user to multi-select which boards they would like to receive notifications for, similar in style to the add-users function in the create command. If the user is admin, they can also configure the board and list which is linked to the guild. This will fail if the user does not have ManageGuild permissions for Discord or isn't an admin for the Trello board they are trying to link.