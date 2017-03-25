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
* Comes from basketballreference.com
* Had to write python scrapers (links to files?)

### Win Shares
* Brief explanation and why we use them

### Acquiring Talent

### Trading Communities
* Need a clustering algorithm that leverages weighted edges
* Modularity measure
* Some results for different decades
<!--![Trade Communities 1990-1999](https://raw.githubusercontent.com/dgrimsman/nba-team-interact/master/docs/imgs/trade_comm_90-99.png "Trade Communities 1990-1999")-->

<div figure{ display: inline-block;}, img{width: 250;}>
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

### Biclustering with Players
* Show an example of biclustering with synthetic data
* Summary of algorithm
* Some results from different decades

### Comparison Between Partitions
* Show the partitions for different decades
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

### Discussion
* Trades are important
* Best bet is to analyze 

### Conclusion
