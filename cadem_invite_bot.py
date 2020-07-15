import discord
from discord.ext import commands
from discord.utils import get
import time
import asyncio
import sql_to_bot
from sqlite3 import InterfaceError


command_list = ["+invited_by", "+print_top_test", "+print_user_list",
                "+help", "+get_top_users", "+get_amount_of_user"]
TOKEN = ""
client = commands.Bot(command_prefix="+")  # the comand prefix
client.remove_command("help")
sql_admin = sql_to_bot.sql_mang()


@client.event
async def on_ready():
    '''this function run when the bot is becoming online gather all the info on the servers users'''
    print("[+]Bot is ready.")
    await client.change_presence(activity=discord.Game(name="+help to get help"))
    name_id = client.get_all_members()
    for i in name_id:
        user_data = str(i).split("#")
        sql_admin.add_to_all_users(int(user_data[1]), user_data[0])
    sql_admin.print_all_users()


@client.event
async def on_message(message):
    '''this function run when ever someone is sending a messege it chack if it ment for the bot'''
    channel = message.channel
    content = message.content
    command = ""

    for i in content:
        if not i == " ":
            command += i
        else:
            break

    if command.startswith("+") and command not in command_list:
        await channel.send("cant find command please use the +help comand to get the avilabel comands")
    elif command in command_list:
        await client.process_commands(message)


@client.command(pass_context=True)
async def invited_by(ctx, name):
    '''the function the bot is built for it the main for this option'''
    global sql_admin
    user_data = str(ctx.author).split("#")
    my_id = int(user_data[1])
    my_user_name = user_data[0]
    inviter_id = sql_admin.find_user_id(name)

    #print(my_user_name, my_id, inviter_id)

    if inviter_id and not sql_admin.if_exist_at_all(int(inviter_id)):
        inviter_id = int(inviter_id)
        if sql_admin.if_used(my_id):
            sql_admin.add_user(my_user_name, my_id)
            sql_admin.add_to_already_used(my_user_name, my_id, name)
            sql_admin.update_invite_amount(inviter_id)

            await ctx.send("added sucssesfully")

            if sql_admin.get_invite_ammount(inviter_id) == 5:
                await give_role(ctx, name)
        else:
            await ctx.send("you can only get invited once")

    else:
        await ctx.send("coudnt find a user with the given name")


@client.event
async def on_member_join(member):
    '''this function run when ever a member join to add him to the existing users table'''
    member_data = str(member).split("#")
    sql_admin.add_to_all_users(int(member_data[1]), member_data[0])


@client.event
async def on_member_remove(member):
    '''when a member is removed it remove him from the db'''
    sql_admin.delete_user(member.id)
    sql_admin.delete_user_from_exist(member.id)
    sql_admin.delete_user_from_server(member.id)


@client.command(pass_context=True)
async def help(ctx):
    '''this is the help command'''
    author = ctx.message.author
    channel = ctx.message.channel

    embed = discord.Embed(  # create embed messeg
        colour=discord.Colour.red()  # give it a color
    )

    embed.set_author(name="help")  # set the tittel
    embed.add_field(name="+invited_by", value="give one point to the user who invited you",
                    inline=False)  # give it some content
    # embed.add_field(name = "+print_top_test" , value = "send the pointes the top users have",inline=False)      #give it some content
    # await channel.send("{0} I sent you a privet meesege with the avilable commands go check your inbox".format(author))
    await author.send(embed=embed)


@client.command(pass_context=True)
# This must be exactly the name of the appropriate role
@commands.has_role("new role")
async def give_role(ctx, name: str):
    '''still working  on this part'''
    role = get(ctx.message.guild.roles, id=721691189828649091)
    name_id = client.get_all_members()

    for i in name_id:
        if str(i.name) == name:
            await i.add_roles(role)


@client.command(pass_contex=True)
async def get_top_users(ctx):
    data_list = sql_admin.find_users()
    sorted(data_list, key=lambda x: x[2])
    embed = discord.Embed(  # create embed messeg
        colour=discord.Colour.red()  # give it a color
    )

    embed.set_author(name="leader board")  # set the tittel
    for i in data_list:
        embed.add_field(name=f"{i[0]}#{i[1]}", value=i[2], inline=False)

    await ctx.send(embed=embed)


@client.command(pass_contex=True)
async def get_amount_of_user(ctx, name):
    user_id = sql_admin.find_user_id(name)
    try:
        amount = sql_admin.get_invite_ammount(user_id)
        await ctx.send(amount)
    except InterfaceError:
        await ctx.send("coudnt find a user with the given name")


if __name__ == "__main__":
    with sql_admin:
        client.run(TOKEN)
