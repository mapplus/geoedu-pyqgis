# geoedu-pyqgis
Learning Python &amp; PyQGIS 


#. Python

#!/usr/bin/env python3 #  유닉스 《셔뱅 (shebang)》 줄 
# -*- coding: utf-8 -*-

"""
***************************************************************************
    공간정보아카데미 PyQGIS 실습
    ---------------------
    Date                 : March 2022
    Copyright            : (C) 2022 by MapPlus
    Email                : mapplus at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
#. 이 문서는 PyQGIS Cookbook과 ㅇㅇㅇㅇ 를 참고하여 작성했습니다.
#. QGIS를 시작하고 [플러그인] - [파이썬 콘솔] 실행
#. 샘플 데이터셋 폴더: C:\OpenData\QGIS

#. 선행학습
  - Python
    - https://docs.python.org/ko/3/
    - https://wikidocs.net/book/1
    - https://wikidocs.net/book/2
    
  - PyQGIS
    - https://qgis.org/pyqgis/3.0/
    - https://qgis.org/api/modules.html
    
  - PyQT
    - https://doc.qt.io/qtforpython-5/api.html
    - https://wikidocs.net/book/2944
    
  - GDAL/OGR
    - https://gdal.org/api/python.html
    - 고급 사용자 추천
"""


###### 교육 참고자료 사이트 ######
https://docs.python.org/ko/3/tutorial/controlflow.html#if-statements
https://wikidocs.net/20
https://wikidocs.net/57


파이썬(Python)은 1990년 암스테르담의 귀도 반 로섬(Guido Van Rossum)이 개발한 인터프리터 언어

# 파이썬 개요에 사용
  - https://myksb1223.github.io/develops/





"""
***************************************************************************
    Chapter X: 파이썬 둘러보기
        reference: XXXXXXXXXXXXXXXXXXXXXXXXXXX
***************************************************************************
"""

C:\Users\mappl>python
Python 3.9.9 (tags/v3.9.9:ccb0e6a, Nov 15 2021, 18:08:50) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> help('keywords')

Here is a list of the Python keywords.  Enter any keyword to get more help.

False               break               for                 not
None                class               from                or
True                continue            global              pass
__peg_parser__      def                 if                  raise
and                 del                 import              return
as                  elif                in                  try
assert              else                is                  while
async               except              lambda              with
await               finally             nonlocal            yield

>>> import keyword
>>> keyword.kwlist

"""
***************************************************************************
    Chapter X: 코딩 스타일
        reference: XXXXXXXXXXXXXXXXXXXXXXXXXXX
***************************************************************************
"""
파이썬 스타일 가이드라인(PEP 8) -- Style Guide: https://www.python.org/dev/peps/pep-0008/


- 들려 쓰기에 4-스페이스를 사용하고, 탭을 사용하지 마세요.
- 4개의 스페이스는 작은 들여쓰기 (더 많은 중첩 도를 허락합니다) 와 큰 들여쓰기 (읽기 쉽습니다) 사이의 좋은 절충입니다. 탭은 혼란을 일으키고, 없애는 것이 최선입니다.
- 79자를 넘지 않도록 줄 넘김 하세요. 라인 연결 문자(\, 백슬래쉬)를 사용하여 다중 라인으로 확장
- 이것은 작은 화면을 가진 사용자를 돕고 큰 화면에서는 여러 코드 파일들을 나란히 볼 수 있게 합니다.
- 함수, 클래스, 함수 내의 큰 코드 블록 사이에 빈 줄을 넣어 분리하세요.
- 가능하다면, 주석은 별도의 줄로 넣으세요.
- 독스트링을 사용하세요.  """ CONTENTS """
- 연산자들 주변과 콤마 뒤에 스페이스를 넣고, 괄호 바로 안쪽에는 스페이스를 넣지 마세요: a = f(1, 2) + g(3, 4).
- 클래스와 함수들에 일관성 있는 이름을 붙이세요; 관례는 클래스의 경우 UpperCamelCase, 함수와 메서드의 경우 lowercase_with_underscores입니다. 첫 번째 메서드 인자의 이름으로는 항상 self를 사용하세요 (클래스와 메서드에 대한 자세한 내용은 클래스와의 첫 만남 을 보세요).
- 여러분의 코드를 국제적인 환경에서 사용하려고 한다면 특별한 인코딩을 사용하지 마세요. 어떤 경우에도 파이썬의 기본, UTF-8, 또는 단순 ASCII조차, 이 최선입니다.
- 마찬가지로, 다른 언어를 사용하는 사람이 코드를 읽거나 유지할 약간의 가능성만 있더라도, 식별자에 ASCII 이외의 문자를 사용하지 마세요.


"""
***************************************************************************
    Chapter X: 자료형
        reference: XXXXXXXXXXXXXXXXXXXXXXXXXXX
***************************************************************************
"""
import os
import sys
from copy import copy

# ------------------------------------------
# 불(bool)
# ------------------------------------------
참, 거짓을 표현하는 불(bool)

is_valid = False
type(is_valid)


# ------------------------------------------
# 숫자
# ------------------------------------------

정수, 실수, 8진수, 16진수

# int & float
# ------------------------
int: 정수
float: 부동소수점 15자리까지 정확도

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

# complex 복소수
# ------------------------
파이썬은 Decimal 이나 Fraction 등의 다른 형의 숫자들도 지원합니다. 
파이썬은 복소수 에 대한 지원도 내장하고 있는데, 허수부를 가리키는데 j 나 J 접미사를 사용합니다 (예를 들어 3+5j).

# Decimal & Franction
# ------------------------
import decimal
10진 모듈, 사용자 정의 유효숫자 지정
float_value = 0.278

print(decimal.Decimal(float_value))
print(decimal.Decimal(str(float_value)))

import fractions
분수(분자와 분모) 넘버를 다루기 위한 모듈

float_value = 2.5
print(fractions.Fraction(float_value))
print(fractions.Fraction('25'))


# 타입 변환과 활용
#  - https://blockdmask.tistory.com/432
# ------------------------
1. 파이썬 정수 변환 - int()
2. 파이썬 실수 변환 - float()
3. 파이썬 문자열 변환 - str()
4. 파이썬 문자 변환 - chr()
5. 파이썬 불리언 변환 - bool()

str_value = '123.45'
int_value = int(str_value) # ValueError

int_value = int(eval(str_value))
float_value = float(str_value)
str_value = str(float_value)

# random
# ------------------------
import random

print(random.randrange(1, 10)

# External classes to handle Python numbers
https://www.techbeamers.com/python-numbers/#python-mathematics
import math

math.ceil(3.4)
math.floor(3.4)
math.cmp(3, 4)
math.exp(4)
math.log(4)
math.log10(4)
math.sqrt(4)
math.pi
math.e

https://docs.python.org/3/library/functions.html

sum eval
min, max, abs , pow, round

# ------------------------------------------
# 문자열
# ------------------------------------------
작은따옴표('...') 나 큰따옴표("...")로 둘러쌀 수 있는데 모두 같은 결과를 줍니다 
따옴표를 이스케이핑 할 때는 \ 를 사용

출력 포맷
https://docs.python.org/ko/3/tutorial/inputoutput.html#fancier-output-formatting

# 텍스트 시퀀스 형 — str
파이썬의 텍스트 데이터는 str, 또는 문자열 (strings), 객체를 사용하여 처리됩니다. 
문자열은 유니코드 코드 포인트의 불변 시퀀스 입니다. 문자열 리터럴은 다양한 방법으로 작성됩니다:
  - 작은따옴표: '"큰" 따옴표를 담을 수 있습니다'
  - Double quotes: "allows embedded 'single' quotes"
  - 삼중 따옴표: '''세 개의 작은따옴표''', """세 개의 큰따옴표"""

# 문자열 메서드
https://docs.python.org/ko/3/library/stdtypes.html#string-methods

# 포맷 문자열 리터럴
포맷 문자열 리터럴(formatted string literal) 또는 f-문자열 (f-string) 은 'f' 나 'F' 를 앞에 붙인 문자열 리터럴입니다. 이 문자열은 치환 필드를 포함할 수 있는데, 중괄호 {} 로 구분되는 표현식입니다. 다른 문자열 리터럴이 항상 상숫값을 갖지만, 포맷 문자열 리터럴은 실행시간에 계산되는 표현식입니다.
https://docs.python.org/ko/3/reference/lexical_analysis.html#f-strings


# 포맷 문자열 문법
str.format() 메서드와 Formatter 클래스는 포맷 문자열에 대해서 같은 문법을 공유합니다 (Formatter 의 경우, 서브 클래스는 그들 자신의 포맷 문자열 문법을 정의 할 수 있습니다). 문법은 포맷 문자열 리터럴 과 관련 있지만, 덜 정교하며, 특히 임의의 표현식을 지원하지 않습니다.
https://docs.python.org/ko/3/library/string.html#formatstrings


# ------------------------------------------
# 리스트
# ------------------------------------------
대괄호 사이에 쉼표로 구분된 값(항목)들의 목록으로 표현될 수 있습니다. 
리스트는 서로 다른 형의 항목들을 포함할 수 있지만, 항목들이 모두 같은 형인 경우가 많습니다.

리스트는 가변 입니다. 즉 내용을 변경할 수 있습니다:

※ 비어 있는 리스트는 a = list()로 생성
squares = []  # = list()
squares = [1, 4, 9, 16, 25]

# ------------------------------------------
# 튜플과 시퀀스
# ------------------------------------------
(a, b) = 'python', 'life'
a, b = ('python', 'life')
** 튜블은 괄호를 생략해도 됨

# ------------------------------------------
# 딕셔너리
# ------------------------------------------
딕셔너리(dict)는 키(key)와 값(value)의 짝으로 이뤄집니다. 이런 것을 매핑

※ 비어 있는 딕셔너리는 a = dict()로 생성
key_values = {} # = dict()
key_values = {'one': 1, 'two': 2, 'three': 3}

# ------------------------------------------
# 집합
# ------------------------------------------
집합을 표현하는 세트(set)도 있습니다.
파이썬은 집합 을 위한 자료 형도 포함합니다. 집합은 중복되는 요소가 없는 순서 없는 컬렉션입니다. 기본적인 용도는 멤버십 검사와 중복 엔트리 제거입니다. 집합 객체는 합집합, 교집합, 차집합, 대칭 차집합과 같은 수학적인 연산들도 지원합니다.
집합을 만들 때는 중괄호나 set() 함수를 사용할 수 있습니다. 주의사항: 빈 집합을 만들려면 set() 을 사용해야 합니다. {} 가 아닙니다; 후자는 빈 딕셔너리를 만드는데, 다음 섹션에서 다룹니다.

fruits = {'apple', 'banana', 'orange'}


"""
***************************************************************************
    Chapter X: 제어 흐름 도구
***************************************************************************
"""

# ------------------------------------------
# if
# ------------------------------------------
https://docs.python.org/ko/3/tutorial/controlflow.html#if-statements

if 조건문에서 "조건문"이란 참과 거짓을 판단하는 문장
비교연산자(<, >, ==, !=, >=, <=) 및 조합(and, or, not)

# 리스트, 튜플, 문자열 포함
x in s, x not in s

squares = [1, 4, 9, 16, 25]
4 in squares


if score >= 60:
    message = "success"
else:
    message = "failure"

# 조건부 표현식(conditional expression)
message = "success" if score >= 60 else "failure"



# ------------------------------------------
# for + range
# ------------------------------------------
https://docs.python.org/ko/3/tutorial/controlflow.html#for-statements
https://docs.python.org/ko/3/tutorial/controlflow.html#the-range-function


# ------------------------------------------
# while
# ------------------------------------------


# ------------------------------------------
# 루프의 break 와 continue 문, 그리고 else 절
# ------------------------------------------
https://docs.python.org/ko/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops


# ------------------------------------------
# pass
# ------------------------------------------
https://docs.python.org/ko/3/tutorial/controlflow.html#pass-statements



# ------------------------------------------
# match statements & enum
# ------------------------------------------
https://docs.python.org/ko/3/tutorial/controlflow.html#match-statements
match statement = switch statement in C, Java or JavaScript 
Python 3.10 버전부터 지원

# enum
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


"""
***************************************************************************
    Chapter X: 함수
***************************************************************************
"""
https://docs.python.org/ko/3/tutorial/controlflow.html#defining-functions



"""
***************************************************************************
    Chapter X: 자료 구조
        reference: XXXXXXXXXXXXXXXXXXXXXXXXXXX
***************************************************************************
"""

# ------------------------------------------
# 리스트
# ------------------------------------------
대괄호 사이에 쉼표로 구분된 값(항목)들의 목록으로 표현될 수 있습니다. 
리스트는 서로 다른 형의 항목들을 포함할 수 있지만, 항목들이 모두 같은 형인 경우가 많습니다.

리스트는 가변 입니다. 즉 내용을 변경할 수 있습니다:

※ 비어 있는 리스트는 a = list()로 생성
squares = []  # = list()

squares = [1, 4, 9, 16, 25]

# del 함수 사용해 리스트 요소 삭제하기
del squares[4]

# 리스트에 요소 추가(append)
squares.append(25)

# 리스트에 요소 삽입(insert)
squares.insert(5, 36)

# 리스트 정렬(sort)
squares.sort()

# 리스트 뒤집기(reverse)
squares.reverse()

# 위치 반환(index)
squares.index(3)

# 리스트 요소 제거(remove)
# remove(x)는 리스트에서 첫 번째로 나오는 x를 삭제
squares.remove(25)

# 리스트 요소 끄집어내기(pop)
# pop()은 리스트의 맨 마지막 요소를 돌려주고 그 요소는 삭제
squares.pop()

# 리스트에 포함된 요소 x의 개수 세기(count)
squares.count(4)

# 리스트 확장(extend)
# extend(x)에서 x에는 리스트만 올 수 있으며 원래의 a 리스트에 x 리스트를 더하
squares.extend([36, 49]) # squares += [36, 49]와 동일

# ------------------------------------------
# 리스트
# ------------------------------------------
대괄호 사이에 쉼표로 구분된 값(항목)들의 목록으로 표현될 수 있습니다. 
리스트는 서로 다른 형의 항목들을 포함할 수 있지만, 항목들이 모두 같은 형인 경우가 많습니다.

리스트는 가변 입니다. 즉 내용을 변경할 수 있습니다:

※ 비어 있는 리스트는 a = list()로 생성
squares = []  # = list()
squares = [1, 4, 9, 16, 25]

# ------------------------------------------
# 튜플과 시퀀스
# ------------------------------------------
(a, b) = 'python', 'life'
a, b = ('python', 'life')
** 튜블은 괄호를 생략해도 됨

# ------------------------------------------
# 딕셔너리
# ------------------------------------------
딕셔너리(dict)는 키(key)와 값(value)의 짝으로 이뤄집니다. 이런 것을 매핑

※ 비어 있는 딕셔너리는 a = dict()로 생성
key_values = {} # = dict()
key_values = {'one': 1, 'two': 2, 'three': 3}

# ------------------------------------------
# 집합
# ------------------------------------------
집합을 표현하는 세트(set)도 있습니다.
파이썬은 집합 을 위한 자료 형도 포함합니다. 집합은 중복되는 요소가 없는 순서 없는 컬렉션입니다. 기본적인 용도는 멤버십 검사와 중복 엔트리 제거입니다. 집합 객체는 합집합, 교집합, 차집합, 대칭 차집합과 같은 수학적인 연산들도 지원합니다.
집합을 만들 때는 중괄호나 set() 함수를 사용할 수 있습니다. 주의사항: 빈 집합을 만들려면 set() 을 사용해야 합니다. {} 가 아닙니다; 후자는 빈 딕셔너리를 만드는데, 다음 섹션에서 다룹니다.


fruits = {'apple', 'banana', 'orange'}

# ------------------------------------------
# 루프 테크닉
# ------------------------------------------
https://docs.python.org/ko/3/tutorial/datastructures.html#looping-techniques




"""
***************************************************************************
    Chapter X: 모듈과 패키지
***************************************************************************
"""
https://docs.python.org/ko/3/tutorial/modules.html




"""
***************************************************************************
    Chapter X: 파일 입력과 출력
***************************************************************************
"""
import os
import sys

# ------------------------------------------
# 경로 다루기
# ------------------------------------------
filename = 'C:\OpenData\QGIS\장난감도서관.csv'

os.path.exists(filename)

target_folder = os.path.dirname(filename)

shp_name = os.path.splitext(os.path.basename(filename))[0]
shapefile_line = os.path.join(target_folder, f'{shp_name}_line.shp')


import glob
glob.glob(r'C:\OpenData\QGIS\*..shp')  

# ------------------------------------------
# 파일 읽기
# ------------------------------------------

# r, w, a  지정하지 않으면 r
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


# ------------------------------------------
# 파일 쓰기
# ------------------------------------------
filename = 'C:\OpenData\QGIS\장난감도서관.txt'
with open(filename, 'w', encoding='utf-8') as file:
    file.write('텍스트파일 쓰기')


"""
***************************************************************************
    Chapter X: 오류와 예외
***************************************************************************
"""



"""
***************************************************************************
    Chapter X: 클래스
***************************************************************************
"""



"""
***************************************************************************
    Chapter X: 표준 라이브러리
***************************************************************************
"""
https://docs.python.org/ko/3/tutorial/stdlib.html
https://docs.python.org/ko/3/tutorial/stdlib2.html

#===================================
# 모듈 참조
#===================================
from 모듈이름 import 모듈함수

# PyQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# QGIS
from qgis.core import *
from qgis.gui import *

# 경로 등 내장 함수
from glob import glob
from os import path

#===================================
# 자료형
#===================================
# string 
say = "Python is very easy."
print(say[2])
print(say[:6])

print("한글") #Ver2에서는 깨짐
print(u"한글")

# number
a = 3   # int
b = 4   # int
print(a / b) #Ver2에서는 소수점까지 표현 안함
print(float(a) / b)

# 형확인 함수 type(a)
print(say + ' ' + str(a))
print(say[4] * 20)

# list
list = [1,3,5,7,9]
print(len(list))
if 3 in list:
    print('exist')
else:
    print('not exist')

#===================================
# 제어문
#===================================
# java for loop
# for (int i = 0; i < 10; i++) {
#     System.out.println(i);
# }

# for
for i in list:
    print(i)

for i in range(10):
    print(i)

for i in range(2, 10):
    print(i)

for i in range(10, -1, -1):
    print(i)
	
# while
treeHit = 0
while 1:
    treeHit = treeHit + 1
    if treeHit == 10:
        print("last 10")
        break
    elif treeHit == 1:
        print("first 1")
    else:
        print(treeHit)

#===================================
# Function & Class
#===================================
# function
def sum(a, b): 
    return(a + b)

print(sum(3, 4))

# function
def sum_and_mul(a, b): 
    return (a + b, a * b)

print(sum_and_mul(3, 4))
(s, m) = sum_and_mul(3, 4)

print(s)
print(m)

# class
# __init__ : 클래스 초기화
# self : 클래스 자신, self를 사용해야 인스턴스에서 함수를 사용할 수 있음
# @staticmethod : static 함수를 선언할때 사용되는 키워드
class Person:
    def __init__(self, name):
        self.name = name
        
    def greet(self):
        print('Hello ' + self.name)
    
    @staticmethod
    def static_greet(name):
        print('Hello ' + name)

# Person 인스턴스 생성
pp = Person('QGIS')
pp.greet()

# Person Class의 staticmethod 호출
Person.static_greet('Quantum GIS')

# delete Function & class : del 명칭

#===================================
# 기타
#===================================
# math
import math

print(math.pi)
print(math.pow(2, 3))

# lambda
# lambda = 인수1, 인수2, ...  : 인수를 이용한 표현식
sum = lambda a, b: a+b 
sum(3,4) 


# 라이브러리 경로 추가
import sys
sys.path.append("C:\OpenGeoSuite\pyqgis20") 

# sys.path : 현재등록된 라이브러리 경로를 확인


if sys.version_info.major > 2:
    do_open = lambda filename: open(filename, encoding='utf-8')
else:
    do_open = lambda filename: open(filename)

with do_open(filename) as file:
    pass
