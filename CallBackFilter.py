from telebot import AdvancedCustomFilter, types
from telebot.callback_data import CallbackDataFilter


class CallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)
