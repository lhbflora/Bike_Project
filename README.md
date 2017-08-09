# Bike_Project
City Bike is one of the largest companies offering public bike service. The good news is that a large cache of data of every month in every year since the company was established is available on its website, which offers prizes for different categories of analysis.

There are a lot of tools that I can use to analyze such a great amount of data, and my tool of choice is SQL server(To clean the data), and Python(To visualize to data). PyData stack NumPy,Pandas,Matplotlib offer a great help to make the data understandable

## Downloading the data

The data is accessible on the official website https://www.citibikenyc.com/system-data
The data is some kind in different format.

## Data Cleaning
#### From 201501-citibike-tripdata.csv
    tripduration,starttime,stoptime,start station id,start station name,start station latitude,start station longitude,end station id,end station name,end station latitude,end station longitude,bikeid,usertype,birth year,gender
    1346,1/1/2015 0:01,1/1/2015 0:24,455,1 Ave & E 44 St,40.75001986,-73.96905301,265,Stanton St & Chrystie St,40.72229346,-73.99147535,18660,Subscriber,1960,2
	363,1/1/2015 0:02,1/1/2015 0:08,434,9 Ave & W 18 St,40.74317449,-74.00366443,482,W 15 St & 7 Ave,40.73935542,-73.99931783,16085,Subscriber,1963,1
#### From 201504-citibike-tripdata.csv 
    "tripduration","starttime","stoptime","start station id","start station name","start station latitude","start station longitude","end station id","end station name","end station latitude","end station longitude","bikeid","usertype","birth year","gender"
    "241","4/1/2015 00:00:23","4/1/2015 00:04:25","494","W 26 St & 8 Ave","40.74734825","-73.99723551","489","10 Ave & W 28 St","40.75066386","-74.00176802","15510","Subscriber","1992","2"
	"578","4/1/2015 00:00:52","4/1/2015 00:10:31","82","St James Pl & Pearl St","40.71117416","-74.00016545","2008","Little West St & 1 Pl","40.70569254","-74.01677685","15014","Subscriber","1982","1"


1. After importing all csv files into SQL Server by "bulk insert" and delete the text qualifier(")
```sql	
bulk insert [CitiBikedata-2015] from 'D:\My_path\201501-citibike-tripdata.csv'with(firstRow=2,Fieldterminator=',',RowTerminator='0x0a')
update [CityBike].[dbo].[CitiBike-tripdata-2015]
set [tripduration] =  replace([tripduration],'"','')
```
2. Insert a column 'trip_ID' as the Primary Key
3. If we want to establish a completed database, the data should be devided into the following parts:





## Data Analysis
After cleaning the data, the exported csv data can be analysis in Python. The processed fileis around 1.57GB. 

Some standard Python package imports needed:
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```
It can be loaded with Pandas.
```python
trips = pd.read_csv('2015_triptime.csv',
                    parse_dates=['starttime', 'stoptime'],low_memory = False,
                    infer_datetime_format=True)
trip.head()
```
![_20170805210650](https://user-images.githubusercontent.com/25804842/28995692-b1a9ed5e-7a22-11e7-8798-ea33101ab202.png)

In the original data, one row is a record for a user in one trip, including Trip_Duration, Start_Time, Stop_Time, station details and users' personal information
#


	
Extract time information
```python
ind = pd.DatetimeIndex(trips.starttime)
trips['date'] = ind.date.astype('datetime64')
trips['hour'] = ind.hour
```
To reduce the size of data, I divided the file into different parts according to the analysis usage so in this repository there are several csv files.
##  Users Type Structure
 Percentage of Annual members and short-term customers
 
 ![7e9d75d2519bb91714769ca1bbc907f](https://user-images.githubusercontent.com/25804842/28996485-fad04a44-7a33-11e7-96a1-4748556b8655.png)
* Most of people are likely to subscribe for a Annual ride while still some short-term users tend to pay for short-term pass

### Age structure
![figure_1](https://user-images.githubusercontent.com/25804842/28996752-b3b1a9be-7a38-11e7-96f3-a0f7d45bfa3f.png)
* People between 25 to 40 take the main position in all the users, followed by people between 40 to 60. 
* As a physical-demanding transportation option, biking is prefered by young office workers, serving as a green and healthy way of commuting.

###  Time regularities
With a pivot table involving starttime, usertype, counting the daily use and total trip duration(sec), we can better restructure the data.

![_20170805215958](https://user-images.githubusercontent.com/25804842/28996071-fa706b96-7a2a-11e7-8e26-cf83031dd779.png)

![by_date](https://user-images.githubusercontent.com/25804842/28996092-62e0bf6e-7a2b-11e7-9fb8-6bb3d458e312.jpg)

This plot shows the daily trend, separated by Annual members (top) and Day-Pass users (bottom). A couple observations:
* In winter, fewer people are willing to ride while the total number of users reach to the top during Sep and Oct
* Day pass users seem to show a steady ebb and flow with the seasons; the usage of annual users has not waned as significantly with the coming of fall.
* Both annual subscribers and day-pass customers seem to show a distinct weekly trend.

Let's take a clearer loolk at the weekly trend by averaging all rides by day of week

![by_weekday](https://user-images.githubusercontent.com/25804842/28996102-876020e6-7a2b-11e7-83da-580be89e2a81.jpg)

* Annual members tend to use their bikes during Monday to Friday (i.e. as part of a commute) while day pass users tend to use their bikes on the weekend(i.e. as temporary riding). 

![by_hour](https://user-images.githubusercontent.com/25804842/28996099-7e586a8a-7a2b-11e7-8d9b-8c9a67613239.jpg)

A great difference can be seen between a "commute" pattern, which sharply peaks in the morning and evening (e.g. annual members during weekdays) and a "recreational" pattern, which has a broad peak in the early afternoon (e.g. annual members on weekends, and short-term users all the time). Interestingly, the average behavior of annual pass holders on weekends seems to be almost identical to the average behavior of day-pass users on weekdays.

##  Trip Duration
![tripduration](https://user-images.githubusercontent.com/25804842/29000310-50774a3c-7a99-11e7-8413-dc284273ef7b.jpg)

Here the red dashed line separating the free rides (left) from the rides which incur a usage fee (right).
* It seems that short-term users are much more sensitive to the system rules: only a small tail of the trip distribution lies beyond 30 minutes.
* On the other hand, with the commute habit, annual Subscribers seems not care about the extra fee. I guess that may results from the lower extra cost(\$2.50 per 15mins) than day pass users(\$4 per 15mins)

## Station Distribution
gmaps is a plugin for including interactive Google maps in the IPython Notebook.\n
Here we use Jupyter Notebook to create a heatmap of bike stations in New York according to the frequency of utilization.

First of all,  counting the frequency with SQL server query
```sql
select  distinct  [start_station_latitude],[start_station_longitude],[start_station_latitude] + ',' +[start_station_longitude] as [start_position], count(*) as [Weight]
from[dbo].[CitiBikedata-2015]
group by [start_station_latitude] + ',' +[start_station_longitude],[start_station_latitude],[start_station_longitude]
```
Then explort the result as a csv file.
Open a new notebook in Jupyter
```python
import gmaps
import pandas as pd
station = pd.read_csv('2015_tripstation.csv',
                    low_memory = False,
                    infer_datetime_format=True)
locations = station[["start_station_latitude","start_station_longitude"]]
print(station.head())
```
![_20170809151924](https://user-images.githubusercontent.com/25804842/29109613-41ecfafa-7d16-11e7-91e7-caae2d195c40.png)
![image](https://user-images.githubusercontent.com/25804842/29109740-b6ecaa3a-7d16-11e7-9d73-b7d3920ddb6f.png)
![map _smaller](https://user-images.githubusercontent.com/25804842/29109770-d8991be6-7d16-11e7-8c68-9b9837a701a8.png)

As a good supplement of public traffic, low cost and convenience rental bike is chosen by millions of people on the way to the bus/subway station to work or just take a leisure riding. So I propose a project to research how to optimize the existing system and what can we do in  the future to promote the development of this environmentally friendly industry. According to the data posted, a lot more things can be explore. For example,compare to the last-year-data, how does percentage of the subscribers and costomers change. According to this change how can we adjust the annual and short time price setting. Or what's near the hottest station such that people are willing to rent the bike and to what extent each factor affect the uage. So we can adjust the amount of  bike to be placed in each station. Moreover, in combination with the infrastructure construction, where should we build the new station. 

