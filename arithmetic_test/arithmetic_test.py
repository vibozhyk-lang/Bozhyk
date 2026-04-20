class MatrixHandler:
    def __init__(self, grid):
        self.values = grid
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0

    def display(self):
        """Вывод матрицы с округлением до 2 знаков"""
        for row in self.values:
            print(' '.join(f"{round(element, 2):g}" for element in row))

    def add(self, other):
        """Сложение двух матриц одинаковой размерности"""
        if self.height != other.height or self.width != other.width:
            print("Ошибка: несовпадение размеров для сложения.")
            return None

        result = [[self.values[i][j] + other.values[i][j] for j in range(self.width)]
                  for i in range(self.height)]
        return MatrixHandler(result)

    def scale(self, factor):
        """Умножение матрицы на скаляр (число)"""
        result = [[val * factor for val in row] for row in self.values]
        return MatrixHandler(result)

    def multiply(self, other):
        """Произведение двух матриц (скалярное произведение строк на столбцы)"""
        if self.width != other.height:
            print("Ошибка: количество столбцов первой матрицы должно быть равно количеству строк второй.")
            return None

        result = [[sum(self.values[i][k] * other.values[k][j] for k in range(self.width))
                   for j in range(other.width)] for i in range(self.height)]
        return MatrixHandler(result)

    def transform(self, variant=1):
        """Различные типы транспонирования и отражения"""
        if variant == 1:  # Относительно главной диагонали
            result = [[self.values[j][i] for j in range(self.height)] for i in range(self.width)]
        elif variant == 2:  # Относительно побочной диагонали
            result = [[self.values[self.height - 1 - j][self.width - 1 - i] for j in range(self.height)]
                      for i in range(self.width)]
        elif variant == 3:  # По вертикальной оси
            result = [line[::-1] for line in self.values]
        elif variant == 4:  # По горизонтальной оси
            result = self.values[::-1]
        else:
            return None
        return MatrixHandler(result)

    def calc_determinant(self):
        """Публичный метод для запуска расчета определителя"""
        if self.height != self.width:
            print("Ошибка: определитель существует только для квадратных матриц.")
            return None
        return self._recursive_det(self.values)

    def _recursive_det(self, m):
        """Внутренняя рекурсивная функция поиска определителя через миноры"""
        if len(m) == 1:
            return m[0][0]
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        total = 0
        for col_idx in range(len(m)):
            # Создаем минор путем исключения первой строки и текущего столбца
            minor = [row[:col_idx] + row[col_idx + 1:] for row in m[1:]]
            total += ((-1) ** col_idx) * m[0][col_idx] * self._recursive_det(minor)
        return total

    def invert(self):
        """Создание обратной матрицы через присоединенную матрицу"""
        det_val = self.calc_determinant()
        if not det_val:
            print("Ошибка: матрица вырожденная (определитель равен 0).")
            return None

        n = self.height
        cofactors = []
        for i in range(n):
            row_cofactors = []
            for j in range(n):
                # Формируем подматрицу для поиска алгебраического дополнения
                sub_matrix = [r[:j] + r[j + 1:] for idx, r in enumerate(self.values) if idx != i]
                row_cofactors.append(((-1) ** (i + j)) * self._recursive_det(sub_matrix))
            cofactors.append(row_cofactors)

        # Транспонируем матрицу дополнений и делим на определитель
        inverted_grid = [[cofactors[j][i] / det_val for j in range(n)] for i in range(n)]
        return MatrixHandler(inverted_grid)


def request_matrix_input():
    """Сбор данных от пользователя для создания объекта MatrixHandler"""
    while True:
        try:
            params = input("Введите количество строк и столбцов (R C): ").split()
            rows, cols = int(params[0]), int(params[1])
            break
        except:
            print("Некорректные параметры.")

    raw_data = []
    print(f"Введите элементы матрицы ({rows}x{cols}):")
    for _ in range(rows):
        while True:
            row_input = input("> ").split()
            if len(row_input) == cols:
                try:
                    raw_data.append([float(x) for x in row_input])
                    break
                except:
                    print("Введите числовые значения.")
            else:
                print(f"Ожидалось элементов: {cols}.")
    return MatrixHandler(raw_data)


def main_loop():
    """Главное меню программы"""
    while True:
        print("\n=== Калькулятор матриц ===")
        print("1. Сложение\n2. Умножение на число\n3. Перемножение матриц")
        print("4. Транспонирование\n5. Определитель\n6. Инверсия\n0. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            a, b = request_matrix_input(), request_matrix_input()
            res = a.add(b)
            if res: res.display()
        elif choice == '2':
            obj = request_matrix_input()
            try:
                mult = float(input("Множитель: "))
                obj.scale(mult).display()
            except:
                pass
        elif choice == '3':
            a, b = request_matrix_input(), request_matrix_input()
            res = a.multiply(b)
            if res: res.display()
        elif choice == '4':
            print("Варианты: 1-Главная, 2-Побочная, 3-Вертикаль, 4-Горизонталь")
            mode = int(input("Тип трансформации: "))
            request_matrix_input().transform(mode).display()
        elif choice == '5':
            val = request_matrix_input().calc_determinant()
            if val is not None: print("Результат:", round(val, 4))
        elif choice == '6':
            res = request_matrix_input().invert()
            if res: res.display()
        elif choice == '0':
            print("Программа завершена.")
            break


if __name__ == "__main__":
    main_loop()