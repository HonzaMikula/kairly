from datetime import time
from collections import namedtuple

Periodicity = namedtuple('Periodicity', ['frequency', 'time', 'dow'])


class PeriodMixin:
    X3_PER_DAY = '3x_per_day'
    DAILY = 'daily'
    WEEKLY = 'weekly'

    PERIOD_CHOICES = (
        (X3_PER_DAY, '3x per day'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
    )

    # TODO refactor get_issue_interval(), use constant
    X3_PER_DAY_HOURS = [6, 12, 18]


def parse_periodicity(periodicity):
    frequency = periodicity.get('frequency')
    if frequency not in (PeriodMixin.X3_PER_DAY, PeriodMixin.DAILY, PeriodMixin.WEEKLY):
        return ValueError('Invalid period')

    if frequency == PeriodMixin.X3_PER_DAY:
        time_of_day = None
        dow = None
    else:
        time_str = periodicity.get('time')
        if time_str not in ('6:00', '9:00', '12:00', '15:00', '18:00', '21:00'):
            return ValueError('Invalid time format')
        time_of_day = time(*map(int, time_str.split(':', maxsplit=1)))

        if frequency == PeriodMixin.WEEKLY:
            dow = int(periodicity.get('dow'))
            if dow < 1 or dow > 7:
                return ValueError('Invalid day of week')
        else:
            dow = None
    return Periodicity(frequency, time_of_day, dow)


def periodicity_to_json(model):
    return {
        'frequency': model.period,
        'dow': model.period_dow,
        'time': model.period_time.strftime("%H:%M") if model.period_time else None,
    }
