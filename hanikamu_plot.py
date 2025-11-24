import numpy as np
import matplotlib.pyplot as plt

# ===設計変数===
l = 7
θ = 20
h = 13

# 外側円半径 設計変数から算出
# Rout = (1 + 2 * np.cos(np.radians(θ/2.0))) * l / (4 * np.sin(np.radians(θ/2.0)))

Rni = (l**2 - l**2 * np.cos(np.radians(180 - θ/2))) / (2 * (np.sin(np.radians(θ/2))**2)) - l**2/4

Rout = np.sqrt(Rni)

n = 360 / θ
n_int = int(n)   # ★追加：range と配列用に int 化

hanikamu = np.zeros((n_int, 4, 2))  # ★int版を使うだけ

# 基準台形
# 点A
hanikamu[0][0][0] = Rout
hanikamu[0][0][1] = l / 2.0

# 点B
hanikamu[0][1][0] = hanikamu[0][0][0]
hanikamu[0][1][1] = - hanikamu[0][0][1]

# 点C
hanikamu[0][2][0] = hanikamu[0][0][0] - h * np.cos(np.radians(θ/2.0))
hanikamu[0][2][1] = hanikamu[0][0][1] - h * np.sin(np.radians(θ/2.0))

# 点D
hanikamu[0][3][0] = hanikamu[0][2][0]
hanikamu[0][3][1] = - hanikamu[0][2][1]

for i in range(1, n_int):  # ★n_int を使う
    # ★インデントを4スペースに修正（中身はそのまま）
    hanikamu[i][0][0] = hanikamu[i-1][0][0] * np.cos(np.radians(θ)) - hanikamu[i-1][0][1] * np.sin(np.radians(θ))
    hanikamu[i][0][1] = hanikamu[i-1][0][0] * np.sin(np.radians(θ)) + hanikamu[i-1][0][1] * np.cos(np.radians(θ))

    hanikamu[i][1][0] = hanikamu[i-1][1][0] * np.cos(np.radians(θ)) - hanikamu[i-1][1][1] * np.sin(np.radians(θ))
    hanikamu[i][1][1] = hanikamu[i-1][1][0] * np.sin(np.radians(θ)) + hanikamu[i-1][1][1] * np.cos(np.radians(θ))

    hanikamu[i][2][0] = hanikamu[i-1][2][0] * np.cos(np.radians(θ)) - hanikamu[i-1][2][1] * np.sin(np.radians(θ))
    hanikamu[i][2][1] = hanikamu[i-1][2][0] * np.sin(np.radians(θ)) + hanikamu[i-1][2][1] * np.cos(np.radians(θ))

    hanikamu[i][3][0] = hanikamu[i-1][3][0] * np.cos(np.radians(θ)) - hanikamu[i-1][3][1] * np.sin(np.radians(θ))
    hanikamu[i][3][1] = hanikamu[i-1][3][0] * np.sin(np.radians(θ)) + hanikamu[i-1][3][1] * np.cos(np.radians(θ))

order = [0, 1, 3, 2, 0]

for i in range(0, n_int):  # ★n_int を使う
    pls = hanikamu[i][order]
    plt.plot(pls[:,0], pls[:, 1], "k-", lw=0.8)  # ★pts → pls に修正

# ===== 外周・内周を“角度順”で一周つなぐ =====

# 外側の2頂点（A,B）を全部集める
outer = np.vstack([hanikamu[:,0,:], hanikamu[:,1,:]])   # shape (2n,2)
ang_outer = np.arctan2(outer[:,1], outer[:,0])
outer_sorted = outer[np.argsort(ang_outer)]
outer_sorted = np.vstack([outer_sorted, outer_sorted[0]])  # 閉じる
plt.plot(outer_sorted[:,0], outer_sorted[:,1], "k-", lw=0.8)

# 内側の2頂点（C,D）を全部集める
inner = np.vstack([hanikamu[:,2,:], hanikamu[:,3,:]])   # shape (2n,2)
ang_inner = np.arctan2(inner[:,1], inner[:,0])
inner_sorted = inner[np.argsort(ang_inner)]
inner_sorted = np.vstack([inner_sorted, inner_sorted[0]])  # 閉じる
plt.plot(inner_sorted[:,0], inner_sorted[:,1], "k-", lw=0.8)

plt.gca().set_aspect("equal", adjustable="box")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Trapezoids arranged every θ degrees")
plt.grid(True)

# ★PDF保存（余白を詰めて保存）
plt.savefig("hanikamu.pdf", bbox_inches="tight")

plt.show()
