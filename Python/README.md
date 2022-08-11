# Learning Python

# 1. 자료형
* https://docs.python.org/ko/3/tutorial/introduction.html

```python
import os
import sys
from copy import copy
```

## 1.1 불(bool)
참, 거짓을 표현하는 불(bool)

```python
is_valid = False
type(is_valid)
```

## 1.2 숫자
정수, 실수, 8진수, 16진수

### 1.2.1 int & float
int: 정수   
float: 부동소수점 15자리까지 정확도

```python
2 + 2

50 - 5*6

(50 - 5*6) / 4

17 / 3  # float을 반환하는 나눗셈

17 // 3  # 몫

17 % 3  # 나머지

5 * 3 + 2  # floored quotient * divisor + remainder

5 ** 2  # 5 squared
 
2 ** 7  # 2 to the power of 7 

octal = 0o177

type(octal)

hexadecimal = 0x8ff

a = 3   # int
b = 4   # int
print(a / b) # Ver2에서는 소수점까지 표현 안함
print(float(a) / b)

```

### 1.2.2 complex 복소수
파이썬은 Decimal 이나 Fraction 등의 다른 형의 숫자들도 지원합니다.    
파이썬은 복소수 에 대한 지원도 내장하고 있는데, 허수부를 가리키는데 j 나 J 접미사를 사용합니다 (예를 들어 3+5j).

### 1.2.3 Decimal & Franction
decimal: 10진 모듈, 사용자 정의 유효숫자 지정
fractions: 분수(분자와 분모) 넘버를 다루기 위한 모듈

```python
import decimal
float_value = 0.278

print(decimal.Decimal(float_value))
print(decimal.Decimal(str(float_value)))

import fractions

float_value = 2.5
print(fractions.Fraction(float_value))
print(fractions.Fraction('25'))
```

### 1.2.4 타입 변환과 활용
* https://blockdmask.tistory.com/432
  * 정수 변환 - int()
  * 실수 변환 - float()
  * 문자열 변환 - str()
  * 문자 변환 - chr()
  * 불리언 변환 - bool()

```python
str_value = '123.45'
type(str_value) # 자료형 확인

int_value = int(str_value) # ValueError

int_value = int(eval(str_value))
float_value = float(str_value)
str_value = str(float_value)
```

### 1.2.5 random
난수 발생

```python
import random

print(random.randrange(1, 10))
```

### 1.2.6 External classes to handle Python numbers
Python Mathmatics
* https://www.techbeamers.com/python-numbers/#python-mathematics

```python
import math

math.ceil(3.4)
math.floor(3.4)
math.cmp(3, 4) # Python Ver 2
math.exp(4)
math.log(4)
math.log10(4)
math.sqrt(4)
math.pi
math.e
```

Python funstions
* https://docs.python.org/3/library/functions.html

```python
values = [1, 2, 3]

sum(values)
min(values)
min(1, 2, 3)
max(values)
abs(-12.34)
pow(2, 4)
round(2.5)
round(3.5)
```

## 1.3 문자열
* https://docs.python.org/ko/3/tutorial/introduction.html#strings


작은따옴표('...') 나 큰따옴표("...")로 감싸는 형태, 따옴표를 이스케이핑 할 때는 \ 를 사용

```python
say = "Python is very easy."
print(say[2])
print(say[:6])

print("한글") # Ver2에서는 깨짐
print(u"한글")
```

### 1.3.1 텍스트 시퀀스 형(str)
* https://docs.python.org/ko/3/library/stdtypes.html#textseq

파이썬의 텍스트 데이터는 str, 또는 문자열 (strings), 객체를 사용하여 처리

문자열은 유니코드 코드 포인트의 불변 시퀀스 입니다. 문자열 리터럴은 다양한 방법으로 작성:
  - 작은따옴표: '"큰" 따옴표를 담을 수 있습니다'
  - Double quotes: "allows embedded 'single' quotes"
  - 삼중 따옴표: '''세 개의 작은따옴표''', """세 개의 큰따옴표"""

### 1.3.2 문자열 메서드
* https://docs.python.org/ko/3/library/stdtypes.html#string-methods

### 1.3.3 포맷 문자열 리터럴
* https://docs.python.org/ko/3/reference/lexical_analysis.html#f-strings

포맷 문자열 리터럴(formatted string literal) 또는 f-문자열 (f-string) 은 'f' 나 'F' 를 앞에 붙인 문자열 리터럴입니다. 

이 문자열은 치환 필드를 포함할 수 있는데, 중괄호 {} 로 구분되는 표현식입니다. 

다른 문자열 리터럴이 항상 상숫값을 갖지만, 포맷 문자열 리터럴은 실행시간에 계산되는 표현식입니다.

### 1.3.4 출력 포맷
* https://docs.python.org/ko/3/tutorial/inputoutput.html#fancier-output-formatting

### 1.3.5 포맷 문자열 문법
* https://docs.python.org/ko/3/library/string.html#formatstrings

str.format() 메서드와 Formatter 클래스는 포맷 문자열에 대해서 같은 문법을 공유합니다 (Formatter 의 경우, 서브 클래스는 그들 자신의 포맷 문자열 문법을 정의 할 수 있습니다). 

문법은 포맷 문자열 리터럴 과 관련 있지만, 덜 정교하며, 특히 임의의 표현식을 지원하지 않습니다.

## 1.4 리스트(list)
* https://docs.python.org/ko/3/tutorial/datastructures.html#more-on-lists

대괄호 사이에 쉼표로 구분된 값(항목)들의 목록으로 표현될 수 있습니다. 

리스트는 서로 다른 형의 항목들을 포함할 수 있지만, 항목들이 모두 같은 형인 경우가 많습니다.

리스트는 가변 입니다. 즉 내용을 변경할 수 있습니다.

※ 비어 있는 리스트는 a = list()로 생성

```python
squares = []  # = list()
squares = [1, 4, 9, 16, 25]

list = [1,3,5,7,9]
print(len(list))

if 3 in list:
    print('exist')
else:
    print('not exist')
    
```

* list 함수 사용하기

```python
#del 함수 사용해 리스트 요소 삭제하기
del squares[4]

#리스트에 요소 추가(append)
squares.append(25)

#리스트에 요소 삽입(insert)
squares.insert(5, 36)

#리스트 정렬(sort)
squares.sort()

#리스트 뒤집기(reverse)
squares.reverse()

#위치 반환(index)
squares.index(4)
squares.index(3) # Exception

#리스트 요소 제거(remove)
#remove(x)는 리스트에서 첫 번째로 나오는 x를 삭제
squares.remove(25)

#리스트 요소 끄집어내기(pop)
#pop()은 리스트의 맨 마지막 요소를 돌려주고 그 요소는 삭제
squares.pop()

#리스트에 포함된 요소 x의 개수 세기(count)
squares.count(4)

#리스트 확장(extend)
#extend(x)에서 x에는 리스트만 올 수 있으며 원래의 리스트에 x 리스트를 더하기

squares.extend([36, 49]) # squares += [36, 49]
```

## 1.5 튜플(tuple)
* https://wikidocs.net/15
* https://wikidocs.net/16042

튜플(tuple)은 몇 가지 점을 제외하곤 리스트와 거의 비슷하며 리스트와 다른 점은 다음과 같다.
  - 리스트는 [ ]으로 둘러싸지만 튜플은 ( )으로 둘러싼다.
  - 리스트는 그 값의 생성, 삭제, 수정이 가능하지만 튜플은 그 값을 바꿀 수 없다.
  - 튜블은 괄호를 생략해도 됨

```python
(a, b) = 'python', 'life'
a, b = ('python', 'life')
```

## 1.6 딕셔너리(dict)
* https://wikidocs.net/16

딕셔너리(dict)는 키(key)와 값(value)로 구성

딕셔너리는 리스트나 튜플처럼 순차적으로(sequential) 해당 요솟값을 구하지 않고 Key를 통해 Value를 얻는다

※ 비어 있는 딕셔너리는 a = dict()로 생성

```python
key_values = {} # = dict()
key_values = {'one': 1, 'two': 2, 'three': 3}
key_values['four'] = 4

```

## 1.7 집합(set)
* https://wikidocs.net/1015
* https://wikidocs.net/16044

집합(set)은 파이썬 2.3부터 지원하기 시작한 자료형으로, 집합에 관련된 것을 쉽게 처리하기 위해 만든 자료형

집합은 중복되는 요소가 없는 순서 없는 컬렉션입니다. 기본적인 용도는 멤버십 검사와 중복 엔트리 제거입니다. 

집합 객체는 합집합, 교집합, 차집합, 대칭 차집합과 같은 수학적인 연산들도 지원합니다.

집합을 만들 때는 중괄호나 set() 함수를 사용할 수 있습니다. 주의사항: 빈 집합을 만들려면 set() 을 사용해야 합니다. {} 가 아닙니다; 


```
fruits = set(['apple', 'banana', 'orange'])
fruits = {'apple', 'banana', 'orange'}

print(fruits)

'orange' in fruits
```

# 2. 제어 흐름 도구

## 2.1 if
* https://docs.python.org/ko/3/tutorial/controlflow.html#if-statements

if 조건문에서 "조건문"이란 참과 거짓을 판단하는 문장

비교연산자(<, >, ==, !=, >=, <=) 및 조합(and, or, not)

```python
score = 40

if score >= 60:
    message = "success"
else:
    message = "failure"
```

### 2.1.1 리스트, 튜플, 문자열 포함
```python
squares = [1, 4, 9, 16, 25]
4 in squares
```

### 2.1.2 조건부 표현식(conditional expression)

```python
message = "success" if score >= 60 else "failure"
```

## 2.2 for + range
* https://docs.python.org/ko/3/tutorial/controlflow.html#for-statements
* https://docs.python.org/ko/3/tutorial/controlflow.html#the-range-function

for 변수 in 리스트(또는 튜플, 문자열):
    수행할 문장1

```python
test_list = ['one', 'two', 'three'] 
for i in test_list: 
    print(i)

add = 0 
for i in range(1, 11): 
    add = add + i 

print(add)

for i in range(10):
    print(i)

for i in range(10, -1, -1):
    print(i)
```

Java for loop
```java
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}
```

## 2.3 while
while문은 조건문이 참인 동안에 while문 아래의 문장이 반복해서 수행

* https://docs.python.org/ko/3/reference/compound_stmts.html#while

```python
hit = 0
while hit < 10:
    hit = hit + 1
    print(f"{hit}")
```

```python
hit = 0
while True:
    hit = hit + 1
    if hit == 10:
        print("last 10")
        break
    elif hit == 1:
        print("first 1")
    else:
        print(hit)
```

## 2.4 루프의 break 와 continue 문, 그리고 else 절
* https://docs.python.org/ko/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops
* https://docs.python.org/ko/3/tutorial/datastructures.html#looping-techniques

## 2.5 pass
* https://docs.python.org/ko/3/tutorial/controlflow.html#pass-statements

## 2.6 match statements & enum
Python 3.10 버전부터 지원

* https://docs.python.org/ko/3/tutorial/controlflow.html#match-statements

```python
from enum import Enum

class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

color = Color(input("Enter your choice of 'red', 'blue' or 'green': "))

match color:
    case Color.RED:
        print("I see red!")
    case Color.GREEN:
        print("Grass is green")
    case Color.BLUE:
        print("I'm feeling the blues :(")
```


# 3. 함수(function)
* https://docs.python.org/ko/3/tutorial/controlflow.html#defining-functions

함수의 기본 구조
```python
def 함수명(파라미터):
    실행될 코드
    return 결과값
```


```python
def add(a, b): 
    return a + b

def add_many(*args):
    result = 0 
    for i in args: 
        result = result + i 
    return result 

result = add_many(1,2,3)

def add_and_mul(a,b): 
    return a+b, a*b

result = add_and_mul(3,4)

result1, result2 = add_and_mul(3, 4)
```

함수의 초기값 설정

```python
def say_myself(name, old, man=True):
    print(f'{name} : {old} : {man}') 
```

인수를 이용한 표현식(lambda): lambda = 인수1, 인수2, ...

```python
sum = lambda a, b: a+b

sum(3,4)
```


# 4. 모듈과 패키지
* https://docs.python.org/ko/3/tutorial/modules.html

from 모듈이름 import 모듈함수

```python
# PyQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# QGIS
from qgis.core import *
from qgis.gui import *

# 경로 등 내장 함수
from glob import glob
from os import path
```

# 5. 파일 입력과 출력
* https://docs.python.org/ko/3/tutorial/inputoutput.html#reading-and-writing-files

## 5.1 경로 다루기

```python
import os
import sys

filename = 'C:\OpenData\QGIS\장난감도서관.csv' # 텍스트파일

os.path.exists(filename)

target_folder = os.path.dirname(filename)

shp_name = os.path.splitext(os.path.basename(filename))[0]
shapefile_line = os.path.join(target_folder, f'{shp_name}_line.shp')


import glob
glob.glob(r'C:\OpenData\QGIS\*..shp')
```

## 5.2 파일 읽기
r, w, a  지정하지 않으면 r

```python
filename = 'C:\OpenData\QGIS\장난감도서관.csv'
file = open(filename, 'r', encoding='utf-8')
while True:
    line = file.readline()
    if not line:
        break
    print(line)

file.close()


with open(filename, 'r', encoding='utf-8') as file:
    while True:
        line = file.readline()
        if not line:
            break
        print(line)


with open(filename, 'r', encoding='utf-8') as file:
    # 파일의 모든 줄을 읽어서 각각의 줄을 요소로 갖는 리스트로
    lines    = file.readlines()
    print(lines)
    
    # 파일의 내용 전체를 문자열로
    contents = file.read() 
    print(contents)
```

## 5.2 파일 쓰기

```python
filename = 'C:\OpenData\QGIS\장난감도서관.txt'
with open(filename, 'w', encoding='utf-8') as file:
    file.write('텍스트파일 쓰기')
```


# 6. 오류와 예외
* https://docs.python.org/ko/3/tutorial/errors.html

# 7. 클래스
* https://docs.python.org/ko/3/tutorial/classes.html

*  __init__ : 클래스 초기화
*  self : 클래스 자신, self를 사용해야 인스턴스에서 함수를 사용할 수 있음
*  @staticmethod : static 함수를 선언할때 사용되는 키워드

```python
class Person:
    def __init__(self, name):
        self.name = name
        
    def greet(self):
        print('Hello ' + self.name)
    
    @staticmethod
    def static_greet(name):
        print('Hello ' + name)

# Person 인스턴스 생성
person = Person('QGIS')
person.greet()

# Person Class의 staticmethod 호출
Person.static_greet('Quantum GIS')

del person # delete class
```

# 8. 표준 라이브러리
https://docs.python.org/ko/3/tutorial/stdlib.html
https://docs.python.org/ko/3/tutorial/stdlib2.html


# 참고사이트
  - Python
    - https://docs.python.org/ko/3/tutorial/index.html
    - https://docs.python.org/ko/3/
    - https://wikidocs.net/book/1553
    - https://wikidocs.net/book/1
    - https://wikidocs.net/book/2
