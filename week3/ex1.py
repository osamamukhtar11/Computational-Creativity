import factgen
import random

all_triples = factgen.read_triples("reverb.txt", min_attested=2)
entities = factgen.collect_entities(all_triples, min_freq=0)
print("Selected entities from total:", len(entities))
c = random.choice(entities)
selectedEntities = []
for i in range(5):
    check = False
    while(not check):
        c = random.choice(entities)
        for j in range(len(entities)):
            if all_triples[j][0]==c:
                check = True
    selectedEntities.append(c)
    print(c,'= choice')
    print('relations: ')
    for j in range(len(entities)):
        if all_triples[j][0]==c:
            print(' ', all_triples[j])