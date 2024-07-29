# main/management/commands/importar_disciplinas.py

from django.core.management.base import BaseCommand
from main.models import Forum
from main.scraping import DisciplineWebScraper

class Command(BaseCommand):
    help = 'Raspa dados das disciplinas do site Sigaa da UnB e salva como fóruns'

    def handle(self, *args, **kwargs):
        departments = ["518", "524", "673"]  
        year = "2024"  
        period = "1"  

        Forum.objects.all().delete()
        self.stdout.write(self.style.WARNING('Todos os fóruns antigos foram removidos.'))

        for department in departments:
            scraper = DisciplineWebScraper(department, year, period)
            disciplines = scraper.get_disciplines()

            for code, names in disciplines.items():
                for name in names:
                    title = f"{code} - {name}"
                    forum, created = Forum.objects.get_or_create(
                        title=title,
                        defaults={'description': ''}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Fórum "{title}" criado com sucesso.'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Fórum "{title}" já existe.'))
