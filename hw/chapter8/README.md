# Chapter 8: Multi-Level Feedback Queue (MLFQ)

학번: 23217474
이름: 시에지위엔

## 과제 내용

OSTEP 8장 MLFQ 과제이다. mlfq.py 시뮬레이터로 2 jobs, 2 queues 환경에서 execution trace를 계산하고, 교재 Figure 8.2~8.7을 재현한다.

## 환경

Codespace: ostep-codespace-lab
Python 3 (python-is-python3)
시뮬레이터: ext/ostep-homework/cpu-sched-mlfq/mlfq.py

## 파일 구조

```
hw/chapter8/
├── README.md
├── analysis.md
└── data/
    ├── q1-seed0.txt
    ├── q1-seed1.txt
    ├── q1-seed2.txt
    ├── q2-fig8.2.txt
    ├── q2-fig8.3.txt
    ├── q2-fig8.4.txt
    ├── q2-fig8.5-no-boost.txt
    ├── q2-fig8.5-boost.txt
    ├── q2-fig8.6-with-S.txt
    ├── q2-fig8.6-no-S.txt
    └── q2-fig8.7.txt
```

## Q1 주요 결과

| Seed | Job0 (runTime) | Job1 (runTime) | Job0 response | Job1 response |
|------|----------------|----------------|---------------|---------------|
| 0 | 17 | 8 | 0 | 10 |
| 1 | 3 | 15 | 0 | 3 |
| 2 | 19 | 2 | 0 | 10 |

## Q2 주요 결과

| Figure | 핵심 현상 | 주요 수치 |
|--------|-----------|-----------|
| 8.2 | 긴 job 강등 | Job0 turnaround=200 |
| 8.3 | 인터랙티브 job 삽입 | Job1 turnaround=20 |
| 8.4 | I/O + CPU 혼합 | Job1이 먼저 완료 |
| 8.5 no boost | 기아 | Job0 turnaround=220 |
| 8.5 boost | 기아 해소 | Job0 turnaround=160 |
| 8.6 with -S | gaming 성공 | Job1 turnaround=111 |
| 8.6 no -S | gaming 방지 | Job1 turnaround=223 |
| 8.7 | 긴 quantum | Job1 response=10, TICKS=40 |

자세한 내용은 analysis.md를 보면 된다.
