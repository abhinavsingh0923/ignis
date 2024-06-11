from celery import shared_task
from .models import Task
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin_data(task_id, coin):
    task = Task.objects.get(id=task_id)
    task.status = 'in_progress'
    task.save()
    
    scraper = CoinMarketCap(coin)
    try:
        data = scraper.scrape()
        task.output = data
        task.status = 'completed'
    except Exception as e:
        task.output = {'error': str(e)}
        task.status = 'failed'
    
    task.save()
