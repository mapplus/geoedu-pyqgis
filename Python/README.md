# Python Practice Guide for QGIS

이 폴더는 `QGIS Python Console`에서 진행하는 Python 기초 실습 자료입니다.  
최종 목표는 Python 문법을 익힌 뒤 PyQGIS 기초로 자연스럽게 넘어가고, 이후에는 스크립팅과 플러그인 개발 과정까지 확장하는 것입니다.

## 교육 범위

- 1단계: Python 기초
- 2단계: PyQGIS 기초
- 이후 확장: QGIS 스크립팅, Processing 자동화, 플러그인 개발

## 실습 환경

- QGIS 내장 Python 3.12
- QGIS Python Console 사용
- 일부 예제는 `.py` 스크립트 파일로 저장해서 다시 실행하는 방식까지 함께 연습

## 교육 목표

- Python의 기본 문법을 QGIS Python Console에서 직접 실행하며 익힌다.
- 변수, 조건문, 반복문, 함수, 자료구조를 사용해 작은 문제를 해결한다.
- 파일 처리와 예외 처리까지 포함한 기본 스크립팅 습관을 익힌다.
- 이후 PyQGIS에서 레이어, 피처, 속성, 지오메트리를 다룰 준비를 마친다.

## 실습 진행 방식

- 학생들과 함께 한 줄씩 실행하면서 결과를 확인합니다.
- 예제는 먼저 따라 치고, 바로 짧은 변형 과제를 풀어봅니다.
- QGIS Python Console에서 바로 실행 가능한 예제를 우선 사용합니다.
- `input()` 기반 예제보다 변수 대입과 식 평가 중심으로 진행합니다.

## 먼저 같이 시작해 보기

이미지 순서는 `자료형`부터 시작하지만, 본격적인 문법으로 들어가기 전에 아래 내용은 먼저 같이 실행해 보겠습니다.

- 변수에 값을 넣고 출력해 보기
- 식을 실행했을 때 어떤 결과가 나오는지 확인해 보기
- 들여쓰기가 Python 문법에서 왜 중요한지 감 잡기

시작 예제:

```python
message = "Hello, QGIS Python Console"
name = "GeoEdu"

print(message)
print(f"{name} 실습을 시작합니다.")
```

## 실습 목차

| 순서 | 주제 | 파일 | 실습 초점 |
| --- | --- | --- | --- |
| 0 | 시작하기 | [00_start_here.md](./00_start_here.md) | 콘솔 사용법, 실행 방식, 첫 코드 |
| 1 | 자료형 | [01_data_types.md](./01_data_types.md) | 숫자, 문자열, bool, 형변환 |
| 2 | 제어 흐름 도구 | [02_control_flow.md](./02_control_flow.md) | if, for, while, break |
| 3 | 함수 | [03_functions.md](./03_functions.md) | def, return, 기본값, 재사용 |
| 4 | 자료구조 | [04_data_structures.md](./04_data_structures.md) | list, tuple, dict, set |
| 5 | 모듈과 패키지 | [05_modules_packages.md](./05_modules_packages.md) | import, 표준 모듈, `qgis.core` 연결 |
| 6 | 파일 입출력 | [06_file_io.md](./06_file_io.md) | 텍스트 저장, 경로, CSV |
| 7 | 오류와 예외 | [07_errors_exceptions.md](./07_errors_exceptions.md) | try, except, 디버깅 습관 |
| 8 | 클래스 | [08_classes.md](./08_classes.md) | 객체 개념, 속성, 메서드 |
| 9 | 표준 라이브러리 | [09_standard_library.md](./09_standard_library.md) | `math`, `datetime`, `pathlib`, `json` |
| 10 | 미니 프로젝트 | [10_mini_project.md](./10_mini_project.md) | Python 기초를 묶어 작은 실습 완성 |

## Python 기초에서 PyQGIS로 이어지는 흐름

Python 기초를 익힌 뒤에는 아래 주제를 PyQGIS 기초 과정으로 연결할 수 있습니다.

- 변수와 자료형 -> 좌표, 속성값, 파일 경로 다루기
- 제어문과 반복문 -> 레이어와 피처 순회하기
- 함수 -> 자주 쓰는 작업을 재사용 가능한 도구로 만들기
- 딕셔너리와 리스트 -> 속성 매핑, 설정값 관리
- 파일 입출력 -> 로그 저장, 결과물 내보내기
- 예외 처리 -> 레이어 누락, 경로 오류, 필드 없음 대응

## 실습 규칙

- 예제를 복사만 하지 말고 직접 입력합니다.
- 실행 전 결과를 먼저 예상해 봅니다.
- 에러가 나면 바로 지우지 말고 메시지를 읽습니다.
- 한 번에 길게 쓰지 않고 작은 단위로 실행합니다.
- 콘솔에서 실행한 코드는 필요한 경우 `.py` 파일로 옮겨 정리합니다.
