from utils import format_salary


class VacanciesNavigator:
    def __init__(self, vacancies_data, per_page=10):
        self.vacancies = vacancies_data['items']
        self.page_size = per_page
        self.total_pages = (len(self.vacancies) + per_page - 1) // per_page
        self.current_page = 0
        self.detailed_vacancy = None

    def get_current_vacancies(self):
        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(self.vacancies))
        return self.vacancies[start_index:end_index]

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            return True
        else:
            print("Вы достигли конца списка вакансий")
            return False

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            return True
        else:
            print("Вы достигли начала списка вакансий")
            return False

    def display_vacancies(self):
        vacancies = self.get_current_vacancies()
        for index, vacancy in enumerate(vacancies, start=1):
            salary = format_salary(vacancy.get('salary'))
            snippet_responsibility = vacancy['snippet']['responsibility'][:75] + '...' if vacancy['snippet'][
                                                                                              'responsibility'] and len(
                vacancy['snippet']['responsibility']) > 75 else vacancy['snippet']['responsibility']
            result = ""
            print(f"{index}. Название вакансии: {vacancy['name']}\n   Заработная плата: {salary}")
            print(f"   Обязанности: {snippet_responsibility}")
            print(f"   Требуемый опыт работы: {vacancy['experience']['name']}")
            print(f"   Тип занятости: {vacancy['employment']['name']}")
            print(f"   График работы: {vacancy['schedule']['name']}")
            print()