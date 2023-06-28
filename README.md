# sqlalchemy-challenge
This was by far one of the most challenging assignments to complete
I did my very best to pull from the resources that I had (TA's, Lectures, Activities, and online forums)
I got started by reviewing the CSV data and all files provided to compelete the assigment (climate_starter.ipynb, and hawaii,sqlite)
Starting with importing the various dependencies for the file "Climate_starte" in Juypter notebook and the same action for app.py file
You can consider this challenge as a vacation or holiday to Honolulu, Hawaii. To help with planning this trip, I was tasked to conduct a climate analysis about the area
Through the analysis and exploration of the climate data, I will use SQLAlchemy ORM queries, Panadas, and Matplotlib to also conduct 

For the climate analysis:
Using the provided starter notebook and hawaii.sqlite files to complete the climate analysis and data exploration.
Choosing a start date and end date range is approximately 3-15 days total.
Use SQLAlchemy create_engine to connect to the sqlite database.
Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.

precipitation analysis: 
I designed a query to retrieve the last 12 months of precipitation data.
Selected only the date and prcp values.
Load the query results into a Pandas DataFrame and set the index to the date column.
Sort the DataFrame values by date.
Plot the results using the DataFrame plot method.

Station Analysis:
Design a query to calculate the total number of stations.
Design a query to find the most active stations.
List the stations and observation counts in descending order.
Which station has the highest number of observations?
Using functions such as func.min, func.max, func.avg, and func.count to query.
Design a query to retrieve the last 12 months of temperature observation data (tobs).
Filter by the station with the highest number of observations.
Plot the results as a histogram with bins=12.

After completing the initial analysis, design a Flask API based on the queries developed abpve

Climate App:
Used FLASK to create your routes
Routes
/
Home page.
List all routes that are available.
/api/v1.0/precipitation
Convert the query results to a Dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.
/api/v1.0/stations
Return a JSON list of stations from the dataset.
/api/v1.0/tobs
query for the dates and temperature observations from a year from the last data point.
Return a JSON list of Temperature Observations (tobs) for the previous year.
/api/v1.0/<start> and /api/v1.0/<start>/<end>
Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

Note: Please see data visuals provided in Jupyter Notebook and subsequent scripts