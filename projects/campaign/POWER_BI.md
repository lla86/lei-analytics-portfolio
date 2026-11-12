# Power BI reconstruction guide

**Demo / synthetic data.** This is a reproducible model specification and DAX starter, not an existing `.pbix` deliverable or screenshot of the original resume project. Use Power BI Desktop to create the workbook; GitHub Pages cannot run Power BI or Python backends.

1. Run `python3 scripts/generate_demo.py` from the repository root.
2. In Power BI Desktop, choose **Get data → Text/CSV** and import `data/synthetic/customers.csv` as **Customers**, and `campaigns.csv` as **Campaigns**.
3. In Power Query, type `customer_id`, `segment`, `campaign` as text; `recency_days`, `purchases_180d`, `responded` as whole numbers; `spend_cad` as fixed decimal. Preserve all 800 rows in each table and check IDs are unique and nonblank.
4. Relate Customers[customer_id] to Campaigns[customer_id] **one-to-one**, single-direction filtering from Customers to Campaigns. Every customer has one recipient record in this demo. Confirm no unmatched IDs. If the model later has multiple campaigns per customer, revise the grain and response denominator before reusing these measures.
5. Create the five measures in `measures.dax`. Format Response Rate as a percentage and spend measures as CAD.
6. Add cards: Customers, Responses, Response Rate and Historical Spend CAD. Add a bar chart of Response Rate by Customers[segment], fixed 0–100% scale. Add a table of Customers[segment], Customers, Responses, Response Rate, Historical Spend CAD and Spend Per Customer CAD. Use the segment field from **Customers** for slicers and axes so the same population filters numerator and denominator.
7. Put a visible heading on every page: **Portfolio reconstruction / synthetic data · September 2025**. Label spend as **pre-campaign historical spend (CAD)**, never campaign revenue. Show counts with rates. Reconcile totals and each segment to `docs/assets/results.json`.

Suggested pages: **Campaign overview** for response, **Customer segments** for recency/purchase/spend profiles, **Definitions** for source window, grain and denominators. Do not add retention or ROI charts without suitable longitudinal or control data. Publish to Power BI only if separately desired; this repository does not embed a report or require public access to a Power BI account.
