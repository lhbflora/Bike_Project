# Bike_Project

As a good supplement of public traffic, low cost and convenience rental bike is chosen by millions of people on the way to the bus/subway 
station to work or just take a leisure riding. So I propose a project to research how to optimize the existing system and what can we do in
 the future to promote the development of this environmentally friendly industry. According to the data posted, a lot of things can be 
explore. For example,compare to the last-year-data, how does percentage of the subscribers and costomers change. According to this change 
how can we adjust the annual and short time price setting. Or what's near the hottest station such that people are willing to rent the bike 
and to what extent each factor affect the uage. So we can adjust the amount of  bike to be placed in each station. Moreover, in combination 
with the infrastructure construction, where should we build the new station. 

City Bike is one of the largest company offering public bike service. The good news is that a large cache of data of every month in every year since the company was established is available on its website, which offers prizes for different categories of analysis.

There are a lot of tools that I can use to analyze such a great amount of data, and my tool of choice is SQL server(To clean the data), and Python(To visualize to data). PyData stack NumPy,Pandas,Matplotlib offer a great help to make the data understandable

#Downloading the data

The data is accessible on the official website https://www.citibikenyc.com/system-data
The data is some kind in different format.

### Data Cleaning
#### From 201501-citibike-tripdata.csv
    tripduration,starttime,stoptime,start station id,start station name,start station latitude,start station longitude,end station id,end station name,end station latitude,end station longitude,bikeid,usertype,birth year,gender
    1346,1/1/2015 0:01,1/1/2015 0:24,455,1 Ave & E 44 St,40.75001986,-73.96905301,265,Stanton St & Chrystie St,40.72229346,-73.99147535,18660,Subscriber,1960,2
	363,1/1/2015 0:02,1/1/2015 0:08,434,9 Ave & W 18 St,40.74317449,-74.00366443,482,W 15 St & 7 Ave,40.73935542,-73.99931783,16085,Subscriber,1963,1
#### From 201504-citibike-tripdata.csv 
    "tripduration","starttime","stoptime","start station id","start station name","start station latitude","start station longitude","end station id","end station name","end station latitude","end station longitude","bikeid","usertype","birth year","gender"
    "241","4/1/2015 00:00:23","4/1/2015 00:04:25","494","W 26 St & 8 Ave","40.74734825","-73.99723551","489","10 Ave & W 28 St","40.75066386","-74.00176802","15510","Subscriber","1992","2"
	"578","4/1/2015 00:00:52","4/1/2015 00:10:31","82","St James Pl & Pearl St","40.71117416","-74.00016545","2008","Little West St & 1 Pl","40.70569254","-74.01677685","15014","Subscriber","1982","1"


1. After importing all csv files into SQL Server by "bulk insert" and delete the text qualifier(")
#
    bulk insert [CitiBikedata-2015] from 'D:\My_path\201501-citibike-tripdata.csv'with(firstRow=2,Fieldterminator=',',RowTerminator='0x0a')
    update [CityBike].[dbo].[CitiBike-tripdata-2015]
	set [tripduration]	 =   replace([tripduration],'"','')

2. Insert a column 'trip_ID' as the Primary Key
3. If we want to establish a completed database, the data should be devided into the following parts:





### Data Analysis
After cleaning the data, the exported csv data can be analysis in Python. The processed fileis around 1.57FB
Some standard Python package imports needed:
#
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt
It can be loaded with Pandas.
#
	trips = pd.read_csv('2015_triptime.csv',
                    parse_dates=['starttime', 'stoptime'],low_memory = False,
                    infer_datetime_format=True)	    
Extract time information
#
	ind = pd.DatetimeIndex(trips.starttime)
	trips['date'] = ind.date.astype('datetime64')
	trips['hour'] = ind.hour



![hotstation](https://user-images.githubusercontent.com/25804842/28555066-ed42c10c-712f-11e7-9b26-72c04826fbdb.png)

![trip_numbers](https://user-images.githubusercontent.com/25804842/28555076-fac818b8-712f-11e7-8186-e3a1f16d94c0.png)
