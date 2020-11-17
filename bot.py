import discord
import asyncio
import valve.rcon

class Bot( discord.Client ):
	def __init__( self, *args, **kwargs ):
		super( ).__init__( *args, **kwargs )

		self.__servers__ = { }
		self.__servers__[ "SERVER_NAME_01" ] = { 
				              "ip_address": "127.0.0.1",  # Server IP Address
				              "port":       27015,        # RCON Port
					      "password":   "Password",   # RCON Password
					     }

		self.__servers__[ "SERVER_NAME_02" ] = { 
				              "ip_address": "127.0.0.1",  # Server IP Address
				              "port":       27017,        # RCON Port
					      "password":   "Password",   # RCON Password
					     }

		self.__servers__[ "SERVER_NAME_03" ] = { 
				              "ip_address": "127.0.0.2",  # Server IP Address
				              "port":       27015,        # RCON Port
					      "password":   "AnotherPassword",   # RCON Password
					     }

	async def on_ready( self ):
		#print( "Logged in as: {}".format( self.user ) )
		#print( "  my_id: {}\n".format( self.user.id ) )

		self.__mention_string__ = "<@!{}>".format( self.user.id )

	async def on_message( self, message ):
		if message.author == self.user:
			return

		#print( "  message.content: [{}]".format( message.content ) )

		if not self.user in message.mentions:
			return

		if not message.content.startswith( self.__mention_string__ ):
			return

		await self.handle_command( message )

	async def handle_ping_command( self, message ):
		#print( "handle_ping_command:" )
		await message.channel.send( "pong!" )

	async def handle_list_command( self, message ):
		reply = "Server List:\n"

		if len( self.__servers__ ) == 0:
			reply += "  No servers configured"
			await message.channel.send( message )
			return

		for s in self.__servers__:
			ip   = self.__servers__[ s ][ "ip_address" ]
			port = self.__servers__[ s ][ "port" ]

			reply += "  {}:  IP Address: {}, Port: {}\n".format( s, ip, port )

		await message.channel.send( reply )

	async def handle_rcon_command( self, message ):
		words = message.content.split( ' ' )
		if len( words ) < 4:
			reply = "Error: invalid parameters\n"
			reply += "  Usage:\n    @{} rcon <server-name> <rcon-command>\n".format( self.user.name )
			reply += "  E.g:\n    @P{} rcon ark-server-name listplayers\n".format( self.user.name )
			await message.channel.send( reply )
			return

		command      = words[ 1 ]
		server_name  = words[ 2 ]
		rcon_command = " ".join( words[ 3: ] )

		if not server_name in self.__servers__:
			reply = "Error: server name not found in list of servers"
			await message.channel.send( reply )
			return

		#print( "  RCON {} {}".format( server_name, rcon_command ) )

		ip           = self.__servers__[ server_name ][ "ip_address" ]
		port         = self.__servers__[ server_name ][ "port" ]
		password     = self.__servers__[ server_name ][ "password" ]
		server_tuple = ( ip, port )

		try:
			rcon = valve.rcon.RCON( server_tuple, password, multi_part = False )
			rcon.connect( )
			rcon.authenticate( )
			response = rcon.execute( rcon_command, timeout = 10 )

		except ( valve.rcon.RCONError, ConnectionRefusedError ) as e:
			await message.channel.send( "Failed to connect to server '{}'".format( server_name ) )
			rcon.close( )
			return

		except valve.rcon.RCONAuthenticationError as e:
			await message.channel.send( "Failed to authenticate to server '{}'".format( server_name ) )
			rcon.close( )
			return

		except valve.rcon.RCONTimeoutError as e:
			await message.channel.send( "Timeout waiting for response from server '{}'".format( server_name ) )
			rcon.close( )
			return

		except valve.rcon.RCONCommunicationError as e:
			await message.channel.send( "Error communicating with server '{}'".format( server_name ) )

		await message.channel.send( "Server response:\n{}".format( response.text ) )

		rcon.close( )
			

	async def handle_command( self, message ):
		#print( "handle_command:" )

		words = message.content.split( ' ' )
		#print( "  words: [{}]".format( words ) )

		if len( words ) < 2:
			await message.channel.send( "Unrecognised command" )
			return

		command = words[ 1 ]
		#print( "  command: [{}]".format( command ) )

		if command == "ping":
			await self.handle_ping_command( message )
		elif command == "list-servers":
			await self.handle_list_command( message )
		elif command == "rcon":
			await self.handle_rcon_command( message )
		else:
			await message.channel.send( "Unrecognised command" )



