# Chapter 8: MLFQ Scheduling

학번: 23217474
이름: 시에지위엔

## 과제 내용

OSTEP 8장 MLFQ(Multi-Level Feedback Queue) 과제이다. mlfq.py 시뮬레이터로 스케줄링 동작을 분석했다.

## 환경

Codespace: ostep-codespace-lab (fictional-umbrella)
시뮬레이터: ext/ostep-homework/cpu-sched-mlfq/mlfq.py
Q4/Q5/Q6: Codespace에서 공식 환경으로 재실행 (codespace-run.log)

## 파일 구조

hw/chapter8/
  README.md
  analysis.md
  data/

## 주요 결과

Q1: 2 jobs, 2 queues, 3개 seed로 MLFQ 기본 동작 확인
Q2: 교재 Figure 8.2–8.7 전부 재현
Q3: `-n 1` 단일 큐로 MLFQ = Round-Robin
Q4: `-S` + ioFreq=99로 gaming job이 time 100–199 구간에서 CPU 99% 차지
Q5: `-B 200`(quantum=10)으로 기아 job 최소 5% CPU 보장 (10/200=5%)
Q6: `-I`는 I/O 완료 job을 큐 앞에 넣음 (없으면 큐 뒤)

자세한 내용은 analysis.md를 보면 된다.
