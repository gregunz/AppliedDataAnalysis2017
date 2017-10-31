## How do conflicts propagate through media depending on their geolocation
# Abstract
As an individual, it is really hard to grasp a broad view of our world. Each media usually focuses on news influenced by its geolocation, political orientation, public of interest or many other variables. Hence, they all provide a biased representation of the world. By merging them altogether, we are able to get a more accurate and authentic view. Using GDELT Project, such diversity of media sources is available, it is focused on conflicts and it aggregates data from all around the world. Those datasets enable us to quantify and visualize the distribution of conflictual events by regions and patterns. By making use of such rich datasets, we attempt to show the spread of specific news and compare it between regions or types.
# Research questions
We wish to answer the following questions:

- How is the distribution of conflictual events in the different regions of the world ?
- Are there inequalities between those regions regarded to any event’s type or to their coverage by the media ?
- Are some countries more prone to media bias than others (e.g some events might have a high coverage (many articles) depending on where they occur) ?
- Can we show how information about a particular event spread on the map ?
- How does it evolve throughout time ? (e.g. with internet, information travel quicker and broader)
- *Can we use machine learning to predict the spread of a conflict?
\* will depend on results and progress of previous questions
# Dataset
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
# A list of internal milestones up until project milestone 2
|Week #|Internal Milestones|
|---|---|
|Week 1<br/>31.10-07.11|Aggregate some sample data and start processing it into manageable data structure.|
|Week 2<br/>07.11-14.11|Do some crawling if some important information is lacking (such as article date for example). Filter events by their types in order to select the most interesting ones. |
|Week 3<br/>14.11-21.11|Visualize some of our data on a world map.|
|Week 4<br/>21.11-28.11|Visualize the spread over time of an event on a world map.|
# Questions for TAs
Can we update our planning for the next milestone depending on the difficulties encountered ?
Can we focus on some particular countries and then extends if time permits?
Do you think our goals are too broad and we should focus on a more specific task?
Is the project complexity and size what you expect from us? Is It too complex? not enough?

