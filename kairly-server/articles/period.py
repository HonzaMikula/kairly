from datetime import time, timedelta
from collections import namedtuple

Periodicity = namedtuple('Periodicity', ['frequency', 'time', 'dow'])
PeriodInterval = namedtuple('PeriodInterval', ['start', 'end', 'title'])


class PeriodMixin:
    X3_PER_DAY = '3x_per_day'
    DAILY = 'daily'
    WEEKLY = 'weekly'

    PERIOD_CHOICES = (
        (X3_PER_DAY, '3x per day'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
    )

    X3_PER_DAY_HOURS = [6, 12, 18]

    def get_period_interval(self, dt, tzinfo):
        dt = dt.astimezone(tzinfo)
        interval = self._get_period_interval_notz(dt)

        # Fix DST shift, perid must be 1 hour longer or shorter when includes DST shift
        start = interval.start.astimezone(tzinfo)
        if start.hour != interval.start.hour:
            start += timedelta(hours=interval.start.hour - start.hour)
            interval = PeriodInterval(start, interval.end, interval.title)

        end = interval.end.astimezone(tzinfo)
        if end.hour != interval.end.hour:
            end += timedelta(hours=interval.end.hour - end.hour)
            interval = PeriodInterval(interval.start, end, interval.title)

        return interval

    def _get_period_interval_notz(self, dt):
        """Construct time interval which includes given datetime and matches
        current periodicity.
        """
        if self.period == self.X3_PER_DAY:
            H1, H2, H3 = self.X3_PER_DAY_HOURS
            if dt.hour < H1:
                return PeriodInterval(
                    dt.replace(hour=H3, minute=0, second=0, microsecond=0) - timedelta(days=1),
                    dt.replace(hour=H1, minute=0, second=0, microsecond=0),
                    '3× per day'
                )
            elif dt.hour >= H1 and dt.hour < H2:
                return PeriodInterval(
                    dt.replace(hour=H1, minute=0, second=0, microsecond=0),
                    dt.replace(hour=H2, minute=0, second=0, microsecond=0),
                    '3× per day'
                )
            elif dt.hour >= H2 and dt.hour < H3:
                return PeriodInterval(
                    dt.replace(hour=H2, minute=0, second=0, microsecond=0),
                    dt.replace(hour=H3, minute=0, second=0, microsecond=0),
                    '3× per day'
                )
            else:
                return PeriodInterval(
                    dt.replace(hour=H3, minute=0, second=0, microsecond=0),
                    dt.replace(hour=H1, minute=0, second=0, microsecond=0) + timedelta(days=1),
                    '3× per day'
                )

        elif self.period == self.DAILY:
            sub_time = self.period_time
            start = dt.replace(hour=sub_time.hour, minute=sub_time.minute, second=0, microsecond=0)
            if start > dt:
                start -= timedelta(days=1)
            return PeriodInterval(start, start + timedelta(days=1), 'Daily summary')

        elif self.period == self.WEEKLY:
            sub_time = self.period_time
            start = dt.replace(hour=sub_time.hour, minute=sub_time.minute, second=0, microsecond=0)
            if start > dt:
                start -= timedelta(days=1)
            while start.isoweekday() != self.period_dow:
                start -= timedelta(days=1)
            return PeriodInterval(start, start + timedelta(days=7), 'Weekly summary')

        else:
            raise ValueError()


def parse_periodicity(periodicity):
    frequency = periodicity.get('frequency')
    if frequency is None:
        raise ValueError('frequency is missing')
    if frequency not in (PeriodMixin.X3_PER_DAY, PeriodMixin.DAILY, PeriodMixin.WEEKLY):
        raise ValueError('Invalid period')

    if frequency == PeriodMixin.X3_PER_DAY:
        time_of_day = None
        dow = None
    else:
        time_str = periodicity.get('time')
        if time_str is None:
            raise ValueError('time is missing')
        time_str = time_str.lstrip('0')
        if time_str not in ('6:00', '9:00', '12:00', '15:00', '18:00', '21:00'):
            raise ValueError('Invalid time format')
        time_of_day = time(*map(int, time_str.split(':', maxsplit=1)))

        if frequency == PeriodMixin.WEEKLY:
            dow = periodicity.get('dow')
            if dow is None:
                raise ValueError('dow is missing')
            dow = int(dow)
            if dow < 1 or dow > 7:
                raise ValueError('Invalid day of week')
        else:
            dow = None
    return Periodicity(frequency, time_of_day, dow)


def periodicity_to_json(model):
    return {
        'frequency': model.period,
        'dow': model.period_dow,
        'time': model.period_time.strftime("%H:%M") if model.period_time else None,
    }
