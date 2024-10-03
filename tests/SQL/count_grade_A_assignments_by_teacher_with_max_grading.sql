-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherGradingCount AS (
    -- Step 1: Find the teacher who graded the most assignments
    SELECT teacher_id, COUNT(*) AS total_graded
    FROM assignments
    WHERE grade IS NOT NULL
    GROUP BY teacher_id
    ORDER BY total_graded DESC
    LIMIT 1
)
-- Step 2: Count the number of grade 'A' assignments given by that teacher
SELECT COUNT(*) AS grade_A_count
FROM assignments
WHERE teacher_id = (SELECT teacher_id FROM TeacherGradingCount)
  AND grade = 'A';
