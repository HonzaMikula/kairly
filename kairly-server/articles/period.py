from datetime import time, timedelta
from collections import namedtuple

from more_itertools import windowed

Periodicity = namedtuple('Periodicity', ['frequency', 'time', 'dow'])
PeriodInterval = namedtuple('PeriodInterval', ['start', 'end', 'title'])


class PeriodMixin:
    X6_PER_DAY = '6x_per_day'
    X3_PER_DAY = '3x_per_day'
    DAILY = 'daily'
    WEEKLY = 'weekly'

    PERIOD_CHOICES = (
        (X6_PER_DAY, '6x per day'),
        (X3_PER_DAY, '3x per day'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
    )

    X3_PER_DAY_HOURS = [6, 12, 18]
    X6_PER_DAY_HOURS = [6, 9, 12, 15, 18, 21]

    def get_period_uid(self):
        """Used as cache key"""
        tokens = [self.period]
        if self.period_time is not None:
            tokens.append(self.period_time.strftime('%H%M'))
        if self.period_dow is not None:
            tokens.append(str(self.period_dow))
        return ':'.join(tokens)

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
        if self.period in [self.X3_PER_DAY, self.X6_PER_DAY]:
            if self.period == self.X3_PER_DAY:
                hours = self.X3_PER_DAY_HOURS
                title = '3× per day'
            else:
                hours = self.X6_PER_DAY_HOURS
                title = '6× per day'

            if dt.hour < hours[0]:
                return PeriodInterval(
                    dt.replace(hour=hours[-1], minute=0, second=0, microsecond=0) - timedelta(days=1),
                    dt.replace(hour=hours[0], minute=0, second=0, microsecond=0),
                    title
                )

            for h1, h2 in windowed(hours, 2):
                if dt.hour >= h1 and dt.hour < h2:
                    return PeriodInterval(
                        dt.replace(hour=h1, minute=0, second=0, microsecond=0),
                        dt.replace(hour=h2, minute=0, second=0, microsecond=0),
                        title
                    )

            return PeriodInterval(
                dt.replace(hour=hours[-1], minute=0, second=0, microsecond=0),
                dt.replace(hour=hours[0], minute=0, second=0, microsecond=0) + timedelta(days=1),
                title
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
    if frequency not in (PeriodMixin.X6_PER_DAY, PeriodMixin.X3_PER_DAY,
                         PeriodMixin.DAILY, PeriodMixin.WEEKLY):
        raise ValueError('Invalid period')

    if frequency in (PeriodMixin.X3_PER_DAY, PeriodMixin.X6_PER_DAY):
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
