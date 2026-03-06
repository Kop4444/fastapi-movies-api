from typing import List, Dict
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("MAIL_SERVER", "smtp.mail.ru")
        self.smtp_port = int(os.getenv("MAIL_PORT", 587))
        self.username = os.getenv("MAIL_USERNAME", "")
        self.password = os.getenv("MAIL_PASSWORD", "")
        self.from_email = os.getenv("MAIL_FROM", "")
        self.admin_email = os.getenv("ADMIN_EMAIL", "")
    
    def send_movie_report(self, movies: List[Dict]) -> bool:
        """
        Отправка отчета о фильмах на email
        """
        try:
            # Создаем сообщение
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.admin_email
            msg['Subject'] = "Ежедневный отчет о фильмах"
            msg['X-Mailer'] = 'FastAPI Movie App'
            
            # Формируем HTML-содержимое
            html = self._generate_movie_report_html(movies)
            msg.attach(MIMEText(html, 'html', 'utf-8'))
            
            # Отправляем через SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"[{self._current_time()}] Отчет успешно отправлен на {self.admin_email}")
            print(f"   Сервер: {self.smtp_server}, Порт: {self.smtp_port}")
            print(f"   Фильмов в отчете: {len(movies)}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"[{self._current_time()}] Ошибка аутентификации: {e}")
            print("   Проверьте логин и пароль. Для Mail.ru нужен пароль приложения!")
            return False
        except smtplib.SMTPException as e:
            print(f"[{self._current_time()}] Ошибка SMTP: {e}")
            return False
        except Exception as e:
            print(f"[{self._current_time()}] Общая ошибка отправки email: {e}")
            return False
    
    def _generate_movie_report_html(self, movies: List[Dict]) -> str:
        """
        Генерация HTML-шаблона для письма
        """
        if not movies:
            movies_html = "<p>В базе данных нет фильмов</p>"
        else:
            movies_rows = ""
            for movie in movies:
                rating_class = "high" if movie.get('rating', 0) and movie.get('rating', 0) >= 8 else "medium" if movie.get('rating', 0) and movie.get('rating', 0) >= 5 else "low"
                movies_rows += f"""
                <tr>
                    <td>{movie.get('id', '')}</td>
                    <td>{movie.get('title', '')}</td>
                    <td>{movie.get('year', '')}</td>
                    <td class="rating-{rating_class}">{movie.get('rating', 'N/A')}</td>
                </tr>
                """
            
            movies_html = f"""
            <table class="movies-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Название</th>
                        <th>Год</th>
                        <th>Рейтинг</th>
                    </tr>
                </thead>
                <tbody>
                    {movies_rows}
                </tbody>
            </table>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .movies-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                .movies-table th {{ background: #333; color: white; padding: 10px; text-align: left; }}
                .movies-table td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                .movies-table tr:hover {{ background-color: #f5f5f5; }}
                .rating-high {{ color: #28a745; font-weight: bold; }}
                .rating-medium {{ color: #ffc107; font-weight: bold; }}
                .rating-low {{ color: #dc3545; font-weight: bold; }}
                .footer {{ margin-top: 30px; text-align: center; color: #666; padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎬 Movie Catalog Report</h1>
                <p>Ежедневная сводка по фильмам</p>
            </div>
            
            <h2>Статистика</h2>
            <p>Всего фильмов: <strong>{len(movies)}</strong></p>
            <p>Дата отчета: <strong>{self._current_time()}</strong></p>
            
            <h2>Список фильмов</h2>
            {movies_html}
            
            <div class="footer">
                <p>© 2026 Movie Catalog App. Автоматическая рассылка.</p>
                <p>Получатель: {self.admin_email}</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def _current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Создаем глобальный экземпляр для использования в приложении
email_service = EmailService()