-- Example query: Average fan temp for CR06-RTU01_004 during June 2024
SELECT 
    Date,
    AVG(Value) AS AvgTemp
FROM 
    [CR06-RTU01_004]
WHERE 
    Date BETWEEN '2024-06-01' AND '2024-06-30'
GROUP BY 
    Date
ORDER BY 
    Date;
