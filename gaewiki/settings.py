# encoding=utf-8

import model
import util


SETTINGS_PAGE_NAME = 'gaewiki:settings'

DEFAULT_SETTINGS = """title: My Wiki
start_page: Welcome
admin_email: nobody@example.com
sidebar: gaewiki:sidebar
footer: gaewiki:footer
open-reading: yes
open-editing: no
editors: user1@example.com, user2@example.com
interwiki-google: http://www.google.ru/search?q=%s
interwiki-wp: http://en.wikipedia.org/wiki/Special:Search?search=%s
---
# gaewiki:settings

Edit me."""

settings = None

def get_host_page():
    """Returns the page that hosts the settings."""
    page = model.WikiContent.gql('WHERE title = :1', SETTINGS_PAGE_NAME).get()
    if page is None:
        page = model.WikiContent(title=SETTINGS_PAGE_NAME, body=DEFAULT_SETTINGS)
        page.put()
    return page


def get_all():
    global settings
    if settings is None:
        settings = util.parse_page(get_host_page().body)
    return settings

def get(key, default_value=None):
    return get_all().get(key, default_value)


def check_and_flush(page):
    """Empties settings cache if the host page is updated."""
    global settings
    if page.title == SETTINGS_PAGE_NAME:
        settings = None


def change(upd):
    """Modifies current settings with the contents of the upd dictionary."""
    current = get_all()
    current.update(upd)
    header = util.pack_page_header(current)
    page_content = header + u'\n---\n' + current['text']


def get_start_page_name():
    return get('start_page', 'Welcome')


def get_interwikis():
    iw = [(k[10:], v) for k, v in get_all().items() if k.startswith('interwiki-')]
    return sorted(iw, key=lambda iw: iw[0])
