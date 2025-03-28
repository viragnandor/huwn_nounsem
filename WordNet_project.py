#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xmltodict
import numpy


# In[2]:


with open('WORDNET_HuWN_final4.xml', 'r', encoding='utf-8') as file:
    wn_xml = file.read()

wn_dict = xmltodict.parse(wn_xml)


# In[3]:


def findAllHyperonym(ssid):
    hlist = set(id_hypo_dict[ssid])
    for i in id_hypo_dict[ssid]:
        hlist = hlist.union(findAllHyperonym(i))
    return hlist

def ancestors(lemmas):
    ret = []
    for lem in lemmas:
        commons = set()
        for ID in lit_id_dict[lem]:
            commons = commons.union(set(findAllHyperonym(ID)))
        ret.append([lem, list(commons)])
    return ret

def commonN(hypl, f):
    N = len(hypl) * f
    unl = []
    ret = []
    for [l, h] in hypl:
        unl = unl + h
    for hyp in set(unl):
        lemmas = [l for [l, h] in hypl if hyp in h]
        if len(lemmas) >= N:
            ret.append([hyp, lemmas])
    return ret

def lowestCommon(hypl, f):
    lowl = []
    cl = commonN(hypl, f)
    for w in cl:
        i = False
        for x in cl:
            if w[0] in findAllHyperonym(x[0]):
                i = True    
        if not i:
            lowl.append(w)
    return lowl


# In[4]:


root = wn_dict['WNXML']['SYNSET']


# In[5]:


id_lit_dict = {}
for x in root:
    if type(x['SYNONYM']['LITERAL']) == list:
        v = [y['#text'] for y in x['SYNONYM']['LITERAL']]
    else:
        v = [x['SYNONYM']['LITERAL']['#text']]
    id_lit_dict[x['ID']] = v


# In[6]:


lit_id_dict = {}
for x in root:
    if type(x['SYNONYM']['LITERAL']) == list:
        v = [y['#text'] for y in x['SYNONYM']['LITERAL']]
    else:
        v = [x['SYNONYM']['LITERAL']['#text']]
    for z in v:
        if z in lit_id_dict.keys():
            lit_id_dict[z] = lit_id_dict[z] + [x['ID']]
        else:
            lit_id_dict[z] = [x['ID']]


# In[7]:


id_hypo_dict = {}
for x in root:
    if 'ILR' not in x.keys():
        id_hypo_dict[x['ID']] = []
        continue
    if type(x['ILR']) == list:
        v = x['ILR']
    else:
        v = [x['ILR']]
    id_hypo_dict[x['ID']] = [y['#text'] for y in v if y['TYPE'] == 'hypernym']


# In[8]:


findAllHyperonym('ENG20-02415757-n')


# In[10]:


hyps = ancestors(["ló", "kutya", "nyúl"])


# In[11]:


commonN(hyps, 0.6)


# In[9]:


print(lowestCommon(hyps, 1))


# In[13]:


id_lit_dict['ENG20-01244626-n']

