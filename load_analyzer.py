from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


DATA_FILE = Path(__file__).with_name("load_bad.csv")
RESULT_FILE = Path(__file__).with_name("load_result.csv")
PLOT_FILE = Path(__file__).with_name("stress_plot.png")
area_mm2 = 100
REFERENCE_STRESS_MPA = 6
REQUIRED_COLUMNS = {"time_s", "force_N"}


def main() -> None:
    source_data = pd.read_csv(DATA_FILE, dtype=str, keep_default_na=False)
    missing_columns = REQUIRED_COLUMNS.difference(source_data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"CSV에 필요한 열이 없습니다: {missing}")

    numeric_values = {}
    valid_rows = pd.Series(True, index=source_data.index)
    for column in ("time_s", "force_N"):
        values = source_data[column].str.strip()
        blank_values = values.eq("")
        numeric = pd.to_numeric(values, errors="coerce")
        invalid_values = blank_values | numeric.isna()
        valid_rows &= ~invalid_values
        numeric_values[column] = numeric

        for index in source_data.index[invalid_values]:
            source_row = index + 2
            problem_value = source_data.at[index, column]
            if blank_values.at[index]:
                print(
                    f"CSV 행 {source_row}: {column} 값이 비어 있습니다 "
                    "(문제 값: 빈칸)"
                )
            else:
                print(
                    f"CSV 행 {source_row}: {column} 값이 숫자가 아닙니다 "
                    f"(문제 값: {problem_value!r})"
                )

    excluded_count = int((~valid_rows).sum())
    data = source_data.loc[valid_rows, ["time_s", "force_N"]].copy()
    for column, numeric in numeric_values.items():
        data[column] = numeric.loc[valid_rows]
    print(f"제외한 행수: {excluded_count}개")
    print(f"유효한 데이터 수: {len(data)}개")

    if data.empty:
        print("유효한 데이터가 없어 계산과 그래프 생성을 중단합니다.")
        return

    data["stress_MPa"] = data["force_N"] / area_mm2
    data.to_csv(RESULT_FILE, index=False)

    maximum_index = data["stress_MPa"].idxmax()
    maximum_stress = data.loc[maximum_index, "stress_MPa"]
    maximum_time = data.loc[maximum_index, "time_s"]
    above_reference_count = int(
        (data["stress_MPa"] > REFERENCE_STRESS_MPA).sum()
    )

    figure, axis = plt.subplots()
    axis.plot(data["time_s"], data["stress_MPa"], marker="o")
    axis.scatter(
        maximum_time,
        maximum_stress,
        color="red",
        zorder=3,
    )
    axis.annotate(
        f"{maximum_stress:g} MPa",
        (maximum_time, maximum_stress),
        xytext=(8, 8),
        textcoords="offset points",
    )
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Stress (MPa)")
    figure.tight_layout()
    figure.savefig(PLOT_FILE)
    plt.close(figure)

    maximum_index = data["force_N"].idxmax()

    print(f"최대 하중: {data.loc[maximum_index, 'force_N']} N")
    print(f"해당 시간: {data.loc[maximum_index, 'time_s']} s")
    print(f"최대 응력: {maximum_stress} MPa")
    print(f"해당 시간: {maximum_time} s")
    print(
        f"기준 응력 {REFERENCE_STRESS_MPA} MPa 초과 데이터 개수: "
        f"{above_reference_count}개"
    )
    print(f"결과 파일: {RESULT_FILE}")
    print(f"그래프 파일: {PLOT_FILE}")


if __name__ == "__main__":
    main()
