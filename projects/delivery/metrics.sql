SELECT zone,
       COUNT(*) AS orders,
       SUM(status = 'delivered') AS delivered,
       SUM(status = 'cancelled') AS cancelled,
       SUM(status = 'delivered' AND actual_minutes <= promised_minutes) AS on_time,
       ROUND(AVG(CASE WHEN status = 'delivered' THEN actual_minutes END), 2) AS mean_minutes,
       ROUND(1.0 * SUM(status = 'delivered' AND actual_minutes <= promised_minutes)
             / NULLIF(SUM(status = 'delivered'), 0), 6) AS on_time_rate
FROM deliveries
GROUP BY zone
ORDER BY zone;
