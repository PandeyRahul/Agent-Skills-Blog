import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BG="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; MUTED="#a3a29c"; GRID="#e6e5e0"
BLUE="#2a78d6"; ORANGE="#eb6834"; AQUA="#1baf7a"; YEL="#eda100"; VIO="#6250d6"
plt.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"figure.facecolor":BG,"axes.facecolor":BG})
def box(ax,x,y,w,h,c,r=0.12,ec=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",fc=c,ec=ec or BG,lw=2))
def arrow(ax,x1,y1,x2,y2):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="-|>",color=INK2,lw=1.8))
MONO="DejaVu Sans Mono"

# 1 HERO
fig,ax=plt.subplots(figsize=(14,7)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,7)
ax.text(0.6,6.1,"Teach your AI agent a new trick",fontsize=34,weight="bold")
ax.text(0.6,5.4,"with one folder and one Markdown file — Agent Skills, now an open standard",fontsize=17,color=INK2)
box(ax,0.6,0.7,5.6,3.9,"#f1f0ec",r=0.25)
for i,(t,c) in enumerate([("medium-post-checker/",INK),("    SKILL.md",BLUE),("    scripts/check_post.py",ORANGE),("    references/checklist.md",AQUA)]):
    ax.text(0.95,4.0-i*0.75,t,fontsize=15,family=MONO,color=c,weight="bold" if i<2 else None)
arrow(ax,6.5,2.65,7.6,2.65)
for i,(t,c) in enumerate([("Pi",VIO),("Claude Code",ORANGE),("Your own Python agent",BLUE)]):
    box(ax,7.9,3.55-i*1.25,5.4,0.95,c); ax.text(10.6,4.02-i*1.25,t,ha="center",va="center",color="white",fontsize=16,weight="bold")
ax.text(7.9,0.55,"same folder, works everywhere that supports the standard",fontsize=12,color=INK2)
fig.savefig("img/01_hero.png",dpi=110,bbox_inches="tight",pad_inches=0.3); plt.close()

# 2 ANATOMY
fig,ax=plt.subplots(figsize=(14,6.2)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(-0.6,5.6)
ax.text(0.3,5.15,"Anatomy of a skill",fontsize=20,weight="bold")
rows=[("medium-post-checker/","the folder name = the skill name",INK,True),
      ("├── SKILL.md","required: YAML frontmatter (name, description) + instructions",BLUE,True),
      ("├── scripts/check_post.py","optional: code the agent can run",ORANGE,False),
      ("└── references/medium-checklist.md","optional: extra docs, read only when needed",AQUA,False)]
for i,(a,b,c,bold) in enumerate(rows):
    y=4.2-i*0.85
    ax.text(0.5,y,a,fontsize=15,family=MONO,color=c,weight="bold" if bold else None,va="center")
    ax.text(7.4,y,b,fontsize=13,color=INK2,va="center")
box(ax,0.5,-0.45,13,1.15,"#f1f0ec",r=0.12)
ax.text(0.8,0.13,"---\nname: medium-post-checker\ndescription: Reviews a Markdown blog draft … Use when the user asks to review a post …\n---",fontsize=11,family=MONO,va="center",color=INK)
fig.savefig("img/02_anatomy.png",dpi=110,bbox_inches="tight",pad_inches=0.3); plt.close()

# 3 PROGRESSIVE DISCLOSURE
fig,ax=plt.subplots(figsize=(14,5.8)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,5.8)
ax.text(0.3,5.35,"Progressive disclosure: the agent only reads what it needs",fontsize=20,weight="bold")
lv=[("1. At startup","name + description of EVERY skill","~100 tokens each",BLUE,5.0),
    ("2. Skill matches the task","full SKILL.md body","under ~5,000 tokens recommended",ORANGE,7.4),
    ("3. While working","scripts/, references/, assets/","only the files it opens",AQUA,10.0)]
for i,(a,b,c,col,w) in enumerate(lv):
    y=3.9-i*1.45
    box(ax,0.3,y,w,1.0,col); ax.text(0.55,y+0.62,a,color="white",fontsize=14,weight="bold"); ax.text(0.55,y+0.25,b,color="white",fontsize=12)
    ax.text(w+0.6,y+0.5,c,fontsize=13,color=INK2,va="center")
ax.text(0.3,0.15,"So you can install 50 skills and your context window barely notices.",fontsize=12.5,color=INK2,style="italic")
fig.savefig("img/03_progressive.png",dpi=110,bbox_inches="tight",pad_inches=0.3); plt.close()

# 4 MINI AGENT FLOW
fig,ax=plt.subplots(figsize=(15,4.6)); ax.axis("off"); ax.set_xlim(0,15); ax.set_ylim(0,4.6)
ax.text(0.2,4.2,"What my 100-line agent does with one request",fontsize=20,weight="bold")
steps=[("You","“Review my\ndraft.md”",MUTED),("Local LLM\n(Ollama)","sees skill\ndescriptions",BLUE),
       ("load_skill()","reads full\nSKILL.md",ORANGE),("run_script()","check_post.py\n→ JSON score",AQUA),("Answer","fixes + score\n+ tags",VIO)]
for i,(a,b,c) in enumerate(steps):
    x=0.2+i*3.0
    box(ax,x,1.3,2.5,1.9,c); ax.text(x+1.25,2.65,a,ha="center",va="center",color="white",fontsize=13.5,weight="bold")
    ax.text(x+1.25,1.85,b,ha="center",va="center",color="white",fontsize=11.5)
    if i<4: arrow(ax,x+2.55,2.25,x+2.95,2.25)
ax.text(0.2,0.6,"Everything runs on my machine. The model decides when to load the skill, my code just gives it the tools.",fontsize=12,color=INK2)
fig.savefig("img/04_agent_flow.png",dpi=110,bbox_inches="tight",pad_inches=0.3); plt.close()
print("ok")
