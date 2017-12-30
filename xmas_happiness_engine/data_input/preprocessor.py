# Packages
import os
import pandas as pd
import numpy as np
import datetime
from bs4 import BeautifulSoup

# File locations
IMPDIR = "I"
OUTDIR = "O"
IMP_dirs = os.listdir(IMPDIR)

# Agents
CHEN = 'chen'
RIC = 'ric'

#!#!# #!#!# THREEMA #!#!# #!#!#
thr_date_ftm = '%d %B %Y at %H:%M:%S'
THR_files = os.listdir(os.path.join(IMPDIR,'threema'))
thr_txt_path = os.path.join(IMPDIR,'threema',THR_files[0])
with open(thr_txt_path, 'r') as thr_txt:
    thr_data = thr_txt.read()
    thr_txt.close()
lines = thr_data.split("\n")

# Messages dataframe
authors, messages, times = [], [], []
for line in lines:
    if line[0:3] == '<<<': authors.append(CHEN)
    elif line[0:3] == '>>>':  authors.append(RIC)
    else: authors.append(np.nan)
    if 'BST' in line: splitter = 'BST'
    elif 'GMT' in line: splitter = 'GMT'
    messages.append(line.split(splitter)[-1][1:].strip())
    times.append(datetime.datetime.strptime(line.split(splitter)[0][4:-1], thr_date_ftm))
thr_msg_df = pd.DataFrame({'author': authors, 'message': messages, 'date': times})

# Ping-pong messages
pings, senders, receivers, msg, dates = [], [], [], '', []
for i in range(0,len(lines) - 1):
    signal_0 = lines[i][0:3]
    signal_1 = lines[i+1][0:3]
    if signal_0 == signal_1: msg += (lines[i].split(":")[-1].strip() + '. ')
    else:
        if lines[i][0:3] == '<<<':
            senders.append(CHEN)
            receivers.append(RIC)
        elif lines[i][0:3] == '>>>':
            senders.append(RIC)
            receivers.append(CHEN)
        else:
            senders.append(np.nan)
            receivers.append(np.nan)
        msg += lines[i].split(":")[-1].strip()
        pings.append(msg)
        if 'BST' in lines[i]: splitter = 'BST'
        elif 'GMT' in lines[i]: splitter = 'GMT'
        dates.append(datetime.datetime.strptime(lines[i].split(splitter)[0][4:-1], thr_date_ftm))
        msg = ''
pongs = pings[1:]
pongs.append(" ")
thr_pp_df = pd.DataFrame({'pinger': senders, 'ping': pings, 'ponger': receivers, 'pong': pongs, 'date': dates})
#!#!# #!#!# #!#!# #!#!# #!#!#!


#!#!# #!#!# WECHAT #!#!# #!#!#
wch_date_ftm = '%m/%d/%Y %H:%M:%S'

# HTML scraping
input_file = "I/wechat/html/yingchen.html"
input_data = open(input_file,'rb').read()
input_data_soup = BeautifulSoup(input_data, "html5lib")
Ps = list(input_data_soup.find_all('p'))
dates = list(input_data_soup.find_all('p', class_="date"))

# Messages dataframe
authors, messages = [], []
for elem in Ps:
    try: elem_class = elem['class'][0]
    except: elem_class = 'no class'
    if elem_class == 'triangle-isosceles' or elem_class == 'triangle-isosceles2':
        messages.append(elem.text.strip())
        if elem_class == 'triangle-isosceles': authors.append(CHEN)
        elif elem_class == 'triangle-isosceles2': authors.append(RIC)
dates = [datetime.datetime.strptime(date.text.strip(), wch_date_ftm) for date in dates]
wch_msg_df = pd.DataFrame({'author': authors[::-1], 'message': messages[::-1], 'date': dates[::-1]})

# Ping-pong messages
pings, senders, receivers, msg, times = [], [], [], '', []
for i in range(0,len(wch_msg_df) - 1):
    signal_0 = wch_msg_df.loc[i, 'author']
    signal_1 =  wch_msg_df.loc[i+1, 'author']
    if signal_0 == signal_1: msg += (wch_msg_df.loc[i, 'message'].strip() + (". "))
    else:
        if wch_msg_df.loc[i, 'author'] == CHEN:
            senders.append(CHEN)
            receivers.append(RIC)
        elif wch_msg_df.loc[i, 'author'] == RIC:
            senders.append(RIC)
            receivers.append(CHEN)
        else:
            senders.append(np.nan)
            receivers.append(np.nan)
        msg += wch_msg_df.loc[i, 'message'].strip()
        pings.append(msg)
        times.append(wch_msg_df.loc[i, 'date'])
        msg = ''
pongs = pings[1:]
pongs.append(" ")
wch_pp_df = pd.DataFrame({'pinger': senders, 'ping': pings, 'ponger': receivers, 'pong': pongs, 'date': times})
#!#!# #!#!# #!#!# #!#!# #!#!#

# Combining dataframes and outputing them as csv
msg_frames = [wch_msg_df, thr_msg_df]
pp_frames = [wch_pp_df, thr_pp_df]
final_msg_df = pd.concat(msg_frames, ignore_index=True)
final_pp_df = pd.concat(pp_frames, ignore_index=True)
final_msg_df.to_pickle((OUTDIR+'/messages.pd'))
final_pp_df.to_pickle((OUTDIR+'/pingpong.pd'))
