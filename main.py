def negative(clause):
    if '-' in clause:
        literal = clause.replace('-', '')
    else:
        literal = '-' + clause
    return literal


def negativeCNF(clause):
    literals = clause.split(' ')

    for i in range(0, len(literals)):
        literals[i] = negative(literals[i])

    return literals


def sort(clause):
    if len(clause) <= 2:
        return clause
    temp = clause
    temp = temp.replace('-', '')
    temp = temp.split()
    temp.sort()
    clauses = []
    for i in temp:
        for j in range(len(clause)):
            if clause[j] == i and clause[j - 1] == '-':
                clauses.append('-')
        clauses.append(i)
    result = clauses[0]
    if len(clauses) > 0:
        for x in range(len(clauses) - 1):
            if clauses[x] != '-':
                result = result + " " + clauses[x + 1];
            else:
                result = result + clauses[x + 1];
    return result


def isResolvable(ci, cj):
    # check for opposite literals
    for i in ci.split(' '):
        i = negative(i)
        if i in cj:
            return True

    # check for repeated literals
    for i in ci.split(' '):
        if i in cj:
            return False

    return False


def unnecessaryResolution(ci, cj):
    literals_ci = ci.split()
    literals_cj = cj.split()

    count = 0
    for i in literals_ci:
        if i in literals_cj:
            count += 1

    if count == len(literals_ci):
        return True

    count = 0
    for i in literals_cj:
        if i in literals_ci:
            count += 1

    if count == len(literals_cj):
        return True


def readFile(name):
    kb = []

    file = open(name, "r")
    alpha = file.readline()[0:-1]
    alpha = alpha.replace(" OR ", " ")
    alpha = sort(alpha)

    kb_size = file.readline()[0:-1]
    clause = None

    for i in range(0, int(kb_size) - 1):
        clause = file.readline()[0:-1]
        clause = clause.replace(" OR ", " ")
        clause = sort(clause)
        kb.append(clause)

    clause = file.readline()
    clause = clause.replace(" OR ", " ")
    clause = sort(clause)
    kb.append(clause)

    file.close()

    return kb, alpha


def PL_RESOLUTION(kb, alpha):
    outfile = open("output.txt", "w")

    clauses = kb + negativeCNF(alpha)

    resolvants = []
    new = []

    while True:
        new.clear()
        newResolvantCount = 0
        n = len(clauses)
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                pairs.append((clauses[i], clauses[j]))

        for (ci, cj) in pairs:
            if not isResolvable(ci, cj):
                continue
            if unnecessaryResolution(ci, cj):
                continue

            resolvent = PL_RESOLVE(ci, cj)

            resolvent = sort(resolvent)

            if resolvent == "":
                continue

            if resolvent == "{}":
                outfile.write(str(newResolvantCount + 1) + '\n')
                for resolvent in new:
                    resolvent = resolvent.replace(" ", " OR ")
                    outfile.write(resolvent + '\n')
                outfile.write("{}\nYES")
                outfile.close()
                return True

            if resolvent not in new:
                if resolvent not in clauses:
                    new.append(resolvent)
                    newResolvantCount += 1

            if resolvent not in resolvent:
                resolvants.append(resolvent)

        outfile.write(str(newResolvantCount) + '\n')
        for resolvent in new:
            resolvent = resolvent.replace(" ", " OR ")
            outfile.write(resolvent)
            outfile.write('\n')

        count = 0
        newLen = len(new)
        for c in new:
            if c in clauses:
                count = count + 1
        if count == newLen:
            outfile.write("NO")
            outfile.close()
            return False

        for resolvent in new:
            if resolvent not in clauses:
                clauses.append(resolvent)


def PL_RESOLVE(ci, cj):
    literals_ci = ci.split()
    literals_cj = cj.split()

    # remove similar literals
    for i in literals_ci:
        for j in literals_cj:
            if i == j:
                literals_cj.remove(j)

    result = ""

    # remove opposite literals
    for i in literals_ci:
        for j in literals_cj:
            if i == '-' + j or '-' + i == j:
                literals = literals_ci + literals_cj
                literals.remove(i)
                literals.remove(j)

                if not literals:
                    return "{}"

                hasOppositePair = 0

                for k in literals:
                    for t in literals:
                        if k == negative(t):
                            hasOppositePair += 1
                            break

                if hasOppositePair == 0:
                    result = literals[0]
                    if len(literals) > 0:
                        for k in range(len(literals) - 1):
                            result = result + " " + literals[k + 1]
                else:
                    continue

    return result


kb, alpha = readFile("input.txt")

print(f'Alpha: {alpha}')
print(f'KB: {kb}')

# print(unnecessaryResolution("A B", "A B C"))
# print(PL_RESOLVE("B C", "-B C"))

print(PL_RESOLUTION(kb, alpha))