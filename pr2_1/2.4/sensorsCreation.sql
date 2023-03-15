/*
sqlite3 sensors.bd < sensorsCreation.sql >out.txt
*/
CREATE TABLE IF NOT EXISTS sensors (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 result_time  DATETIME,
 epoch INT,
 nodeid INT,
 light INT,
 temp INT,
 voltage INT) ;


INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 09:10:18',639,1,555,26,400);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 10:20:10',653,1,556,12,420);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 10:30:11',683,1,557,38,430);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 11:33:15',712,1,558,15,433);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 11:40:23',715,1,560,0,512);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 12:42:28',725,1,562,27,323);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES (DATETIME('now'),727,1,555,20,401);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES (DATETIME('now'),729,1,566,12,333);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES (DATETIME('now'),732,1,568,13,0);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 09:10:18',639,2,555,0,325);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 10:20:10',653,2,556,5,386);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 10:30:11',683,2,557,10,402);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 11:33:15',712,2,558,11,415);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 11:40:23',715,2,560,12,411);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 12:42:28',725,2,562,13,450);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES (DATETIME('now'),727,2,564,14,300);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES (DATETIME('now'),729,2,566,15,400);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES (DATETIME('now'),734,2,568,16,408);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 09:10:18',639,3,555,-2,418);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 10:20:10',653,3,556,0,300);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 10:30:11',683,3,557,2,0);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 11:33:15',712,3,558,4,420);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 11:40:23',715,3,560,10,478);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES ('2015-03-05 12:42:28',725,3,562,12,499);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES (DATETIME('now'),727,3,564,13,501);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES (DATETIME('now'),729,3,566,14,512);
INSERT INTO sensors (result_time,epoch,nodeid,light,temp,voltage) VALUES (DATETIME('now'),729,3,568,15,534);


CREATE TABLE calib_temp as select temp, avg(temp)+temp as calib from sensors group by temp;
CREATE TABLE calib_light as select light, avg(light)+light as calib from sensors group by light;


-- Exercise 1
SELECT result_time, (SELECT calib from calib_light WHERE light = sensors.light) as calib_light
FROM sensors
WHERE (SELECT calib from calib_light WHERE light = sensors.light) > 500;
-- Result
-- 639|1110.0
-- 653|1112.0
-- 683|1114.0
-- 712|1116.0
-- 715|1120.0
-- ...

-- Exercise 2
SELECT avg((SELECT calib from calib_light WHERE light = sensors.light)) as calib_light
FROM sensors
WHERE nodeid = 1 AND strftime('%H:%M:%S', result_time) BETWEEN '18:00:00' AND '21:00:00';
-- Result
-- [Nothing]
-- This is because I started the database before 6PM and the only hardcoded results are on the morning.

-- Exercise 3
SELECT avg((SELECT calib from calib_light WHERE light = sensors.light)) as calib_light,
       avg((SELECT calib from calib_temp WHERE temp = sensors.temp)) as calib_temp
FROM sensors
WHERE voltage <= 418 AND strftime('%H:%M:%S', result_time) BETWEEN '18:00:00' AND '21:00:00';
-- Result
-- [Again, nothing]
-- Without the last where statement we would get
-- 1119.75|22.625

-- Exercise 4
SELECT strftime('%H', result_time) as hour, AVG((SELECT calib FROM calib_temp WHERE temp = sensors.temp)) as calib_temp
FROM sensors
WHERE nodeid = 2 AND strftime('%H:%M:%S', result_time) BETWEEN '18:00:00' AND '21:00:00'
GROUP BY hour;
-- Result (without the last where)
-- 09|0.0
-- 10|15.0
-- 11|23.0
-- 12|26.0
-- 15|30.0

-- Exercise 5
SELECT epoch
FROM sensors
WHERE nodeid IN (1,2)
GROUP BY epoch
HAVING COUNT(DISTINCT result_time) != 1;
-- Result
-- [nothing]
-- Note that the data above is `correct`, so we don't get anything.
-- We've tried to change the data and saw results.

-- Exercise 6
SELECT epoch
FROM sensors
GROUP BY epoch
HAVING COUNT(*) < 3
ORDER BY epoch DESC;
-- Result (didn't need to use nested queries for this one)
-- 734
-- 732

-- Exercise 7
SELECT epoch, (SELECT temp FROM sensors WHERE nodeid=1 AND epoch<=s.epoch ORDER BY epoch DESC LIMIT 1) as s1,
              (SELECT temp FROM sensors WHERE nodeid=2 AND epoch<=s.epoch ORDER BY epoch DESC LIMIT 1) as s2,
              (SELECT temp FROM sensors WHERE nodeid=3 AND epoch<=s.epoch ORDER BY epoch DESC LIMIT 1) as s3
FROM sensors s
GROUP BY epoch;
-- Result
-- 639|26|0|-2
-- 653|12|5|0
-- 683|38|10|2
-- 712|15|11|4
-- 715|0|12|10
-- 725|27|13|12
-- 727|20|14|13
-- 729|12|15|14
-- 732|13|15|14
-- 734|13|16|14


-- Exercise 8
-- The only way we managed to make a range.
-- We are not very confidents about this query :D
WITH RECURSIVE numbers AS (
  SELECT 639 AS num
  UNION ALL
  SELECT num + 1
  FROM numbers
  WHERE num < 735
)
SELECT num
FROM numbers
WHERE NOT EXISTS (
  SELECT 1
  FROM sensors
  WHERE epoch = num
);
-- Result
-- 640
-- 641
-- 642
-- 643
-- 644
-- 645
-- 646
-- 647
-- 648
-- ...
