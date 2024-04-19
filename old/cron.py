from crontab import CronTab
cron = CronTab()
job = cron.new(command='python dynamic-lb.py')
job.minute.every(1)
cron.write('cron.txt')