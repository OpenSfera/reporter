# reporter

persist sensors data.

### How works

reporter listen on `local/status` for sensors data and save data every `reporter_sample_time` (10 minutes by default)

10 minutes per sample mean 
 - in a hour 6
 - in a day 144
 - in a week 1008
 - in month 4320
 - in year 51840

### TODO
