\copy (select tms1.curr, tms2.curr, sum(cast(ws_to as float)) from trades inner join teams as tms1 on trades.from_team = tms1.abbr inner join teams as tms2 on trades.to_team=tms2.abbr where cast(substring("date" from '.{4}$') as integer) >= 2000 and cast(substring("date" from '.{4}$') as integer) <= 2009 group by tms1.curr, tms2.curr) to '../csv/trades_00-09.csv' with csv

--\copy (select from_team, to_team, sum(cast(ws_to as float)), cast(substr("date", -4) as integer) as year from trades where year >= 1990 and year <= 1999 group by from_team, to_team, dt) to 'trades.csv' with csv
