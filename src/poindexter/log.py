#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Logger:
    def __init__(self, group_api):
        self.__api = group_api

    def __call__(self, user_id, log):
        self.__api.vk.messages.send(user_id=user_id, message=log)
        print(log)


def logable(before=None, after=None, pred=None, error_message=None):
    def decorator(func):
        def wrapped(*values, **keys):
            print(before)

            res = func(*values, **keys)
            if pred is not None and not pred(res):
                print(error_message)
                raise Exception(error_message)
            print(after)

            return res

        return wrapped

    return decorator
