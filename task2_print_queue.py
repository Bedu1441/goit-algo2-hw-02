from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера.

    Жадібна стратегія:
    - Спочатку сортуємо за пріоритетом (1 -> 3), зберігаючи вхідний порядок в межах пріоритету.
    - Далі формуємо "партії" друку послідовно: додаємо модель у поточну партію,
      якщо не перевищимо max_items і max_volume, інакше — закриваємо партію та починаємо нову.
    - Час партії = max(print_time) серед моделей у партії.
    """
    jobs = [
        PrintJob(
            id=j["id"],
            volume=float(j["volume"]),
            priority=int(j["priority"]),
            print_time=int(j["print_time"]),
        )
        for j in print_jobs
    ]
    printer = PrinterConstraints(
        max_volume=float(constraints["max_volume"]),
        max_items=int(constraints["max_items"]),
    )

    # Валідація базових обмежень
    if printer.max_volume <= 0 or printer.max_items <= 0:
        raise ValueError("Некоректні обмеження принтера (max_volume/max_items мають бути > 0)")

    for j in jobs:
        if j.volume <= 0 or j.print_time <= 0:
            raise ValueError(f"Некоректні параметри задачі {j.id} (volume/print_time мають бути > 0)")
        if j.priority not in (1, 2, 3):
            raise ValueError(f"Некоректний пріоритет у задачі {j.id} (має бути 1,2,3)")
        if j.volume > printer.max_volume:
            raise ValueError(
                f"Модель {j.id} має об'єм {j.volume}, що перевищує max_volume={printer.max_volume}"
            )

    # Стабільне сортування за пріоритетом (в межах однакового пріоритету порядок збережеться)
    jobs.sort(key=lambda x: x.priority)

    print_order: List[str] = []
    total_time = 0

    current_group: List[PrintJob] = []
    current_volume = 0.0
    current_group_time = 0

    def flush_group() -> None:
        nonlocal current_group, current_volume, current_group_time, total_time
        if not current_group:
            return
        # порядок друку — як у групах, у тому порядку, як ми їх сформували
        for job in current_group:
            print_order.append(job.id)
        # час групи — максимальний час серед моделей групи
        total_time += current_group_time

        current_group = []
        current_volume = 0.0
        current_group_time = 0

    for job in jobs:
        exceeds_items = len(current_group) + 1 > printer.max_items
        exceeds_volume = current_volume + job.volume > printer.max_volume

        if exceeds_items or exceeds_volume:
            flush_group()

        current_group.append(job)
        current_volume += job.volume
        if job.print_time > current_group_time:
            current_group_time = job.print_time

    flush_group()

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
