from django.conf import settings
from django.template.loader import render_to_string

from mailgun import api as mailgun_api
from sequence import models as sequence_api

import pygal

import subprocess
import datetime


def test_stats():
    stats = {
        'group-4-30@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 38, u'clicked': 2, u'opened': 176, u'unsubscribed': 0, u'bounced': 0, u'dropped': 2}, u'unique': {u'clicked': {u'link': 2, u'recipient': 2}, u'opened': {u'recipient': 12}}, 'messages': 11},
        'group-4-24@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 39, u'clicked': 0, u'opened': 7, u'unsubscribed': 0, u'bounced': 0, u'dropped': 1}, u'unique': {u'clicked': {u'link': 0, u'recipient': 0}, u'opened': {u'recipient': 5}}, 'messages': 11},
        'group-4-35@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 39, u'clicked': 5, u'opened': 26, u'unsubscribed': 0, u'bounced': 0, u'dropped': 1}, u'unique': {u'clicked': {u'link': 2, u'recipient': 3}, u'opened': {u'recipient': 17}}, 'messages': 1},
        'group-4-2@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 40, u'clicked': 0, u'opened': 17, u'unsubscribed': 1, u'bounced': 0, u'dropped': 0}, u'unique': {u'clicked': {u'link': 0, u'recipient': 0}, u'opened': {u'recipient': 7}}, 'messages': 2},
        'group-4-5@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 38, u'clicked': 2, u'opened': 86, u'unsubscribed': 1, u'bounced': 0, u'dropped': 2}, u'unique': {u'clicked': {u'link': 1, u'recipient': 2}, u'opened': {u'recipient': 15}}, 'messages': 8},
        'group-4-37@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 37, u'clicked': 1, u'opened': 23, u'unsubscribed': 0, u'bounced': 0, u'dropped': 3}, u'unique': {u'clicked': {u'link': 1, u'recipient': 1}, u'opened': {u'recipient': 9}}, 'messages': 3},
        'group-4-15@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 40, u'clicked': 0, u'opened': 50, u'unsubscribed': 0, u'bounced': 0, u'dropped': 0}, u'unique': {u'clicked': {u'link': 0, u'recipient': 0}, u'opened': {u'recipient': 17}}, 'messages': 5},
        'group-4-22@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 38, u'clicked': 1, u'opened': 57, u'unsubscribed': 0, u'bounced': 0, u'dropped': 2}, u'unique': {u'clicked': {u'link': 1, u'recipient': 1}, u'opened': {u'recipient': 15}}, 'messages': 5},
        'group-4-18@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 40, u'clicked': 1, u'opened': 105, u'unsubscribed': 0, u'bounced': 0, u'dropped': 0}, u'unique': {u'clicked': {u'link': 1, u'recipient': 1}, u'opened': {u'recipient': 21}}, 'messages': 7},
        'group-4-20@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 38, u'clicked': 0, u'opened': 25, u'unsubscribed': 0, u'bounced': 0, u'dropped': 2}, u'unique': {u'clicked': {u'link': 0, u'recipient': 0}, u'opened': {u'recipient': 13}}, 'messages': 3},
        'group-4-17@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 37, u'clicked': 0, u'opened': 37, u'unsubscribed': 1, u'bounced': 0, u'dropped': 1}, u'unique': {u'clicked': {u'link': 0, u'recipient': 0}, u'opened': {u'recipient': 13}}, 'messages': 5},
        'group-4-9@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 39, u'clicked': 2, u'opened': 21, u'unsubscribed': 0, u'bounced': 0, u'dropped': 1}, u'unique': {u'clicked': {u'link': 1, u'recipient': 1}, u'opened': {u'recipient': 12}}, 'messages': 4},
        'group-4-43@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 34, u'clicked': 1, u'opened': 35, u'unsubscribed': 0, u'bounced': 0, u'dropped': 2}, u'unique': {u'clicked': {u'link': 1, u'recipient': 1}, u'opened': {u'recipient': 8}}, 'messages': 6},
        'group-4-34@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 38, u'clicked': 0, u'opened': 25, u'unsubscribed': 0, u'bounced': 0, u'dropped': 2}, u'unique': {u'clicked': {u'link': 0, u'recipient': 0}, u'opened': {u'recipient': 14}}, 'messages': 5},
        'group-4-6@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 37, u'clicked': 0, u'opened': 27, u'unsubscribed': 0, u'bounced': 0, u'dropped': 1}, u'unique': {u'clicked': {u'link': 0, u'recipient': 0}, u'opened': {u'recipient': 10}}, 'messages': 4},
        'group-4-1@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 39, u'clicked': 2, u'opened': 70, u'unsubscribed': 0, u'bounced': 0, u'dropped': 1}, u'unique': {u'clicked': {u'link': 2, u'recipient': 1}, u'opened': {u'recipient': 12}}, 'messages': 6},
        'group-4-13@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 38, u'clicked': 0, u'opened': 21, u'unsubscribed': 1, u'bounced': 0, u'dropped': 0}, u'unique': {u'clicked': {u'link': 0, u'recipient': 0}, u'opened': {u'recipient': 11}}, 'messages': 5},
        'group-4-31@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 40, u'clicked': 1, u'opened': 38, u'unsubscribed': 1, u'bounced': 0, u'dropped': 0}, u'unique': {u'clicked': {u'link': 1, u'recipient': 1}, u'opened': {u'recipient': 10}}, 'messages': 3},
        'group-4-33@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 37, u'clicked': 1, u'opened': 44, u'unsubscribed': 0, u'bounced': 0, u'dropped': 3}, u'unique': {u'clicked': {u'link': 1, u'recipient': 1}, u'opened': {u'recipient': 9}}, 'messages': 7},
        'group-4-7@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 40, u'clicked': 2, u'opened': 36, u'unsubscribed': 0, u'bounced': 0, u'dropped': 0}, u'unique': {u'clicked': {u'link': 1, u'recipient': 1}, u'opened': {u'recipient': 14}}, 'messages': 6},
        'group-4-32@mechanicalmooc.org': {u'total': {u'complained': 0, u'delivered': 38, u'clicked': 2, u'opened': 30, u'unsubscribed': 0, u'bounced': 0, u'dropped': 2}, u'unique': {u'clicked': {u'link': 2, u'recipient': 2}, u'opened': {u'recipient': 14}}, 'messages': 4}
    }
    return stats


def get_stats():
    logs = mailgun_api.get_logs(limit=0)
    week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    date = lambda x: datetime.datetime.strptime(x, '%a, %d %b %Y %H:%M:%S GMT')
    date_filter = lambda x: date(x['created_at']) > week_ago
    logs['items'] = filter(date_filter, logs['items'])

    stats = {}
    for group_number in range(1,44):
        group = 'group-4-{0}@mechanicalmooc.org'.format(group_number)
        #if group in settings.EXPERIMENTAL_GROUPS:
        #    stats[group] = mailgun_api.get_list_stats(group)
        #else:
        stats[group] = {}
        event_filter = lambda x: x['hap'] == 'listexpand' and group in x['message']
        stats[group]['messages'] = len(filter(event_filter, logs['items']))
    return stats


def make_group_graph(group_stats):
    line_chart = pygal.HorizontalBar()
    line_chart.title = 'List activity'
    #line_chart.add('Clicks', group_stats['unique']['clicked']['link'])
    #line_chart.add('Opens', group_stats['unique']['opened']['recipient'])
    line_chart.add('Messages', group_stats['messages'])
    return line_chart


def make_global_graph(stats):
    line_chart = pygal.Bar()
    line_chart.title = 'Overall activity'
    line_chart.x_labels = map(str, range(1,44))
    line_chart.x_tite = 'Group'
    group_name = lambda group_number: 'group-4-{0}@mechanicalmooc.org'.format(group_number)
    line_chart.add('Messages', [stats[group_name(i)]['messages'] for i in range(1,44)])
    return line_chart


def upload_to_s3(filename):
    import boto
    c = boto.connect_s3()
    b = c.get_bucket('p2pu-resources') # substitute your bucket name here
    from boto.s3.key import Key
    k = Key(b)
    k.key = filename
    k.set_contents_from_filename(filename, policy='public-read')
    return k.generate_url(expires_in=0, query_auth=False, force_http=True)


def send_group_updates():

    # get stats for all groups from mailgun
    stats = get_stats()
    print(stats)

    global_graph = make_global_graph(stats)
    postfix = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    global_graph.render_to_file("global-stats-{0}.svg".format(postfix))
    process = subprocess.call('inkscape -e global-stats-{0}.png global-stats-{0}.svg'.format(postfix).split(' '))

    global_graph_url = upload_to_s3('global-stats-{0}.png'.format(postfix))

    for group in settings.EXPERIMENTAL_GROUPS:
        print(group)
        print(stats[group])
        graph = make_group_graph(stats[group])
        graph.render_to_file("{0}-{1}.svg".format(group, postfix))
        cmd = 'inkscape -e {0}-{1}.png {0}-{1}.svg'.format(group, postfix)
        subprocess.call(cmd.split(' '))
        group_stats_url = upload_to_s3('{0}-{1}.png'.format(group, postfix))
        context = {
            'stats': stats, 
            'group': group,
            'group_stats': stats[group],
            'group_number': group[8:group.find('@')],
            'group_stats_url': group_stats_url,
            'all_stats_url': global_graph_url,
        } 

        html_body = render_to_string('stats/mail.html', context)
        text_body = render_to_string('stats/mail.txt', context)
        print(html_body)
        mailgun_api.send_email(
            group,
            'the-machine@mechanicalmooc.org',
            'Weekly Snapshot: What\'s the Mechanical MOOC Community Up To',
            text_body,
            html_body,
            ['sequence_4', 'week_3', 'group_encourage'],
            sequence_api.sequence_campaign(4)
        )
