WITH flags AS (
    SELECT players.player_id, players.signup_date, players.variant,
           MAX(CASE WHEN sessions.day_number = 1 THEN 1 ELSE 0 END) AS d1,
           MAX(CASE WHEN sessions.day_number = 7 THEN 1 ELSE 0 END) AS d7
    FROM players
    LEFT JOIN sessions USING (player_id)
    WHERE date(players.signup_date, '+7 days') <= :observation_end
    GROUP BY players.player_id, players.signup_date, players.variant
)
SELECT signup_date AS cohort, variant, COUNT(*) AS players,
       SUM(d1) AS retained_d1, SUM(d7) AS retained_d7,
       1.0 * SUM(d1) / COUNT(*) AS d1_rate,
       1.0 * SUM(d7) / COUNT(*) AS d7_rate
FROM flags
GROUP BY signup_date, variant
ORDER BY signup_date, variant;
