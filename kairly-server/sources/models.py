import feedparser
import yaml

from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=160)
    provider = models.CharField(max_length=32, unique=True, help_text="Source identifier (namespace for guid)")
    rss = models.CharField(max_length=250)
    parse_content_from_rss = models.BooleanField(default=False)
    parsing_rules = models.TextField(help_text="YAML with perex and content keys")
    parser = models.TextField(help_text="Parse rules to get content from webpage.", blank=True)
    author = models.ForeignKey('articles.Author', models.SET_NULL, blank=True, null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        rules = yaml.load(self.parsing_rules)
        assert 'perex' in rules, 'perex key is missing'
        assert 'content' in rules, 'content key is missing'
        super(Channel, self).save(*args, **kwargs)

    def parse_rss(self):
        return feedparser.parse(self.rss)
