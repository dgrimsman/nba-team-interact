\copy (select from_team, to_team, sum(cast(ws_to as float)) from trades group by from_team, to_team) to 'trades.csv' with csv

