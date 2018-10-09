#! /usr/bin/env python
# -*- coding: utf-8 -*-

import dependency
from Handlers import *

bot = inject.instance(VKBot)
bot.auth()
bot.run()
