## Citi Bike MapReduce Execution Log

### Job: mr1_user_behavior
- **Status**: SUCCESS
- **Duration**: 8.3 seconds
- **Records Output**: 4

### Job: mr2_top_routes
- **Status**: SUCCESS
- **Duration**: 14.01 seconds
- **Records Output**: 4185

### Job: mr3_hourly_trends
- **Status**: SUCCESS
- **Duration**: 12.4 seconds
- **Records Output**: 24

### Job: mr4_weekly_analysis
- **Status**: SUCCESS
- **Duration**: 8.5 seconds
- **Records Output**: 14

### Job: mr5_distance_calc
- **Status**: SUCCESS
- **Duration**: 6.98 seconds
- **Records Output**: 4185

### Job: mr6_anomaly_detection
- **Status**: SUCCESS
- **Duration**: 12.26 seconds
- **Records Output**: 0

### Job: mr7_station_capacity
- **Status**: SUCCESS
- **Duration**: 7.95 seconds
- **Records Output**: 3

### Job: mr8_station_status_check
- **Status**: SUCCESS
- **Duration**: 9.41 seconds
- **Records Output**: 2

### Job: mr1_user_behavior
- **Status**: SUCCESS
- **Duration**: 8.12 seconds
- **Records Output**: 4

### Job: mr1_user_behavior
- **Status**: FAILED
- **Duration**: 4.59 seconds
- **Records Output**: 0

### Job: mr2_top_routes
- **Status**: FAILED
- **Duration**: 4.46 seconds
- **Records Output**: 0

### Job: mr3_hourly_trends
- **Status**: FAILED
- **Duration**: 4.3 seconds
- **Records Output**: 0

### Job: mr4_weekly_analysis
- **Status**: FAILED
- **Duration**: 4.25 seconds
- **Records Output**: 0

### Job: mr5_distance_calc
- **Status**: FAILED
- **Duration**: 4.39 seconds
- **Records Output**: 0

### Job: mr6_anomaly_detection
- **Status**: FAILED
- **Duration**: 4.33 seconds
- **Records Output**: 0

### Job: mr7_station_capacity
- **Status**: FAILED
- **Duration**: 4.3 seconds
- **Records Output**: 0

### Job: mr8_station_status_check
- **Status**: FAILED
- **Duration**: 4.26 seconds
- **Records Output**: 0

### Job: mr1_user_behavior
- **Status**: FAILED
- **Duration**: 3.68 seconds
- **Records Output**: 0

### Job: mr2_top_routes
- **Status**: FAILED
- **Duration**: 3.58 seconds
- **Records Output**: 0

### Job: mr3_hourly_trends
- **Status**: FAILED
- **Duration**: 3.47 seconds
- **Records Output**: 0

### Job: mr4_weekly_analysis
- **Status**: FAILED
- **Duration**: 4.05 seconds
- **Records Output**: 0

### Job: mr5_distance_calc
- **Status**: FAILED
- **Duration**: 3.83 seconds
- **Records Output**: 0

### Job: mr6_anomaly_detection
- **Status**: FAILED
- **Duration**: 3.37 seconds
- **Records Output**: 0

### Job: mr7_station_capacity
- **Status**: FAILED
- **Duration**: 3.35 seconds
- **Records Output**: 0

### Job: mr8_station_status_check
- **Status**: FAILED
- **Duration**: 3.62 seconds
- **Records Output**: 0

### Job: mr1_user_behavior
- **Status**: FAILED
- **Duration**: 3.33 seconds
- **Records Output**: 0- **Hadoop Log Tail**:
``text
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:48:33,166 INFO mapred.LocalJobRunner: map task executor complete.
2026-06-10 13:48:33,174 WARN mapred.LocalJobRunner: job_local780948756_0001
java.lang.Exception: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.mapred.LocalJobRunner$Job.runTasks(LocalJobRunner.java:492)
	at org.apache.hadoop.mapred.LocalJobRunner$Job.run(LocalJobRunner.java:552)
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 10 more
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	... 15 more
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 18 more
Caused by: java.lang.RuntimeException: configuration exception
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:222)
	at org.apache.hadoop.streaming.PipeMapper.configure(PipeMapper.java:66)
	... 23 more
Caused by: java.io.IOException: Cannot run program "python3": error=2, No such file or directory
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1048)
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:209)
	... 24 more
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:48:33,939 INFO mapreduce.Job: Job job_local780948756_0001 running in uber mode : false
2026-06-10 13:48:33,940 INFO mapreduce.Job:  map 0% reduce 0%
2026-06-10 13:48:33,942 INFO mapreduce.Job: Job job_local780948756_0001 failed with state FAILED due to: NA
2026-06-10 13:48:33,947 INFO mapreduce.Job: Counters: 0
2026-06-10 13:48:33,947 ERROR streaming.StreamJob: Job not successful!
Streaming Command Failed!

``

### Job: mr2_top_routes
- **Status**: FAILED
- **Duration**: 3.64 seconds
- **Records Output**: 0- **Hadoop Log Tail**:
``text
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:48:40,422 INFO mapred.LocalJobRunner: map task executor complete.
2026-06-10 13:48:40,430 WARN mapred.LocalJobRunner: job_local398576616_0001
java.lang.Exception: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.mapred.LocalJobRunner$Job.runTasks(LocalJobRunner.java:492)
	at org.apache.hadoop.mapred.LocalJobRunner$Job.run(LocalJobRunner.java:552)
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 10 more
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	... 15 more
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 18 more
Caused by: java.lang.RuntimeException: configuration exception
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:222)
	at org.apache.hadoop.streaming.PipeMapper.configure(PipeMapper.java:66)
	... 23 more
Caused by: java.io.IOException: Cannot run program "python3": error=2, No such file or directory
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1048)
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:209)
	... 24 more
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:48:41,220 INFO mapreduce.Job: Job job_local398576616_0001 running in uber mode : false
2026-06-10 13:48:41,220 INFO mapreduce.Job:  map 0% reduce 0%
2026-06-10 13:48:41,222 INFO mapreduce.Job: Job job_local398576616_0001 failed with state FAILED due to: NA
2026-06-10 13:48:41,227 INFO mapreduce.Job: Counters: 0
2026-06-10 13:48:41,227 ERROR streaming.StreamJob: Job not successful!
Streaming Command Failed!

``

### Job: mr3_hourly_trends
- **Status**: FAILED
- **Duration**: 3.43 seconds
- **Records Output**: 0- **Hadoop Log Tail**:
``text
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:48:47,409 INFO mapred.LocalJobRunner: map task executor complete.
2026-06-10 13:48:47,419 WARN mapred.LocalJobRunner: job_local1855540850_0001
java.lang.Exception: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.mapred.LocalJobRunner$Job.runTasks(LocalJobRunner.java:492)
	at org.apache.hadoop.mapred.LocalJobRunner$Job.run(LocalJobRunner.java:552)
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 10 more
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	... 15 more
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 18 more
Caused by: java.lang.RuntimeException: configuration exception
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:222)
	at org.apache.hadoop.streaming.PipeMapper.configure(PipeMapper.java:66)
	... 23 more
Caused by: java.io.IOException: Cannot run program "python3": error=2, No such file or directory
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1048)
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:209)
	... 24 more
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:48:48,164 INFO mapreduce.Job: Job job_local1855540850_0001 running in uber mode : false
2026-06-10 13:48:48,167 INFO mapreduce.Job:  map 0% reduce 0%
2026-06-10 13:48:48,172 INFO mapreduce.Job: Job job_local1855540850_0001 failed with state FAILED due to: NA
2026-06-10 13:48:48,180 INFO mapreduce.Job: Counters: 0
2026-06-10 13:48:48,180 ERROR streaming.StreamJob: Job not successful!
Streaming Command Failed!

``

### Job: mr4_weekly_analysis
- **Status**: FAILED
- **Duration**: 3.4 seconds
- **Records Output**: 0- **Hadoop Log Tail**:
``text
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:48:54,567 INFO mapred.LocalJobRunner: map task executor complete.
2026-06-10 13:48:54,576 WARN mapred.LocalJobRunner: job_local199799149_0001
java.lang.Exception: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.mapred.LocalJobRunner$Job.runTasks(LocalJobRunner.java:492)
	at org.apache.hadoop.mapred.LocalJobRunner$Job.run(LocalJobRunner.java:552)
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 10 more
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	... 15 more
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 18 more
Caused by: java.lang.RuntimeException: configuration exception
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:222)
	at org.apache.hadoop.streaming.PipeMapper.configure(PipeMapper.java:66)
	... 23 more
Caused by: java.io.IOException: Cannot run program "python3": error=2, No such file or directory
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1048)
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:209)
	... 24 more
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:48:55,387 INFO mapreduce.Job: Job job_local199799149_0001 running in uber mode : false
2026-06-10 13:48:55,388 INFO mapreduce.Job:  map 0% reduce 0%
2026-06-10 13:48:55,390 INFO mapreduce.Job: Job job_local199799149_0001 failed with state FAILED due to: NA
2026-06-10 13:48:55,394 INFO mapreduce.Job: Counters: 0
2026-06-10 13:48:55,394 ERROR streaming.StreamJob: Job not successful!
Streaming Command Failed!

``

### Job: mr5_distance_calc
- **Status**: FAILED
- **Duration**: 3.47 seconds
- **Records Output**: 0- **Hadoop Log Tail**:
``text
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:49:01,941 INFO mapred.LocalJobRunner: map task executor complete.
2026-06-10 13:49:01,953 WARN mapred.LocalJobRunner: job_local14010253_0001
java.lang.Exception: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.mapred.LocalJobRunner$Job.runTasks(LocalJobRunner.java:492)
	at org.apache.hadoop.mapred.LocalJobRunner$Job.run(LocalJobRunner.java:552)
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 10 more
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	... 15 more
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 18 more
Caused by: java.lang.RuntimeException: configuration exception
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:222)
	at org.apache.hadoop.streaming.PipeMapper.configure(PipeMapper.java:66)
	... 23 more
Caused by: java.io.IOException: Cannot run program "python3": error=2, No such file or directory
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1048)
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:209)
	... 24 more
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:49:02,719 INFO mapreduce.Job: Job job_local14010253_0001 running in uber mode : false
2026-06-10 13:49:02,720 INFO mapreduce.Job:  map 0% reduce 0%
2026-06-10 13:49:02,722 INFO mapreduce.Job: Job job_local14010253_0001 failed with state FAILED due to: NA
2026-06-10 13:49:02,729 INFO mapreduce.Job: Counters: 0
2026-06-10 13:49:02,729 ERROR streaming.StreamJob: Job not successful!
Streaming Command Failed!

``

### Job: mr6_anomaly_detection
- **Status**: FAILED
- **Duration**: 3.77 seconds
- **Records Output**: 0- **Hadoop Log Tail**:
``text
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:49:09,084 INFO mapred.LocalJobRunner: map task executor complete.
2026-06-10 13:49:09,094 WARN mapred.LocalJobRunner: job_local865068596_0001
java.lang.Exception: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.mapred.LocalJobRunner$Job.runTasks(LocalJobRunner.java:492)
	at org.apache.hadoop.mapred.LocalJobRunner$Job.run(LocalJobRunner.java:552)
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 10 more
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	... 15 more
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 18 more
Caused by: java.lang.RuntimeException: configuration exception
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:222)
	at org.apache.hadoop.streaming.PipeMapper.configure(PipeMapper.java:66)
	... 23 more
Caused by: java.io.IOException: Cannot run program "python3": error=2, No such file or directory
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1048)
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:209)
	... 24 more
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:49:09,883 INFO mapreduce.Job: Job job_local865068596_0001 running in uber mode : false
2026-06-10 13:49:09,883 INFO mapreduce.Job:  map 0% reduce 0%
2026-06-10 13:49:09,885 INFO mapreduce.Job: Job job_local865068596_0001 failed with state FAILED due to: NA
2026-06-10 13:49:09,890 INFO mapreduce.Job: Counters: 0
2026-06-10 13:49:09,890 ERROR streaming.StreamJob: Job not successful!
Streaming Command Failed!

``

### Job: mr7_station_capacity
- **Status**: FAILED
- **Duration**: 3.38 seconds
- **Records Output**: 0- **Hadoop Log Tail**:
``text
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:49:16,196 INFO mapred.LocalJobRunner: map task executor complete.
2026-06-10 13:49:16,210 WARN mapred.LocalJobRunner: job_local1647481968_0001
java.lang.Exception: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.mapred.LocalJobRunner$Job.runTasks(LocalJobRunner.java:492)
	at org.apache.hadoop.mapred.LocalJobRunner$Job.run(LocalJobRunner.java:552)
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 10 more
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	... 15 more
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 18 more
Caused by: java.lang.RuntimeException: configuration exception
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:222)
	at org.apache.hadoop.streaming.PipeMapper.configure(PipeMapper.java:66)
	... 23 more
Caused by: java.io.IOException: Cannot run program "python3": error=2, No such file or directory
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1048)
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:209)
	... 24 more
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:49:16,988 INFO mapreduce.Job: Job job_local1647481968_0001 running in uber mode : false
2026-06-10 13:49:16,989 INFO mapreduce.Job:  map 0% reduce 0%
2026-06-10 13:49:16,991 INFO mapreduce.Job: Job job_local1647481968_0001 failed with state FAILED due to: NA
2026-06-10 13:49:16,996 INFO mapreduce.Job: Counters: 0
2026-06-10 13:49:16,996 ERROR streaming.StreamJob: Job not successful!
Streaming Command Failed!

``

### Job: mr8_station_status_check
- **Status**: FAILED
- **Duration**: 3.21 seconds
- **Records Output**: 0- **Hadoop Log Tail**:
``text
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:49:23,157 INFO mapred.LocalJobRunner: map task executor complete.
2026-06-10 13:49:23,165 WARN mapred.LocalJobRunner: job_local1420981098_0001
java.lang.Exception: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.mapred.LocalJobRunner$Job.runTasks(LocalJobRunner.java:492)
	at org.apache.hadoop.mapred.LocalJobRunner$Job.run(LocalJobRunner.java:552)
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapTask.runOldMapper(MapTask.java:462)
	at org.apache.hadoop.mapred.MapTask.run(MapTask.java:349)
	at org.apache.hadoop.mapred.LocalJobRunner$Job$MapTaskRunnable.run(LocalJobRunner.java:271)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 10 more
Caused by: java.lang.RuntimeException: Error in configuring object
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:113)
	at org.apache.hadoop.util.ReflectionUtils.setConf(ReflectionUtils.java:79)
	at org.apache.hadoop.util.ReflectionUtils.newInstance(ReflectionUtils.java:137)
	at org.apache.hadoop.mapred.MapRunner.configure(MapRunner.java:38)
	... 15 more
Caused by: java.lang.reflect.InvocationTargetException
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.hadoop.util.ReflectionUtils.setJobConf(ReflectionUtils.java:110)
	... 18 more
Caused by: java.lang.RuntimeException: configuration exception
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:222)
	at org.apache.hadoop.streaming.PipeMapper.configure(PipeMapper.java:66)
	... 23 more
Caused by: java.io.IOException: Cannot run program "python3": error=2, No such file or directory
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1048)
	at org.apache.hadoop.streaming.PipeMapRed.configure(PipeMapRed.java:209)
	... 24 more
Caused by: java.io.IOException: error=2, No such file or directory
	at java.lang.UNIXProcess.forkAndExec(Native Method)
	at java.lang.UNIXProcess.<init>(UNIXProcess.java:247)
	at java.lang.ProcessImpl.start(ProcessImpl.java:134)
	at java.lang.ProcessBuilder.start(ProcessBuilder.java:1029)
	... 25 more
2026-06-10 13:49:23,972 INFO mapreduce.Job: Job job_local1420981098_0001 running in uber mode : false
2026-06-10 13:49:23,973 INFO mapreduce.Job:  map 0% reduce 0%
2026-06-10 13:49:23,974 INFO mapreduce.Job: Job job_local1420981098_0001 failed with state FAILED due to: NA
2026-06-10 13:49:23,978 INFO mapreduce.Job: Counters: 0
2026-06-10 13:49:23,978 ERROR streaming.StreamJob: Job not successful!
Streaming Command Failed!

``

### Job: mr1_user_behavior
- **Status**: FAILED
- **Duration**: 2.01 seconds
- **Records Output**: 0- **Hadoop Log Tail**:
``text
docker : 2026-06-10 13:50:35,568 INFO impl.MetricsConfig: Loaded properties from hadoop-metrics2.properties
At D:\Bigdata\New game\citibike_tool_stack\scripts\run-all-jobs.ps1:72 char:5
+     docker exec -i citibike-namenode hadoop jar $STREAMING_JAR `
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (2026-06-10 13:5...ics2.properties:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError

2026-06-10 13:50:35,642 INFO impl.MetricsSystemImpl: Scheduled Metric snapshot period at 10 second(s).
2026-06-10 13:50:35,642 INFO impl.MetricsSystemImpl: JobTracker metrics system started
2026-06-10 13:50:35,654 WARN impl.MetricsSystemImpl: JobTracker metrics system already initialized!
2026-06-10 13:50:35,787 ERROR streaming.StreamJob: Error Launching job : Output directory
hdfs://namenode:9000/data/citibike/mapreduce/mr1_user_behavior already exists
Streaming Command Failed!

``

### Job: mr2_top_routes
- **Status**: SUCCESS
- **Duration**: 4.56 seconds
- **Records Output**: 4185

### Job: mr3_hourly_trends
- **Status**: SUCCESS
- **Duration**: 3.25 seconds
- **Records Output**: 24

### Job: mr4_weekly_analysis
- **Status**: SUCCESS
- **Duration**: 4.73 seconds
- **Records Output**: 14

### Job: mr5_distance_calc
- **Status**: SUCCESS
- **Duration**: 4.35 seconds
- **Records Output**: 4185

### Job: mr6_anomaly_detection
- **Status**: SUCCESS
- **Duration**: 3.51 seconds
- **Records Output**: 0

### Job: mr7_station_capacity
- **Status**: SUCCESS
- **Duration**: 3.43 seconds
- **Records Output**: 3

### Job: mr8_station_status_check
- **Status**: SUCCESS
- **Duration**: 3.22 seconds
- **Records Output**: 2

### Job: mr1_user_behavior
- **Status**: SUCCESS
- **Duration**: 3.57 seconds
- **Records Output**: 4
