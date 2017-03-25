DELETE FROM trades a USING (
      SELECT MIN(ctid) as ctid, date, from_team, to_team, player
        FROM trades
            GROUP BY date, from_team, to_team, player HAVING COUNT(*) > 1
              ) b
                  WHERE a.date = b.date and a.from_team = b.from_team and a.to_team = b.to_team and a.player = b.player
                      AND a.ctid <> b.ctid
