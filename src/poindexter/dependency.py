import inject
from Bot.VkBot import VKBot


def bot_config(binder):
    binder.bind_to_constructor(VKBot, VKBot())

