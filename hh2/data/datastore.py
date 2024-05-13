from data.jsonpy import read_from_json
from collections import defaultdict
from utils import format_salary
import requests

def analyze_salaries_by_region():
    vacancies_data = read_from_json("vacancies.json")
    regions = defaultdict(list)
    for vacancy in vacancies_data["items"]:
        region = vacancy["area"]["name"]
        salary_data = vacancy.get("salary")
        if salary_data and salary_data.get('currency') == 'RUR':
            salary = format_salary(salary_data)
            if salary is not None:
                regions[region].append(salary)
    for region, salaries in regions.items():
        if salaries:
            salaries = [salary for salary in salaries if salary > 0]
            if salaries:
                minimum_salary = min(salaries)
                maximum_salary = max(salaries)
                average_salary = sum(salaries) / len(salaries)
                print(f"Регион: {region}, Средняя зп: {average_salary:.2f} RUR, "
                      f"Максимальная зп: {maximum_salary} RUR, "
                      f"Минимальная зп: {minimum_salary} RUR")

def display_detailed_vacancy(vacancy, include_manager=False):
    # собрать строку с выводом или адапатировать под один print()
    print(f"Название вакансии: {vacancy['name']}")
    print(f"Заработная плата: {format_salary(vacancy.get('salary'))}")
    print(f"Ссылка: {vacancy['alternate_url']}")
    print(f"Обязанности: {vacancy['snippet']['responsibility']}")
    print(f"Требования: {vacancy['snippet']['requirement']}")
    print(f"Компания: {vacancy['employer']['name']}")
    description = vacancy.get('description')
    if description:
        print(f"Описание: {description}")
    else:
        print("Описание: Отсутствует")
    if include_manager:
        contacts = vacancy.get('contacts')
        if contacts:
            manager_name = contacts.get('name')
            if manager_name:
                print(f"Руководитель: {manager_name}")
            else:
                print("Информация о руководителе отсутствует (имя не указано).")
        else:
            print("Информация о руководителе отсутствует (нет поля контактов).")

def get_vacancies(url, parameters, ca_certificate_path=None):
    response = requests.get(url, params=parameters, verify=ca_certificate_path)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Не удалось загрузить данные с {url}")
        return None

def get_all_regions(vacancies_data):
    regions = set()
    for vacancy in vacancies_data['items']:
        region_name = vacancy['area']['name']
        regions.add(region_name)
        # Проверка на наличие вложенных регионов:
        for vacancy in vacancies_data['items']:
            if vacancy['area']['name'] == region_name and vacancy['area'].get('parent_name'):
                regions.add(vacancy['area']['parent_name'])
    return sorted(list(regions))