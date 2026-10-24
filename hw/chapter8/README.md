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
    └── q1-seed2.txt
```

## Q1 주요 결과

| Seed | Job0 (runTime) | Job1 (runTime) | Job0 response | Job1 response |
|------|----------------|----------------|---------------|---------------|
| 0 | 17 | 8 | 0 | 10 |
| 1 | 3 | 15 | 0 | 3 |
| 2 | 19 | 2 | 0 | 10 |

자세한 내용은 analysis.md를 보면 된다.
