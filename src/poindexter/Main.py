#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Handlers import *

bot = inject.instance(VKBot)
bot.auth()
bot.run()
