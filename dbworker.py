from vedis import Vedis
import config


def get_current_state(user_id):
    with Vedis(config.vdb_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return config.States.S_ACTION_CHOICE.value


def set_states(user_id, value):
    with Vedis(config.vdb_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            raise Exception
