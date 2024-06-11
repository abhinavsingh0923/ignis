from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job, Task
from .serializer import JobSerializer
from .tasks import scrape_coin_data
import uuid

class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data
        if not all(isinstance(coin, str) for coin in coins):
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

        job = Job.objects.create()
        for coin in coins:
            task = Task.objects.create(job=job, coin=coin)  
            scrape_coin_data.delay(task.id, coin)

        return Response({'job_id': job.id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            serializer = JobSerializer(job)
            return Response(serializer.data)
        except (ValueError, Job.DoesNotExist):
            return Response({'error': 'Invalid job_id'}, status=status.HTTP_400_BAD_REQUEST)
