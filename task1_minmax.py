from typing import List, Tuple

def find_min_max(arr: List[float]) -> Tuple[float, float]:
    """
    Знаходить мінімальний та максимальний елементи в масиві
    методом «розділяй і володарюй».

    Args:
        arr: список чисел довільної довжини

    Returns:
        (мінімум, максимум)

    Complexity:
        O(n) за часом, O(log n) за пам’яттю (через рекурсію)
    """
    if not arr:
        raise ValueError("Масив не повинен бути порожнім")

    def helper(left: int, right: int) -> Tuple[float, float]:
        if left == right:  # 1 елемент
            return arr[left], arr[left]

        if right - left == 1:  # 2 елементи
            if arr[left] < arr[right]:
                return arr[left], arr[right]
            return arr[right], arr[left]

        mid = (left + right) // 2
        min1, max1 = helper(left, mid)
        min2, max2 = helper(mid + 1, right)

        return min(min1, min2), max(max1, max2)

    return helper(0, len(arr) - 1)


if __name__ == "__main__":
    data = [3, 1, 9, -2, 7, 7]
    print("Array:", data)
    print("Min/Max:", find_min_max(data))

