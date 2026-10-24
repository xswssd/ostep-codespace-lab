# Chapter 9: Lottery Scheduling

학번: 23217474
이름: 시에지위엔

## 과제 내용

OSTEP 9장 Lottery Scheduling 과제이다. lottery.py 시뮬레이터로 비례 배분 스케줄링 동작을 분석한다.

## 환경

Codespace: ostep-codespace-lab (fictional-umbrella)
시뮬레이터: ext/ostep-homework/cpu-sched-lottery/lottery.py
Q1–Q5: Codespace에서 공식 lottery.py로 재실행 (codespace-run.log)

## 파일 구조

hw/chapter9/
  README.md
  analysis.md
  data/

## 주요 결과

Q1: 3 jobs, seed 1/2/3으로 lottery trace 수동 계산 및 -c 검증
  - Seed 1: Job0 time 2, Job1 time 12, Job2 time 6
  - Seed 2: Job0 time 14, Job1 time 22, Job2 time 23
  - Seed 3: Job0 time 5, Job1 time 4, Job2 time 11
Q2: ticket 1:100 불균형 — Job0은 Job1 완료 전 실행 확률 ~9.5%, 대부분 seed에서 Job1이 time 10에 먼저 종료
Q3: ticket 100:100 동일 — seed 0–9에서도 완료 시간 차이 1–19 (평균 8.5), F 평균 ≈ 0.96 (완전 공정 아님)
Q4: quantum 증가 시 불공정성 증가 — q=1(평균 F 0.973) → q=50(평균 F 0.700), 평균 차이 5.4→60
Q5: Figure 9.2 재현 — R=1(F 0.50) → R=1000(F 0.98); Stride는 모든 R에서 F≈1

자세한 내용은 analysis.md를 보면 된다.
