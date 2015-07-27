import timeit as t

from gurobipy import *

import data as d
import stats as st


"""
Creates ILP model based on given data.

model - existing Model instance
selection_keys = tuplelist instance of model's variables dictionary
selection - model's variables dictionary, is expected to have (name,version) as key
deps - (name, refs_count) list, name represents library name (key for selection)
split - if true, create constraints so that there is only a single feasible solution
"""
def addConstraints(model, selection_keys, selection, deps, split):
    for name, count in deps:
        versions = []
        for sel in selection_keys.select(name, '*'):
            versions.append(selection[sel])

        allCount = count / 2 if split else count #top constraint index till which all components satisfy the constraint
        lower = 3 * count / 4 if split else 0   #if split, top constraint index till which the first half of components satisfies the constraint
        upper = count if split else 0 #if split, top constraint index till wihch the second half of components satisfies the constraint
        for i in range(allCount):
            reqs = '%s-%d' % (name, i)
            model.addConstr(quicksum(versions) == 1, 'req_%s' % reqs)

        if split:
            verlen = len(versions)
            subver1 = versions[0:verlen/2 + 1] #only the middle component satisfies all constraints
            subver2 = versions[verlen/2: verlen]
            for i in range(allCount, lower):
                reqs = '%s-%d' % (name, i)
                model.addConstr(quicksum(subver1) == 1, 'req_%s' % reqs)


            for i in range(lower, upper):
                reqs = '%s-%d' % (name, i)
                model.addConstr(quicksum(subver2) == 1, 'req_%s' % reqs)


"""
Handles experiment flow based on given parameters

split - if True, there is only one feasible solution in the set
provider-names = list of provider (library) names which are to participate in the run
magnification = desired magnification value
"""
def runExperiment(app_name, exp_desc, split = False, provider_names=[], magnification = 1):
    providers = d.readProviders(provider_names, magnification)
    deps = d.readDeps(provider_names, magnification)

    m = Model(app_name + ' ' + exp_desc)
    m.setParam('LogToConsole', 0)

    selection = {}
    for prv in providers:
        selection[prv.name, prv.version] = m.addVar(ub=1, obj=prv.cost, vtype=GRB.INTEGER, name='%s-%s' % (prv.name, prv.version))

    m.update()
    selection_keys = tuplelist(selection)

    addConstraints(m, selection_keys, selection, deps, split)

    m.optimize()


#the actual experiment run for all scenarios
args = [['ant'], ['ant', 'ant-junit'], ['ant', 'ant-junit', 'junit'], ['ant-junit', 'junit'], ['junit'], ['ant-junit']]
magnifiers = [1, 10, 100, 1000]
splits = [False, True]
results = {}
for a in range(len(args)):
    for m in magnifiers:
        for s in splits:
            func = lambda: runExperiment("ILP Search Initial Eval", '%s-%s-%s' % (a, m, s), s, args[a], m)
            results[a, m, s] = t.repeat(func, number=1, repeat=100)

#print results to console
for a, m, s in results:
    stat = st.makeStats(results[a,m,s])
    print('%s-%d: %f %f %s' % (args[a], m, stat[0], stat[1], s))
