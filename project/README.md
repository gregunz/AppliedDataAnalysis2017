## How do conflicts propagate through media depending on their geolocation
# Abstract
As an individual, it is really hard to grasp a broad view of our world. Each media usually focuses on news influenced by its geolocation, political orientation, public of interest or many other variables. Hence, they all provide a biased representation of the world. By merging them altogether, we are able to get a more accurate and authentic view. Using GDELT Project, such diversity of media sources is available, it is focused on conflicts and it aggregates data from all around the world. Those datasets enable us to quantify and visualize the distribution of conflictual events by regions and patterns. By making use of such rich datasets, we attempt to show the spread of specific news and compare it between regions or types.
# Research questions
We wish to answer the following questions:

1. How is the distribution of conflictual events in the different regions of the world ?
1. Are there inequalities between those regions regarded to any event’s type or to their coverage by the media ?
1. Are some countries more prone to media bias than others (e.g some events might have a high coverage (many articles) depending on where they occur) ?
1. Can we show how information about a particular event spread on the map ?
1. How does it evolve throughout time ? (e.g. with internet, information travel quicker and broader)
1. *Can we use machine learning to predict the spread of a conflict?

*will depend on results and progress of previous questions

# Update on research question
After data acquisition, the questions we wished to answer were updated as follows:
1. The data we have gathered allows perfectly to answer to this question, we still have to complete our map of (newspaper URL) -> Country, but overall we are already able to draw sankey diagrams, bubble maps and heatmaps for different distribution of conflictual events such as:
    - Which countries a specific countries talk the most about
    - Which countries talk the most of a specific country

1. This question is heavily linked with the previous one, hence it is of course easily achievable in our current state.
1. Same as above
1. This question is on standby for now as we want to focus on answering the previous questions before switching to this one.
1. Again as for question 1 and 2, our current state already allows to do that, we haven't done it yet as it is more a matter of vizualisation.
1. Same as for 4.

# Dataset

**Update from Milestone 1**

We first planned to go with GDELT 1.0 but we finally chose to use 2.0.

Among all the column offered by GDELT we, for now, chose to keep these columns:
- EventCode
- SOURCEURL
- ActionGeo_CountryCode
- ActionGeo_Lat
- ActionGeo_Long
- IsRootEvent
- QuadClass
- GoldsteinScale
- AvgTone
- NumMentions
- NumSources
- NumArticles
- ActionGeo_Type
- Day

We refer to the cookbook provided by GDELT for more details on each columns: http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf

Also we spent a significant amount of time to fetch information about which country a specific URL corresponds to as we cannot rely on GDELT to provide us with which country the news was written in. We currently achieve a semi-satisfying accuracy but we are still trying to improve by alyways crawling the web for missing data. Indeed there are a tons of differents website in the time span 2015-2017 in the entire world! Some website are now dead, not referenced anymore, etc.. However we are pretty confident we can achieve an accuracy of nearly 100% in the coming days as we improve our fetching. We are also trying to find a way to get the country of origin from news where we don't have the URLs but as these are in very inconsistent format and are nearly not present in the dataset, we omitted them for now.

With GDELT combined with the URL map we are now able to fully focus on the last bit of aggregation and then fully on vizualisation.

# Dropped ideas

Since we are now using GDELT 2.0 instead of 1.0, we only have the data since 2015 and not 1979, hence everything we planned by analyzing the spread overtime have now to be adapted accordingly. Even though we loose the ability to go that much back in time, we think that focusing on the 2015 onwards period is also very rich in its own as we now focus on the digital era and hence focus our analysis in the current period, hence being more actual. Basically we are more doing the job of analysts than the job of historians!

# Questions for TAs (Milestone 2)

# Archives
Below you can find previous sections of the readme for previous milestone we still consider important but take too much visibility above.

## Milestone 1

### Dataset
We plan to use the GDELT Project datasets.
Even though, the datasets are quite complete, we can add categories for each event in order to be able to use custom filters later. How ? For each event, the source is provided as a set of URLs and we can crawl those URLs to collect more data.
The complete dataset is very large but very well structured and partitioned into smaller chunks where each of them represents the data for a specific day/month/year. At the moment we consider the following attributes to be the most relevant :
- Actor1Code: Code describing the main actor in the event.
- EventCode: Code describing the action taken by Actor1 on Actor2.
- NumMentions: Number of times the events is mentioned across our sources.
- NumSources: Number of sources the events is mentioned in.
- SOURCEURL: Array of the sources’ URLs.
- And many others

(information taken from http://data.gdeltproject.org/documentation/GDELT-Data_Format_Codebook.pdf)

### A list of internal milestones up until project milestone 2
|Week #|Internal Milestones|
|---|---|
|Week 1<br/>31.10-07.11|~~Aggregate some sample data and start processing it into manageable data structure.~~ Done|
|Week 2<br/>07.11-14.11|~~Do some crawling if some important information is lacking (such as article date for example). Filter events by their types in order to select the most interesting ones.~~ Done|
|Week 3<br/>14.11-21.11|~~Visualize some of our data on a world map.~~ Done|
|Week 4<br/>21.11-28.11|~~Visualize the spread over time of an event on a world map.~~ Goal changed|

### A list of internal milestones up until project milestone 3 (The end)
|Week #|Internal Milestones|
|---|---|
|Week 5<br/>28.11-05.12|Finish the crawling on the news website and setup the website for the visualisations|
|Week 6<br/>05.12-12.12|Finalize the different maps|
|Week 7<br/>12.12-19.12|Stick all the pieces together|

### Questions for TAs (Milestone 1) with answers
- *Can we update our planning for the next milestone depending on the difficulties encountered ?* Absolutely
- *Can we focus on some particular countries and then extends if time permits?* This is a reasonable approach btw
- *Do you think our goals are too broad and we should focus on a more specific task?* Your project is feasible, (except the crawling part). Considering your motivations I think is a good project
- *Is the project complexity and size what you expect from us? Is It too complex? not enough?* Is enough, consider to come up with a good visualization.