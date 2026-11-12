SELECT customers.segment, COUNT(*) AS customers,
       SUM(campaigns.responded) AS responses,
       1.0 * SUM(campaigns.responded) / COUNT(*) AS response_rate,
       ROUND(SUM(customers.spend_cad), 2) AS historical_spend_cad
FROM customers
JOIN campaigns USING (customer_id)
GROUP BY customers.segment
ORDER BY response_rate DESC;
