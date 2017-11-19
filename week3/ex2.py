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

def compute_cond_probability(lhs,r,rhs):
    prX = 0
    pYr = 0
    count_lh = count_lhs(all_triples, lhs)
    count_r = count_relationships(all_triples, r)
    count_l_r = count_lhs_r(all_triples, lhs, r)
    for e in all_rhs:
        if e != rhs:
            #print('\nCount for left entity (', lhs, ') is:', count_lh)
            #print('Count for relationship (', r, ') is:', count_r)
            #count_rh = count_rhs(all_triples, e)
            #print('- Count for right entity (', e, ') is:', count_rh)
            count_rh_r = count_rhs_r(all_triples, e, r)
            #print('- Count for r-rh combination is:', count_rh_r)
            #print('Count for l-r combination is:', count_l_r)
            #print('Count for r-rh combination is:', count_rh_r)
            prX = count_l_r / count_lh
            #print('prx =', prX)
            pYr = count_rh_r / count_r
            #print('pYr =', pYr)
            #print(prX,pYr,prX*pYr)
    return lhs+' '+r+' '+rhs, prX, pYr, prX*pYr

def generate_from_lhs(choice,all_triples):
    print('entity=', choice)
    print('relations: ')
    for j in range(len(entities)):
        if all_triples[j][0]==choice:
            print(' ', all_triples[j])
            c_triples.append(all_triples[j])
            if (not all_lhs.__contains__(all_triples[j][0])):
                all_lhs.append(all_triples[j][0])
            if (not all_rhs.__contains__(all_triples[j][2])):
                all_rhs.append(all_triples[j][2])
            if (not all_r.__contains__(all_triples[j][1])):
                all_r.append(all_triples[j][1])
    print()
    print('ENTITIES:',all_lhs)
    print('RELATIONS:',all_r)
    print('ENTITIES',all_rhs)
    print()

    print('All uses of relationship:')
    for lhs,r,rhs in all_triples:
        if r in all_r:
            print('     ',lhs,r,rhs)
    print()

    possibilities=[]
    for e in all_lhs:
        for f in all_r:
            for g in all_rhs:
                #print('FOR the sentence:',e,f,g)
                sent, px, py, prob = compute_cond_probability(e,f,g)
                if(prob>0.0):
                    #print('Possible sentence:',sent,'=>',prob,px,py)
                    possibilities.append(str(prob)+' - '+sent)
                    possibilities.sort(reverse=True)
    for e in possibilities:
        print(e)
    return possibilities

all_triples = factgen.read_triples("reverb.txt", min_attested=2)
entities = factgen.collect_entities(all_triples, min_freq=1)
c_triples=[]
all_lhs=[]
all_rhs=[]
all_r=[]
QUERY_TERM= 'lunch'
generate_from_lhs(QUERY_TERM, all_triples)