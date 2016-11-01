# -*- coding: utf-8 -*-

##############################################################################
#
# Title: Twitter Video Downloader

# Description: Basic video downloader from a twitter status

# Version: 1.0.0
# Date: 01/11/2016
# Author: https://github.com/vkpk

##############################################################################
from sys import argv
from tweepy import OAuthHandler, API
from re import findall
from urllib.request import urlretrieve
from os import mkdir, path, getcwd

##############################################################################
# fill with your IDs
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
dl_folder = 'VIDEOS'
##############################################################################


def connect_api():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    return api


def get_data(id_status):
    status = connect_api().get_status(id_status)
    data = status._json
    return data


def get_best_vid(data):
    media_data = data['extended_entities']['media']
    for md in media_data:
        quals = md['video_info']['variants']

    max_qual = 0
    for qual in quals:
        if (len(qual) == 3 and qual['bitrate'] > max_qual):
            max_qual = qual['bitrate']
            video_url = qual['url']
    return video_url


def download_video(id_status):
    data = get_data(id_status)
    if not path.isdir(dl_folder):
        mkdir(dl_folder)

    video_file = path.join(
        getcwd() + '\\' + dl_folder, data['user']['screen_name'] + '_' + id_status + '.mp4')
    print('\n##### File destination : '+video_file)
    urlretrieve(get_best_vid(data), video_file)

##############################################################################

def main():
    # example video, just change the value:
    url_status = 'https://twitter.com/businessinsider/status/788509233419431936'
    id_status = findall(r'\d+', url_status)[0]
    download_video(id_status)

##############################################################################
if __name__ == '__main__':
    main()
