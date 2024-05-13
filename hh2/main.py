from data.remotestore import VacanciesNavigator
from data.jsonpy import save_to_json
from data.db import save_to_sqlite
from data.datastore import display_detailed_vacancy,analyze_salaries_by_region,get_vacancies,get_all_regions


def main():
    try:
        url = "https://api.hh.ru/vacancies"
        per_page = 10
        number_of_pages = int(input("Введите количество страниц для загрузки: "))
        parameters = {
            "text": "Python",
            "currency": "RUR",
            "per_page": per_page,
            "page": 0
        }
        all_vacancies_data = []
        for page in range(number_of_pages):
            vacancies_data = get_vacancies(url, parameters)
            if vacancies_data:
                all_vacancies_data.extend(vacancies_data['items'])
                parameters['page'] += 1
            else:
                break

        if all_vacancies_data:
            save_to_json({'items': all_vacancies_data}, "vacancies.json")
            save_to_sqlite({'items': all_vacancies_data})  # Сохраняем в SQLite
            all_regions = get_all_regions({'items': all_vacancies_data})
            print("Доступные регионы:")
            for region in all_regions:
                print(region)
            while True:
                print("\nВыберите действие:")
                print("1. Просмотреть вакансии")
                print("2. Анализ зарплат")
                print("3. Выход")
                choice = input("> ")
                match choice:
                    case '1':
                        navigator = VacanciesNavigator(
                            {'items': all_vacancies_data}, per_page
                        )
                        while True:
                            navigator.display_vacancies()
                            choice = input(
                                "Введите команду (n - next, b - back, q - quit, номер вакансии - детали): "
                            )
                            match choice:
                                case num if num.isdigit():
                                    #вынести расчеты в отдельную фунцию, передавать только значение из input
                                    vacancy_index = (int(num) - 1) + (navigator.current_page * navigator.page_size)
                                    if 0 <= vacancy_index < len(all_vacancies_data):
                                        display_detailed_vacancy(all_vacancies_data[vacancy_index], include_manager=True)  # Pass the flag here
                                        input("Нажмите Enter для продолжения...")
                                        choice = None
                                    else:
                                        print("Неверный номер вакансии.")
                                case 'n' | 'next':
                                    if not navigator.next_page():
                                        break
                                case 'b' | 'back':
                                    if not navigator.previous_page():
                                        break
                                case 'q' | 'quit' | '3':
                                    break
                                case _:
                                    print(
                                        "Неверная команда! Допустимые команды: n (next), b (back), q (quit)"
                                    )
                    case '2':
                        analyze_salaries_by_region()
                    case '3':
                        break
                    case _:
                        print("Неверный выбор.")
    except KeyboardInterrupt:
        print("\nПрограмма завершена по запросу пользователя.")


if __name__ == "__main__":
    main()