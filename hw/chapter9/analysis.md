# Chapter 9 Lottery Scheduling 분석

학번: 23217474
이름: 시에지위엔

이번 과제는 lottery.py로 Lottery Scheduling(복권 스케줄링)을 분석하는 내용이다.
각 job은 ticket 수에 비례해 CPU를 받을 확률이 결정된다.

계산 문제는 먼저 -c 없이 답을 예측하고, 그 다음 -c로 시뮬레이터 결과를 확인했다.
원본 출력은 data 폴더에 저장했다.

## 핵심 알고리즘

```
winning_ticket = random_number % total_tickets
```

ticket 범위를 job 순서대로 누적하여 winning ticket이 속한 job을 선택한다.
예: Job0이 84장(0–83), Job1이 25장(84–108), Job2가 44장(109–152)이면 총 153장.
winning ticket 119는 Job2 범위에 속한다.

job이 종료되면 해당 ticket은 제거되고, 남은 job만으로 다시 lottery를 진행한다.

## Q1. 3 jobs — seed 1, 2, 3

공통 명령:
```
./lottery.py -j 3 -s <SEED>      # 문제 확인
./lottery.py -j 3 -s <SEED> -c   # 검증
```

설정: 3개 job, quantum=1(기본값), maxlen=10, maxticket=100

### Seed 1

출력 파일: data/q1-seed1.txt

Job 목록:
| Job | length | tickets | ticket 범위 |
|-----|--------|---------|-------------|
| 0 | 1 | 84 | 0–83 |
| 1 | 7 | 25 | 84–108 |
| 2 | 4 | 44 | 109–152 |
| 합계 | | **153** | |

예측 (핵심 단계):

| step | Random | % total | winning | 실행 | 결과 |
|------|--------|---------|---------|------|------|
| 1 | 651593 | 153 | 119 | Job 2 | timeleft 4→3 |
| 2 | 788724 | 153 | 9 | Job 0 | timeleft 1→0, **time 2에 종료** |
| 3 | 93859 | 69 | 19 | Job 1 | timeleft 7→6 |
| 4 | 28347 | 69 | 57 | Job 2 | timeleft 3→2 |
| 5 | 835765 | 69 | 37 | Job 2 | timeleft 2→1 |
| 6 | 432767 | 69 | 68 | Job 2 | timeleft 1→0, **time 6에 종료** |
| 7–12 | (6회) | 25 | — | Job 1만 | **time 12에 종료** |

Job 0 종료 후 total tickets = 25+44 = 69.
Job 2 종료 후 total tickets = 25.

완료 시간:
| Job | 완료 time |
|-----|-----------|
| 0 | 2 |
| 1 | 12 |
| 2 | 6 |

검증: 시뮬레이터 결과와 일치했다.

### Seed 2

출력 파일: data/q1-seed2.txt

Job 목록:
| Job | length | tickets | ticket 범위 |
|-----|--------|---------|-------------|
| 0 | 9 | 94 | 0–93 |
| 1 | 8 | 73 | 94–166 |
| 2 | 6 | 30 | 167–196 |
| 합계 | | **197** | |

예측 (핵심 단계):

| step | Random | % total | winning | 실행 | 비고 |
|------|--------|---------|---------|------|------|
| 1 | 605944 | 197 | 169 | Job 2 | |
| 2 | 606802 | 197 | 42 | Job 0 | |
| 3 | 581204 | 197 | 54 | Job 0 | |
| … | … | … | … | Job 0 다수 실행 | ticket 94로 가장 넓음 |
| 14 | 27444 | 197 | 61 | Job 0 | **time 14에 종료** |
| 15–21 | | 103 | | Job 1, 2 | Job 1 **time 22 종료** |
| 22–23 | | 30 | | Job 2 | **time 23 종료** |

Job 0 종료 후 total = 73+30 = 103. Job 1 종료 후 total = 30.

완료 시간:
| Job | 완료 time |
|-----|-----------|
| 0 | 14 |
| 1 | 22 |
| 2 | 23 |

검증: 시뮬레이터 결과와 일치했다.

### Seed 3

출력 파일: data/q1-seed3.txt

Job 목록:
| Job | length | tickets | ticket 범위 |
|-----|--------|---------|-------------|
| 0 | 2 | 54 | 0–53 |
| 1 | 3 | 60 | 54–113 |
| 2 | 6 | 6 | 114–119 |
| 합계 | | **120** | |

예측 (핵심 단계):

| step | Random | % total | winning | 실행 | 비고 |
|------|--------|---------|---------|------|------|
| 1 | 13168 | 120 | 88 | Job 1 | |
| 2 | 837469 | 120 | 109 | Job 1 | |
| 3 | 259354 | 120 | 34 | Job 0 | |
| 4 | 234331 | 120 | 91 | Job 1 | **time 4에 Job 1 종료** |
| 5 | 995645 | 60 | 5 | Job 0 | **time 5에 Job 0 종료** |
| 6–11 | | 6 | 1–4 | Job 2만 | ticket 6장만 남음, **time 11 종료** |

Job 1이 ticket 60으로 가장 많아 초반에 자주 선택된다.
Job 2는 ticket이 6장뿐이라 마지막에만 단독 실행된다.

완료 시간:
| Job | 완료 time |
|-----|-----------|
| 0 | 5 |
| 1 | 4 |
| 2 | 11 |

검증: 시뮬레이터 결과와 일치했다.

### Q1 정리

세 가지 시나리오에서 lottery 기본 동작을 확인했다:
- **Seed 1**: Job 0이 1 time unit만 필요해 2번째 lottery에서 즉시 종료. 이후 Job 2(44 tickets)와 Job 1(25 tickets)이 비율에 따라 실행.
- **Seed 2**: Job 0이 ticket 94로 가장 많아 초반에 CPU를 많이 받고 time 14에 종료. Job 1·2는 순차적으로 마무리.
- **Seed 3**: Job 1(ticket 60)이 먼저 완료(time 4), Job 0(time 5), Job 2(ticket 6)는 마지막에 단독 실행.

공통 규칙: `random % total_tickets`로 winning ticket을 구하고, 누적 ticket 범위로 job을 선택한다. job 종료 시 해당 ticket은 시스템에서 제거된다.

실행 환경: GitHub Codespace (`fictional-umbrella`)에서 공식 `lottery.py`로 재실행함 (`data/codespace-run.log`).

## Q2. Ticket 불균형 (1 vs 100)

명령:
```
./lottery.py -l 10:1,10:100      # 문제 확인
./lottery.py -l 10:1,10:100 -c   # 검증
```

출력 파일: data/q2-imbalance.txt

### Workload

| Job | length | tickets | ticket 범위 |
|-----|--------|---------|-------------|
| 0 | 10 | 1 | 0 (1장만) |
| 1 | 10 | 100 | 1–100 |
| 합계 | | **101** | |

### 예측

Job 0이 선택되려면 `winning_ticket = 0`이어야 한다.
두 job이 모두 살아 있을 때 매 lottery에서 Job 0이 당첨될 확률:

```
P(Job 0) = 1 / 101 ≈ 0.99%
P(Job 1) = 100 / 101 ≈ 99.01%
```

Job 1이 완료되려면 10 time unit이 필요하므로, 그 동안 약 10번의 lottery가 진행된다.
Job 1 완료 전에 Job 0이 **한 번 이상** 실행될 확률:

```
1 - (100/101)^10 ≈ 9.47%
```

10번 lottery 동안 Job 0의 **기대 실행 횟수** ≈ 10 × (1/101) ≈ **0.099회** (거의 0).

**결론 예측:** Job 0은 Job 1 완료 전에 실행될 **수는 있지만 매우 드물다**. 대부분의 seed에서는 Job 1이 먼저 10번 연속(또는 거의 연속) 실행되어 time 10에 종료하고, Job 0은 time 10–19에 단독 실행된다.

### 검증 (seed 0, 기본)

| 단계 | winning ticket | 실행 | 비고 |
|------|----------------|------|------|
| 1–10 | 6–79 (전부 1–100) | **Job 1만** 10회 | Job 0 timeleft 계속 10 |
| time 10 | — | JOB 1 DONE | |
| 11–20 | 0 (전부) | **Job 0만** 10회 | ticket 1장만 남음 |
| time 20 | — | JOB 0 DONE | |

seed 0에서는 Job 1 완료 전 Job 0 실행 횟수 = **0회**.
Job 0 완료 time = **20**, Job 1 완료 time = **10**.

### 추가 확인 (seed 2)

seed 2에서는 Job 1 완료 전 Job 0이 **1회** 실행되었다 (`winning ticket = 0`이 한 번 나옴).
이는 확률적으로 가능한 드문 경우이다.

seed 0–49 스캔 결과: 6/50 seed(12%)에서 Job 0이 Job 1 완료 전 실행됨. 이론값 9.47%와 유사한 수준.

### Q2 정리

| 질문 | 답 |
|------|-----|
| Job 0이 Job 1 완료 전에 실행되나? | **가능하지만 매우 드묾** (약 1/101 per lottery) |
| 얼마나 자주? | 10번 lottery 중 기대값 **~0.1회**; 한 번 이상 확률 **~9.5%** |
| ticket 불균형의 영향? | CPU가 거의 전부 Job 1에 몰림 → Job 0 **기아(starvation) 위험**; 비례 배분이 장기적으로는 1:100이지만 단기·중기에는 극단적 불공정 |

검증: 시뮬레이터(-c) 결과와 일치했다.

## Q3. 공정성 측정 (동일 ticket 100:100)

질문: 두 job이 각각 length 100, ticket 100:100일 때 lottery 스케줄러는 얼마나 **불공정**한가? 여러 random seed로 실험하고, 완료 시간 차이와 공정성 지표 **F**를 계산한다.

### Workload

| Job | length | tickets | ticket 범위 |
|-----|--------|---------|-------------|
| 0 | 100 | 100 | 0–99 |
| 1 | 100 | 100 | 100–199 |
| 합계 | | **200** | |

공통 명령 (Codespace):
```
./lottery.py -l 100:100,100:100 -s <SEED> -c
```

seed 0–9 각각 실행하여 `data/q3-seed0.txt` … `data/q3-seed9.txt`에 저장했다.
요약: `data/q3-summary.txt`, `data/q3-done-all.txt`

### 공정성 지표 F (교재 Figure 9.2)

```
F = min(finish_A, finish_B) / max(finish_A, finish_B)
```

- F = 1: 두 job이 **동시에** 완료 (완전 공정)
- F가 작을수록: 한 job이 다른 job보다 **훨씬 먼저** 끝남 → 불공정

불공정도(차이): `|finish_0 - finish_1|`

### 예측

ticket이 100:100으로 **동일**하므로 장기적으로 각 job이 CPU를 받을 확률은 50%이다.
그러나 lottery는 매 quantum마다 **무작위**로 job을 고르므로, 단기·중기적으로는 한 job이 연속으로 여러 번 선택될 수 있다.
따라서 완료 시간은 seed마다 달라지며, F < 1인 경우가 **흔할 것**으로 예상했다.
(두 job 총 작업량 200 time unit이므로, 마지막 job 완료 시점은 대략 200 전후일 것이다.)

### 검증 (seed 0–9)

| seed | Job0 완료 time | Job1 완료 time | 차이 | F |
|------|---------------|---------------|------|-----|
| 0 | 192 | 200 | 8 | 0.9600 |
| 1 | 200 | 196 | 4 | 0.9800 |
| 2 | 200 | 190 | 10 | 0.9500 |
| 3 | 196 | 200 | 4 | 0.9800 |
| 4 | 200 | 199 | 1 | 0.9950 |
| 5 | 200 | 181 | 19 | 0.9050 |
| 6 | 200 | 193 | 7 | 0.9650 |
| 7 | 200 | 185 | 15 | 0.9250 |
| 8 | 200 | 191 | 9 | 0.9550 |
| 9 | 200 | 192 | 8 | 0.9600 |

10개 seed 통계:
- 완료 시간 차이: 최소 **1**, 최대 **19**, 평균 **8.5**
- F: 최소 **0.9050** (seed 5), 최대 **0.9950** (seed 4), 평균 **≈ 0.958**

seed 4는 거의 동시 완료(F=0.995, 차이 1)이고, seed 5는 Job1이 time 181에 끝난 반면 Job0은 time 200에 끝나 **19 time unit** 차이가 난다.
8/10 seed에서 Job0이 time 200에 완료되었고, Job1은 seed마다 181–200 사이에서 완료되었다.

### Q3 정리

| 질문 | 답 |
|------|-----|
| 동일 ticket이면 완전 공정한가? | **아니다.** lottery의 **확률적** 선택 때문에 완료 시간이 seed마다 다름 |
| 불공정 정도는? | 차이 1–19 (평균 8.5), F 평균 ≈ 0.96 |
| 왜 발생하나? | 매 lottery가 독립적이므로 한 job이 연속 당첨되면 다른 job 완료가 지연됨 |
| 장기적으로는? | ticket 비율이 50:50이면 CPU 점유율은 장기적으로 50:50에 **수렴**하지만, 유한 실행에서는 완료 시점 불공정이 남음 |

검증: 시뮬레이터(-c) 결과와 일치했다.
실행 환경: GitHub Codespace (`fictional-umbrella`)에서 공식 `lottery.py`로 재실행함 (`data/codespace-run.log`).

## Q4. Quantum(-q)이 불공정성에 미치는 영향

질문: Q3과 동일 workload에서 **quantum(`-q`)이 커지면** 불공정성이 어떻게 변하는가?

### Workload (Q3와 동일)

| Job | length | tickets |
|-----|--------|---------|
| 0 | 100 | 100 |
| 1 | 100 | 100 |

공통 명령 (Codespace):
```
./lottery.py -l 100:100,100:100 -q <Q> -s <SEED> -c
```

비교 quantum: **1, 2, 5, 10, 50**
각 q마다 seed **0–4** (5회) 실행.
출력: `data/q4-q{q}-seed{s}.txt`, 요약: `data/q4-avg.txt`, `data/q4-done-all.txt`

### 예측

- **q=1**: 매 lottery마다 1 time unit만 실행 → 무작위 선택이 매 step마다 섞임 → 완료 시간 차이가 **상대적으로 작음**
- **q가 커질 때**: 한 번 당첨되면 **연속 q time unit** 실행 → 한 job이 긴 burst를 가질 수 있음 → 다른 job 완료가 지연 → **완료 시간 차이 증가**, F 감소
- ticket 비율(50:50)은 장기적으로 유지되지만, **단기 burst** 때문에 유한 실행에서는 q가 클수록 불공정

### 검증 — quantum별 평균 (seed 0–4)

| quantum (-q) | 평균 완료 시간 차이 | 평균 F | 불공정성 |
|--------------|-------------------|--------|----------|
| 1 | **5.4** | **0.973** | 가장 공정 |
| 2 | **7.6** | **0.962** | |
| 5 | **21.0** | **0.895** | |
| 10 | **24.0** | **0.880** | |
| 50 | **60.0** | **0.700** | 가장 불공정 |

**명확한 추세:** q가 커질수록 평균 차이가 증가하고 F가 감소한다 (1→50: 차이 5.4→60, F 0.973→0.700).

### 대표 사례

**q=1, seed 0** (`data/q4-q1-seed0.txt`): Job0 time 192, Job1 time 200 → diff=8, F=0.96

**q=10, seed 0** (`data/q4-q10-seed0.txt`): Job1 time 150, Job0 time 200 → diff=50, F=0.75
→ q=1 대비 한 job이 50 time unit 먼저 끝남.

**q=50, seed 2** (`data/q4-q50-seed2.txt`): Job0 time 100, Job1 time 200 → diff=100, F=0.50
→ quantum=50이면 한 job이 50×2 burst로 먼저 100을 채우고, 다른 job은 time 200까지 대기.

### Q4 정리

| 질문 | 답 |
|------|-----|
| q가 커지면? | **불공정성 증가** (평균 차이 ↑, F ↓) |
| 왜? | 당첨 시 **더 오래 연속 실행** → burst가 커져 완료 시점 차이 확대 |
| Q3(q=1)과 비교? | Q3 평균 차이 8.5 / F≈0.96 (seed 0–9); Q4 q=1 평균 차이 5.4 / F=0.973 (seed 0–4) — 같은 방향 |
| 장기 CPU 비율? | ticket 50:50이므로 여전히 **장기적으로 50:50 수렴**; 단기·유한 실행에서만 불공정 |

검증: 시뮬레이터(-c) 결과와 일치했다.
실행 환경: GitHub Codespace (`fictional-umbrella`)에서 공식 `lottery.py`로 재실행함 (`data/codespace-run.log`).

## Q5. Figure 9.2 재현 + Stride Scheduler 비교

질문: 교재 Figure 9.2( job 길이 R vs 평균 공정성 F )를 재현할 수 있는가? Stride scheduler는 어떤 그래프가 될까?

### Figure 9.2 설정

- 두 job: 각각 길이 **R**, ticket **100:100** (동일)
- quantum = 1 (기본값)
- 각 R마다 **30회** trial (seed 0–29)
- 공정성: `F = min(finish_0, finish_1) / max(finish_0, finish_1)`
- 평균 F를 R에 따라 측정

명령 예:
```
./lottery.py -l R:100,R:100 -s <SEED> -c
```

배치 수집: `data/q5_collect.py` → `data/q5-fairness-data.txt`, `data/q5-progress.txt`
대표 trace: `data/q5-sample-R100-seed0.txt` (R=100, seed=0; Q3 `q3-seed0.txt`와 동일 workload)

### 예측

- **R이 작을 때**: lottery 횟수가 적어 무작위성 영향이 큼 → 한 job이 먼저 끝나기 쉬움 → **F 낮음**
- **R이 클 때**: 많은 lottery로 50:50 비율이 **법률의 큰 수**로 수렴 → 완료 시점도 가까워짐 → **F → 1**
- **Stride**: ticket에 비례한 **deterministic** 순서 → 매 실행마다 정확히 비율 유지 → **모든 R에서 F ≈ 1** (평평한 상단 곡선)

### 검증 — R별 평균 F (30 trials)

| Job 길이 R | 평균 F | 해석 |
|-----------|--------|------|
| 1 | **0.5000** | 각 job 1 time unit → 한쪽이 time 1, 다른 쪽 time 2 → F=0.5 고정 |
| 10 | **0.8467** | 짧은 job → 불공정성 큼 |
| 50 | **0.9370** | 중간 길이 → 개선 |
| 100 | **0.9437** | Q3/Q4 workload와 동일 R |
| 500 | **0.9782** | 장 job → 거의 공정 |
| 1000 | **0.9833** | F → 1에 수렴 |

**Figure 9.2 추세 재현:** R이 증가하면 평균 F가 **단조 증가**하여 1에 가까워진다. R=1에서 F=0.5(최악), R=1000에서 F≈0.98.

R=1에서 모든 seed가 F=0.5000인 이유: 두 job이 각 1 time unit이므로 한 job은 time 1, 다른 job은 time 2에 완료되어 항상 `F = 1/2`.

### Stride Scheduler 비교 (교재 9.6절)

| 항목 | Lottery | Stride |
|------|---------|--------|
| 선택 방식 | **무작위** (ticket 비례 확률) | **결정적** (pass 값 최소 job) |
| F vs R | R 작으면 낮음, R 크면 → 1 | **모든 R에서 F ≈ 1** |
| 그래프 형태 | 하단에서 상단으로 **상승 곡선** | **상단 평평** (≈1.0) |
| trial 간 분산 | seed마다 F 다름 (확률적) | trial마다 **동일** (결정적) |
| 단점 | 단기 불공정 | pass 갱신·신규 job 삽입 시 **전역 상태** 필요 |

Stride 동작 요약:
```
stride_i = BIG / tickets_i
매 실행 후 pass_i += stride_i
다음 실행 job = argmin(pass)
```
ticket 100:100이면 두 job이 **정확히 번갈아** 실행 → 완료 시점이 항상 거의 동시 → F≈1.

Lottery는 R=100에서도 평균 F≈0.94로 stride보다 낮다. **장기 비례 배분**은 lottery도 달성하지만, **유한 실행·짧은 job**에서는 stride가 더 공정하다.

### Q5 정리

| 질문 | 답 |
|------|-----|
| Figure 9.2 재현? | **가능** — R↑ → 평균 F↑, R=1000에서 ≈0.98 |
| R=1이 특별한 이유? | 총 2 time unit만 실행 → F=0.5 고정 |
| Stride 그래프? | 모든 R에서 **F≈1** 평평 곡선 |
| 무엇을 더 탐구할 수 있나? | ticket 불균형 + stride, `-q`와 stride 결합, 신규 job 삽입 시 pass 조정 |

검증: 시뮬레이터(-c) 결과와 일치했다. 공식 `lottery.py`로 30×6=180회 실행 (`data/q5-fairness-data.txt`, `data/q5-progress.txt`).
실행 환경: GitHub Codespace (`fictional-umbrella`)에서 `data/q5_collect.py` 배치 실행 (`data/codespace-run.log`).
