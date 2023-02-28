SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:      diego.garzon
-- Create Date: 20230220
-- Description: SP that process and fill the table challengue.employees_hired_by_quarter
-- Requirement: Number of employees hired for each job and department in 2021 divided by quarter.
--				The table must be ordered alphabetically by department and job.
-- =============================================
CREATE PROCEDURE [challenge].[sp_employees_hired_by_quarter]
(
	@year int
)
AS
BEGIN
    -- SET NOCOUNT ON added to prevent extra result sets from
    -- interfering with SELECT statements.
    SET NOCOUNT ON

    IF OBJECT_ID('tempdb..#tmp_employees_hired') IS NOT NULL
	BEGIN
		DROP TABLE #tmp_employees_hired
	END

	SELECT
		department,
		job,
		QuarterNumberCalendar
	INTO
		#tmp_employees_hired
	FROM
		[challenge].[employees] a
		INNER JOIN challenge.departments b ON a.department_id = b.id
		INNER JOIN challenge.jobs c ON a.job_id = c.id
		INNER JOIN challenge.dim_tiempo d ON a.date = d.DateKey
	WHERE
		YearCalendar = @year;

	TRUNCATE TABLE challenge.employees_hired_by_quarter;

	INSERT INTO challenge.employees_hired_by_quarter
	SELECT department, job, [1] AS Q1, [2] AS Q2, [3] AS Q3, [4] AS Q4  
	FROM   
	(
		SELECT department, job, QuarterNumberCalendar  
		FROM #tmp_employees_hired
	) p  
	PIVOT  
	(  
		COUNT (QuarterNumberCalendar)  
		FOR QuarterNumberCalendar IN  ( [1], [2], [3], [4] )  
	) AS pvt  
	ORDER BY pvt.department, pvt.job;  

	DROP TABLE #tmp_employees_hired;

	SELECT * FROM challenge.employees_hired_by_quarter ORDER BY department, job ASC;

END
GO
