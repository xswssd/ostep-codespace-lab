# Chapter 7: CPU Scheduling

학번: 23217474
이름: 시에지위엔

## 과제 내용

OSTEP 7장 CPU 스케줄링 과제이다. scheduler.py 시뮬레이터로 FIFO, SJF, RR 세 가지 정책을 비교했다.

## 환경

Codespace: ostep-codespace-lab
Python 3.12.3
시뮬레이터: ext/ostep-homework/cpu-sched/scheduler.py

## 파일 구조

hw/chapter7/
  README.md
  analysis.md
  data/

## 주요 결과

Q1: 작업 길이가 같으면 FIFO와 SJF 결과가 같다
Q2: 도착 순서가 길이 순이면 FIFO와 SJF 결과가 같다
Q3: RR q=1은 응답이 빠르지만 반환 시간이 크다
Q4: SJF와 FIFO Turnaround이 같으려면 길이가 같거나 도착 순서가 길이 순이어야 한다
Q5: SJF와 RR Response가 같으려면 작업 길이가 같고 quantum이 작업 길이와 같아야 한다
Q6: SJF에서 작업이 길어지면 평균 Response도 커진다
Q7: RR에서 quantum이 커지면 Response는 커지고 Turnaround은 줄어든다

자세한 내용은 analysis.md를 보면 된다.
