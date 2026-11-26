from src.api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.storage import JSONSaver
from typing import List


def filter_aeroplanes(aeroplanes: List[Aeroplane], filter_countries: List[str]) -> List[Aeroplane]:
    if not filter_countries:
        return aeroplanes
    return [a for a in aeroplanes if any(fc.lower() in a.origin_country.lower() for fc in filter_countries)]


def get_aeroplanes_by_altitude(aeroplanes: List[Aeroplane], altitude_range: str) -> List[Aeroplane]:
    try:
        min_alt, max_alt = map(float, altitude_range.split("-"))
        return [a for a in aeroplanes if min_alt <= a.baro_altitude <= max_alt]
    except ValueError:
        print("Неверный формат диапазона высот. Ожидается: 1000 - 10000")
        return aeroplanes


def sort_aeroplanes(aeroplanes: List[Aeroplane]) -> List[Aeroplane]:
    return sorted(aeroplanes, reverse=True)  # DESC по высоте (__lt__)


def get_top_aeroplanes(aeroplanes: List[Aeroplane], top_n: int) -> List[Aeroplane]:
    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: List[Aeroplane]):
    if not aeroplanes:
        print("Самолеты не найдены по заданным критериям.")
        return
    print("\n" + "=" * 80)
    for a in aeroplanes:
        print(a)
    print("=" * 80 + "\n")


def user_interaction():
    api = AeroplanesAPI()
    json_saver = JSONSaver()

    country = input("Введите название страны: ")
    raw_data = api.get_aeroplanes(country)
    aeroplanes = Aeroplane.cast_to_object_list(raw_data)

    if not aeroplanes:
        print("Нет данных о самолетах. Проверьте название страны или повторите попытку позже.")
        return

    # Сохраняем в файл
    for a in aeroplanes:
        json_saver.add_aeroplane(a)
    print(f"Данные о {len(aeroplanes)} самолетах сохранены в JSON-файл.")

    try:
        top_n = int(input("Введите количество самолетов для вывода в топ N: "))
        filter_words = input("Введите названия стран для фильтрации по стране регистрации (через пробел): ").split()
        altitude_range = input("Введите диапазон высот полета (например, 0 - 10000): ")

        filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)
        ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)
        sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
        top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
        print_aeroplanes(top_aeroplanes)
    except ValueError:
        print("Ошибка: введите корректное число для топа N.")


if __name__ == "__main__":
    user_interaction()
