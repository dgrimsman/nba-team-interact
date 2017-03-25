# Interaction Among NBA Teams

### The National Basketball Association
The National Basketball Association (NBA) is comprised of 30 professional basketball teams. The league was founded in 1946 with 11 franchises, and has since merged with 2 other leagues: the NBL in 1949 and the ABA in 1976. Each season, teams compete for 82 games before a 4-round playoff determines the champion. Thus each team must compete to acquire as much talent as possible, reflected in the staff and players that the team has hired. The purpose of this project to explore how teams acquire on-the-court talent, and analyze how teams interact with one another to accomplish this goal.

There are three means by which a team can add a player: drafting the player, trading to get the player from another team, or signing the player if he is not under contract to another team. Usually this last option is signing the player as a free agent, but we will also lump any other means into this option. Therefore, we refer to it as "other". First we will discuss how successful teams have been gathering talent in the last 40 years, and then we will deep dive into how teams interact, mostly through trading.

The analyses presented here reflect only wins in the regular season, but further analysis could be done to include playoff wins and championships.

### Goals
In order to accomplish the purpose set forth in this project, we describe 3 specific goals:
1. Plot how many wins for each team can be attributed to each method of talent acquisition: trades, the draft, and other. This will motivate a deeper dive into trade dynamics.
2. Cluster teams into communities based on how impactful trading is among the teams. In other words, teams will be considered in a community if their trade interactions are impactful in terms of wins.
3. Cluster teams based on which players have played for them. In this case, teams will be considered in a cluster if similar players have played for them.
4. We will compare the clusters form Steps 2 and 3 to see what insights might be drawn from them.

Since these are goals relevant to a given time period, we show graphs and draw conclusions based on data from 6 different time periods: 1975-84, 1980-89, 1985-94, 1990-99, 1995-2004, and 2000-2009. Cutting off at 2009 allows analysis for the impact of a given trade.

### Gathering Data
This analysis is very much data-driven, therefore it requires a reliable source of information. We chose to use the site http://basketball-reference.com, since it offers access to draft and trade data, and well as win shares (see below). However, the challenge is that the site does not offer an accessible API, thus custom-written scrapers were created as part of this project. All the scraping files can be found [here](https://github.com/dgrimsman/nba-team-interact/tree/master/scrape). Essentially, 3 tables of data were required:
1. All player trades that have occurred
2. All draft picks from every year
3. The team and win shares (see below) associated with each player for each season he played.
The scrapers download the data and store it in a local PostgreSQL database.

### Win Shares
In order to analyze the impact that a trade has on a team, we use the metric known as win shares (WS). For a comprehensive explanation of WS and how it is calculated, see [here](http://www.basketball-reference.com/about/ws.html). In essence, the goal of WS is to try and account for how many wins that a player contributes to his team over the course of a season. In short WS is a function of many offensive and defensive statistics that are tracked, normalized by the pace of the player's team. Constants in the function have been tuned so that the sum of WS for all players on a team roughly equals the total wins for the team, thus it can be thought of as the player's win contribution.

While this metric is not immune to criticism, it is outside the scope of this project to invent a new one. Since WS appears to be a metric recognized in the sports statistics community, we use it here to gauge a player's productivity. To give a sense of the order of magnitude for WS, Kareem Abdul-Jabbar has the most career WS at 273.4 and the highest for a season at 25.4. Most players in the league have fewer than 7 per season. Note also that WS can be negative, although generally such WS values are not less than -1.

### Acquiring Talent
As mention above, there are 3 ways that a team can acquire talent: the draft, trades, and other. However, much has been made as to which of these 3 is the best. Common thought is that big-market teams have the luxury of attracting free agents, since players can make more money from endorsements in larger media markets. In addition, these teams are often willing to incur the penalties for spending above the salary cap, since their franchises are often more profitable. In contrast to this, there do currently exist small-market teams that seem to attract good free agents: San Antonio or Cleveland, for instance. Another point to consider is that many winning teams (small and large market) seem to acquire their best players through the draft: Magic Johnson and Larry Bird, for instance, were franchise staples their entire careers. Thus it is worth looking at some of the best teams in given periods of time to see to what source their wins can be attributed. Consider the charts below for the 1990-1999 time period:

<div figure{ display: inline-block;}>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/dvt_90-99.png" width="250">
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/dvo_90-99.png" width="250">
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/ovt_90-99.png" width="250">
</div>

Similar images for the other time periods can be found [here](https://github.com/dgrimsman/nba-team-interact/tree/master/docs/imgs). Each of these charts compares two methods for talent acquisition. The resounding message that comes from this is that for many teams, the largest source of win shares is through trades. In the 90s, Utah happens to be an exception to this, because they drafted Karl Malone and John Stockton in the 80s: two hall-of-famers that played 18 years together on the same team. Likewise we see San Antonio in the 00s with many win shares from the draft, due to Tim Duncan and other smart picks. For most teams, though, draft is second, and other is farther behind. Thus an analysis of trades is important to understanding how teams think and interact.

### Trading Communities
For the first analysis of the trading network, we leverage community detection, a common problem addressed in social networks. Generally, the goal is to find communities of people (or in our this case, teams) that have close interactions with each other and not with others outside the community. Here we use the trade data to create a graph, where each node is a team and each directed edge represents a player going from one team to another. The weight on the edge is the WS that the player earns with the new team. Thus, the "strength" of the interaction is how impactful the trade was, at least for one team.

While several algorithms offer community detection, this project uses the louvain method, implemented in python [here](http://perso.crans.org/aynaud/communities/). Given a graph, the louvain method seeks to partition the nodes in order to maximize the *modularity*, *Q*, of the partition. In precise terms (taken from [Wikipedia](https://en.wikipedia.org/wiki/Louvain_Modularity))

<img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/eq.png" width="550">

One could think of this metric as measuring the density of edges within each community versus the density of edges outside the community. The the algorithm runs with the following 2 steps:
1. For each node, and each neighbor of that node, see whether moving the node into the neighbor's community would increase the modularity.
2. Reassign communities suing this information

Of course, the above presentation is a very cursory look at the algorithm, but the goal is to communicate what the algorithm does on a high level. For each of the six time periods considered, the optimal clustering based on trade data is:

<div figure{ display: inline-block;}>
<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/trade_comm_75-84.png" width="250">
  <figcaption>Years 1975-1984</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/trade_comm_80-89.png" width="250">
  <figcaption>Years 1980-1989</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/trade_comm_85-94.png" width="250">
  <figcaption>Years 1985-1994</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/trade_comm_90-99.png" width="250">
  <figcaption>Years 1990-1999</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/trade_comm_95-04.png" width="250">
  <figcaption>Years 1995-2004</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/trade_comm_00-09.png" width="250">
  <figcaption>Years 2000-2009</figcaption>
</figure>
</div>

In these diagrams, the size of the node indicates the number of WS "flow in" to the team. Small nodes are teams that are giving away WS without getting equal value in return. There are a few observations that can be made about these communities. First, notice that the thick lines (more impactful trades) generally occur within the communities. Next we see that the algorithm chose 6 clusters for the first time period, 4 for the last time period, and 5 for the rest. This is somewhat surprising, considering there are only 24 teams in the 1975-1984 time period as opposed to 30 in 2000-2009. It seems to imply that the NBA is becoming more tight-knit in terms of trading. We see less "blockbuster" trades, and more of the medium-sized trades. Finally, we can see that these groupings tend to be fluid - in other words, there does not appear to be tight groups staying constant throughout time.

### Biclustering with Players
Another method we leverage in grouping teams is biclustering. Here we group teams based on what players have played for them: teams within a cluster are teams that have had similar players. Note that if a player has played for two teams, it need not be the case that he was traded from one to the other: he could have been waived and then signed, or perhaps he was traded to a 3rd team in the intermediate. This type of clustering also does not take into account the impact of WS: all edges in the graph will be weighted equally.

This project uses the python implmentation of biclustering found [here](http://scikit-learn.org/stable/modules/biclustering.html). The classic biclustering problem is that of trying to group documents by which words they contain while simultaneously grouping words by which documents they're in. Some synthetic data might look like this:

<img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/shuffled.png" width="400">

In the classic example, each row would represent a word and each column a document. Then the shade of the cell represents how many times that word appeared in that document. In our case, The rows are be players and the columns teams. Instead of shading, we have onyl a binary value: black if the player played on that team and white otherwise. The biclustering algorithm simply (we say "simply", but this is an NP-Hard problem in general) reorders the rows and columns so that both rows and columns are clustered:

<img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/matched.png" width="400">

Of course, real-world data is rarely this clean, and the NBA data is no exception. Generally, biclustering does well to find a number of tight clusters, and then one cluster is usually large and sparse. We will see this in the examples below. Also, a challenge with biclustering (unlike community detection) is that the algorithm does not determine on its own the optimal number of clusters. In this project we use 6, to allow for a small cluster, but also to be on the same order of clusters as the community detection. Certainly there is room for more tuning in this area.

### Comparison Between Partitions
We now show how the clusters given by the community detection compare to the clusters given by the biclustering algorithm. In order to explore this we use the following charts:

<div figure{ display: inline-block;}>
<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/biclust_75-84.png" width="250">
  <figcaption>Years 1975-1984</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/biclust_80-89.png" width="250">
  <figcaption>Years 1980-1989</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/biclust_85-94.png" width="250">
  <figcaption>Years 1985-1994</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/biclust_90-99.png" width="250">
  <figcaption>Years 1990-1999</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/biclust_95-04.png" width="250">
  <figcaption>Years 1995-2004</figcaption>
</figure>

<figure>
  <img src="https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/biclust_00-09.png" width="250">
  <figcaption>Years 2000-2009</figcaption>
</figure>
</div>

In these charts, the physical location of the nodes matches that of the diagrams in the community detection. For further emphasis, black ovals were placed around those nodes that were determined to be in the same cluster. The difference is that the colors now represent the clusters from the biclustering. Thus, if both sets of clusterings matched, every node inside a circle would also be the same color. While we see one instance where this is true, the general observation is that the two clusterings are not in harmony. 

### Discussion
Using these results, we can gain several insights. The most obvious is that the communities formed by the most impactful trades are not the communities formed by common players. In fact, the majority of impactful trades are between two teams that are not in the same biclustering cluster. This means that for general managers, making a bold move has often been the result of reaching across whatever the social norms are that induce the biclustering. Therefore, a general manager on the proverbial hot seat should take a risk and approach teams which have no or few players in common.

Another interesting insight we see from this data is that neither clustering seems to coincide with division boundaries. As background, the teams are partitioned by the NBA into divisions - loosely based on geography. Currently, a team plays all teams in its division four times a year, whereas a team across the country it may only play twice. The fact that we don't see large trades within divisions or many player clusters within divisions matches the intuition that a team shouldn't trade with its rival. It can be thought of as a zero-sum game: any help that a team A gives team B in its division will ultimately hurt team A. However, if team A helps team C across the country get better, it can be thought of as a cooperative game. In other words, team C's improvement that does not hurt team A as much, since they play less and will not meet in the playoffs until potentially the championship.

In either case, the analysis at the beginning of the project shows that begin able to draft well and trade have been keys to success for NBA teams. To that point, some of the biggest trades in terms of WS have been for young players, sometimes even on draft day itself. For example, one of the biggest trades we see is Charlotte trading Kobe Bryant to Los Angeles on draft day. Therefore, a team's general manager should invest as much time and ebergy as possible to be able to correctly evaluate young talent.

### Conclusion and Future Work
In this project, we have shown how NBA teams acquire talent and why we should be interested in the trade structre that exists within the league. We have examined this structure of interactions, based both on the strength of trades in terms of WS and on common players. This data was then used to gain insights into the social community that exists. 

Future work on this project would probably start with tuning the algorithms to this work a little more to fit the needs of the data. A possible extension could be to create a GUI-based tool for manipulating the data and allowing for analysis on custom time intervals. Another idea would be to explore adjusting the WS for draft-day trades or trades for draft picks, since its not clear how much credit should go to the trade and how much to the draft. Finally, moving forward, it would be interesting to use this type of social analysis to generate data-based best practices for trading in the NBA.
