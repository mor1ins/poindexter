#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Logger:
    BEGIN_MESSAGE = u"Привет! Я бот для загрузки конспектов в группу."
    NO_ADMIN_MESSAGE = u"Интерфейс для пользоватей в данный момент не реализован."

    START_VK_DL = u"Необходимо загрузить zip-архивы с фотографиями конспектов\n" \
                  u"-- все фото должны лежать на первом уровне вложенности (никаких папок в архиве)\n" \
                  u"-- имя архива должно удовлетворять паттерну"
    START_PS_DL = u"Пока не реализовано."

    DOC_IN_QUEUE = u"Документов добавлено в очередь: %d\n"

    START_DL_NOTES = u"Начинаем загрузку конспектов"
    SUCCESS_ADD_NOTE = u"успешно!\n"
    ERROR_ADD_NOTE = u"ошибка!\n"
    NOTHING_FOR_DL = u"Нечего грузить"
    END_DL_NOTES = u"Загрузка завершена."

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
