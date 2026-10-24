# Chapter 8 MLFQ 분석

학번: 23217474
이름: 시에지위엔

이번 과제는 mlfq.py로 MLFQ(Multi-Level Feedback Queue) 스케줄러를 분석하는 내용이다.
응답 시간(response)은 작업이 도착한 후 처음 CPU를 받는 시간이고,
반환 시간(turnaround)은 도착부터 완료까지 걸린 시간이다.

계산 문제는 먼저 -c 없이 답을 예측하고, 그 다음 -c로 시뮬레이터 결과를 확인했다.
원본 출력은 data 폴더에 저장했다.

## Q1. 2 jobs, 2 queues, I/O 없음 — 3개 seed

공통 명령:
```
./mlfq.py -s <SEED> -n 2 -j 2 -m 20 -M 0      # 문제 확인
./mlfq.py -s <SEED> -n 2 -j 2 -m 20 -M 0 -c    # 검증
```

설정: 2개 큐, quantum=10, allotment=1, boost=0, I/O 없음 (-M 0)

### Seed 0 (Job0: 17ms, Job1: 8ms)

출력 파일: data/q1-seed0.txt

예측:
Job 0이 Queue 1에서 먼저 실행된다. 10ms quantum을 다 쓰면 Priority 0으로 내려간다.
그 다음 Job 1이 Priority 1에서 8ms 실행 후 종료된다.
Job 0은 Priority 0에서 남은 7ms를 실행한다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 25 |
| 1 | 10 | 18 |
| Avg | 5.00 | 21.50 |

검증: 시뮬레이터 결과와 일치했다.

### Seed 1 (Job0: 3ms, Job1: 15ms)

출력 파일: data/q1-seed1.txt

예측:
Job 0은 3ms만 필요해서 quantum을 다 쓰기 전에 끝난다.
Job 1은 Job 0이 끝난 후(time 3) 실행을 시작한다.
Job 1은 Priority 1에서 10ms 후 Priority 0으로 내려가 나머지 5ms를 실행한다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 3 |
| 1 | 3 | 18 |
| Avg | 1.50 | 10.50 |

검증: 시뮬레이터 결과와 일치했다.

### Seed 2 (Job0: 19ms, Job1: 2ms)

출력 파일: data/q1-seed2.txt

예측:
Seed 0과 비슷한 구조이다. Job 0이 먼저 10ms quantum을 쓰고 내려간다.
Job 1은 time 10에 시작해서 2ms만 실행하고 끝난다.
Job 0은 Priority 0에서 남은 9ms를 실행한다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 21 |
| 1 | 10 | 12 |
| Avg | 5.00 | 16.50 |

검증: 시뮬레이터 결과와 일치했다.

### Q1 정리

세 가지 시나리오를 확인했다:
- Seed 0: 긴 job이 먼저 quantum을 다 쓰고 내려감 → 짧은 job이 기다림
- Seed 1: 짧은 job이 먼저 끝남 → 긴 job이 나중에 실행
- Seed 2: Seed 0과 대칭 구조

MLFQ 규칙: 새 job은 최고 우선순위 큐에 들어가고, quantum/allotment을 다 쓰면 한 단계 내려간다.
같은 큐에서는 FIFO 순서로 실행된다.

## Q2. 교재 Figure 8.2–8.7 재현

공통 설정: 3개 큐(-n 3), quantum=10(-q 10), allotment=1(기본값)
`-l x,y,z`는 startTime, runTime, ioFreq를 의미한다.

### Figure 8.2 — 긴 CPU job의 점진적 강등

명령:
```
./mlfq.py -n 3 -q 10 -l 0,200,0 -c
```

출력 파일: data/q2-fig8.2.txt

예측:
200ms CPU 집약 job 하나가 최고 우선순위(Priority 2)에서 시작한다.
10ms마다 allotment을 다 쓰면 한 단계씩 내려간다.
time 0–9: Priority 2, time 10–19: Priority 1, time 20 이후: Priority 0.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 200 |

검증: Priority 2→1→0 순서로 강등되며 turnaround=200과 일치했다.

### Figure 8.3 — 인터랙티브 job 삽입

명령:
```
./mlfq.py -n 3 -q 10 -l 0,180,0:100,20,0 -c
```

출력 파일: data/q2-fig8.3.txt

예측:
Job 0은 180ms CPU job이다. Job 1은 time 100에 20ms job으로 도착한다.
Job 0이 낮은 우선순위에서 실행 중일 때 Job 1이 도착하면,
Job 1은 즉시 최고 우선순위에서 실행된다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 200 |
| 1 | 0 | 20 |

검증: time 100에 Job 1이 Priority 2에서 바로 실행되고, time 120에 완료되었다.

### Figure 8.4 — I/O 집약 + CPU 집약 혼합

명령:
```
./mlfq.py -n 3 -q 10 -l 0,175,0:50,25,1 -i 5 -S -c
```

출력 파일: data/q2-fig8.4.txt

예측:
Job 0은 CPU 집약(175ms), Job 1은 I/O 집약(매 1ms마다 I/O, I/O 시간 5ms).
`-S` 옵션으로 I/O 후 원래 우선순위를 유지한다.
Job 1이 빈번한 I/O로 높은 우선순위를 유지하고 먼저 완료된다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 200 |
| 1 | 0 | 145 |

검증: Job 1이 IO_START/IO_DONE을 반복하며 높은 우선순위를 유지했다.

### Figure 8.5 — Priority Boost (기아 방지)

#### 8.5a: Boost 없음 (기아)

명령:
```
./mlfq.py -n 3 -q 10 -l 0,120,0:100,50,1:100,50,1 -i 1 -S -c
```

출력 파일: data/q2-fig8.5-no-boost.txt

예측:
Job 0은 CPU 집약(120ms). Job 1, 2는 time 100에 I/O 집약 job으로 도착한다.
I/O job들이 `-S`로 높은 우선순위를 유지하면 Job 0이 기아 상태에 빠진다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 220 |
| 1 | 0 | 99 |
| 2 | 1 | 100 |

검증: Job 0 turnaround=220으로 마지막에 완료되어 기아가 발생했다.

#### 8.5b: Boost 있음 (기아 해소)

명령:
```
./mlfq.py -n 3 -q 10 -l 0,120,0:100,50,1:100,50,1 -i 1 -S -B 50 -c
```

출력 파일: data/q2-fig8.5-boost.txt

예측:
`-B 50`으로 50ms마다 모든 job을 최고 우선순위로 올린다.
Job 0이 주기적으로 boost를 받아 실행 기회를 얻는다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 160 |
| 1 | 10 | 119 |
| 2 | 11 | 120 |

검증: Job 0 turnaround가 220→160으로 줄어 boost가 기아를 해소함을 확인했다.

### Figure 8.6 — Gaming (우선순위 조작)

#### 8.6a: 구 규칙 (`-S` 있음, gaming 가능)

명령:
```
./mlfq.py -n 3 -q 10 -i 1 -S -l 0,200,0:80,100,9 -c
```

출력 파일: data/q2-fig8.6-with-S.txt

예측:
Job 1이 9ms마다 I/O를 발생시켜 `-S` 규칙으로 높은 우선순위를 유지한다(gaming).
Job 0은 CPU를 거의 못 받고 Job 1이 빠르게 완료된다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 300 |
| 1 | 0 | 111 |

검증: Job 1 turnaround=111, Job 0=300으로 gaming이 성공했다.

#### 8.6b: 신 규칙 (`-S` 없음, gaming 방지)

명령:
```
./mlfq.py -n 3 -q 10 -i 1 -l 0,200,0:80,100,9 -c
```

출력 파일: data/q2-fig8.6-no-S.txt

예측:
`-S` 없이 I/O 후 우선순위가 유지되지 않으면 gaming이 실패한다.
Job 1이 강등되어 Job 0의 실행 기회가 늘어난다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 272 |
| 1 | 0 | 223 |

검증: Job 1 turnaround가 111→223으로 증가하여 신 규칙이 gaming을 막았다.

### Figure 8.7 — 낮은 우선순위에 더 긴 quantum

명령:
```
./mlfq.py -n 3 -a 2 -Q 10,20,40 -l 0,200,0:0,200,0 -c
```

출력 파일: data/q2-fig8.7.txt

예측:
`-Q 10,20,40`으로 각 큐 quantum이 10/20/40ms이다.
`-a 2`로 각 레벨에서 2번의 time slice를 쓴 후 강등한다.
두 200ms job이 동시 도착하면 낮은 큐에서 TICKS가 40까지 증가한다.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 380 |
| 1 | 10 | 400 |

검증: Job 1 response=10, 낮은 큐 TICKS=40, 교재 Figure 8.7과 일치했다.

### Q2 정리

| Figure | 핵심 현상 |
|--------|-----------|
| 8.2 | 긴 job이 Priority 2→1→0으로 강등 |
| 8.3 | 새 인터랙티브 job이 즉시 최고 우선순위 |
| 8.4 | `-S`로 I/O job이 높은 우선순위 유지 |
| 8.5 | Boost 없으면 기아(220), Boost 있으면 해소(160) |
| 8.6 | `-S`로 gaming 가능(111), 없으면 방지(223) |
| 8.7 | 낮은 큐 quantum=40, allotment=2 |


## Q3. MLFQ를 Round-Robin으로 설정

질문: 어떤 파라미터로 MLFQ를 RR(Round-Robin) 스케줄러와 동일하게 만들 수 있을까?

### 설정 방법

핵심은 **`-n 1` (단일 큐)**이다.

| 파라미터 | 값 | 의미 |
|----------|-----|------|
| `-n 1` | 1개 큐 | 우선순위 레벨이 하나뿐 → 강등 없음 |
| `-q 10` | quantum=10ms | RR time slice |
| `-j 3 -m 30 -M 0` | 3 jobs, 최대 30ms, I/O 없음 | 검증용 workload |

MLFQ가 RR로 동작하는 이유:
- 여러 큐가 없으면 job이 한 단계 아래로 내려갈 곳이 없다.
- allotment을 다 써도 같은 큐(Priority 0)에 남는다.
- 같은 큐에서는 FIFO + time slice로 CPU를 나누므로, 이것이 곧 Round-Robin이다.

명령:
```
./mlfq.py -n 1 -q 10 -j 3 -m 30 -M 0 -c
```

출력 파일: data/q3-rr.txt

### 예측

3개 job이 동시 도착하면, 각 job이 10ms씩 번갈아 실행된다.
time 0–9: Job 0, time 10–19: Job 1, time 20–29: Job 2,
time 30–39: Job 0, time 40–49: Job 1, … 순서로 라운드 로빈.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 53 |
| 1 | 10 | 43 |
| 2 | 20 | 48 |

검증: trace에서 Job 0→1→2→0→1→2→0 순서로 10ms quantum씩 실행되었고,
시뮬레이터 결과와 일치했다. 단일 큐 MLFQ = RR가 확인되었다.


## Q3. MLFQ를 Round-Robin으로 설정

질문: 어떤 파라미터로 MLFQ를 RR(Round-Robin) 스케줄러와 동일하게 만들 수 있을까?

### 설정 방법

핵심은 **`-n 1` (단일 큐)**이다.

| 파라미터 | 값 | 의미 |
|----------|-----|------|
| `-n 1` | 1개 큐 | 우선순위 레벨이 하나뿐 → 강등 없음 |
| `-q 10` | quantum=10ms | RR time slice |
| `-j 3 -m 30 -M 0` | 3 jobs, 최대 30ms, I/O 없음 | 검증용 workload |

MLFQ가 RR로 동작하는 이유:
- 여러 큐가 없으면 job이 한 단계 아래로 내려갈 곳이 없다.
- allotment을 다 써도 같은 큐(Priority 0)에 남는다.
- 같은 큐에서는 FIFO + time slice로 CPU를 나누므로, 이것이 곧 Round-Robin이다.

명령:
```
./mlfq.py -n 1 -q 10 -j 3 -m 30 -M 0 -c
```

출력 파일: data/q3-rr.txt

### 예측

3개 job이 동시 도착하면, 각 job이 10ms씩 번갈아 실행된다.
time 0–9: Job 0, time 10–19: Job 1, time 20–29: Job 2,
time 30–39: Job 0, time 40–49: Job 1, … 순서로 라운드 로빈.

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 53 |
| 1 | 10 | 43 |
| 2 | 20 | 48 |

검증: trace에서 Job 0→1→2→0→1→2→0 순서로 10ms quantum씩 실행되었고,
시뮬레이터 결과와 일치했다. 단일 큐 MLFQ = RR가 확인되었다.

## 결론 (Q1–Q3)

Q1에서 2 jobs, 2 queues 환경의 MLFQ 기본 동작을 확인했고,
Q2에서 교재 Figure 8.2–8.7의 7가지 시나리오를 명령으로 재현했다.
Q3에서 `-n 1` 단일 큐 설정으로 MLFQ가 RR과 동일하게 동작함을 확인했다.
모든 예측이 시뮬레이터(-c) 결과와 일치했다.

시뮬레이터 원본 출력은 hw/chapter8/data/ 폴더에 있다.