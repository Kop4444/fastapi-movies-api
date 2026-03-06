from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from datetime import datetime
import logging
import threading
from fastapi import FastAPI

from database import SessionLocal
import crud
from app.email_service import email_service

# Импортируем состояние
from app.state import get_email_status

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def send_movie_report_job():
    """
    Фоновая задача для отправки отчета о фильмах
    Запускается каждые 5 минут, но отправляет только если флаг включен
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Получаем актуальный статус отправки
    email_sending_enabled = get_email_status()
    
    logger.info("=" * 70)
    logger.info(f"🔔 ЗАПУСК ЗАДАЧИ: {current_time}")
    logger.info("=" * 70)
    
    # Логируем статус
    status_icon = "✅" if email_sending_enabled else "❌"
    status_text = "ВКЛЮЧЕНА" if email_sending_enabled else "ОТКЛЮЧЕНА"
    logger.info(f"{status_icon} Статус отправки: {status_text} (email_sending_enabled = {email_sending_enabled})")
    
    # Проверяем, включена ли отправка
    if not email_sending_enabled:
        logger.info("⚠️ ОТПРАВКА НА ПОЧТУ ОТКЛЮЧЕНА (кнопка на сайте)")
        logger.info("Задача завершена без отправки email")
        logger.info("=" * 70)
        logger.info("")
        return
    
    logger.info("✓ ОТПРАВКА НА ПОЧТУ ВКЛЮЧЕНА, продолжаем выполнение...")
    
    try:
        # Получаем сессию БД
        logger.info("📦 Подключение к базе данных...")
        db = SessionLocal()
        logger.info("✓ Подключение к БД установлено")
        
        # Получаем все фильмы
        logger.info("🔍 Получение списка фильмов...")
        movies = crud.get_movies(db)
        logger.info(f"✓ Получено фильмов: {len(movies)}")
        
        # Преобразуем в словари
        movies_data = []
        for movie in movies:
            movies_data.append({
                'id': movie.id,
                'title': movie.title,
                'year': movie.year,
                'rating': movie.rating
            })
        
        # Логируем информацию о фильмах
        if movies_data:
            logger.info(f"📊 Подготовлено фильмов для отправки: {len(movies_data)}")
            logger.info("📋 Первые 3 фильма:")
            for i, movie in enumerate(movies_data[:3]):
                rating_star = "⭐" * int(movie['rating']/2) if movie['rating'] else "❌"
                logger.info(f"   {i+1}. ID:{movie['id']} | {movie['title']} ({movie['year']}) | Рейтинг: {movie['rating']} {rating_star}")
            if len(movies_data) > 3:
                logger.info(f"   ... и еще {len(movies_data) - 3} фильмов")
        else:
            logger.info("📭 В базе данных нет фильмов")
        
        # Отправляем отчет
        logger.info(f"📧 Отправка email на Yugrinkd@mail.ru...")
        success = email_service.send_movie_report(movies_data)
        
        if success:
            logger.info(f"✅ ОТЧЕТ УСПЕШНО ОТПРАВЛЕН на Yugrinkd@mail.ru")
            logger.info(f"   Фильмов в отчете: {len(movies_data)}")
        else:
            logger.error(f"❌ ОШИБКА ОТПРАВКИ ОТЧЕТА")
        
        db.close()
        logger.info("🔒 Соединение с БД закрыто")
        
    except Exception as e:
        logger.error(f"🔥 КРИТИЧЕСКАЯ ОШИБКА В ЗАДАЧЕ: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    logger.info("=" * 70)
    logger.info(f"✅ ЗАДАЧА ЗАВЕРШЕНА: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)
    logger.info("")  # Пустая строка для разделения логов

# Создаем планировщик
scheduler = BackgroundScheduler(
    job_defaults={
        'coalesce': True,        # Объединять пропущенные запуски
        'max_instances': 1,      # Только один экземпляр задачи одновременно
        'misfire_grace_time': 30 # 30 секунд на выполнение после пропуска
    }
)

# Настройка триггеров - КАЖДЫЕ 5 МИНУТ
test_trigger = IntervalTrigger(minutes=5)

# Добавляем задачу в планировщик
scheduler.add_job(
    send_movie_report_job,
    trigger=test_trigger,  # КАЖДЫЕ 5 МИНУТ
    id='send_movie_report',
    name='Send movie report every 5 minutes',
    replace_existing=True,
    next_run_time=datetime.now()  # Запускаем сразу при старте
)

# Логируем информацию о запуске
logger.info("")
logger.info("╔" + "═" * 68 + "╗")
logger.info("║              НАСТРОЙКА ПЛАНИРОВЩИКА ЗАДАЧ               ║")
logger.info("╠" + "═" * 68 + "╣")
logger.info(f"║ Задача: send_movie_report                                  ║")
logger.info(f"║ Интервал: КАЖДЫЕ 5 МИНУТ                                  ║")
logger.info(f"║ Получатель: Yugrinkd@mail.ru                              ║")
logger.info(f"║ Управление: через кнопки на сайте                         ║")
logger.info(f"║ Начальный статус: {get_email_status()}                                   ║")
logger.info("╚" + "═" * 68 + "╝")
logger.info("")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом планировщика
    Запуск при старте приложения и остановка при завершении
    """
    logger.info("")
    logger.info("╔" + "═" * 68 + "╗")
    logger.info("║              ЗАПУСК ПРИЛОЖЕНИЯ FASTAPI               ║")
    logger.info("╚" + "═" * 68 + "╝")
    logger.info("")
    
    # Запускаем планировщик
    scheduler.start()
    logger.info("✓ Планировщик задач ЗАПУЩЕН")
    
    # Получаем информацию о задаче
    job = scheduler.get_job('send_movie_report')
    if job:
        next_run = job.next_run_time
        logger.info(f"✓ Задача 'send_movie_report' активна")
        logger.info(f"  Следующий запуск: {next_run.strftime('%Y-%m-%d %H:%M:%S') if next_run else 'Не запланирован'}")
        logger.info(f"  Интервал: каждые 5 минут")
        logger.info(f"  Текущий статус: {'✅ ВКЛЮЧЕНА' if get_email_status() else '❌ ОТКЛЮЧЕНА'}")
    
    logger.info("")
    logger.info("╔" + "═" * 68 + "╗")
    logger.info("║         ЗАПУСК НАЧАЛЬНОЙ ЗАДАЧИ (ПРИ СТАРТЕ)         ║")
    logger.info("╚" + "═" * 68 + "╝")
    logger.info("")
    
    # Запускаем задачу сразу при старте
    thread = threading.Thread(target=send_movie_report_job)
    thread.daemon = True
    thread.start()
    
    logger.info("✓ Начальная задача запущена")
    logger.info("  Следующие запуски будут каждые 5 минут")
    logger.info("  Нажимайте кнопки на сайте для включения/отключения")
    logger.info("")
    
    yield  # Здесь работает приложение
    
    logger.info("")
    logger.info("╔" + "═" * 68 + "╗")
    logger.info("║              ОСТАНОВКА ПРИЛОЖЕНИЯ                     ║")
    logger.info("╚" + "═" * 68 + "╝")
    logger.info("")
    
    # Останавливаем планировщик
    scheduler.shutdown()
    logger.info("✓ Планировщик задач ОСТАНОВЛЕН")
    logger.info("")