import logging

from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)

from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        logging.exception("Can't demote chat creator")
        return True

    elif isinstance(exception, MessageNotModified):
        logging.exception('Message is not modified')
        return True
    elif isinstance(exception, MessageCantBeDeleted):
        logging.exception('Message cant be deleted')
        return True

    elif isinstance(exception, MessageToDeleteNotFound):
        logging.exception('Message to delete not found')
        return True

    elif isinstance(exception, MessageTextIsEmpty):
        logging.exception('MessageTextIsEmpty')
        return True

    elif isinstance(exception, Unauthorized):
        logging.exception(f'Unauthorized: {exception}')
        return True

    elif isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    elif isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    elif isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    elif isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    logging.exception(f'Update: {update} \n{exception}')
