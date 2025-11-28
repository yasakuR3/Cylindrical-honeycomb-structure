import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():
    # ===設計変数===
    l = 10
    θ = 30
    h = 13
    a = 120  # 基本固定

    t = 1.0 # 厚さ
 
    # === 外側円半径 Rout を計算 ===
    term1 = l**2 + l**2 * np.cos(np.radians(180 - a))**2
    term2 = 2 * l**2 * np.cos(np.radians(180 - a)) * np.cos(np.radians(180 - θ/2))
    denominator = 4 * (np.sin(np.radians(θ/2))**2)

    Rni = (term1 - term2) / denominator - (l**2 / 4)
    Rout = np.sqrt(Rni)

    print(f"計算された外半径 Rout: {Rout:.4f}")

    # === 周方向分割数 ===
    n = 360 / θ
    n_int = int(n)

    # hanikamu[h, i, j, k]
    #   h : 台形の厚さを考慮　(0, 1)
    #   i : 周方向インデックス (0 ～ n_int-1)
    #   j : 台形の頂点 (0:A, 1:B, 2:C, 3:D)
    #   k : 座標 (0:x, 1:y, 2:z)
    hanikamu = np.zeros((2, n_int, 4, 3))

    # === 基準台形 (i = 0) ===
    # 点A
    hanikamu[0][0][0][0] = Rout
    hanikamu[0][0][0][1] = l / 2.0
    hanikamu[0][0][0][2] = l * np.sin(np.radians(180 - a))  # z座標

    # 点B
    hanikamu[0][0][1][0] = hanikamu[0][0][0][0]
    hanikamu[0][0][1][1] = -hanikamu[0][0][0][1]
    hanikamu[0][0][1][2] = hanikamu[0][0][0][2]

    # 点C
    hanikamu[0][0][2][0] = hanikamu[0][0][0][0] - h * np.cos(np.radians(θ/2.0))
    hanikamu[0][0][2][1] = hanikamu[0][0][0][1] - h * np.sin(np.radians(θ/2.0))
    hanikamu[0][0][2][2] = hanikamu[0][0][0][2]

    # 点D
    hanikamu[0][0][3][0] = hanikamu[0][0][2][0]
    hanikamu[0][0][3][1] = -hanikamu[0][0][2][1]
    hanikamu[0][0][3][2] = hanikamu[0][0][0][2]

    # 基準台形の厚さを考慮
    # 点A_1
    hanikamu[1][0][0][0] = hanikamu[0][0][0][0]
    hanikamu[1][0][0][1] = hanikamu[0][0][0][1]
    hanikamu[1][0][0][2] = hanikamu[0][0][0][2] + t

    # 点B_1
    hanikamu[1][0][1][0] = hanikamu[0][0][1][0]
    hanikamu[1][0][1][1] = hanikamu[0][0][1][1]
    hanikamu[1][0][1][2] = hanikamu[0][0][1][2] + t

    # 点C_1
    hanikamu[1][0][2][0] = hanikamu[0][0][2][0]
    hanikamu[1][0][2][1] = hanikamu[0][0][2][1]
    hanikamu[1][0][2][2] = hanikamu[0][0][2][2] + t

    # 点D_1
    hanikamu[1][0][3][0] = hanikamu[0][0][3][0]
    hanikamu[1][0][3][1] = hanikamu[0][0][3][1]
    hanikamu[1][0][3][2] = hanikamu[0][0][3][2] + t


    # === 回転して全周に並べる ===
    cos_theta = np.cos(np.radians(θ))
    sin_theta = np.sin(np.radians(θ))

     for i in range(1, n_int):
        for j in range(4):
            x_prev = hanikamu[0][i-1][j][0]
            y_prev = hanikamu[0][i-1][j][1]

            hanikamu[0][i][j][0] = x_prev * cos_theta - y_prev * sin_theta
            hanikamu[0][i][j][1] = x_prev * sin_theta + y_prev * cos_theta

            hanikamu[1][i][j][0] = x_prev * cos_theta - y_prev * sin_theta
            hanikamu[1][i][j][1] = x_prev * sin_theta + y_prev * cos_theta

        # zは 1つおきに 0 / 基準高さ を切り替え
        if i % 2 == 1:
            hanikamu[0, i, j, 2] = 0
            hanikamu[1, i, j, 2] = t

        else:
            hanikamu[0, i, j, 2] = hanikamu[0, 0, 0, 2]
            hanikamu[1, i, j, 2] = hanikamu[0, 0, 0, 2] + t
    
    # 法線ベクトルの求め方

    bekutoru[0, 0] = hanikamu[0, 0, 2, 0] - hanikamu[0, 0, 0, 0]
    bekutoru[0, 1] = hanikamu[0, 0, 2, 1] - hanikamu[0, 0, 0, 1]
    bekutoru[0, 2] = hanikamu[0, 0, 2, 2] - hanikamu[0, 0, 0, 2]

    bekutoru[1, 0] = hanikamu[0, 1, 1, 0] - hanikamu[0, 0, 0, 0]
    bekutoru[1, 1] = hanikamu[0, 1, 1, 1] - hanikamu[0, 0, 0, 1]
    bekutoru[1, 2] = hanikamu[0, 1, 1, 2] - hanikamu[0, 0, 0, 2]

    hosen[0, 0] = bekutoru[0, 1] * bekutoru[1, 2] - bekutoru[0, 2] * bekutoru[1, 1]
    hosen[0, 1] = bekutoru[0, 2] * bekutoru[1, 0] - bekutoru[0, 0] * bekutoru[1, 2]
    hosen[0, 2] = bekutoru[0, 0] * bekutoru[1, 1] - bekutoru[0, 1] * bekutoru[1, 0]


    # 媒介変数m 
    m = t / np.sqrt(hosen[0, 0] ** 2 + hosen[0, 1] ** 2 + hosen[0, 2] ** 2)

    # 新点A

    hosen[1, 0] = hanikamu[0, 0, 0, 0] + m * hosen[0, 0]
    hosen[1, 1] = hanikamu[0, 0, 0, 1] + m * hosen[0, 1]
    hosen[1, 2] = hanikamu[0, 0, 0, 2] + m * hosen[0, 2]

    hosen[2, 0] = hanikamu[0, 1, 1, 0] + m * hosen[0, 0]
    hosen[2, 1] = hanikamu[0, 1, 1, 1] + m * hosen[0, 1]
    hosen[2, 2] = hanikamu[0, 1, 1, 2] + m * hosen[0, 2]

    koten[0, 0] = hosen[1, 0] - hosen[2, 0]
    koten[0, 1] = hosen[1, 1] - hosen[2, 1]
    koten[0, 2] = hosen[1, 2] - hosen[2, 2]

    koten[1, 0] = hanikamu[0, 0, 0, 0] - hanikamu[0, 0, 1, 0]
    koten[1, 1] = hanikamu[0, 0, 0, 1] - hanikamu[0, 0, 1, 1]
    koten[1, 2] = hanikamu[0, 0, 0, 2] - hanikamu[0, 0, 1, 2]

    w[0] = hosen[2, 0] - hanikamu[0, 0, 1, 0]
    w[1] = hosen[2, 1] - hanikamu[0, 0, 1, 1]
    w[2] = hosen[2, 2] - hanikamu[0, 0, 1, 2]

    # a・a
    A = koten[0, 0] ** 2 + koten[0, 1] ** 2 + koten[0 , 2] ** 2

    # a・b
    B = koten[0, 0] * koten[1, 0] + koten[0, 1] * koten[1, 1] + koten[0, 2] * koten[1, 2]

    # b・b
    C = koten[1, 0] ** 2 + koten[1, 1] ** 2 + koten[1, 2] ** 2

    # a・w
    D = koten[0, 0] * w[0] + koten[0, 1] * w[1] + koten[0, 2] * w[2]

    # b・w
    E = koten[1, 0] * w[0] + koten[1, 1] * w[1] + koten[1, 2] * w[2]

    p = (B * E - C * D) / (A * C - B**2)

    k = (A * E - B * D) / (A * C - B**2)

    saitan[0, 0] = hosen[2, 0] + p * koten[0, 0]
    saitan[0, 1] = hosen[2, 1] + p * koten[0, 1]
    saitan[0, 2] = hosen[2, 2] + p * koten[0, 2]

    saitan[1, 0] = hanikamu[0, 0, 1, 0] + k * koten[1, 0]
    saitan[1, 1] = hanikamu[0, 0, 1, 1] + k * koten[1, 1]
    saitan[1, 2] = hanikamu[0, 0, 1, 2] + k * koten[1, 2]

    # 新点B

    hosen2[0, 0] = hanikamu[0, 0, 2, 0] + m * hosen[0, 0]
    hosen2[0, 1] = hanikamu[0, 0, 2, 1] + m * hosen[0, 1]
    hosen2[0, 2] = hanikamu[0, 0, 2, 2] + m * hosen[0, 2]

    hosen2[1, 0] = hanikamu[0, 1, 3, 1] + m * hosen[0, 0]
    hosen2[1, 1] = hanikamu[0, 1, 3, 2] + m * hosen[0, 1]
    hosen2[1, 2] = hanikamu[0, 1, 3, 3] + m * hosen[0, 2]

    koten2[0, 0] = hosen2[0, 0] - hosen2[1, 0]
    koten2[0, 1] = hosen2[0, 1] - hosen2[1, 1]
    koten2[0, 2] = hosen2[0, 2] - hosen2[1, 2]

    koten2[1, 0] = hanikamu[0, 0, 2, 0] - hanikamu[0, 0, 3, 0]
    koten2[1, 1] = hanikamu[0, 0, 2, 1] - hanikamu[0, 0, 3, 1]
    koten2[1, 2] = hanikamu[0, 0, 2, 2] - hanikamu[0, 0, 3, 2]

    w2[0] = hosen2[1, 0] - hanikamu[0, 0, 3, 0]
    w2[1] = hosen2[1, 1] - hanikamu[0, 0, 3, 1]
    w2[2] = hosen2[1, 2] - hanikamu[0, 0, 3, 2]

    A2 = koten2[0, 0] ** 2 + koten2[0, 1] ** 2 + koten[0, 2] ** 2

    B2 = koten2[0, 0] * koten2[1, 0] + koten2[0, 1] * koten2[1, 1] + koten2[0, 2] * koten2[1, 2]

    C2 = koten2[1, 0] ** 2 + koten2[1, 1] ** 2 + koten2[1, 2] ** 2

    D2 = koten2[0, 0] * w2[0] + koten2[0, 1] * w2[1] + koten2[0, 2] * w2[2]

    E2 = koten2[1, 0] * w2[0] + koten2[1, 1] * w2[1] + koten2[1, 2] * w2[2]

    p2 = (B2 * E2 - C2 * D2) / (A2 * C2 - B2 ** 2)

    k2 = (A2 * E2 - B2 * D2) / (A2 * C2 - B2 ** 2)

    saitan2[0, 0] = hosen2[1, 0] + p2 * koten2[0, 0]
    saitan2[0, 1] = hosen2[1, 1] + p2 * koten2[0, 1]
    saitan2[0, 2] = hosen2[1, 2] + p2 * koten2[0, 2]

    saitan2[1, 0] = hanikamu[0, 0, 3, 0] + k2 * koten2[1, 0]
    saitan2[1, 1] = hanikamu[0, 0, 3, 1] + k2 * koten2[1, 1]
    saitan2[1, 2] = hanikamu[0, 0, 3, 2] + k2 * koten2[1, 2]

    # 新点C

    koten3[0, 0] = hosen[1, 0] - hosen[2, 0]
    koten3[0, 1] = hosen[1, 1] - hosen[2, 1]
    koten3[0, 2] = hosen[1, 2] - hosen[2, 2]

    koten3[1, 0] = hanikamu[1, 1, 0, 0] - hanikamu[1, 1, 1, 0]
    koten3[1, 1] = hanikamu[1, 1, 0, 1] - hanikamu[1, 1, 1, 1]
    koten3[1, 2] = hanikamu[1, 1, 0, 2] - hanikamu[1, 1, 1, 2]

    w3[0] = hosen[2, 0] - hanikamu[1, 1, 1, 0]
    w3[1] = hosen[2, 1] - hanikamu[1, 1, 1, 1]
    w3[2] = hosen[2, 2] - hanikamu[1, 1, 1, 2] 

    A3 = koten3[0, 0] ** 2 + koten3[0, 1] ** 2 + koten3[0, 2] ** 2

    B3 = koten3[0, 0] * koten3[1, 0] + koten3[0, 1] * koten3[1, 1] + koten3[0, 2] * koten3[1, 2]

    C3 = koten3[1, 0] ** 2 + koten3[1, 1] ** 2 + koten3[1, 2] ** 2

    D3 = koten3[0, 0] * w3[0] + koten3[0, 1] * w3[1] + koten3[0, 2] * w3[2]

    E3 = koten3[1, 0] * w3[0] + koten3[1, 1] * w3[1] + koten3[1, 2] * w3[2]

    p3 = (B3 * E3 - C3 * D3) / (A3 * C3 - B3 ** 2)

    k3 = (A3 * E3 - B3 * D3) / (A3 * C3 - B3 ** 2)

    saitan3[0, 0] = hosen[2, 0] + p3 * koten3[0, 0]
    saitan3[0, 1] = hosen[2, 1] + p3 * koten3[0, 1]
    saitan3[0, 2] = hosen[2, 2] + p3 * koten3[0, 2]

    saitan3[1, 0] = hanikamu[1, 1, 1, 0] + k3 * koten3[1, 0]
    saitan3[1, 1] = hanikamu[1, 1, 1, 1] + k3 * koten3[1, 1]
    saitan3[1, 2] = hanikamu[1, 1, 1, 2] + k3 * koten3[1, 2]

    # 新点D

    koten4[0, 0] =  hosen2[0, 0] - hosen2[1, 0]
    koten4[0, 1] =  hosen2[0, 1] - hosen2[1, 1]
    koten4[0, 2] =  hosen2[0, 2] - hosen2[1, 2]

    koten4[1, 0] = hanikamu[1, 1, 2, 0] - hanikamu[1, 1, 3, 0]
    koten4[1, 1] = hanikamu[1, 1, 2, 1] - hanikamu[1, 1, 3, 1]
    koten4[1, 2] = hanikamu[1, 1, 2, 2] - hanikamu[1, 1, 3, 2]

    w4[0] = hosen2[1, 0] - hanikamu[1, 1, 3, 0]
    w4[1] = hosen2[1, 1] - hanikamu[1, 1, 3, 1]
    w4[2] = hosen2[1, 2] - hanikamu[1, 1, 3, 2]

    A4 = koten4[0, 0] ** 2 + koten4[0, 1] ** 2 + koten4[0, 2] ** 2

    B4 = koten4[0, 0] * koten4[1, 0] + koten4[0, 1] * koten4[1, 1] + koten4[0, 2] * koten4[1, 2]

    C4 = koten4[1, 0] ** 2 + koten4[1, 1] ** 2 + koten4[1, 2] ** 2

    D4 = koten4[0, 0] * w4[0] + koten4[0, 1] * w4[1] + koten4[0, 2] * w4[2]

    E4 = koten4[1, 0] * w4[0] + koten4[1, 1] * w4[1] + koten4[1, 2] * w4[2]

    p4 = (B4 * E4 - C4 * D4) / (A4 * C4 - B4 ** 2)

    k4 = (A4 * E4 - B4 * D4) / (A4 * C4 - B4 ** 2)

    saitan4[0, 0] = hosen[1, 0] + p4 * koten4[0, 0]
    saitan4[0, 1] = hosen[1, 1] + p4 * koten4[0, 1]
    saitan4[0, 2] = hosen[1, 2] + p4 * koten4[0, 2]

    saitan4[1, 0] = hanikamu[1, 1, 3, 0] + k4 * koten4[1, 0]
    saitan4[1, 1] = hanikamu[1, 1, 3, 1] + k4 * koten4[1, 1]
    saitan4[1, 2] = hanikamu[1, 1, 3, 2] + k4 * koten4[1, 2]

    hanikamu[1, 0, 0, 0] = (saitan[0, 0] + saitan[1, 0]) / 2.0
    hanikamu[1, 0, 0, 1] = (saitan[0, 1] + saitan[1, 1]) / 2.0
    hanikamu[1, 0, 0, 2] = (saitan[0, 2] + saitan[1, 2]) / 2.0

    hanikamu[1, 0, 1, 0] = hanikamu[1, 0, 0, 0]
    hanikamu[1, 0, 1, 1] = -hanikamu[1, 0, 0, 1]
    hanikamu[1, 0, 1, 2] = hanikamu[1, 0, 0, 2]

    hanikamu[1, 0, 2, 0] = (saitan2[0, 0] + saitan2[1, 0]) / 2.0
    hanikamu[1, 0, 2, 1] = (saitan2[0, 1] + saitan2[1, 1]) / 2.0
    hanikamu[1, 0, 2, 2] = (saitan2[0, 2] + saitan2[1, 2]) / 2.0

    hanikamu[1, 0, 3, 0] = hanikamu[1, 0, 2, 0]
    hanikamu[1, 0, 3, 1] = -hanikamu[1, 0, 2, 1]
    hanikamu[1, 0, 3, 2] = hanikamu[1, 0, 2, 2]

    for i range(n_int)
















    

    # === 3D表示 ===
    points = hanikamu.reshape(-1, 3)
    xs = points[:, 0]
    ys = points[:, 1]
    zs = points[:, 2]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 点
    ax.scatter(xs, ys, zs, c='b', marker='o', s=20)

    # 台形の枠線（A-B-D-C-A）
    for i in range(n_int):
        quad = hanikamu[i]
        idx = [0, 1, 3, 2, 0]
        xq = quad[idx, 0]
        yq = quad[idx, 1]
        zq = quad[idx, 2]
        ax.plot(xq, yq, zq, linewidth=1.0)

    # === 台形同士を結ぶ線（ユーザー指定部分） ===
    # 書き方:
    #   (i1, j1, i2, j2)
    #   i*: 周方向インデックス 0～n_int-1
    #   j*: 頂点インデックス 0:A, 1:B, 2:C, 3:D
    connections = []

    connections += [
        # ここに好きな組み合わせを書いていく
        # 例: 0番台形のAと1番台形のAを結ぶ
        # (0, 0, 1, 0),
        # 例: 0番台形のCと1番台形のCを結ぶ
        # (0, 2, 1, 2),
        (i, 2, i+1, 3)
        for i in range(n_int-1)
    ]
    connections += [(n_int-1, 2, 0, 3)]

    connections += [
        (i, 0, i+1, 1)
        for i in range(n_int-1)
    ]

    connections += [(n_int-1, 0, 0, 1)]

    connections += [
        (i, 1, i, 2)
        for i in range(n_int)
    ]

    connections += [
        (i, 0, i+1, 3)
        for i in range(n_int-1)
    ]

    connections += [(n_int-1, 0, 0, 3)]


    for (i1, j1, i2, j2) in connections:
        p1 = hanikamu[i1, j1]  # [x, y, z]
        p2 = hanikamu[i2, j2]
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            [p1[2], p2[2]],
            linewidth=1.0
        )

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Cylindrical Honeycomb Mesh')

    # アスペクト比を揃える
    max_range = np.array([
        xs.max()-xs.min(),
        ys.max()-ys.min(),
        zs.max()-zs.min()
    ]).max() / 2.0
    mid_x = (xs.max()+xs.min()) * 0.5
    mid_y = (ys.max()+ys.min()) * 0.5
    mid_z = (zs.max()+zs.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
