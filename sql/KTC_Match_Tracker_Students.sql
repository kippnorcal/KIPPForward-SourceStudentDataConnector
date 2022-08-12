/* CTE to identify student advisor, teacher of Advisory course */
WITH Advisory_Courses AS(
    SELECT DISTINCT
          a.student_number
        , a.teacher_first +' ' + a.teacher_last AS Advisor
    FROM custom.vw_Enrollment_course_section_PS a
    WHERE 1=1
        AND a.Schoolyear4digit = custom.fn_SchoolYear4Digit(GETDATE())
        AND a.course_name LIKE '%Advisory%'
        AND a.seq_latestEnrollment = 1
),
/* CTE to identify which period the Seminar course is for a student */
Seminar_Courses AS(
    SELECT DISTINCT
          s.student_number
        , s.period_abbreviation AS Seminar_Period
    FROM custom.vw_Enrollment_course_section_PS s
    WHERE 1=1
        AND s.Schoolyear4digit = custom.fn_SchoolYear4Digit(GETDATE())
        AND s.course_name LIKE '%Seminar%'
        AND s.seq_latestEnrollment = 1
),
/* CTE to pull in weighted GPAs */
Weighted_GPA AS(
    SELECT
          gpa.SystemStudentID
        , gpa.value
    FROM custom.Fact_GPA gpa
    WHERE 1=1
        AND gpa.is_inProgress = 0
        AND gpa.is_cumulative = 1
        AND gpa.is_finalMostRecent = 1
        AND gpa.calculation_method = 'KIPP NorCal Weighted'
)
SELECT
      s.SystemStudentID AS PS_Id
    , c.Id AS ADB_Id
    , s.LastName
    , s.FirstName
    , LEFT(sem.Seminar_Period,1) AS Seminar_Period
    , s.Standardized_PrimaryEthnicity AS Ethnicity
    , s.Standardized_Gender AS Gender
    , s.Standardized_PrimaryEthnicity + ' - ' + s.Standardized_Gender AS Ethnicity_and_Gender
    , s.Standardized_LunchStatus AS FRL_Status
    , '' AS Counselor -- Don't pull this in until updated in ADB con.Name AS Counselor
    , adv.Advisor
    , s.StudentEmail AS Personal_Email
   -- , c.Phone AS Cell_Phone
    , s.GradeLevel_Numeric AS Grade
    , s.ClassOf AS HS_Class
    , s.SchoolName_MostRecent AS HS_Name
    , s.EnrollmentStatus
    , s.SchoolYearEntryDate
    , s.SchoolYearExitDate
    , s.Standardized_PrimaryDisability AS IEP_Status
    , g.value AS Weighted_GPA
FROM dw.DW_dimStudent s
LEFT JOIN custom.KTC_Contact c
    ON s.SystemStudentID = c.School_SIS_ID__c
LEFT JOIN custom.KTC_Contact con
    ON c.College_Counselor__c = con.Id
LEFT JOIN Advisory_Courses adv
    ON s.SystemStudentID = adv.student_number
LEFT JOIN Seminar_Courses sem
    ON s.SystemStudentID = sem.student_number
LEFT JOIN Weighted_GPA g
    ON g.SystemStudentID = s.SystemStudentID
WHERE 1=1
    AND s.GradeLevel_Numeric IN (11,12)
    -- Update this date once the 8/1/22 issue is resolved!
    AND s.SchoolYearEntryDate > '07-31-22' -- Update each school year
    AND s.SchoolYearEntryDate <> s.SchoolYearExitDate -- Exclude no shows
ORDER BY s.SchoolName_MostRecent, s.LastName OFFSET 0 ROWS