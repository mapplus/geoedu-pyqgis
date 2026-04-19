# 06. 파일 입출력

## 학습 목표

- 텍스트 파일을 읽고 쓸 수 있다.
- 경로를 다루는 기본 방법을 익힌다.
- 나중에 로그 저장, 결과 저장, 설정 파일 읽기로 확장할 수 있다.

## 경로 다루기

```python
from pathlib import Path

base_dir = Path.home()
output_file = base_dir / "qgis_python_practice.txt"

print(output_file)
print(output_file.name)
print(output_file.suffix)
```

## 파일 쓰기

```python
from pathlib import Path

output_file = Path.home() / "qgis_python_practice.txt"

with output_file.open("w", encoding="utf-8") as file:
    file.write("QGIS Python Console practice\n")
    file.write("Layer export ready\n")
```

## 파일 읽기

```python
from pathlib import Path

output_file = Path.home() / "qgis_python_practice.txt"

with output_file.open("r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

## CSV 저장 맛보기

```python
import csv
from pathlib import Path

csv_file = Path.home() / "layer_summary.csv"
rows = [
    ["layer_name", "feature_count"],
    ["roads", 120],
    ["buildings", 48],
]

with csv_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(rows)
```

## 꼭 짚고 갈 것

- 파일은 `with open(...)` 또는 `Path.open()`으로 다루는 습관이 좋습니다.
- 한글이 포함되면 `encoding="utf-8"`을 명시합니다.
- 읽기, 쓰기, 추가 모드를 구분합니다.

## 같이 해보기

1. 바탕화면이나 홈 경로 기준으로 텍스트 파일 경로를 만들어 봅니다.
2. 한 줄짜리 파일을 저장하고 다시 읽어 봅니다.
3. 레이어 이름과 피처 수를 CSV로 저장해 봅니다.

## PyQGIS 연결

- 처리 결과 로그 저장
- 레이어 요약 결과 CSV 저장
- 플러그인 설정 파일 읽기/쓰기

