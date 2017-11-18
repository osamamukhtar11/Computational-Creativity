import factgen
import random

def count_relationships(all_triples, r):
    count = 0
    for i in range(len(all_triples)):
        if r == all_triples[i][1]:
            count = count + 1
    return count

def count_lhs(all_triples, lhs):
    count = 0
    for i in range(len(all_triples)):
        if lhs == all_triples[i][0]:
            count = count + 1
    return count

def count_lhs_r(all_triples, lhs, r):
    count = 0
    for i in range(len(all_triples)):
        if lhs == all_triples[i][0]:
            if r == all_triples[i][1]:
                count = count + 1
    return count

def count_rhs(all_triples, rhs):
    count = 0
    for i in range(len(all_triples)):
        if rhs == all_triples[i][2]:
            count = count + 1
    return count

def count_rhs_r(all_triples, rhs, r):
    count = 0
    for i in range(len(all_triples)):
        if rhs == all_triples[i][2]:
            if r == all_triples[i][1]:
                count = count + 1
    return count


def generate_from_lhs(lhs, all_triples):
    prX = 0
    pYr = 0
    for lhs, r, rhs in c_triples:
        count_lh = count_lhs(all_triples, lhs)
        count_r = count_relationships(all_triples, r)
        count_l_r = count_lhs_r(all_triples, lhs, r)
        count_rh = count_rhs(all_triples, rhs)
        count_rh_r = count_rhs_r(all_triples, rhs, r)
        print('\nCount for entity (', lhs, ') is:', count_lh)
        print('Count for entity (', rhs, ') is:', count_rh)
        print('Count for relationship (', r, ') is:', count_r)
        print('Count for l-r combination is:', count_l_r)
        print('Count for r-rh combination is:', count_rh_r)
        prX = count_l_r / count_lh
        print('prx =', prX)
        pYr = count_rh_r / count_r
        print('pYr =', pYr)
        print()

    # print('LHS:',lhs,'R:',r,'RHS:',rhs)
    generated = []
    for lhs1, rel1, rhs1 in all_triples:
        if r == rel1:
            count_lh = count_lhs(all_triples, lhs1)
            count_r = count_relationships(all_triples, rel1)
            count_l_r = count_lhs_r(all_triples, lhs1, rel1)
            count_rh = count_rhs(all_triples, rhs1)
            count_rh_r = count_rhs_r(all_triples, rhs1, rel1)
            prX = count_l_r / count_lh
            pYr = count_rh_r / count_r
            prob = prX * pYr
            print('For given relationship, all options:', lhs1, rel1, rhs1, '(', prob, ')')
            temp = lhs1 + ' ' + rel1 + ' ' + rhs1 + ' (' + str(prob) + ')'
            generated.append(temp)
            #        if(lhs == lhs1):
            #            print('B- For given relationship,lhs, all options:', lhs1, rel1, rhs1, '(',prob,')')

            # if(rhs != rhs1):
            #    print('C- For given relationship,lhs,not rhs, all options:', lhs1, rel1, rhs1)

    print('Generated Text:', generated)
    return generated

all_triples = factgen.read_triples("reverb.txt", min_attested=2)
entities = factgen.collect_entities(all_triples, min_freq=0)
print("Selected entities from total:", len(entities))
c = random.choice(entities)
check = False
c_triples=[]
while(not check):
    c = random.choice(entities)
    for j in range(len(entities)):
        if all_triples[j][0]==c:
            check = True
print('entity=',c)
print('relations: ')
for j in range(len(entities)):
    if all_triples[j][0]==c:
        print(' ', all_triples[j])
        c_triples.append(all_triples[j])

generate_from_lhs(c,all_triples)
#Still need to do the ordering based on score