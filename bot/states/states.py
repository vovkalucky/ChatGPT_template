from aiogram.fsm.state import State, StatesGroup, default_state


class UseGPT(StatesGroup):
    state1_user_request = State()
    state2_user_request_voice = State()
    state1_group_user_request = State()

