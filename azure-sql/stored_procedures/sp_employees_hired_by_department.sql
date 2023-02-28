SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:      diego.garzon
-- Create Date: 20230220
-- Description: SP that process and fill the table challengue.employees_hired_by_department
-- Requirement: List of ids, name and number of employees hired of each department that hired more
--				employees than the mean of employees hired in 2021 for all the departments, ordered
--				by the number of employees hired (descending).
-- =============================================
CREATE PROCEDURE [challenge].[sp_employees_hired_by_department]
(
    @year int
)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON

    IF OBJECT_ID('tempdb..#tmp_departmens_hired') IS NOT NULL
	BEGIN
		DROP TABLE #tmp_departmens_hired
	END

	IF OBJECT_ID('tempdb..#tmp_departmens_hired_full') IS NOT NULL
	BEGIN
		DROP TABLE #tmp_departmens_hired_full
	END

	SELECT
		b.id
		,b.department
		,c.YearCalendar
		,count(0) AS hired
		,AVG(count(0)) OVER(PARTITION BY YearCalendar) AS AvgHired
	INTO
		#tmp_departmens_hired
	FROM
		[challenge].[employees] a
		INNER JOIN [challenge].[departments] b ON a.department_id = b.id
		INNER JOIN [challenge].[dim_tiempo] c ON a.date = c.DateKey
	WHERE
		c.YearCalendar = @year
	GROUP BY b.id, b.department, c.YearCalendar;

	SELECT 
		 id
		,department
		,YearCalendar
		,AvgHired
		,hired
		,CASE 
			WHEN hired > AvgHired THEN 1
			ELSE 0
		END AS flag
	INTO
		#tmp_departmens_hired_full
	FROM
		#tmp_departmens_hired;

	TRUNCATE TABLE challenge.employees_hired_by_department;

	INSERT INTO challenge.employees_hired_by_department
	SELECT 
		id,
		department,
		hired
	FROM #tmp_departmens_hired_full
	WHERE flag = 1;

	DROP TABLE  #tmp_departmens_hired;
	DROP TABLE #tmp_departmens_hired_full;

	SELECT * FROM challenge.employees_hired_by_department ORDER BY hired DESC;
END
GO
