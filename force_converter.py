import tkinter as tk
from tkinter import ttk

GRAVITY = 9.80665

UNIT_FACTORS = {
    "N": 1.0,
    "kN": 1000.0,
    "MN": 1000000.0,
    "kgf": 9.80665,
    "lbf": 4.44822161526,
}


def convert_force_value(value, from_unit, to_unit):
    """주어진 값과 단위를 기준으로 다른 힘 단위로 변환합니다."""
    base_n = value * UNIT_FACTORS[from_unit]
    return base_n / UNIT_FACTORS[to_unit]


def convert_force():
    print("=== 힘 단위 변환기 ===")
    print("* 종료하려면 'q' 또는 '종료'를 입력하세요.\n")

    while True:
        user_input = input("변환할 힘 값을 입력하세요: ").strip()

        if user_input.lower() in ['q', 'quit', 'exit', '종료']:
            print("프로그램을 종료합니다.")
            break

        try:
            value = float(user_input)
            print("입력 단위: N, kN, MN, kgf, lbf")
            from_unit = input("입력 단위를 선택하세요: ").strip()
            to_unit = input("출력 단위를 선택하세요: ").strip()

            if from_unit not in UNIT_FACTORS or to_unit not in UNIT_FACTORS:
                print("오류: 지원하지 않는 단위입니다.")
                continue

            result = convert_force_value(value, from_unit, to_unit)
            print(f"  ▶ [결과] {value} {from_unit} = {result:,.2f} {to_unit}")
            print("-" * 40)
        except ValueError:
            print("  ❌ [오류] 올바른 숫자(정수 또는 실수)를 입력해주세요.")
            print("-" * 40)


class ForceConverterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("힘 단위 변환기")
        self.geometry("500x500")
        self.resizable(False, False)

        self.history = []

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.heading = ttk.Label(
            self,
            text="힘 단위 변환기",
            font=("맑은 고딕", 18, "bold")
        )
        self.heading.pack(pady=(18, 8))

        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(entry_frame, text="값:", font=("맑은 고딕", 11)).pack(side="left")

        self.entry = ttk.Entry(entry_frame, width=18, font=("맑은 고딕", 12))
        self.entry.pack(side="left", padx=(8, 10))
        self.entry.focus()
        self.entry.bind("<Return>", self.calculate)

        self.calc_button = ttk.Button(entry_frame, text="계산", command=self.calculate)
        self.calc_button.pack(side="left")

        self.clear_button = ttk.Button(entry_frame, text="초기화", command=self.clear)
        self.clear_button.pack(side="left", padx=(8, 0))

        unit_frame = ttk.Frame(main_frame)
        unit_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(unit_frame, text="입력 단위:", font=("맑은 고딕", 11)).pack(side="left")
        self.from_unit = ttk.Combobox(unit_frame, values=list(UNIT_FACTORS.keys()), state="readonly", width=8)
        self.from_unit.pack(side="left", padx=(8, 15))
        self.from_unit.set("kN")

        self.swap_button = ttk.Button(unit_frame, text="바꾸기", command=self.swap_units)
        self.swap_button.pack(side="left", padx=(0, 15))

        ttk.Label(unit_frame, text="출력 단위:", font=("맑은 고딕", 11)).pack(side="left")
        self.to_unit = ttk.Combobox(unit_frame, values=list(UNIT_FACTORS.keys()), state="readonly", width=8)
        self.to_unit.pack(side="left", padx=(8, 0))
        self.to_unit.set("N")

        result_frame = ttk.LabelFrame(main_frame, text="결과", padding=(12, 10))
        result_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.result_text = tk.Text(result_frame, height=7, width=40, state="disabled", font=("맑은 고딕", 11))
        self.result_text.pack(fill="both", expand=True)

        history_frame = ttk.LabelFrame(main_frame, text="이전 계산 기록", padding=(12, 10))
        history_frame.pack(fill="both", expand=True)

        self.history_text = tk.Text(history_frame, height=8, width=40, state="disabled", font=("맑은 고딕", 10))
        self.history_text.pack(fill="both", expand=True)

        self.clear()

    def swap_units(self):
        from_unit = self.from_unit.get()
        to_unit = self.to_unit.get()
        self.from_unit.set(to_unit)
        self.to_unit.set(from_unit)

    def calculate(self, event=None):
        user_input = self.entry.get().strip()

        if user_input.lower() in ['q', 'quit', 'exit', '종료']:
            self.show_result("프로그램을 종료합니다.")
            return

        try:
            value = float(user_input)
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()

            if from_unit not in UNIT_FACTORS or to_unit not in UNIT_FACTORS:
                self.show_result("오류: 지원하지 않는 단위입니다.")
                return

            result = convert_force_value(value, from_unit, to_unit)
            record = f"{value} {from_unit} = {result:,.2f} {to_unit}"
            self.history.append(record)

            message = (
                f"입력값: {value} {from_unit}\n"
                f"출력 단위: {to_unit}\n"
                f"▶ {value} {from_unit} = {result:,.2f} {to_unit}"
            )
            self.show_result(message)
            self.show_history()
            self.entry.select_range(0, tk.END)
            self.entry.focus()

        except ValueError:
            self.show_result("오류: 올바른 숫자(정수 또는 실수)를 입력해주세요.")
            self.entry.select_range(0, tk.END)
            self.entry.focus()

    def show_result(self, text):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.configure(state="disabled")

    def show_history(self):
        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", tk.END)

        if not self.history:
            self.history_text.insert(tk.END, "아직 계산 기록이 없습니다.")
        else:
            for index, record in enumerate(self.history, start=1):
                self.history_text.insert(tk.END, f"{index}. {record}\n")

        self.history_text.configure(state="disabled")

    def clear(self):
        self.entry.delete(0, tk.END)
        self.history = []
        self.show_history()
        self.show_result("값을 입력하고 단위를 선택한 뒤 계산 버튼을 누르세요.\n같은 창에서 여러 번 다시 계산할 수 있습니다.")


if __name__ == "__main__":
    app = ForceConverterGUI()
    app.mainloop()