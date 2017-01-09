# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:19:12 2016

@author: mfreeman
"""

import networkx as nx
import matplotlib.pyplot as plt
import time
import pickle
import os

def main_menu(test):
    while True:
        print "1. Create New Goal Architecture."
        print "2. Load and Edit Existing Goal Architecture."
        choice = my_input(": ","1",test)
        if(choice == "1"):
            new_goal_structure(test)
            break
        elif(choice == "2"):
            while True:
                goals,actions = load_files(test)
                cls()
                print "Goals loaded."
                print "Would you like to ... "
                print "1. Input more goals"
                print "2. Input more actions"
                print "3. Develop your goal interdependency graph"
                print "4. Develop your action interdependency graph"
                print "5. Find and remove goal dependency loops"
                print "6. Visualize your goal graph"
                print "X. Return to load menu."
                #main_goal_input_loop(goals,actions,1,test)
                choice = my_input(": ","1",test)
                if(choice == "1"):
                    goals = add_goals(goals,test)
                elif(choice == "2"):
                    actions = add_actions(actions,test)
                elif(choice == "3"):
                    goals = goal_support(goals,test)
                elif(choice == "4"):
                    goals = action_support(goals,actions)
                elif(choice == "5"):
                    main_loop_removal_loop(goals,test)
                elif(choice == "6"):
                    network_digraph(goals,actions)
                elif(choice == "X"):
                    break
                else:
                    print "Invalid choice."
                save_files(goals,actions)
        else:
            print "Invalid choice."

def cls():
    print "\n"*100
    os.system("clear")
    os.system("CLS")

def my_input(input_field,test_input_text,test={"status":False,"phase":"0"}):
    if(test["status"]==True):
        return test_input_text
    else:
        return raw_input(input_field)


def rerank_goals(input_goals):
    cls()
    print "Re-rank your goals in order of priority. Enter the goal reference number, from most to least important, separated by commas. \n(e.g. Enter 3,1,2 if #3 is most important, followed by #1, with #2 being least important.)"

    for inx,goal in enumerate(input_goals):
        print str(inx+1)+". "+goal[0]

    goal_reranking = raw_input(": ")

    reranked_goals = [input_goals[int(kk)-1] for kk in goal_reranking.split(",")]

    return reranked_goals


def add_goals(goals_init=[],test={"status":False,"phase":"0"}):
    cls()
    print "Begin listing what you feel to be your goals. These can be terminal or temporary, irreducible or complex, end-state or intermediate goals, values, or objectives. \nList them in whatever order they occur to you. \nDon't worry about precision, we'll sort that out later. Think of this as brainstorming.\nConsider adding some 'avoid' goals such as 'avoid financial catastrophe'.\n(Press Enter after each goal. Enter X when done inputting goals. You'll have a chance to add more later.)"

    goals_count = len(goals_init)
    while True:
        goals_count += 1
        goal = my_input(str(goals_count)+". ",str(goals_count) if goals_count < 7*(1+int(test["phase"])) else "x",test)  # "goal_ex"+str(goals_count) if goals_count<(base_length+6) else "x"
        if(goal.lower() == "x"): break
        goals_init.append([goal,[],[]])

    return goals_init



def goal_support(goals_init,test={"status":False,"phase":"0"}):
    cls()
    print "Some goals are more fundamental than others. We are going to map out how your goals feed into and support each other.\nYour most fundamental, irreducible goals will be something akin to Maslow's Hierarchy of Human Needs.\n"

    for inx,goal in enumerate(goals_init):
        for inxx,goalx in enumerate(goals_init):
            print str(inxx+1)+". "+goalx[0]

        subgoals = my_input("Which of the above goals feeds into or supports '"+goal[0]+"'? Goals can support more than one other goal. \n(List their indices separated by commas. Enter 'x' if there are none that feed into this goal.) \n: ",["6,3","x","2,6","6","x","4,5","3","7","5,2","5,2","4","4","7","1","3"][inx],test)
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

def add_actions(actions_init=[],test={"status":False,"phase":"0"}):
    cls()
    print "Begin listing actions that you do frequently or plan to do frequently.\nList them in whatever order they occur to you. \nDon't worry about precision, we'll sort that out later. Think of this as brainstorming.\nThese should be things you like doing and should be doing, or things you wish you didn't do.\n(Press Enter after each action. Enter X when done inputting actions. You'll have a chance to add more later.)"

    actions_count = len(actions_init)
    while True:
        actions_count += 1
        action = my_input(str(actions_count)+". ", "a"+str(actions_count) if actions_count<2 else "x",test)  # "action_ex"+str(actions_count) if actions_count<8 else "x"
        if(action.lower() == "x"): break
        actions_init.append([action,[]])
    return actions_init

def action_support(goals_init,actions_init,test={"status":False,"phase":"0"}):
    cls()
    print "Now trace how your actions support your goals.\n"

    for inx,goal in enumerate(goals_init):
        for inxx,actionx in enumerate(actions_init):
            print str(inxx+1)+". "+actionx[0]
        subactions = my_input("Which of the above actions feeds into or supports '"+goal[0]+"'? Actions can support more than one goal. \n(List their indices separated by commas. Enter 'x' if there are none that feed into this goal.) \n: ",["x","x","x","1","x","x","x","1","x","x","x","x","x"][inx],test)  # ["2,4,3","1,2","3","2","2,3","x","5,6","2,4,7","x","7,5","4,7"]
        if(subactions.lower() != "x"):
            goals_init[inx][2] = [int(kk)-1 for kk in subactions.split(",")]
        cls()
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

def network_digraph(goals,actions):
    G = nx.DiGraph()
    G.correlation={}
    edge_cmap = []

    for g in goals:
        children = g[1]
        for child in [goals[c] for c in children]:
            G.add_edge(child[0],g[0],weight=1.0)
            edge_cmap.append(1.0)
        action_children = g[2]
        for action_child in [actions[c] for c in action_children]:
            G.add_edge(action_child[0],g[0],weight=10.0)
            edge_cmap.append(0.5)
    nx.draw(G,with_labels=True,legend=True,alpha=0.5,edge_cmap=edge_cmap,layout=nx.spring_layout(G,k=0.001,iterations=200),arrows=True)
    #nx.draw(G,with_labels=True,legend=True,alpha=0.5,edge_cmap=edge_cmap,pos=nx.graphviz_layout(G),arrows=True)


def main_goal_input_loop(goals_init,actions_init,iteration,test={"status":False,"phase":"0"}):
    while True:
        iteration += 1
        goals_init = add_goals(goals_init,test=test)
        goals_init = goal_support(goals_init,test)
        actions_init = add_actions(actions_init,test)
        goals_init = action_support(goals_init,actions_init,test)

        pretty_tree(goals_init,actions_init)

        print "At this point, you may notice that you've left out some important goals or actions. We're going to iterate through the previous process again and add and connect goals where appropriate."
        save_files(goals_init,actions_init)
        iterate = my_input("Do you want to revise your goal/action structure? We recommend three iterations to be sure. (y/n)",["y","n","n"][iteration-1],test)
        if(iterate.lower() == 'n'): break
    return goals_init,actions_init,iteration

def main_loop_removal_loop(goals_init,test={"status":False,"phase":"0"}):
    global all_loops
    while True:
        all_loops = [] # global
        final_all_loops = find_loops(goals_init)

        if(len(final_all_loops) == 0):
            print "All loops have now been removed."
            break

        if(len(final_all_loops) > 0):
            loops_present = True

        if(loops_present):
            print "There were some dependency loops in your goal structure. At this point, you will choose which goal has the lowest precedence."
            print "Here is one of your loops:\n "
            val, idx = min((len(val),idx) for (idx,val) in enumerate(final_all_loops))
            print "\n ----> \n".join([str(kk+1)+". "+goals_init[gx][0] for kk,gx in enumerate(final_all_loops[idx])]),"\n"

            """
            lowest = goals_init[final_all_loops[idx][-2]]
            #print lowest
            print "The low-priority goal is inferred to be '"+lowest[0]+"' so this is where the loop will be cut."
            """
            lowest = my_input("Enter the number for the lowest-priority goal in this loop. This is where the loop will be broken. \n : ","1",test)

            goals_init[final_all_loops[idx][-2]][1].remove(final_all_loops[int(lowest)-1][-1])

            """
            print "In order to break this loop, please select which of those goals is the most fundamental or most important."
            for ii,g in enumerate(final_all_loops[idx][0:-1]):
                print str(ii+1)+". "+goals_init[g][0]
            """
    return goals_init

#pretty_tree(goals_init,actions_init)

def new_goal_structure(test):

    goals_init = []
    actions_init = []
    all_loops = []

    iteration = 0

    goals_init,actions_init,iteration = main_goal_input_loop(goals_init,actions_init,iteration,test)
    print "EXIT MAIN_GOAL_INPUT_LOOP"
    goals_init = main_loop_removal_loop(goals_init,test)
    #network_digraph(goals_init,actions_init)

    cls()
    print "This is an opportunity to notice incongruities between your stated goals and their interactions and potential contradictions, and how your day-to-day actions may not be serving your goals."
    print "Some things to consider: "
    print " - If you see a goal with no arrows pointing away from it, that can be considered a terminal goal. It you find that you have a terminal goal in your graph which is not very important to you, check and see what subordinate goals stem from that goal, and consider whether you should prune that whole section of your goal graph and eliminate the actions that serve it."

    """
    test["phase"] = 1
    goals_init,actions_init,iteration = main_goal_input_loop(goals_init,actions_init,iteration,test)

    """
    network_digraph(goals_init,actions_init)

    save_files(goals_init,actions_init)

def save_files(goals_init,actions_init):
    fg = open("goals.p","w")
    fa = open("actions.p","w")

    pickle.dump(goals_init,fg)
    pickle.dump(actions_init,fa)

def load_files(test):
    fg = open("goals.p","r")
    fa = open("actions.p","r")
    goals = pickle.load(fg)
    actions = pickle.load(fa)

    return goals,actions

if __name__ == '__main__':

    test = {"status":False,"phase":0}
    cls()
    main_menu(test)