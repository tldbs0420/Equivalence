# 이번 과제는 A = {1, 2, 3, 4, 5} 로 진행한다.
A = [1, 2, 3, 4, 5]

# 이번 과제는 5 x 5 행렬로 진행된다.
n = 5

# 행렬 출력
def PrintMatrix(M):
    print("┌ ", end = "")
    for i in range(n):
        print("%2d " %M[0][i], end = "")
    print(" ┐")

    for x in range(1, n-1):
        print("│ ",  end = "")
        for y in range(n):
            print("%2d " %M[x][y],  end = "")
        print(" │")

    print("└ ", end = "")
    for i in range(n):
        print("%2d " %M[n-1][i],  end = "")
    print(" ┘")

# 행렬을 비교하는 함수
def CompareMatrix(M, N):
    for i in range(len(M)):
        for j in range(len(N)):
            if M[i][j] != N[i][j]:
                return False
    return True

# 반사 관계인지 확인
def IsReflexive(R):
    for i in range(n):
        if R[i][i] != 1:
            return False
    return True

# 대칭 관계인지 확인
def IsSymmetric(R):
    for i in range(n):
        for j in range(n):
            if R[i][j] != R[j][i]:
                return False
    return True

# 추이 관계인지 확인
def IsTransitive(R):
    for i in range(n):
        for k in range(n):
            if R[i][k] == 1:
                for j in range(n):
                    if R[k][j] == 1 and R[i][j] == 0:
                        return False
    return True

# 반사 폐포 생성
def ReflexiveClosure(R):
    newR = [row[:] for row in R]
    for i in range(n):
        newR[i][i] = 1
    return newR

# 대칭 폐포 생성
def SymmetricClosure(R):
    newR = [row[:] for row in R]
    for i in range(n):
        for j in range(n):
            if newR[i][j] == 1:
                newR[j][i] = 1
    return newR

# 추이 폐포 생성
def TransitiveClosure(R):
    newR = [row[:] for row in R]  # 원본 복사

    while True:
        changed = False
        # R ∘ R 계산해서 누락된 (i,j) 추가
        for i in range(n):
            for j in range(n):
                if newR[i][j] == 1:
                    continue  # 이미 1이면 신경 안 써도 됨
                # (i,j)가 0이라면, i→k, k→j 경로가 있는지 확인
                for k in range(n):
                    if newR[i][k] == 1 and newR[k][j] == 1:
                        newR[i][j] = 1   # 새로 추가
                        changed = True
                        break            # 이 (i,j)는 더 볼 필요 없음
        if not changed:
            break  # 더 이상 늘어나는 쌍이 없으면 종료
    return newR

# 추이 폐포 생성 (Warshall 알고리즘)
def TransitiveClosureWarshall(R):
    newR = [row[:] for row in R]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if newR[i][k] == 1 and newR[k][j] == 1:
                    newR[i][j] = 1
    return newR

# 입력 행렬을 동치로 만드는 함수
def EquivalenceClosure(R):
     return TransitiveClosure(SymmetricClosure(ReflexiveClosure(R)))

# 반사 폐포가 아닌 원인 위치 리턴
def FindReflexiveCounterexample(R):
    for i in range(n):
        if R[i][i] != 1:
            return i+1
    return None

# 대칭 폐포가 아닌 원인 이유 리턴
def FindSymmetricCounterexample(R):
    for i in range(n):
        for j in range(n):
            if R[i][j] != R[j][i]:
                return (i+1, j+1)
    return None

# 추이 폐포가 아닌 원인 이유 리턴
def FindTransitiveCounterexample(R):
    for i in range(n):
        for k in range(n):
            if R[i][k] == 1:
                for j in range(n):
                    if R[k][j] == 1 and R[i][j] == 0:
                        return (i+1, k+1, j+1)
    return None

# 각 성질 판별
def PrintProperties(R):
    ref = IsReflexive(R)
    sym = IsSymmetric(R)
    tra = IsTransitive(R)

    print("\n[관계 성질 판별 결과]")
    if (ref):
        print("반사성 (Reflexive): O")
    else:
        print("반사성 (Reflexive): X", end = "")
        reason = FindReflexiveCounterexample(R)
        print(f"  (사유: ({reason},{reason})가 0임)")

    if (sym):
        print("대칭성 (Symmetric): O")
    else:
        print("대칭성 (Symmetric): X", end = "")
        reason = FindSymmetricCounterexample(R)
        i,j = reason
        print(f"  (사유: ({i},{j})와 ({j},{i}) 값이 다름)")

    if (tra):
        print("추이성 (Transitive): O \n")
    else:
        print("추이성 (Transitive): X", end = "")
        reason = FindTransitiveCounterexample(R)
        i,k,j = reason
        print(f"  (사유: ({i},{k})=1, ({k},{j})=1 인데 ({i},{j})=0) \n")

    if (ref and sym and tra) : PrintEquivalenceClasses(R)

# 동치류 리스트 리턴
def EquivalenceClass(R, x):
    idx = A.index(x)
    eq = []
    for j in range(n):
        if R[idx][j] == 1 and R[j][idx] == 1:  # 양방향 연결 확인
            eq.append(A[j])
    return eq
    
# 동치류 출력 함수
def PrintEquivalenceClasses(R):
    print("[동치류]")
    for x in A:
        eq = EquivalenceClass(R, x)
        contents = ", ".join(str(e) for e in eq)
        print(f"  [{x}] = {{ {contents} }}")
    print()

def main():
    while(True):
        print("5 x 5 관계행렬을 입력하세요 (띄어쓰기로 구분 | -1 To Exit ):")

        # n * n (5 x 5) 행렬 생성 및 0으로 채워넣기
        R = [[float(0) for _ in range(n)] for _ in range(n)]

        checkExit = False
        inputNumbers = []
        while len(inputNumbers) < n * n:
            # 숫자 입력 (띄어쓰기 구분 가능)
            inputLine = input("숫자 입력 : ").split()

            # 입력받은 줄 내에서 해석 가능 범위까지 해석 및 추가
            try:
                for num in inputLine:
                    if (int(num) == 0 or int(num) == 1):
                        inputNumbers.append(int(num))
                    elif (int(num) == -1):
                        checkExit = True
                        break
                    else:
                        raise ValueError
            except:
                print("숫자를 제대로 입력해주세요. (0 또는 1 입력)")
            if checkExit:
                break
        if checkExit:
            break

        # 숫자 할당
        for i in range(n):
            for j in range(n):
                R[i][j] = inputNumbers[i * n + j]

        print("\n[입력한 관계행렬]")
        PrintMatrix(R)

        # 첫 판별
        PrintProperties(R)

        # 반사 폐포
        refR = ReflexiveClosure(R)
        print("[반사 폐포 결과]")
        PrintMatrix(refR)
        PrintProperties(refR)

        # 대칭 폐포
        symR = SymmetricClosure(R)
        print("[대칭 폐포 결과]")
        PrintMatrix(symR)
        PrintProperties(symR)

        # 추이 폐포
        traR = TransitiveClosure(R)
        print("[추이 폐포 결과] - 정의 기반 알고리즘")
        PrintMatrix(traR)
        warR = TransitiveClosureWarshall(R)
        print("[추이 폐포 결과 - Warshall 알고리즘]")
        PrintMatrix(warR)
        # 두 결과가 같은지 비교
        if CompareMatrix(traR, warR):
            print("두 알고리즘의 추이 폐포 결과가 완전히 같습니다.")
        else:
            print("두 알고리즘의 추이 폐포 결과가 서로 다릅니다.")
            print("     (다른 원소의 위치와 값)")

            for i in range(n):
                for j in range(n):
                    if traR[i][j] != warR[i][j]:
                        print(f"     위치 ({i+1}, {j+1}): 정의기반={traR[i][j]}, Warshall={warR[i][j]}")
        PrintProperties(traR)

        # 동치 폐포 (반사 → 대칭 → 추이 한 번씩)
        EQ = EquivalenceClosure(R)
        print("[동치 폐포 결과]")
        PrintMatrix(EQ)
        PrintProperties(EQ)

if __name__ == "__main__":
    main()