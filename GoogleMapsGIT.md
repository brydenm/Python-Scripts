
# Google Maps Distance Calculation

Problem:  I need to calculate total distance driven from a list of work related car trips (for tax purposes!)

Approach:
Import the CSV containing the list of destinations into Python Pandas.
Using the googlemaps places API (via Python) we can conver the from/to location to specific addresses.
Using the googlemaps maps API we determine driving distances between the addresses
We convert destinations to addresses using googlemaps places API.

Resources:
Credit to https://www.datahubbs.com/google-maps-python/ for info on using googlemaps API via Python

Prerequisites:
Python Libraries: googlemaps, pandas, time
Google maps and places API keys (available via google developers site)



```python
#import the required libraries
import googlemaps
import pandas as pd
import time #to add a time delay in call to google api to avoid timeout errors

#store our key values
places_key = "put your google places key here"
maps_key = "put your maps places key here"

#pass the places key to the google API
gmaps = googlemaps.Client(places_key)
```

Step 3: Import our location data into pandas 


```python
#Import out CSV containing our location data and clean
file = "./Source/carjourneys.csv"
df = pd.read_csv(file, encoding='latin-1')
```


```python
#inspect the first 5 rows
df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SUMMARY</th>
      <th>Date</th>
      <th>ORIGIN</th>
      <th>LOCATION</th>
      <th>LOCATION_ADDRESS</th>
      <th>KM DISTANCE</th>
      <th>KM ROUND TRIP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>43</th>
      <td>Gig</td>
      <td>2018-12-01</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Bay Sports Club, 5 Bias Ave, Bateau Bay NS...</td>
      <td>5 Bias Ave, Bateau Bay NSW 2261, Australia</td>
      <td>16.599</td>
      <td>33.198</td>
    </tr>
    <tr>
      <th>44</th>
      <td>Gig</td>
      <td>2018-01-28</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Breakers Country Club Wamberal\n64 Dover Road,...</td>
      <td>64 Dover Rd, Wamberal NSW 2260, Australia</td>
      <td>9.170</td>
      <td>18.340</td>
    </tr>
    <tr>
      <th>45</th>
      <td>Catelyne Wedding Pre- Reception</td>
      <td>2018-02-03</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Long Reef Golf Club\nAnzac Avenue, Collaroy NS...</td>
      <td>Anzac Ave, Collaroy NSW 2097, Australia</td>
      <td>85.007</td>
      <td>170.014</td>
    </tr>
    <tr>
      <th>46</th>
      <td>Crista Ceremony and pre reception</td>
      <td>2018-09-03</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Address:æ993 Bells Line of Rd, Kurrajong Hills...</td>
      <td>Bells Line of Rd, Kurrajong Hills NSW 2758, Au...</td>
      <td>112.587</td>
      <td>225.174</td>
    </tr>
    <tr>
      <th>47</th>
      <td>Vuki and Sifa 1st bday gig</td>
      <td>2018-07-04</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Berowra Community Centre, Australia</td>
      <td>Gully Road, Berowra NSW 2081, Australia</td>
      <td>45.733</td>
      <td>91.466</td>
    </tr>
  </tbody>
</table>
</div>




```python
#show the dataframe shape (rows/columns)
df.shape
```




    (24, 7)



#check the datatype of each column
df.dtypes


```python
#change the date column into a datetime format (instead of object/string)
df.Date = pd.to_datetime(df.Date)
```


```python
#add a column with the 'origin', or starting location of each journey
df['ORIGIN'] = "50 Smith Road, Sydney NSW"
#select only the relevant columns
df = df[['SUMMARY','DTSTART-DATE','ORIGIN','LOCATION']]
#add a blank column for the destination address that we will obtain via googlemaps
df['LOCATION_ADDRESS'] = ""
#append 'australia' to each destination to avoid international addresses being retrieved
df['LOCATION'] = df['LOCATION'] + ", Australia"
```


```python
#inspect the list of destinations
df['LOCATION'].unique()
```




    array(['Dural, Australia',
           'The Bay Sports Club, 5 Bias Ave, Bateau Bay NSW 2261, Australia, Australia',
           'Club Umina, Australia', 'Dam Hotel Wyong, Australia',
           'Kincumber hotel, Australia', 'Kincumber Hotel, Australia',
           'Asquith golf club, Australia',
           'Mount Colah NSW 2079, Australia, Australia',
           'Avalon Beach, Australia',
           'Mount Penang Gardens\\nKariong NSW 2250, Australia, Australia',
           'Avoca Beach Bowling Club, Australia',
           'Mingara Recreation Club\\n12 Mingara Drive, Tumbi Umbi NSW 2261, Australia, Australia',
           'Wyong, Australia', 'Canton Beach Sports Club, Australia',
           'Mt Colah, Australia', 'Manly, Australia',
           'Niagara Park, Australia', 'Wollongong, Australia',
           'Hunter TAFE - Ourimbah Campus\\nBrush Road, Ourimbah NSW 2258, Australia, Australia',
           'Budgewoi Soccer Club\\n1 Millington Way, Buff Point NSW 2262, Australia, Australia',
           "Rafferty's Resort Lake Macquarie, Australia",
           'Miramare Gardens Terrey Hills, Australia',
           'Kibble Park Gosford, Australia', 'Wyong Leagues Club, Australia',
           'Gosford Sailing Club, Australia',
           'Breakers Country Club Wamberal\\n64 Dover Road, Wamberal NSW 2260, Australia, Australia',
           'Long Reef Golf Club\\nAnzac Avenue, Collaroy NSW 2097, Australia,, Australia',
           'Address:æ993 Bells Line of Rd, Kurrajong Hills NSW 2758, Australia',
           'Berowra Community Centre, Australia', 'Terrigal Hotel, Australia',
           'Wollombi, Australia', 'Kantara house, Australia',
           'Norah Head, Australia', 'Brunkerville, Australia',
           '1840 wollombi rd, Cedar Creek include set and pack up, Australia',
           'The Springs Golf Club\\n1080 Peats Ridge Road, Peats Ridge NSW 2250, Australia, Australia',
           '245 Newline Road Dural, Australia',
           '37 Greenwood Road KellyVille, Australia',
           'The Boathouse, Koolewong, Australia'], dtype=object)




```python
#filter out the rows where the destination is 'ignore'
df = df.loc[(df['LOCATION'] != "ignore")].dropna()
```

    (112, 5)
    (67, 5)


Now having our dataset with list of places ready - we move on to Geocoding


```python
#get address from googlemaps
f = lambda x: gmaps.geocode(x)
df["LOCATION_ADDRESS"] = df["LOCATION"].apply(f)
```


```python
#extrapolate the address from the list/dict of values returned from googlemaps
f = lambda x: x[0]["formatted_address"]
df["LOCATION_ADDRESS"] = df["LOCATION_ADDRESS"].apply(f)
```


```python
#set origin and destination address to a variable to be input into our distance function
x1 = df.ORIGIN.tolist()
x2 = df.LOCATION_ADDRESS.tolist()
```


```python
#pass our origin and destination addresses to our distance matrix function, loop through dataframe with a 2sec delay
result = []
for i in range(len(x1)):
    result.append(gmaps.distance_matrix(x1[i], x2[i], mode = "driving"))
    time.sleep(2)
```


```python
#unpack the results into a list
distances = []
for i in range(len(result)):
    distances.append(result[i]['rows'][0]['elements'][0]['distance']['value']/1000)

```


```python
#transfer the list values to the distance column in our dataframe
df['DISTANCE'] = pd.Series(distances)
```


```python
#rename our columns
df.columns = ['SUMMARY', 'DATE', 'ORIGIN', 'LOCATION',
       'LOCATION_ADDRESS', 'KM DISTANCE']
```


```python
df.sort_values('KM DISTANCE', ascending=False)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SUMMARY</th>
      <th>DTSTART-DATE</th>
      <th>ORIGIN</th>
      <th>LOCATION</th>
      <th>LOCATION_ADDRESS</th>
      <th>KM DISTANCE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>31</th>
      <td>Wedding Private Ceremony Wollongong</td>
      <td>5/08/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Wollongong, Australia</td>
      <td>Wollongong NSW 2500, Australia</td>
      <td>160.777</td>
    </tr>
    <tr>
      <th>46</th>
      <td>Crista Ceremony and pre reception</td>
      <td>9/03/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Address:æ993 Bells Line of Rd, Kurrajong Hills...</td>
      <td>Bells Line of Rd, Kurrajong Hills NSW 2758, Au...</td>
      <td>112.587</td>
    </tr>
    <tr>
      <th>61</th>
      <td>Laura Heslop ceremony and pre reception - appr...</td>
      <td>6/10/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>1840 wollombi rd, Cedar Creek include set and ...</td>
      <td>1840 Wollombi Rd, Wollombi NSW 2325, Australia</td>
      <td>90.271</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Avalon Carols</td>
      <td>10/12/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Avalon Beach, Australia</td>
      <td>Avalon Beach NSW 2107, Australia</td>
      <td>88.433</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Jubes Rehearsal @ Avalon</td>
      <td>28/11/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Avalon Beach, Australia</td>
      <td>Avalon Beach NSW 2107, Australia</td>
      <td>88.433</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Private Function</td>
      <td>17/06/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Manly, Australia</td>
      <td>Manly NSW 2095, Australia</td>
      <td>87.573</td>
    </tr>
    <tr>
      <th>45</th>
      <td>Catelyne Wedding Pre- Reception</td>
      <td>2/03/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Long Reef Golf Club\nAnzac Avenue, Collaroy NS...</td>
      <td>Anzac Ave, Collaroy NSW 2097, Australia</td>
      <td>85.007</td>
    </tr>
    <tr>
      <th>52</th>
      <td>Wedding Rene</td>
      <td>5/05/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Wollombi, Australia</td>
      <td>Wollombi NSW 2325, Australia</td>
      <td>81.023</td>
    </tr>
    <tr>
      <th>65</th>
      <td>40th bday gig</td>
      <td>10/11/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>37 Greenwood Road KellyVille, Australia</td>
      <td>37 Greenwood Rd, Kellyville NSW 2155, Australia</td>
      <td>77.682</td>
    </tr>
    <tr>
      <th>36</th>
      <td>PRIVATE Wedding</td>
      <td>21/10/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Miramare Gardens Terrey Hills, Australia</td>
      <td>48 Myoora Rd, Terrey Hills NSW 2084, Australia</td>
      <td>71.969</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Yuletide Dinner Gig 23/07/2016 @ 2PM</td>
      <td>23/07/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Dural, Australia</td>
      <td>Dural NSW 2158, Australia</td>
      <td>70.958</td>
    </tr>
    <tr>
      <th>30</th>
      <td>Xmas in July</td>
      <td>15/07/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Dural, Australia</td>
      <td>Dural NSW 2158, Australia</td>
      <td>70.958</td>
    </tr>
    <tr>
      <th>64</th>
      <td>Shannon ceremony n pre reception</td>
      <td>9/11/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>245 Newline Road Dural, Australia</td>
      <td>245 New Line Rd, Dural NSW 2158, Australia</td>
      <td>68.402</td>
    </tr>
    <tr>
      <th>60</th>
      <td>Emma &amp; Fiona Wedding hr wedding gig</td>
      <td>29/09/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Brunkerville, Australia</td>
      <td>Brunkerville NSW 2323, Australia</td>
      <td>66.991</td>
    </tr>
    <tr>
      <th>50</th>
      <td>Bday Gig Debbie Shoobert</td>
      <td>21/04/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Mount Colah NSW 2079, Australia, Australia</td>
      <td>Mount Colah NSW 2079, Australia</td>
      <td>54.701</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Don Summer Gig - Music in the Park (Mt Colah)</td>
      <td>20/11/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Mount Colah NSW 2079, Australia, Australia</td>
      <td>Mount Colah NSW 2079, Australia</td>
      <td>54.701</td>
    </tr>
    <tr>
      <th>40</th>
      <td>Don Summer Gig - Music in the Park (Mt Colah)</td>
      <td>18/11/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Mount Colah NSW 2079, Australia, Australia</td>
      <td>Mount Colah NSW 2079, Australia</td>
      <td>54.701</td>
    </tr>
    <tr>
      <th>26</th>
      <td>MND Fundraiser - Private Function.</td>
      <td>17/06/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Mt Colah, Australia</td>
      <td>Mount Colah NSW 2079, Australia</td>
      <td>54.701</td>
    </tr>
    <tr>
      <th>6</th>
      <td>asquith golf club gig</td>
      <td>11/11/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Asquith golf club, Australia</td>
      <td>Lord St, Mount Colah NSW 2079, Australia</td>
      <td>53.062</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Asquith Golf Club Gig</td>
      <td>17/02/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Asquith golf club, Australia</td>
      <td>Lord St, Mount Colah NSW 2079, Australia</td>
      <td>53.062</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Wedding - Karyn Simpson (Bride-Emma)</td>
      <td>16/09/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Rafferty's Resort Lake Macquarie, Australia</td>
      <td>Raffertys Rd, Cams Wharf NSW 2281, Australia</td>
      <td>51.835</td>
    </tr>
    <tr>
      <th>51</th>
      <td>Premium Full package Wedding</td>
      <td>22/04/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Rafferty's Resort Lake Macquarie, Australia</td>
      <td>Raffertys Rd, Cams Wharf NSW 2281, Australia</td>
      <td>51.835</td>
    </tr>
    <tr>
      <th>47</th>
      <td>Vuki and Sifa 1st bday gig</td>
      <td>7/04/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Berowra Community Centre, Australia</td>
      <td>Gully Road, Berowra NSW 2081, Australia</td>
      <td>45.733</td>
    </tr>
    <tr>
      <th>41</th>
      <td>Tentative booking</td>
      <td>8/12/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Wyong Leagues Club, Australia</td>
      <td>40 Lake Haven Dr, Kanwal NSW 2259, Australia</td>
      <td>40.976</td>
    </tr>
    <tr>
      <th>34</th>
      <td>Gig</td>
      <td>1/09/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Budgewoi Soccer Club\n1 Millington Way, Buff P...</td>
      <td>1 Millington Way, Buff Point NSW 2262, Australia</td>
      <td>38.391</td>
    </tr>
    <tr>
      <th>39</th>
      <td>Budgewoi Soccer Club</td>
      <td>17/11/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Budgewoi Soccer Club\n1 Millington Way, Buff P...</td>
      <td>1 Millington Way, Buff Point NSW 2262, Australia</td>
      <td>38.391</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Wyomg dam hotel</td>
      <td>28/10/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Dam Hotel Wyong, Australia</td>
      <td>Cnr Minnesota Rd &amp; Pacific Hwy, Hamlyn Terrace...</td>
      <td>32.640</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Canton Beach Sports Club</td>
      <td>7/04/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Canton Beach Sports Club, Australia</td>
      <td>11 Hibbard St, Toukley NSW 2263, Australia</td>
      <td>32.332</td>
    </tr>
    <tr>
      <th>59</th>
      <td>Lauren Thomson Basic reception</td>
      <td>22/09/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Norah Head, Australia</td>
      <td>Norah Head NSW 2263, Australia</td>
      <td>32.301</td>
    </tr>
    <tr>
      <th>63</th>
      <td>Rebecca Wedding Ceremony and Canapí©s</td>
      <td>27/10/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Springs Golf Club\n1080 Peats Ridge Road, ...</td>
      <td>1080 Peats Ridge Rd, Peats Ridge NSW 2250, Aus...</td>
      <td>28.077</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Club Umina</td>
      <td>14/05/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Club Umina, Australia</td>
      <td>509 Ocean Beach Rd, Umina Beach NSW 2257, Aust...</td>
      <td>21.624</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Club Umina Gig</td>
      <td>11/12/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Club Umina, Australia</td>
      <td>509 Ocean Beach Rd, Umina Beach NSW 2257, Aust...</td>
      <td>21.624</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Mingara Hotel Gig</td>
      <td>25/02/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Mingara Recreation Club\n12 Mingara Drive, Tum...</td>
      <td>12-14 Mingara Dr, Tumbi Umbi NSW 2261, Australia</td>
      <td>17.730</td>
    </tr>
    <tr>
      <th>55</th>
      <td>Gig Mingara</td>
      <td>28/07/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Mingara Recreation Club\n12 Mingara Drive, Tum...</td>
      <td>12-14 Mingara Dr, Tumbi Umbi NSW 2261, Australia</td>
      <td>17.730</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Bateau Bay Sports Club</td>
      <td>18/12/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Bay Sports Club, 5 Bias Ave, Bateau Bay NS...</td>
      <td>5 Bias Ave, Bateau Bay NSW 2261, Australia</td>
      <td>16.599</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Bateau Bay Bowlo Gig</td>
      <td>27/01/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Bay Sports Club, 5 Bias Ave, Bateau Bay NS...</td>
      <td>5 Bias Ave, Bateau Bay NSW 2261, Australia</td>
      <td>16.599</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Bateau Bay Bowling Club</td>
      <td>21/04/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Bay Sports Club, 5 Bias Ave, Bateau Bay NS...</td>
      <td>5 Bias Ave, Bateau Bay NSW 2261, Australia</td>
      <td>16.599</td>
    </tr>
    <tr>
      <th>43</th>
      <td>Gig</td>
      <td>12/01/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Bay Sports Club, 5 Bias Ave, Bateau Bay NS...</td>
      <td>5 Bias Ave, Bateau Bay NSW 2261, Australia</td>
      <td>16.599</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GIG: Bateau Bay Bowling Club 8PM 30/09/2016</td>
      <td>30/09/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Bay Sports Club, 5 Bias Ave, Bateau Bay NS...</td>
      <td>5 Bias Ave, Bateau Bay NSW 2261, Australia</td>
      <td>16.599</td>
    </tr>
    <tr>
      <th>37</th>
      <td>Gig</td>
      <td>3/11/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Bay Sports Club, 5 Bias Ave, Bateau Bay NS...</td>
      <td>5 Bias Ave, Bateau Bay NSW 2261, Australia</td>
      <td>16.599</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Bateau Bay Bowling Club - 8pm</td>
      <td>23/06/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Bay Sports Club, 5 Bias Ave, Bateau Bay NS...</td>
      <td>5 Bias Ave, Bateau Bay NSW 2261, Australia</td>
      <td>16.599</td>
    </tr>
    <tr>
      <th>32</th>
      <td>Hunter TAFE Gig</td>
      <td>12/08/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Hunter TAFE - Ourimbah Campus\nBrush Road, Our...</td>
      <td>Loop Rd, Ourimbah NSW 2258, Australia</td>
      <td>16.163</td>
    </tr>
    <tr>
      <th>66</th>
      <td>Wedding Brianne</td>
      <td>8/12/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Boathouse, Koolewong, Australia</td>
      <td>Brisbane Water Dr, Koolewong NSW 2256, Australia</td>
      <td>14.287</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Garden shed studio recording</td>
      <td>2/07/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Niagara Park, Australia</td>
      <td>Niagara Park NSW 2250, Australia</td>
      <td>12.193</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Busk gig</td>
      <td>4/12/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Mount Penang Gardens\nKariong NSW 2250, Austra...</td>
      <td>16 The Avenue, Kariong NSW 2250, Australia</td>
      <td>12.018</td>
    </tr>
    <tr>
      <th>44</th>
      <td>Gig</td>
      <td>28/01/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Breakers Country Club Wamberal\n64 Dover Road,...</td>
      <td>64 Dover Rd, Wamberal NSW 2260, Australia</td>
      <td>9.170</td>
    </tr>
    <tr>
      <th>58</th>
      <td>Terrigal Hotel Gig</td>
      <td>21/09/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Terrigal Hotel, Australia</td>
      <td>176 Terrigal Dr, Terrigal NSW 2260, Australia</td>
      <td>8.848</td>
    </tr>
    <tr>
      <th>48</th>
      <td>Terrigal Hotel</td>
      <td>13/04/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Terrigal Hotel, Australia</td>
      <td>176 Terrigal Dr, Terrigal NSW 2260, Australia</td>
      <td>8.848</td>
    </tr>
    <tr>
      <th>53</th>
      <td>Terrigal Hotel</td>
      <td>8/06/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Terrigal Hotel, Australia</td>
      <td>176 Terrigal Dr, Terrigal NSW 2260, Australia</td>
      <td>8.848</td>
    </tr>
    <tr>
      <th>62</th>
      <td>Avoca Beach Bowling Club</td>
      <td>20/10/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Avoca Beach Bowling Club, Australia</td>
      <td>Avoca Dr &amp; Townsend Ave, Avoca Beach NSW 2251,...</td>
      <td>8.689</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Avoca Beach Markets (Fairplay Stage)</td>
      <td>26/02/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Avoca Beach Bowling Club, Australia</td>
      <td>Avoca Dr &amp; Townsend Ave, Avoca Beach NSW 2251,...</td>
      <td>8.689</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Avoca Bowling Club</td>
      <td>13/01/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Avoca Beach Bowling Club, Australia</td>
      <td>Avoca Dr &amp; Townsend Ave, Avoca Beach NSW 2251,...</td>
      <td>8.689</td>
    </tr>
    <tr>
      <th>56</th>
      <td>Avoca Beach Bowling Club</td>
      <td>18/08/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Avoca Beach Bowling Club, Australia</td>
      <td>Avoca Dr &amp; Townsend Ave, Avoca Beach NSW 2251,...</td>
      <td>8.689</td>
    </tr>
    <tr>
      <th>54</th>
      <td>Avoca Beach Bowling Club</td>
      <td>22/06/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Avoca Beach Bowling Club, Australia</td>
      <td>Avoca Dr &amp; Townsend Ave, Avoca Beach NSW 2251,...</td>
      <td>8.689</td>
    </tr>
    <tr>
      <th>49</th>
      <td>Avoca Beach Bowling Club</td>
      <td>20/04/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Avoca Beach Bowling Club, Australia</td>
      <td>Avoca Dr &amp; Townsend Ave, Avoca Beach NSW 2251,...</td>
      <td>8.689</td>
    </tr>
    <tr>
      <th>38</th>
      <td>Gig Food festival entertainment</td>
      <td>9/11/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Kibble Park Gosford, Australia</td>
      <td>Kibble Park, Gosford NSW 2250, Australia</td>
      <td>5.995</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Gig Kincumber Hotel</td>
      <td>6/11/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Kincumber Hotel, Australia</td>
      <td>6 Carrak Rd, Kincumber NSW 2251, Australia</td>
      <td>5.546</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Gig @ kincumber hotel</td>
      <td>6/11/2016</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Kincumber hotel, Australia</td>
      <td>6 Carrak Rd, Kincumber NSW 2251, Australia</td>
      <td>5.546</td>
    </tr>
    <tr>
      <th>42</th>
      <td>Staff Xmas party gig</td>
      <td>16/12/2017</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Gosford Sailing Club, Australia</td>
      <td>28 Masons Parade, Gosford NSW 2250, Australia</td>
      <td>5.293</td>
    </tr>
    <tr>
      <th>57</th>
      <td>Wedding Victoria</td>
      <td>7/09/2018</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Kantara house, Australia</td>
      <td>431 Avoca Dr, Green Point NSW 2251, Australia</td>
      <td>3.795</td>
    </tr>
  </tbody>
</table>
<p>67 rows × 6 columns</p>
</div>




```python
#multiply the km distance by 2 and store in the round trip column
df['KM ROUND TRIP'] = df['KM DISTANCE'] * 2
```


```python
df = df.reset_index(drop=True)
```


```python
df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SUMMARY</th>
      <th>Date</th>
      <th>ORIGIN</th>
      <th>LOCATION</th>
      <th>LOCATION_ADDRESS</th>
      <th>KM DISTANCE</th>
      <th>KM ROUND TRIP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Yuletide Dinner Gig 23/07/2016 @ 2PM</td>
      <td>2016-07-23</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Dural, Australia</td>
      <td>Dural NSW 2158, Australia</td>
      <td>70.958</td>
      <td>141.916</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GIG: Bateau Bay Bowling Club 8PM 30/09/2016</td>
      <td>2016-09-30</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>The Bay Sports Club, 5 Bias Ave, Bateau Bay NS...</td>
      <td>5 Bias Ave, Bateau Bay NSW 2261, Australia</td>
      <td>16.599</td>
      <td>33.198</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Club Umina Gig</td>
      <td>2016-09-10</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Club Umina, Australia</td>
      <td>509 Ocean Beach Rd, Umina Beach NSW 2257, Aust...</td>
      <td>21.624</td>
      <td>43.248</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Wyomg dam hotel</td>
      <td>2016-10-28</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Dam Hotel Wyong, Australia</td>
      <td>Cnr Minnesota Rd &amp; Pacific Hwy, Hamlyn Terrace...</td>
      <td>32.640</td>
      <td>65.280</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Gig @ kincumber hotel</td>
      <td>2016-06-11</td>
      <td>78 Koolang Road, Green Point, NSW</td>
      <td>Kincumber hotel, Australia</td>
      <td>6 Carrak Rd, Kincumber NSW 2251, Australia</td>
      <td>5.546</td>
      <td>11.092</td>
    </tr>
  </tbody>
</table>
</div>




```python
#filter the dataframe to the journeys for the required time period...
df = df[df.DATE >= '01/07/2018']
```


```python
#check the total distances
df[['KM DISTANCE','KM ROUND TRIP']].sum()
```




    KM DISTANCE       917.491
    KM ROUND TRIP    1834.982
    dtype: float64




```python
#export to CSV > email to the tax agent!
df.to_csv('gigdistances.csv',encoding='latin8')
```
