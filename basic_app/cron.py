from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule
from .models import Story
from .views import delete_stories
class MyCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'myapp.my_cron_job'

    def do(self):
        expired_at = datetime.now() - timedelta(days=1)
        st_to_delete = Story.objects.filter(created_at__lte=expired_at)
        for story in st_to_delete:
            story.delete()
class DeleteOldStories(CronJobBase):
    RUN_AT_TIMES = ['00:00'] # Thời điểm để chạy cron job.

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'myapp.delete_old_stories'

    def do(self):
        delete_stories(None) # Thực hiện view delete_stories.