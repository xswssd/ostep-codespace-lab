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


## Q4. Gaming 스케줄러 — 99% CPU

질문: 구 규칙 4a/4b(`-S`)를 이용해, 2개 job workload에서 한 job이 **특정 시간 구간**에 CPU의 **99%**를 차지하도록 설계하라.

### Workload 설계

교재는 allotment을 다 쓰기 전에 I/O를 내어 우선순위를 유지하는 gaming을 설명한다.
quantum=100ms일 때 **99ms마다 I/O**(`ioFreq=99`)를 내면, 한 주기(100 time unit) 안에서 gaming job이 Run 99회, 상대 job이 1회(I/O 대기 중) → **정확히 99% CPU**가 된다.

| 파라미터 | 값 | 의미 |
|----------|-----|------|
| `-n 3 -q 100` | 3개 큐, quantum=100ms | 최고 큐 allotment = 100ms |
| `-l 0,500,0:0,500,99` | Job0: CPU 500ms / Job1: CPU 500ms, ioFreq=99 | Job1이 gaming job |
| `-i 1` | I/O 시간 1ms | I/O 중 Job0가 1 tick CPU 사용 |
| `-S` | stayAfterIO | I/O 후 Priority 2 유지 (구 규칙 4a/4b) |

명령:
```
./mlfq.py -n 3 -q 100 -l 0,500,0:0,500,99 -i 1 -S -c
```

출력 파일: data/q4-gaming.txt
실행 환경: GitHub Codespace (`fictional-umbrella`)에서 공식 `mlfq.py`로 재실행함 (`data/codespace-run.log`).

### Gaming 원리

1. Job 0이 time 0–99에 최고 우선순위에서 첫 quantum(100ms)을 사용한다.
2. time 100부터 Job 1이 실행을 시작한다.
3. Job 1은 99ms CPU 실행 후 I/O를 발생시킨다 (`ioFreq=99`).
4. `-S` 때문에 I/O 후에도 Priority 2에 남고, ticks/allotment이 리셋된다.
5. I/O 1ms 동안 Job 0이 1 tick만 실행되고, Job 1이 다시 최고 우선순위로 돌아온다.
6. 이 패턴이 반복되면 Job 1이 CPU를 거의 독점한다.

### 99% CPU 시간 구간

**첫 번째 gaming 주기: time 100–199**

| 구간 | Job 1 Run | Job 0 Run | Job 1 비율 |
|------|-----------|-----------|------------|
| time 100–199 | 99 | 1 | **99.0%** |

동일 패턴이 time 200–299, 300–399, … 에서 반복된다.
Job 1이 완료되기 전까지 각 100ms 주기마다 99%를 유지한다.

trace에서 확인:
- time 199: `IO_START by JOB 1` (99ms 실행 직후)
- time 100–198: `Run JOB 1 at PRIORITY 2` 연속 99회
- time 199: `Run JOB 0` 1회 (Job 1 I/O 중)

### 예측 (통계)

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 1000 |
| 1 | 100 | 605 |

Job 0은 gaming 때문에 turnaround가 길고, Job 1은 빠르게 완료된다.

검증: time 100–199 구간 Run 행 100개 중 Job 1이 99개(99.0%)였고,
시뮬레이터 최종 통계와 위 표가 일치했다.


## Q5. Boost 주기 — 최소 5% CPU 보장

질문: 최고 큐 quantum이 10ms일 때, `-B`를 얼마로 설정해야
장기 실행(기아 가능) job이 **최소 5% CPU**를 받도록 보장할 수 있을까?

### 답: **200 ms**

### 수학적 유도

Priority boost는 모든 job을 최고 우선순위(Priority 2)로 올린다.
기아 상태의 긴 CPU job은 boost 직후 **한 번의 quantum(10ms)** 을 받을 수 있다.

최악의 경우, 긴 job은 boost 주기마다 10ms만 실행된다:

```
CPU 비율 ≥ quantum / B = 10 / B
```

5% 이상을 보장하려면:

```
10 / B ≥ 0.05  →  B ≤ 200 ms
```

따라서 **`-B 200`** 이 5%를 보장하는 최대 boost 주기이다.
(B가 200보다 크면 한 주기에 10ms 미만의 비율로 떨어질 수 있다.)

### 검증용 Workload

Figure 8.5와 유사하게, I/O 집약 job 2개가 `-S`로 높은 우선순위를 유지해
Job 0(CPU 집약)을 기아시키는 환경을 사용했다.

| 파라미터 | 값 | 의미 |
|----------|-----|------|
| `-n 3 -q 10` | 3개 큐, quantum=10ms | 최고 큐 time slice |
| `-l 0,200,0:0,200,1:0,200,1` | Job0: CPU 200ms / Job1,2: I/O 매 1ms | 기아 시나리오 |
| `-i 1 -S` | I/O 1ms, 구 규칙 | I/O job 우선순위 유지 |
| `-B 200` | 200ms마다 boost | 기아 방지 |

명령:
```
./mlfq.py -n 3 -q 10 -l 0,200,0:0,200,1:0,200,1 -i 1 -S -B 200 -c
```

출력 파일: data/q5-boost.txt

실행 환경: GitHub Codespace (`fictional-umbrella`)에서 공식 `mlfq.py`로 재실행함 (`data/codespace-run.log`).

### 예측

- time 200, 400에 `BOOST ( every 200 )` 이벤트 발생
- boost 직후 Job 0이 Priority 2에서 10ms 실행
- I/O job이 완료되기 전 구간(time 0–399)에서 Job 0 CPU 비율 ≈ 5%

| Job | response | turnaround |
|-----|----------|------------|
| 0 | 0 | 600 |
| 1 | 10 | 429 |
| 2 | 11 | 430 |

### CPU 비율 검증 (trace 통계)

| 구간 | Job 0 Run | 전체 Run | Job 0 비율 |
|------|-----------|----------|------------|
| time 0–199 | 10 | 200 | **5.0%** |
| time 200–399 | 10 | 200 | **5.0%** |

trace에서 time 200, 400에 BOOST가 나타났고,
I/O job이 살아 있는 동안 Job 0이 정확히 5.0% CPU를 받았다.
이는 `10ms / 200ms = 5%` 유도와 일치한다.


## Q6. `-I` 플래그 (I/O 완료 후 큐 위치)

질문: I/O가 끝난 job은 큐의 **앞(head)** 에 넣을까, **뒤(tail)** 에 넣을까?
`-I` 플래그가 이 동작을 어떻게 바꾸는지 같은 workload로 비교하라.

### `-I` 동작 (mlfq.py)

| 설정 | I/O 완료 후 큐 삽입 | 코드 |
|------|------------------|------|
| 기본 ( `-I` 없음) | **큐 뒤** (`append`) | FIFO 순서 유지 |
| `-I` (iobump) | **큐 앞** (`insert(0)`) | I/O 완료 job이 즉시 다음 실행 |

### Workload (동일)

| 파라미터 | 값 | 의미 |
|----------|-----|------|
| `-n 2 -q 10` | 2개 큐, quantum=10ms | MLFQ |
| `-l 0,50,0:0,50,11` | Job0: CPU 50ms / Job1: I/O 매 11ms | I/O 완료 후 큐 위치 비교 |
| `-i 1 -S` | I/O 1ms, 구 규칙 | I/O job이 주기적으로 블로킹 |

**`-I` 없음:**
```
./mlfq.py -n 2 -q 10 -l 0,50,0:0,50,11 -i 1 -S -c
```
출력 파일: data/q6-no-I.txt

**`-I` 있음:**
```
./mlfq.py -n 2 -q 10 -l 0,50,0:0,50,11 -i 1 -S -I -c
```
출력 파일: data/q6-with-I.txt

실행 환경: GitHub Codespace (`fictional-umbrella`)에서 공식 `mlfq.py`로 재실행함 (`data/codespace-run.log`).

### 예측

I/O 완료 시:
- **`-I` 없음:** Job 1이 큐 뒤로 가므로 Job 0이 먼저 계속 실행된다.
- **`-I` 있음:** Job 1이 큐 앞으로 가므로 I/O 직후 Job 1이 바로 CPU를 받는다.

### trace 차이 (첫 I/O 이후, time 31–32)

**`-I` 없음** — time 32 `IO_DONE` 후 Job 0 계속 실행:
```
time 31: IO_START by JOB 1
time 32: IO_DONE by JOB 1 → Run JOB 0  (Job 1은 큐 뒤)
time 33–41: Run JOB 0 연속
time 42: Run JOB 1
```

**`-I` 있음** — time 32 `IO_DONE` 후 Job 1 즉시 실행:
```
time 31: IO_START by JOB 1
time 32: IO_DONE by JOB 1 → Run JOB 1  (Job 1이 큐 앞으로 삽입)
time 33–41: Run JOB 1 연속
time 42: Run JOB 0
```

### 통계 비교

| | Job 0 response | Job 0 turnaround | Job 1 response | Job 1 turnaround |
|---|----------------|------------------|----------------|------------------|
| `-I` 없음 | 0 | **72** | 10 | 102 |
| `-I` 있음 | 0 | **93** | 10 | **101** |

검증:
- Job 1 response는 동일(10)이지만, `-I`로 I/O 후 즉시 실행되어 turnaround가 102→101로 약간 개선되었다.
- Job 0 turnaround는 72→93으로 증가했다. I/O job이 줄을 서지 않고 앞에 끼어들어 CPU job이 더 오래 기다렸다.
- `-I`는 인터랙티브(I/O) job의 반응성을 높이지만, CPU 집약 job의 공정성을 해칠 수 있다.


## 결론 (Q1–Q6)

Q1에서 2 jobs, 2 queues 환경의 MLFQ 기본 동작을 확인했고,
Q2에서 교재 Figure 8.2–8.7의 7가지 시나리오를 명령으로 재현했다.
Q3에서 `-n 1` 단일 큐 설정으로 MLFQ가 RR과 동일하게 동작함을 확인했다.
Q4에서 `-S`와 `ioFreq=99`(quantum=100)로 gaming job이 time 100–199 구간에서 CPU 99%를 차지함을 확인했다.
Q5에서 `-B 200`(quantum=10)으로 기아 job이 최소 5% CPU를 받음을 유도하고 trace로 검증했다.
Q6에서 `-I`가 I/O 완료 job을 큐 앞에 넣어 인터랙티브 job에 유리하고 CPU job 대기 시간을 늘림을 확인했다.
모든 예측이 시뮬레이터(-c) 결과와 일치했다.

시뮬레이터 원본 출력은 hw/chapter8/data/ 폴더에 있다.