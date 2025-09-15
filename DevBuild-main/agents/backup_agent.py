# backup_agent.py

from agent_logic import AgentLogic
import shutil
import os
import datetime
import zipfile

class BackupAgent(AgentLogic):
    def __init__(self):
        super().__init__("Backup")
        self.backup_directory = "backups"
        self.source_directory = "data_directory"  # Исходная директория для бэкапа
        self.max_backups = 10  # Максимальное количество хранимых бэкапов
        self.backup_interval = 86400  # Интервал между бэкапами в секундах (1 день)

    def execute(self):
        """Основной метод выполнения агента"""
        self.logger.info("Запуск процесса резервного копирования...")
        
        # Проверяем существование директории для бэкапов
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)
            self.logger.info("Создана директория для бэкапов")

        # Формируем имя файла бэкапа
        backup_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Создаем архив
            shutil.make_archive(
                os.path.join(self.backup_directory, backup_name),
                'zip',
                self.source_directory
            )
            self.logger.info(f"Бэкап успешно создан: {backup_name}")
            
            # Очищаем старые бэкапы
            self.cleanup_old_backups()
            
        except Exception as e:
            self.logger.error(f"Ошибка при создании бэкапа: {str(e)}")

    def cleanup_old_backups(self):
        """Удаление старых бэкапов"""
        self.logger.info("Проверка количества бэкапов...")
        
        # Получаем список всех бэкапов
        backup_files = [
            f for f in os.listdir(self.backup_directory) 
            if f.endswith('.zip')
        ]
        
        # Сортируем по дате создания
        backup_files.sort(key=lambda x: os.path.getmtime(
            os.path.join(self.backup_directory, x)
        ))
        
        # Удаляем лишние бэкапы
        for file in backup_files[:-self.max_backups]:
            try:
                os.remove(os.path.join(self.backup_directory, file))
                self.logger.info(f"Удален старый бэкап: {file}")
            except Exception as e:
                self.logger.error(f"Ошибка при удалении бэкапа {file}: {str(e)}")

    def check_integrity(self):
        """Проверка целостности всех бэкапов"""
        self.logger.info("Проверка целостности бэкапов...")
        
        for file in os.listdir(self.backup_directory):
            if file.endswith('.zip'):
                try:
                    with zipfile.ZipFile(
                        os.path.join(self.backup_directory, file), 
                        'r'
                    ) as zf:
                        zf.testzip()
                    self.logger.info(f"Бэкап {file} цел")
                except Exception as e:
                    self.logger.error(f"Ошибка целостности бэкапа {file}: {str(e)}")

    def restore_from_backup(self, backup_name: str):
        """Восстановление из указанного бэкапа"""
        self.logger.info(f"Восстановление из бэкапа {backup_name}")
        
        try:
            # Распаковываем архив
            shutil.unpack_archive(
                os.path.join(self.backup_directory, backup_name),
                self.source_directory
            )
            self.logger.info("Восстановление успешно завершено")
            
        except Exception as e:
            self.logger.error(f"Ошибка при восстановлении: {str(e)}")