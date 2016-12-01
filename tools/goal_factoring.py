# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:19:12 2016

@author: mfreeman
"""

import networkx as nx
import matplotlib.pyplot as plt

def my_input(input_field,test_input_text,test=False):
    if(test==True):
        return test_input_text
    else:
        return raw_input(input_field)


def rerank_goals(input_goals):
    print "Re-rank your goals in order of priority. Enter the goal reference number, from most to least important, separated by commas. \n(e.g. Enter 3,1,2 if #3 is most important, followed by #1, with #2 being least important.)"

    for inx,goal in enumerate(input_goals):
        print str(inx+1)+". "+goal[0]

    goal_reranking = raw_input(": ")

    reranked_goals = [input_goals[int(kk)-1] for kk in goal_reranking.split(",")]

    return reranked_goals


def add_goals(goals_init=[],test=False):
    print "Begin listing what you feel to be your goals. These can be terminal or temporary, irreducible or complex, end-state or intermediate goals, values, or objectives. \nList them in whatever order they occur to you. \nDon't worry about precision, we'll sort that out later. Think of this as brainstorming.\n(Press Enter after each goal. Enter X when done inputting goals. You'll have a chance to add more later.)"

    base_length = len(goals_init)
    goals_count = len(goals_init)
    while True:
        goals_count += 1
        goal = my_input(str(goals_count)+". ",str(goals_count) if goals_count < 7 else "x",test)  # "goal_ex"+str(goals_count) if goals_count<(base_length+6) else "x"
        if(goal.lower() == "x"): break
        goals_init.append([goal,[],[]])

    return goals_init



def goal_support(goals_init,test=False):
    print "Some goals are more fundamental than others. We are going to map out how your goals feed into and support each other.\nYour most fundamental, irreducible goals will be something akin to Maslow's Hierarchy of Human Needs.\n"

    for inx,goal in enumerate(goals_init):
        for inxx,goalx in enumerate(goals_init):
            print str(inxx+1)+". "+goalx[0]
        subgoals = my_input("Which of the above goals feeds into or supports '"+goal[0]+"'? Goals can support more than one other goal. \n(List their indices separated by commas. Enter 'x' if there are none that feed into this goal.) \n: ",["6,3","x","2,6","6","x","4,5"][inx],test)  # ["3,4","3,5","4","5","x","6","5","x","2,4","2","x","3,4,5"]
        if(subgoals.lower() != "x"):
            goals_init[inx][1] = [int(kk)-1 for kk in subgoals.split(",")]

    return goals_init



"""
reranked_goals = rerank_goals(goals_init)

while True:
    for inx,goal in enumerate(reranked_goals):
        print str(inx+1)+". "+goal
    verify_choice = raw_input("\n\nHere is your new ranking. Is it correct? (y/n)")

    if(verify_choice.lower() == "n"):
        reranked_goals = rerank_goals(reranked_goals)
    else:
        break
"""

def add_actions(actions_init=[],test=False):
    print "Begin listing actions that you do frequently or plan to do frequently.\nList them in whatever order they occur to you. \nDon't worry about precision, we'll sort that out later. Think of this as brainstorming.\nThese should be things you like doing and should be doing, or things you wish you didn't do.\n(Press Enter after each action. Enter X when done inputting actions. You'll have a chance to add more later.)"

    actions_count = len(actions_init)
    while True:
        actions_count += 1
        action = my_input(str(actions_count)+". ", str(actions_count) if actions_count<2 else "x",test)  # "action_ex"+str(actions_count) if actions_count<8 else "x"
        if(action.lower() == "x"): break
        actions_init.append([action,[]])
    return actions_init

def action_support(goals_init,actions_init,test=False):
    print "Now trace how your actions support your goals.\n"

    for inx,goal in enumerate(goals_init):
        for inxx,actionx in enumerate(actions_init):
            print str(inxx+1)+". "+actionx[0]
        subactions = my_input("Which of the above actions feeds into or supports '"+goal[0]+"'? Actions can support more than one goal. \n(List their indices separated by commas. Enter 'x' if there are none that feed into this goal.) \n: ",["x","x","x","x","x","x","x"][inx],test)  # ["2,4,3","1,2","3","2","2,3","x","5,6","2,4,7","x","7,5","4,7"]
        if(subactions.lower() != "x"):
            goals_init[inx][2] = [int(kk)-1 for kk in subactions.split(",")]
    return goals_init


def pretty_tree(goals,actions):
    for g in goals:
        print g[0]
        for ii in g[1]:
            print "---"+goals[ii][0]
            ##for jj in goals[ii][1]:
            ##    print "------"+goals[jj][0]
            ##    for kk in goals[jj][1]:
            ##        print "---------"+goals[kk][0]
        for ii in g[2]:
            print "---"+actions[ii][0]



def rec(children,goals,idx,looptrace=[]):
    # There's gotta be something better than using a global in a recursive function.
    global all_loops
    for subid,xx in enumerate(children):

        if(len(children) == 0):
            looptrace = []
        else:
            looptrace.append(xx)
        if(xx in looptrace[:-1]):
            #print "Loop found at: ", [kk+1 for kk in looptrace]
            return looptrace
        else:
            # continue down chain ...
            grandchildren = goals[xx][1]
            found_loop = rec(grandchildren,goals,xx,looptrace)
            if(type(found_loop) == type([])): all_loops.append(found_loop)
            looptrace = []

def find_loops(goals):
    global all_loops
    for idx,g in enumerate(goals):
        trc = rec(g[1],goals,idx,looptrace=[idx])
    return all_loops

test = True

goals_init = []
actions_init = []

iteration = 0
while True:
    iteration += 1
    goals_init = add_goals(goals_init,test=test)
    goals_init = goal_support(goals_init,test)
    actions_init = add_actions(actions_init,test)
    goals_init = action_support(goals_init,actions_init,test)

    pretty_tree(goals_init,actions_init)

    print "At this point, you may notice that you've left out some important goals or actions. We're going to iterate through the previous process again and add and connect goals where appropriate."

    iterate = my_input("Do you want to revise your goal/action structure? We recommend three iterations to be sure. (y/n)",["y","n","n"][iteration-1],test)
    if(iterate.lower() == 'n'): break


while True:
    all_loops = []

    final_all_loops = find_loops(goals_init)
    if(len(final_all_loops) == 0):
        print "All loops have now been removed."
        break

    if(len(final_all_loops) > 0):
        loops_present = True

    if(loops_present):
        print "There were some dependency loops in your goal structure. The loops will be automatically removed based on inferred priority, and then you'll have a chance to adjust your goal dependency structure."
        print "Here is one of your loops:\n "
        val, idx = min((len(val),idx) for (idx,val) in enumerate(final_all_loops))
        print " --> ".join([goals_init[gx][0] for gx in final_all_loops[idx]])

        lowest = goals_init[final_all_loops[idx][-2]]
        print lowest
        print "The low-priority goal is inferred to be '"+lowest[0]+"' so this is where the loop will be cut."
        print "looking in",goals_init[final_all_loops[idx][-2]][1], "for",final_all_loops[idx][-1]
        goals_init[final_all_loops[idx][-2]][1].remove(final_all_loops[idx][-1])

        """
        print "In order to break this loop, please select which of those goals is the most fundamental or most important."
        for ii,g in enumerate(final_all_loops[idx][0:-1]):
            print str(ii+1)+". "+goals_init[g][0]
        """

pretty_tree(goals_init,actions_init)

G = nx.DiGraph()
G.correlation={}
edge_cmap = []

for g in goals_init:
    children = g[1]
    for child in [goals_init[c] for c in children]:
        print g, child
        G.add_edge(g[0],child[0],weight=1.0)
        edge_cmap.append(1.0)
nx.draw(G,with_labels=True,legend=True,alpha=0.5,edge_cmap=edge_cmap,layout=nx.spring_layout(G),arrows=True)

