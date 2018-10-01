#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Handlers import bot_commands
from credentials import vk_token
from Bot.VkBot import VKBot


# if you want use bot by community token
bot = VKBot(token=vk_token, commands=bot_commands)
# if you want use bot by your account
# bot = VKBot(log='your_login', passwd='your_passwd')
bot.run()
