import time

import redis
from datetime import timedelta
from collections.abc import MutableMapping

from app.core import redis_settings,user_settings


def __setflat_skeys__(
        r: redis.Redis,
        obj: dict,
        prefix: str,
        delim: str = ":",
        *,
        _autopfix=""
) -> None:
    allowed_vtypes = (str, bytes, float, int)
    for key, value in obj.items():
        key = _autopfix + key
        if isinstance(value, allowed_vtypes):
            r.set(f"{prefix}{delim}{key}", value)
        elif isinstance(value, MutableMapping):
            __setflat_skeys__(
                r, value, prefix, delim, _autopfix=f"{key}{delim}"
            )
        else:
            raise TypeError(f"Unsupported value type: {type(value)}")


def study_room_starting():
    return {
        "status": "study",
        "study_rooms": "",
        "last_access": 1,
        "sleep": {
            "count": 0,
            "sec": 0
        },
        "phone": {
            "count": 0,
            "sec": 0
        },
        "await": {
            "count": 0,
            "sec": 0
        },
        "rest": {
            "count": 0,
            "sec": 0
        }
    }


def __generate_value_string__(user_id, user_monitoring, disturb_info=None):
    if disturb_info is None:
        return f"{user_id}:{user_monitoring}"
    return f"{user_id}:{user_monitoring}:{disturb_info}"


class redis_function:
    redis = redis.Redis(port=redis_settings.PORT, host=redis_settings.HOST, charset="utf-8", decode_responses=True)
    # redis = redis.Redis(port=6000, host='localhost', charset="utf-8", decode_responses=True)

    def __del__(self):
        self.redis.close()

    def logout(self, token: str, user_email: str):
        self.redis.setex(token, timedelta(minutes=user_settings.ACCESS_TOKEN_EXPIRE_MINUTES), user_email)

    def check_black_list(self, token: str):
        self.redis.exists(token)

    def start_study_init(self, user_id: str):
        __setflat_skeys__(self.redis, study_room_starting(), user_id)

    def set_study_room(self, user_id: str, study_room_id: str):
        self.redis.set(__generate_value_string__(user_id, "study_rooms"), study_room_id)

    def get_user_study_info(self, user_id, user_monitoring, disturb_info=None):
        return self.redis.get(
            __generate_value_string__(user_id, user_monitoring, disturb_info)
        )

    def check_join(self, user_id: str):
        return self.redis.get(
            __generate_value_string__(user_id, 'study_rooms')
        )

    def add_current_log(self, user_id, disturb_type, disturb_time):
        # status를 업데이트 해야함
        # 이 때, 이전 상태를 저장해야 함.
        status_key = __generate_value_string__(user_id, "status")
        last_status = self.redis.get(status_key)
        self.redis.set(status_key, disturb_type)

        # 이전 상태가 study가 아닐 경우 last_access와 비교하여 시간을 알아내야 함.
        last_access_key = __generate_value_string__(user_id, "last_access")
        last_access = self.redis.get(last_access_key)

        self.redis.set(last_access_key, disturb_time)

        print(f"User(id : {user_id}) update status({last_status}-> {disturb_type}).")

        if last_status != "study":
            status_time = disturb_time - float(last_access)
            self.redis.incr(__generate_value_string__(user_id, last_status, 'count'), 1)
            self.redis.incr(__generate_value_string__(user_id, last_status, 'sec'), int(status_time))
            print(f"Save Status Log({last_status} {int(status_time)}sec.)")

    def delete_user_study_info(self, user_id: str):
        target_key = self.redis.keys(f"{user_id}:*")
        for key in target_key:
            self.redis.delete(key)

    def end_study(self, user_id: str):
        if not self.check_join(user_id):
            return None

        self.add_current_log(user_id, "study", time.time())
        result = self.get_user_all_info(user_id)
        self.delete_user_study_info(user_id)

        return result

    def get_status_value(self, user_id: str, status: str):
        return {
            "count": self.redis.get(__generate_value_string__(user_id, status, 'count')),
            "sec": self.redis.get(__generate_value_string__(user_id, status, 'sec'))
        }

    def get_user_all_info(self, user_id: str):
        study_room_id = self.redis.get(__generate_value_string__(user_id, "study_rooms"))
        sleep_values = self.get_status_value(user_id, "sleep")
        phone_values = self.get_status_value(user_id, "phone")
        await_values = self.get_status_value(user_id, "await")
        rest_values = self.get_status_value(user_id, "rest")

        return {
            "study_room_id": study_room_id,
            "sleep": sleep_values,
            "smartphone": phone_values,
            "await": await_values,
            "rest": rest_values
        }


if __name__ == "__main__":
    r = redis_function()

    r.start_study_init(1, "test")

    time.sleep(3)
    r.add_current_log(1, "phone", time.time())
    time.sleep(4)
    r.add_current_log(1, "sleep", time.time())
    time.sleep(3)
    r.add_current_log(1, "study", time.time())
    r.add_current_log(1, "rest", time.time())

    print(r.end_study(1))
