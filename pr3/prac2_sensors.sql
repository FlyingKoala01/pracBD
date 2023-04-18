/*
sqlite3 sensors.bd < t2_4.sql
*/

CREATE TABLE IF NOT EXISTS sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_time  DATETIME,
    epoch INT,
    nodeid INT,
    light INT,
    temp INT,
    voltage INT
);


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


CREATE TABLE IF NOT EXISTS calib_temp as select temp, avg(temp)+temp as calib from sensors group by temp;
CREATE TABLE IF NOT EXISTS calib_light as select light, avg(light)+light as calib from sensors group by light;

--.headers ON

-- Exercise 7
SELECT epoch, IFNULL((SELECT temp FROM sensors WHERE nodeid=1 AND epoch<=s.epoch ORDER BY epoch DESC LIMIT 1), 'null') as s1,
              IFNULL((SELECT temp FROM sensors WHERE nodeid=2 AND epoch<=s.epoch ORDER BY epoch DESC LIMIT 1), 'null') as s2,
              IFNULL((SELECT temp FROM sensors WHERE nodeid=3 AND epoch<=s.epoch ORDER BY epoch DESC LIMIT 1), 'null') as s3
FROM sensors s
GROUP BY epoch;

-- Implementacio alternativa, utilitzant case i joint
-- SELECT s1.epoch,
--     CASE
--         WHEN s1.temp IS NOT NULL THEN s1.temp
--         WHEN (
--             SELECT temp
--             FROM sensors
--             WHERE epoch < s1.epoch AND nodeid = 1
--             LIMIT 1
--         ) IS NOT NULL THEN (
--             SELECT temp
--             FROM sensors
--             WHERE epoch < s1.epoch AND nodeid = 1
--             LIMIT 1
--         )
--         ELSE 'null'
--     END AS 's1',
--     CASE
--         WHEN s2.temp IS NOT NULL THEN s2.temp
--         WHEN (
--             SELECT temp
--             FROM sensors
--             WHERE epoch < s1.epoch AND nodeid = 2
--             LIMIT 1
--         ) IS NOT NULL THEN (
--             SELECT temp
--             FROM sensors
--             WHERE epoch < s1.epoch AND nodeid = 2
--             LIMIT 1
--         )
--         ELSE 'null'
--     END AS 's2',
--     CASE
--         WHEN s2.temp IS NOT NULL THEN s2.temp
--         WHEN (
--             SELECT temp
--             FROM sensors
--             WHERE epoch < s1.epoch AND nodeid = 3
--             LIMIT 1
--         ) IS NOT NULL THEN (
--             SELECT temp
--             FROM sensors
--             WHERE epoch < s1.epoch AND nodeid = 3
--             LIMIT 1
--         )
--         ELSE 'null'
--     END AS 's3'
-- FROM sensors s1
-- LEFT OUTER JOIN sensors s2 ON s1.epoch = s2.epoch
-- LEFT OUTER JOIN sensors s3 ON s1.epoch = s3.epoch
-- GROUP BY s1.epoch;

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

