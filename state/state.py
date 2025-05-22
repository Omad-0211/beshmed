from aiogram.dispatcher.filters.state import State, StatesGroup

class ReportStates(StatesGroup):
    waiting_for_person = State()
    waiting_for_comment = State()