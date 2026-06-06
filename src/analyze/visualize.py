import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

q1 = pd.read_csv('result/q1_valence.csv')
q2 = pd.read_csv('result/q2_tempo_duration.csv')
q3 = pd.read_csv('result/q3_acousticness.csv')

fig, axes = plt.subplots(3, 1, figsize=(10, 15))

axes[0].plot(q1['decade'], q1['avg_valence'], marker='o', color='steelblue', linewidth=2)
axes[0].set_title('Q1: 시대별 음악 감정(Valence) 변화', fontsize=13, fontweight='bold')
axes[0].set_xlabel('시대')
axes[0].set_ylabel('평균 Valence (0=우울, 1=행복)')
axes[0].set_xticks(q1['decade'])
axes[0].grid(alpha=0.3)

ax2 = axes[1]
ax2b = ax2.twinx()
ax2.bar(q2['decade'], q2['avg_duration_sec'], width=7, color='steelblue', alpha=0.6, label='곡 길이(초)')
ax2b.plot(q2['decade'], q2['avg_tempo'], marker='o', color='tomato', linewidth=2, label='템포(BPM)')
ax2.set_title('Q2: 시대별 평균 곡 길이 & 템포 변화', fontsize=13, fontweight='bold')
ax2.set_xlabel('시대')
ax2.set_ylabel('평균 곡 길이 (초)', color='steelblue')
ax2b.set_ylabel('평균 템포 (BPM)', color='tomato')
ax2.set_xticks(q2['decade'])
ax2.grid(alpha=0.3)

axes[2].plot(q3['decade'], q3['avg_acousticness'], marker='o', color='green', linewidth=2, label='어쿠스틱')
axes[2].plot(q3['decade'], q3['avg_energy'], marker='s', color='orange', linewidth=2, label='에너지')
axes[2].set_title('Q3: 시대별 어쿠스틱 vs 전자음악 변화', fontsize=13, fontweight='bold')
axes[2].set_xlabel('시대')
axes[2].set_ylabel('수치 (0~1)')
axes[2].set_xticks(q3['decade'])
axes[2].legend()
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('result/music_analysis.png', dpi=150, bbox_inches='tight')
print("Done!")
