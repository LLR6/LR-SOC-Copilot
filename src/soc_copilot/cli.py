import argparse,json,math,re,sys
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path

SEV={"info":1,"low":2,"medium":4,"high":7,"critical":10}
WORD=re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,}|[\u4e00-\u9fff]{2,}")

def ts(s):
 s=str(s).replace("Z","+00:00");d=datetime.fromisoformat(s)
 if d.tzinfo is None:d=d.replace(tzinfo=timezone.utc)
 return d.astimezone(timezone.utc)

def load_alerts(path):
 out=[]
 for n,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
  if not line.strip():continue
  try:a=json.loads(line);a["_time"]=ts(a["timestamp"]);a["_ref"]=f"{path.name}:L{n}";a["entities"]=sorted(set(map(str,a.get("entities",[]))));a["severity"]=str(a.get("severity","low")).lower()
  except (json.JSONDecodeError,KeyError,ValueError) as e:raise ValueError(f"{path}:{n}: {e}") from e
  out.append(a)
 return sorted(out,key=lambda x:x["_time"])

def correlate(alerts,window=900):
 parent=list(range(len(alerts)))
 def find(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 def union(a,b):
  a,b=find(a),find(b)
  if a!=b:parent[b]=a
 for i,a in enumerate(alerts):
  ea=set(a["entities"])
  for j in range(i+1,len(alerts)):
   b=alerts[j];delta=(b["_time"]-a["_time"]).total_seconds()
   if delta>window:break
   if ea & set(b["entities"]):union(i,j)
 groups={}
 for i,a in enumerate(alerts):groups.setdefault(find(i),[]).append(a)
 cases=[]
 for num,items in enumerate(sorted(groups.values(),key=lambda g:g[0]["_time"]),1):
  score=min(100,sum(SEV.get(x["severity"],2) for x in items)*5+len({x.get('rule','') for x in items})*3)
  links=[]
  for i,left in enumerate(items):
   for right in items[i+1:]:
    shared=sorted(set(left["entities"]) & set(right["entities"]))
    delta=int((right["_time"]-left["_time"]).total_seconds())
    if shared and 0<=delta<=window:
     links.append({"left":left["_ref"],"right":right["_ref"],"shared_entities":shared,"delta_seconds":delta})
  cases.append({"id":f"CASE-{num:03d}","score":score,"start":items[0]["_time"].isoformat().replace("+00:00","Z"),"end":items[-1]["_time"].isoformat().replace("+00:00","Z"),"entities":sorted(set(y for x in items for y in x["entities"])),"correlation_edges":links,"alerts":items})
 return sorted(cases,key=lambda x:(-x["score"],x["start"]))

def chunks(folder):
 out=[]
 for p in sorted(folder.glob("*.md")):
  for i,text in enumerate(re.split(r"\n(?=##?\s)",p.read_text(encoding="utf-8"))):
   if text.strip():out.append({"ref":f"{p.name}#chunk-{i+1}","text":text.strip()})
 return out

def tokens(text):return Counter(x.lower() for x in WORD.findall(text))
def retrieve(query,docs,k=3):
 q=tokens(query);scored=[]
 for d in docs:
  v=tokens(d["text"]);dot=sum(q[x]*v[x] for x in q);den=math.sqrt(sum(x*x for x in q.values())*sum(x*x for x in v.values()))
  scored.append((dot/den if den else 0,d))
 return [{"ref":d["ref"],"score":round(s,4),"excerpt":d["text"][:420]} for s,d in sorted(scored,key=lambda x:-x[0])[:k] if s>0]

def evidence_coverage(evidence):
 if not evidence:return {"complete":0,"total":0,"ratio":0.0}
 complete=sum(bool(x.get("source") and x.get("timestamp") and x.get("rule") and x.get("entities")) for x in evidence)
 return {"complete":complete,"total":len(evidence),"ratio":round(complete/len(evidence),4)}

def serialize_case(case,docs,top_k=3):
 evidence=[]
 for i,a in enumerate(case["alerts"],1):
  evidence.append({"id":f"E{i}","source":a["_ref"],"timestamp":a["_time"].isoformat().replace("+00:00","Z"),"rule":a.get("rule","unknown"),"severity":a["severity"],"summary":a.get("summary",""),"entities":a["entities"]})
 query=" ".join(x["rule"]+" "+x["summary"]+" ".join(x["entities"]) for x in evidence)
 return {k:v for k,v in case.items() if k!="alerts"}|{"evidence":evidence,"evidence_coverage":evidence_coverage(evidence),"runbooks":retrieve(query,docs,top_k)}

def markdown(cases):
 rows=["# LR SOC Copilot · Investigation Brief","",f"Cases: {len(cases)}","","> Every claim below points to source evidence. Scores are triage heuristics, not incident verdicts.",""]
 for c in cases:
  rows += [f"## {c['id']} · score {c['score']}","",f"时间：`{c['start']}` → `{c['end']}`",f"实体：{', '.join(f'`{x}`' for x in c['entities'])}","","### Evidence",""]
  for e in c["evidence"]:rows.append(f"- **[{e['id']}]** `{e['timestamp']}` · {e['severity'].upper()} · {e['rule']} · {e['summary']} (`{e['source']}`)")
  coverage=c.get("evidence_coverage",{})
  rows += ["",f"Evidence coverage: **{coverage.get('complete',0)}/{coverage.get('total',0)}** ({coverage.get('ratio',0):.0%})","","### Correlation rationale",""]
  edges=c.get("correlation_edges",[])
  rows += [f"- {x['left']} ↔ {x['right']} · shared {', '.join(x['shared_entities'])} · Δ {x['delta_seconds']}s" for x in edges] or ["- Single-alert case; no correlation edge."]
  rows += ["","### Suggested runbooks",""]
  rows += [f"- `{x['ref']}` · similarity {x['score']} · {x['excerpt'].splitlines()[0]}" for x in c["runbooks"]] or ["- No matching local runbook."]
  rows += ["","### Investigator checklist","","- [ ] Validate the earliest evidence against the source system.","- [ ] Confirm whether the shared entities belong to one activity.","- [ ] Record benign explanations and contradictory evidence.",""]
 return "\n".join(rows)

def main(argv=None):
 p=argparse.ArgumentParser(description="Correlate alerts and retrieve evidence-grounded local runbooks")
 p.add_argument("alerts",type=Path);p.add_argument("--runbooks",type=Path,default=Path("runbooks"));p.add_argument("--window",type=int,default=900);p.add_argument("--format",choices=("markdown","json"),default="markdown");p.add_argument("--output",type=Path)
 p.add_argument("--top-runbooks",type=int,default=3,help="maximum local runbook chunks per case")
 p.add_argument("--min-score",type=int,default=0,help="only emit cases at or above this triage score")
 a=p.parse_args(argv)
 if a.top_runbooks<0:p.error("--top-runbooks must be >= 0")
 if not 0<=a.min_score<=100:p.error("--min-score must be between 0 and 100")
 try:
  docs=chunks(a.runbooks)
  result=[serialize_case(x,docs,a.top_runbooks) for x in correlate(load_alerts(a.alerts),a.window) if x["score"]>=a.min_score]
 except (ValueError,OSError) as e:p.error(str(e))
 text=json.dumps({"schema":"lr-soc-copilot/v1","cases":result},ensure_ascii=False,indent=2)+"\n" if a.format=="json" else markdown(result)+"\n"
 a.output.write_text(text,encoding="utf-8") if a.output else print(text,end="");return 0
if __name__=="__main__":sys.exit(main())
