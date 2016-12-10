SELECT GovernmentForm, SUM(SurfaceArea) AS SumSufraceArea
FROM Country
GROUP BY GovernmentForm
ORDER BY SumSufraceArea DESC LIMIT 1;
