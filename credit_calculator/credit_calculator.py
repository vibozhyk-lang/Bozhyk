import math
import argparse
import sys


class LoanCalculator:
    def __init__(self, args):
        self.calc_type = args.type
        self.debt_amount = args.principal
        self.monthly_installment = args.payment
        self.months_count = args.periods
        self.annual_rate = args.interest

        # Валидация наличия и корректности процентной ставки
        if self.annual_rate is None or self.annual_rate <= 0:
            print("Ошибка: параметры указаны неверно.")
            sys.exit()

        # Месячная процентная ставка в долях
        self.monthly_rate = self.annual_rate / (12 * 100)

    def _show_extra_costs(self, total_sum, start_sum):
        """Вычисляет и выводит итоговую переплату."""
        print(f"Переплата по кредиту: {int(total_sum - start_sum)}")

    def calculate_annuity_payment(self):
        """Расчет суммы ежемесячного платежа."""
        compound_factor = (1 + self.monthly_rate) ** self.months_count
        payment = self.debt_amount * (self.monthly_rate * compound_factor) / (compound_factor - 1)
        payment = math.ceil(payment)
        print(f"Ваш ежемесячный аннуитетный платеж составит {payment}.")
        self._show_extra_costs(payment * self.months_count, self.debt_amount)

    def calculate_principal_value(self):
        """Расчет максимально возможной суммы займа."""
        compound_factor = (1 + self.monthly_rate) ** self.months_count
        principal = self.monthly_installment / ((self.monthly_rate * compound_factor) / (compound_factor - 1))
        principal = math.floor(principal)
        print(f"Основная сумма займа: {principal}.")
        self._show_extra_costs(self.monthly_installment * self.months_count, principal)

    def calculate_period_length(self):
        """Расчет времени, необходимого для погашения долга."""
        log_argument = self.monthly_installment / (self.monthly_installment - self.monthly_rate * self.debt_amount)
        total_months = math.ceil(math.log(log_argument, 1 + self.monthly_rate))

        years, months = divmod(total_months, 12)
        duration_parts = []
        if years > 0:
            duration_parts.append(f"{years} {'год' if years == 1 else 'года' if 2 <= years <= 4 else 'лет'}")
        if months > 0:
            duration_parts.append(f"{months} {'месяц' if months == 1 else 'месяца' if 2 <= months <= 4 else 'месяцев'}")

        print(f"Срок выплаты составит {' и '.join(duration_parts)}.")
        self._show_extra_costs(self.monthly_installment * total_months, self.debt_amount)

    def calculate_diff_payments(self):
        """Расчет дифференцированных платежей по месяцам."""
        total_payout = 0
        for m in range(1, self.months_count + 1):
            unpaid_balance = self.debt_amount * (m - 1) / self.months_count
            current_installment = (self.debt_amount / self.months_count) + self.monthly_rate * (self.debt_amount - unpaid_balance)
            current_installment = math.ceil(current_installment)
            total_payout += current_installment
            print(f"Месяц {m}: платеж — {current_installment}")

        self._show_extra_costs(total_payout, self.debt_amount)

    def is_input_valid(self):
        """Проверка логической связности и корректности входных данных."""
        inputs = [self.debt_amount, self.monthly_installment, self.months_count, self.annual_rate]
        # Значения не могут быть отрицательными
        if any(v is not None and v < 0 for v in inputs):
            return False

        # Дифференцированные платежи несовместимы с фиксированным ежемесячным взносом
        if self.calc_type == "diff" and self.monthly_installment is not None:
            return False

        # Должно быть заполнено минимум 4 параметра из 5 (тип + 3 числовых)
        check_list = [self.debt_amount, self.monthly_installment, self.months_count]
        if sum(1 for item in check_list if item is not None) < 2:
            return False

        return True

    def process(self):
        """Запуск соответствующего алгоритма расчета."""
        if not self.is_input_valid():
            print("Ошибка: параметры указаны неверно.")
            return

        if self.calc_type == "annuity":
            if self.monthly_installment is None:
                self.calculate_annuity_payment()
            elif self.debt_amount is None:
                self.calculate_principal_value()
            elif self.months_count is None:
                self.calculate_period_length()
        elif self.calc_type == "diff":
            self.calculate_diff_payments()
        else:
            print("Ошибка: тип расчета не определен.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Финансовый калькулятор")

    parser.add_argument("--type", choices=["annuity", "diff"], help="Тип платежа")
    parser.add_argument("--principal", type=float, help="Тело кредита")
    parser.add_argument("--payment", type=float, help="Ежемесячный взнос")
    parser.add_argument("--periods", type=int, help="Срок в месяцах")
    parser.add_argument("--interest", type=float, help="Процентная ставка (годовая)")

    user_input = parser.parse_args()
    calculator = LoanCalculator(user_input)
    calculator.process()