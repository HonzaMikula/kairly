from datetime import datetime, timezone
from collections import namedtuple

from django.db import connection
from django.contrib.sitemaps import Sitemap

from articles.period import PeriodMixin


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class NewspaperSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        sql = """
            SELECT n.period, CONCAT(u.username, '/', n.slug) full_name, j.published modified
            FROM (
              SELECT n.id, MAX(i.number) number
              FROM articles_newspaper n
              JOIN users_user u ON (n.editor_id = u.id)
              LEFT OUTER JOIN articles_issue i ON (i.newspaper_id = n.id)
              GROUP BY n.id
            ) x
            JOIN articles_newspaper n ON (x.id = n.id)
            JOIN users_user u ON (n.editor_id = u.id)
            LEFT OUTER JOIN articles_issue j ON (j.newspaper_id = n.id AND x.number = j.number)
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return namedtuplefetchall(cursor)

    def location(self, obj):
        return '/' + obj.full_name

    def changefreq(self, obj):
        if obj.period == PeriodMixin.WEEKLY:
            return 'weekly'
        if obj.period == PeriodMixin.DAILY:
            return 'daily'
        return 'hourly'

    def lastmod(self, obj):
        return obj.modified


class PostSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        sql = """
            SELECT p.published, CONCAT(u.username, '/', p.slug) full_name
            FROM
               articles_post p
               JOIN users_user u ON (p.author_id = u.id)
            WHERE
               source IS NULL AND
               draft = 0 AND
               u.username != 'kairly-newuser' AND
               published BETWEEN '2018-11-01 00:00:00' AND NOW()
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            return namedtuplefetchall(cursor)

    def location(self, obj):
        return '/' + obj.full_name

    def changefreq(self, obj):
        return 'never'

    def lastmod(self, obj):
        return obj.published
