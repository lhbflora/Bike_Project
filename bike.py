import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

trips = pd.read_csv('2015_triptime.csv',
                    parse_dates=['starttime', 'stoptime'],low_memory = False,
                    infer_datetime_format=True)
trips.head().to_csv('D:\\dataextract.csv', sep=' ', header=True, index=True)
# Find the start date
ind = pd.DatetimeIndex(trips.starttime)
trips['date'] = ind.date.astype('datetime64')
trips['hour'] = ind.hour
# print(trips)
cut_trip = pd.DataFrame()
cut_trip['date'] = trips['date']
cut_trip['hour'] = trips['hour']
cut_trip['starttime'] = trips['starttime']
cut_trip['usertype'] = trips['usertype']

by_date = trips.pivot_table( aggfunc={'starttime':'count','tripduration':'sum'},
                            values = ['starttime','tripduration'],
                            index='date',columns = 'usertype' )

print(by_date)
fig = by_date['starttime'].plot( title = 'Average Daily Use(2015)',legend = True)
plt.legend(['Annual Subscribers','Short-term Pass'])
plt.savefig('by_date.jpg')
plt.show()

#Exploring trend by week
by_weekday = by_date.groupby([by_date.index.dayofweek]).mean()
by_weekday.columns.name = None      #remove label for plot
fig = by_weekday['starttime'].plot(title = 'Average Use by Day of Week (2015)',legend = True)
fig.set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
fig.set_xlabel('Weekdays')
plt.legend(['Annual Subscribers','Short-term Pass'])
plt.savefig('by_weekday.jpg')
plt.show()

# #Exploring trend by hour
by_hour = cut_trip.pivot_table(aggfunc = 'count', index = ['date', 'hour'], columns = 'usertype').fillna(0).reset_index('hour')
print(by_hour)
by_hour['weekday'] = (by_hour.index.dayofweek > 5)
by_hour = by_hour.groupby(['weekday','hour']).mean()
by_hour.index.set_levels([['weekday','weekend'],["{0}:00".format(i) for i in range(24)]],inplace = True)
by_hour.columns.name = None
fig,ax = plt.subplots(1,2,figsize = (16,8))
by_hour.loc['weekday'].plot(title = 'Average Hourly Use (Mon - Fri)',ax = ax[0])
by_hour.loc['weekend'].plot(title = 'Average Hourly Use (Sat - Sun)',ax = ax[1])
ax[0].set_ylabel('Average Trips per Hour')
ax[0].legend(['Annual Subscribers','Short-term Pass'])
ax[1].legend(['Annual Subscribers','Short-term Pass'])
plt.savefig('by_hour.jpg')
plt.show()

Exploring tripduration
trips['minutes'] = trips.tripduration / 60
trips.groupby('usertype')['minutes'].hist(bins = np.arange(61),alpha = 0.5,normed = True)
plt.xlabel('Duration (minutes)')
plt.ylabel('relative frequency')
plt.title('Trip Durations')
plt.xlim(0,60)

plt.text(34,0.05,"Short-term users\nFree Trips\n\nAdditional Fee", ha = 'right', size = 18, rotation = 90, alpha = 0.5, color = 'red')
plt.text(49,0.05,"Annual Subscribers\nFree Trips\n\nAdditional Fee", ha = 'right', size = 18, rotation = 90, alpha = 0.5, color = 'black')
plt.legend(['Annual Subscribers','Short-term Pass'])
plt.axvline(x = 30, linestyle = '--', color = 'red', alpha = 0.3)
plt.axvline(x = 45, linestyle = '--', color = 'black', alpha = 0.3)
plt.savefig('tripduration.jpg')
plt.show()
