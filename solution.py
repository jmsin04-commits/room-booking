# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN_HOUR = 9        # 운영 시작
CLOSE_HOUR = 21      # 운영 종료 (모든 예약은 21시까지 끝나야 함)
MAX_HOURS = 3        # 한 번에 예약할 수 있는 최대 시간
MAX_PER_DAY = 2      # 한 사람이 같은 요일에 할 수 있는 최대 예약 수 (강의실 합산)


def _is_hour(value):
    """정수(시)인지 확인. True/False는 파이썬에서 정수 취급되지만 여기서는 시각으로 보지 않음."""
    return isinstance(value, int) and not isinstance(value, bool)


def _valid_place(room, day):
    return room in ROOMS and day in DAYS


class RoomBooking:
    def __init__(self):
        # (강의실, 요일) → [(시작, 끝, 이름), ...]  지금까지 받은 예약을 기억
        self._bookings = {}

    def book(self, room, day, start, end, name):
        # 1. 없는 강의실·요일
        if not _valid_place(room, day):
            return False
        # 2. 시각이 정수가 아님 (True/False 포함)
        if not (_is_hour(start) and _is_hour(end)):
            return False
        # 3. 운영 시간(9~21시) 밖
        if start < OPEN_HOUR or end > CLOSE_HOUR:
            return False
        # 4. 시작이 끝보다 늦거나 같음
        if start >= end:
            return False
        # 5. 한 번에 3시간 초과
        if end - start > MAX_HOURS:
            return False
        # 6. 같은 강의실·요일의 기존 예약과 겹침 (끝나는 시각에 바로 시작하는 건 괜찮음)
        for s, e, _ in self._bookings.get((room, day), []):
            if start < e and s < end:
                return False
        # 7. 같은 사람은 같은 요일에 최대 2건 (강의실이 달라도 합산)
        count = sum(
            1
            for (r, d), items in self._bookings.items()
            if d == day
            for _, _, n in items
            if n == name
        )
        if count >= MAX_PER_DAY:
            return False

        self._bookings.setdefault((room, day), []).append((start, end, name))
        return True

    def cancel(self, room, day, start, name):
        if not _valid_place(room, day) or not _is_hour(start):
            return False
        items = self._bookings.get((room, day), [])
        for i, (s, _, n) in enumerate(items):
            if s == start:
                if n != name:          # 본인 예약이 아니면 취소하지 않음
                    return False
                del items[i]
                return True
        return False                   # 그 시각에 시작하는 예약이 없음

    def get_schedule(self, room, day):
        if not _valid_place(room, day):
            return []
        # 시작 시각이 빠른 순서로, 새 목록을 만들어 돌려줌 (밖에서 고쳐도 기록은 안전)
        return sorted(self._bookings.get((room, day), []), key=lambda b: b[0])
