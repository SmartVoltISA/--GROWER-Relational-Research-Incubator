from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
import math
import random

N=100; STEPS=5000; SEEDS=range(1001,1021)
WORLD_SIZE=1.0; RADIUS=0.16; CELL_COUNT=10
INITIAL_RESOURCE=10.0; CAPACITY=20.0
SCARCE_REPLENISHMENT=0.025; ABUNDANT_REPLENISHMENT=0.25
CONSUMPTION=0.035; MEMORY_LENGTH=20
INITIAL_WEIGHT=0.10; REINFORCE=0.01; DECAY=0.002

@dataclass
class Agent:
    x: float; y: float; resource: float=INITIAL_RESOURCE; state:int=0
    memory: deque[int]=field(default_factory=lambda:deque(maxlen=MEMORY_LENGTH))
    inertia: float=0.25; alive:bool=True; lifetime:int=0

def dist(a,b): return math.hypot(a.x-b.x,a.y-b.y)

def pairs(agents):
    alive=[i for i,a in enumerate(agents) if a.alive]
    return [(i,j) for p,i in enumerate(alive) for j in alive[p+1:] if dist(agents[i],agents[j])<=RADIUS]

def transfer(a,b):
    if a.resource>b.resource: donor,receiver=a,b
    else: donor,receiver=b,a
    surplus=max(0.0,donor.resource-CAPACITY/2)
    need=max(0.0,CAPACITY/2-receiver.resource)
    return min(0.05,surplus*0.05,need*0.05)

def resource_field(seed, abundant=False):
    rng=random.Random(seed+7919)
    base=ABUNDANT_REPLENISHMENT if abundant else SCARCE_REPLENISHMENT
    return [[base*rng.uniform(0.5,1.5) for _ in range(CELL_COUNT)] for _ in range(CELL_COUNT)]

def run(condition,seed):
    rng=random.Random(seed)
    agents=[Agent(rng.random(),rng.random()) for _ in range(N)]
    field=resource_field(seed,condition=="ABUNDANT_RESOURCE")
    edges={}; checkpoint_edges=None; transfers={}
    survival=[]; giant=[]; diversity=[]; interaction_counts=[]
    for t in range(STEPS):
        alive=[i for i,a in enumerate(agents) if a.alive]
        if not alive:
            survival.append(0.0); giant.append(0.0); diversity.append(0.0); interaction_counts.append(0); continue
        for i in alive:
            a=agents[i]
            a.x=min(1.0,max(0.0,a.x+rng.uniform(-0.03,0.03)))
            a.y=min(1.0,max(0.0,a.y+rng.uniform(-0.03,0.03)))
            cx=min(CELL_COUNT-1,int(a.x*CELL_COUNT)); cy=min(CELL_COUNT-1,int(a.y*CELL_COUNT))
            a.resource=min(CAPACITY,a.resource+field[cx][cy])
        ps=pairs(agents); touched=set(); interaction_counts.append(len(ps))
        for i,j in ps:
            e=(i,j); touched.add(e); old=edges.get(e,INITIAL_WEIGHT); edges[e]=old
            q=transfer(agents[i],agents[j])
            if q:
                if agents[i].resource>agents[j].resource:
                    agents[i].resource-=q; agents[j].resource+=q
                else:
                    agents[j].resource-=q; agents[i].resource+=q
                transfers[e]=transfers.get(e,0.0)+q
            if condition not in ("NO_FEEDBACK","RANDOM"):
                if agents[i].resource<agents[j].resource: agents[i].state=agents[j].state
                elif agents[j].resource<agents[i].resource: agents[j].state=agents[i].state
            if condition=="FULL" and q>0: edges[e]=min(1.0,old+REINFORCE)
        for i in alive:
            a=agents[i]; impulse=max(0.0,1.0-a.resource/CAPACITY); desired=a.state
            if condition not in ("NO_MEMORY","RANDOM") and a.memory:
                m=sum(a.memory)/len(a.memory); desired=1 if m>0.5 else 0 if m<0.5 else desired
            if impulse>0.75 and rng.random()<0.5: desired=1-desired
            if rng.random()<a.inertia: desired=a.state
            a.state=desired
            if condition not in ("NO_MEMORY","RANDOM"): a.memory.append(a.state)
            a.resource-=CONSUMPTION+0.015*impulse; a.lifetime+=1
            if a.resource<=0: a.alive=False
        for e in list(edges):
            if e not in touched: edges[e]*=(1.0-DECAY)
            if edges[e]<0.05: del edges[e]
        if t==999: checkpoint_edges=set(edges)
        alive_now=[i for i,a in enumerate(agents) if a.alive]
        survival.append(len(alive_now)/N)
        adj={i:set() for i in alive_now}
        for u,v in edges:
            if u in adj and v in adj: adj[u].add(v); adj[v].add(u)
        unseen=set(adj); largest=0
        while unseen:
            root=unseen.pop(); stack=[root]; size=1
            while stack:
                u=stack.pop()
                for v in adj[u]:
                    if v in unseen: unseen.remove(v); stack.append(v); size+=1
            largest=max(largest,size)
        giant.append(largest/max(1,len(alive_now)))
        diversity.append(len(set(agents[i].state for i in alive_now))/2 if alive_now else 0.0)
    persistence=(len(checkpoint_edges & set(edges))/max(1,len(checkpoint_edges))) if checkpoint_edges else float('nan')
    total=sum(transfers.values()); concentration=sum((v/total)**2 for v in transfers.values()) if total else 0.0
    return dict(condition=condition,seed=seed,final_survival=survival[-1],mean_survival=sum(survival)/STEPS,
                mean_persistence_duration=sum(a.lifetime for a in agents)/(N*STEPS),relation_persistence=persistence,
                giant_component_fraction=giant[-1],mean_giant_component_fraction=sum(giant)/STEPS,
                state_diversity_occupancy=sum(diversity)/STEPS,resource_flow_concentration=concentration,
                edge_count=len(edges),mean_degree=2*len(edges)/max(1,len([a for a in agents if a.alive])),
                mean_interactions=sum(interaction_counts)/STEPS)

if __name__=="__main__":
    fields=["condition","seed","final_survival","mean_survival","mean_persistence_duration","relation_persistence",
            "giant_component_fraction","mean_giant_component_fraction","state_diversity_occupancy",
            "resource_flow_concentration","edge_count","mean_degree","mean_interactions"]
    print(','.join(fields))
    for c in ["RANDOM","NO_MEMORY","NO_FEEDBACK","ABUNDANT_RESOURCE","FULL"]:
        for s in SEEDS:
            r=run(c,s); print(','.join(str(r[k]) for k in fields))
