import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import trimesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

def build_mesh_from_indices(hanikamu, triangle_indices):
    vertices = []
    faces = []
    vertex_map = {} 

    for tri in triangle_indices:
        face = []
        for key in tri:
            if key not in vertex_map:
                h_idx, i_idx, j_idx = key
                x, y, z = hanikamu[h_idx, i_idx, j_idx, :]
                vertex_map[key] = len(vertices)
                vertices.append([x, y, z])
            face.append(vertex_map[key])
        faces.append(face)

    vertices = np.array(vertices, dtype=float)
    faces = np.array(faces, dtype=int)

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    return mesh

def main():
    # ===設計変数===
    l = 7
    θ = 20
    h = 10
    t = 1.0 # 厚さ

    a = 120  # 基本固定
 
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
    #   h : 台形の厚さを考慮　(0, 1, 2)
    #   i : 周方向インデックス (0 ～ n_int-1)
    #   j : 台形の頂点 (0:A, 1:B, 2:C, 3:D)
    #   k : 座標 (0:x, 1:y, 2:z)
    hanikamu = np.zeros((3, n_int, 4, 3))

    # === 基準台形 (i = 0) ===
    # 点A
    hanikamu[0, 0, 0, 0] = Rout
    hanikamu[0, 0, 0, 1] = l / 2.0
    hanikamu[0, 0, 0, 2] = l * np.sin(np.radians(180 - a))  # z座標

    # 点B x軸で対称
    hanikamu[0, 0, 1, 0] = hanikamu[0, 0, 0, 0]
    hanikamu[0, 0, 1, 1] = - hanikamu[0, 0, 0, 1]
    hanikamu[0, 0, 1, 2] = hanikamu[0, 0, 0, 2]

    # 点C
    hanikamu[0, 0, 2, 0] = hanikamu[0, 0, 0, 0] - h * np.cos(np.radians(θ/2.0))
    hanikamu[0, 0, 2, 1] = hanikamu[0, 0, 0, 1] - h * np.sin(np.radians(θ/2.0))
    hanikamu[0, 0, 2, 2] = hanikamu[0, 0, 0, 2]

    # 点D x軸で対称
    hanikamu[0, 0, 3, 0] = hanikamu[0, 0, 2, 0]
    hanikamu[0, 0, 3, 1] = -hanikamu[0, 0, 2, 1]
    hanikamu[0, 0, 3, 2] = hanikamu[0, 0, 2, 2]

    # 基準台形の厚さを考慮　プラス方向
    # 点A_1
    hanikamu[1, 0, 0, 0] = hanikamu[0, 0, 0, 0] 
    hanikamu[1, 0, 0, 1] = hanikamu[0, 0, 0, 1] + (t / 2.0) * np.tan(np.radians((180-a)/2.0))
    hanikamu[1, 0, 0, 2] = hanikamu[0, 0, 0, 2] + (t / 2.0)

    # 点B_1 x軸で対称
    hanikamu[1, 0, 1, 0] = hanikamu[1, 0, 0, 0]
    hanikamu[1, 0, 1, 1] = -hanikamu[1, 0, 0, 1]
    hanikamu[1, 0, 1, 2] = hanikamu[1, 0, 0, 2]

    # 点C_1
    hanikamu[1, 0, 2, 0] = hanikamu[0, 0, 2, 0]
    hanikamu[1, 0, 2, 1] = hanikamu[0, 0, 2, 1] + (t / 2.0) * np.tan(np.radians((180-a)/2.0))
    hanikamu[1, 0, 2, 2] = hanikamu[0, 0, 2, 2] + (t / 2.0)

    # 点D_1 x軸で対称
    hanikamu[1, 0, 3, 0] = hanikamu[1, 0, 2, 0]
    hanikamu[1, 0, 3, 1] = -hanikamu[1, 0, 2, 1]
    hanikamu[1, 0, 3, 2] = hanikamu[1, 0, 2, 2]

    # 基準台形の厚さを考慮　マイナス方向
    # 点A_2
    hanikamu[2, 0, 0, 0] = hanikamu[0, 0, 0, 0]
    hanikamu[2, 0, 0, 1] = hanikamu[0, 0, 0, 1] - (t / 2.0) * np.tan(np.radians((180-a)/2.0))
    hanikamu[2, 0, 0, 2] = hanikamu[0, 0, 0, 2] - (t / 2.0)

    # 点B_2
    hanikamu[2, 0, 1, 0] = hanikamu[2, 0, 0, 0]
    hanikamu[2, 0, 1, 1] = -hanikamu[2, 0, 0, 1]
    hanikamu[2, 0, 1, 2] = hanikamu[2, 0, 0, 2]

    # 点C_2
    hanikamu[2, 0, 2, 0] = hanikamu[0, 0, 2, 0]
    hanikamu[2, 0, 2, 1] = hanikamu[0, 0, 2, 1] - (t / 2.0) * np.tan(np.radians((180-a)/2.0))
    hanikamu[2, 0, 2, 2] = hanikamu[0, 0, 2, 2] - (t / 2.0)

    # 点D_2
    hanikamu[2, 0, 3, 0] = hanikamu[2, 0, 2, 0]
    hanikamu[2, 0, 3, 1] = -hanikamu[2, 0, 2, 1]
    hanikamu[2, 0, 3, 2] = hanikamu[2, 0, 2, 2]

    # 厚さを考慮した2番目の台形 プラス方向
    team_x = hanikamu[1, 0, 0, 0] - hanikamu[1, 0, 2, 0]
    team_y = hanikamu[1, 0, 0, 1] - hanikamu[1, 0, 2, 1]

    kakudo = np.degrees(np.arctan2(team_y , team_x))

    h1 =  (hanikamu[1, 0, 1, 0] * np.cos(np.radians(2*θ)) - hanikamu[1, 0, 1, 1] * np.sin(np.radians(2*θ)))
    h2 = (hanikamu[1, 0, 3, 0] * np.cos(np.radians(2*θ)) - hanikamu[1, 0, 3, 1] * np.sin(np.radians(2*θ)))

    team2_x = h1 - h2

    h3 = (hanikamu[1, 0, 1, 0] * np.sin(np.radians(2*θ)) + hanikamu[1, 0, 1, 1] * np.cos(np.radians(2*θ)))
    h4 = (hanikamu[1, 0, 3, 0] * np.sin(np.radians(2*θ)) + hanikamu[1, 0, 3, 1] * np.cos(np.radians(2*θ)))

    team2_y = h3 - h4

    team_b = np.degrees(np.arctan2(team2_y , team2_x))

    hanikamu[1, 1, 0, 0] = (hanikamu[1, 0, 1, 0] * np.cos(np.radians(2*θ)) - hanikamu[1, 0, 1, 1] * np.sin(np.radians(2*θ))) + l * np.cos(np.radians(180-a)) * np.sin(np.radians(team_b))
    hanikamu[1, 1, 0, 1] = (hanikamu[1, 0, 1, 0] * np.sin(np.radians(2*θ)) + hanikamu[1, 0, 1, 1] * np.cos(np.radians(2*θ))) - l * np.cos(np.radians(180-a)) * np.cos(np.radians(team_b))
    hanikamu[1, 1, 0, 2] = (t / 2.0)

    hanikamu[1, 1, 1, 0] = hanikamu[1, 0, 0, 0] - l * np.cos(np.radians(180-a)) * np.sin(np.radians(kakudo))
    hanikamu[1, 1, 1, 1] = hanikamu[1, 0, 0, 1] + l * np.cos(np.radians(180-a)) * np.cos(np.radians(kakudo))
    hanikamu[1, 1, 1, 2] = (t / 2.0)

    hanikamu[1, 1, 2, 0] = (hanikamu[1, 0, 3, 0] * np.cos(np.radians(2*θ)) - hanikamu[1, 0, 3, 1] * np.sin(np.radians(2*θ))) + l * np.cos(np.radians(180-a)) * np.sin(np.radians(team_b))
    hanikamu[1, 1, 2, 1] = (hanikamu[1, 0, 3, 0] * np.sin(np.radians(2*θ)) + hanikamu[1, 0, 3, 1] * np.cos(np.radians(2*θ))) - l * np.cos(np.radians(180-a)) * np.cos(np.radians(team_b))
    hanikamu[1, 1, 2, 2] = (t / 2.0)

    hanikamu[1, 1, 3, 0] = hanikamu[1, 0, 2, 0] - l * np.cos(np.radians(180-a)) * np.sin(np.radians(kakudo))
    hanikamu[1, 1, 3, 1] = hanikamu[1, 0, 2, 1] + l * np.cos(np.radians(180-a)) * np.cos(np.radians(kakudo))
    hanikamu[1, 1, 3, 2] = (t / 2.0)

    # 厚さを考慮した2番目の台形 マイナス方向
    team3_x = hanikamu[2, 0, 0, 0] - hanikamu[2, 0, 2, 0]
    team3_y = hanikamu[2, 0, 0, 1] - hanikamu[2, 0, 2, 1]

    kakudo2 = np.degrees(np.arctan2(team3_y , team3_x))

    h5 =  (hanikamu[2, 0, 1, 0] * np.cos(np.radians(2*θ)) - hanikamu[2, 0, 1, 1] * np.sin(np.radians(2*θ)))
    h6 = (hanikamu[2, 0, 3, 0] * np.cos(np.radians(2*θ)) - hanikamu[2, 0, 3, 1] * np.sin(np.radians(2*θ)))

    team4_x = h5 - h6

    h7 = (hanikamu[2, 0, 1, 0] * np.sin(np.radians(2*θ)) + hanikamu[2, 0, 1, 1] * np.cos(np.radians(2*θ)))
    h8 = (hanikamu[2, 0, 3, 0] * np.sin(np.radians(2*θ)) + hanikamu[2, 0, 3, 1] * np.cos(np.radians(2*θ)))

    team4_y = h7 - h8

    team2_b = np.degrees(np.arctan2(team4_y , team4_x))

    hanikamu[2, 1, 0, 0] = (hanikamu[2, 0, 1, 0] * np.cos(np.radians(2*θ)) - hanikamu[2, 0, 1, 1] * np.sin(np.radians(2*θ))) + l * np.cos(np.radians(180-a)) * np.sin(np.radians(team2_b))
    hanikamu[2, 1, 0, 1] = (hanikamu[2, 0, 1, 0] * np.sin(np.radians(2*θ)) + hanikamu[2, 0, 1, 1] * np.cos(np.radians(2*θ))) - l * np.cos(np.radians(180-a)) * np.cos(np.radians(team2_b))
    hanikamu[2, 1, 0, 2] = -(t / 2.0)

    hanikamu[2, 1, 1, 0] = hanikamu[2, 0, 0, 0] - l * np.cos(np.radians(180-a)) * np.sin(np.radians(kakudo2))
    hanikamu[2, 1, 1, 1] = hanikamu[2, 0, 0, 1] + l * np.cos(np.radians(180-a)) * np.cos(np.radians(kakudo2))
    hanikamu[2, 1, 1, 2] = -(t / 2.0)

    hanikamu[2, 1, 2, 0] = (hanikamu[2, 0, 3, 0] * np.cos(np.radians(2*θ)) - hanikamu[2, 0, 3, 1] * np.sin(np.radians(2*θ))) + l * np.cos(np.radians(180-a)) * np.sin(np.radians(team2_b))
    hanikamu[2, 1, 2, 1] = (hanikamu[2, 0, 3, 0] * np.sin(np.radians(2*θ)) + hanikamu[2, 0, 3, 1] * np.cos(np.radians(2*θ))) - l * np.cos(np.radians(180-a)) * np.cos(np.radians(team2_b))
    hanikamu[2, 1, 2, 2] = -(t / 2.0)

    hanikamu[2, 1, 3, 0] = hanikamu[2, 0, 2, 0] - l * np.cos(np.radians(180-a)) * np.sin(np.radians(kakudo2))
    hanikamu[2, 1, 3, 1] = hanikamu[2, 0, 2, 1] + l * np.cos(np.radians(180-a)) * np.cos(np.radians(kakudo2))
    hanikamu[2, 1, 3, 2] = -(t / 2.0)

    # === 回転して全周に並べる ===
    cos_theta = np.cos(np.radians(θ))
    sin_theta = np.sin(np.radians(θ))

    for i in range(1, n_int):
        for j in range(4):
            x_prev = hanikamu[0, i-1, j, 0]
            y_prev = hanikamu[0, i-1, j, 1]

            hanikamu[0, i, j, 0] = x_prev * cos_theta - y_prev * sin_theta
            hanikamu[0, i, j, 1] = x_prev * sin_theta + y_prev * cos_theta

        # zは 1つおきに 0 / 基準高さ を切り替え
        if i % 2 == 1:
            hanikamu[0, i, :, 2] = 0
        else:
            hanikamu[0, i, :, 2] = hanikamu[0, 0, 0, 2]

    cos_theta2 = np.cos(np.radians(2*θ))
    sin_theta2 = np.sin(np.radians(2*θ))

    for i in range(2, n_int):
        if i % 2 == 0:
            for j in range(4):
                x_prev2 = hanikamu[1, i-2, j, 0]
                y_prev2 = hanikamu[1, i-2, j, 1]

                hanikamu[1, i, j, 0] = x_prev2 * cos_theta2 - y_prev2 * sin_theta2
                hanikamu[1, i, j, 1] = x_prev2 * sin_theta2 + y_prev2 * cos_theta2

                hanikamu[1, i, j, 2] = hanikamu[1, 0, 0, 2]

        else:
            for j in range(4):
                x_prev3 = hanikamu[1, i-2, j, 0]
                y_prev3 = hanikamu[1, i-2, j, 1]

                hanikamu[1, i, j, 0] = x_prev3 * cos_theta2 - y_prev3 * sin_theta2
                hanikamu[1, i, j, 1] = x_prev3 * sin_theta2 + y_prev3 * cos_theta2
 
                hanikamu[1, i, j, 2] = hanikamu[1, 1, 0, 2]

    for i in range(2, n_int):
        if i % 2 == 0:
            for j in range(4):
                x_prev2 = hanikamu[2, i-2, j, 0]
                y_prev2 = hanikamu[2, i-2, j, 1]

                hanikamu[2, i, j, 0] = x_prev2 * cos_theta2 - y_prev2 * sin_theta2
                hanikamu[2, i, j, 1] = x_prev2 * sin_theta2 + y_prev2 * cos_theta2

                hanikamu[2, i, j, 2] = hanikamu[2, 0, 0, 2]

        else:
            for j in range(4):
                x_prev3 = hanikamu[2, i-2, j, 0]
                y_prev3 = hanikamu[2, i-2, j, 1]

                hanikamu[2, i, j, 0] = x_prev3 * cos_theta2 - y_prev3 * sin_theta2
                hanikamu[2, i, j, 1] = x_prev3 * sin_theta2 + y_prev3 * cos_theta2
 
                hanikamu[2, i, j, 2] = hanikamu[2, 1, 0, 2]

    triangle_indices = []

    for i in range(0, n_int):

        triangle_indices.append(((2, i, 0), (2, i, 1), (2, i, 2)))
        triangle_indices.append(((2, i, 1), (2, i, 2), (2, i, 3)))

        triangle_indices.append(((1, i, 0), (1, i, 1), (1, i, 2)))
        triangle_indices.append(((1, i, 1), (1, i, 2), (1, i, 3)))

        if i != n_int-1:
            triangle_indices.append(((2, i, 0), (2, i, 2), (2, i+1, 3)))
            triangle_indices.append(((2, i, 0), (2, i+1, 1), (2, i+1, 3)))

            triangle_indices.append(((1, i, 0), (1, i, 2), (1, i+1, 3)))
            triangle_indices.append(((1, i, 0), (1, i+1, 1), (1, i+1, 3)))

        else:
            triangle_indices.append(((2, i, 0), (2, i, 2), (2, 0, 3)))
            triangle_indices.append(((2, i, 0), (2, 0, 1), (2, 0, 3)))

            triangle_indices.append(((1, i, 0), (1, i, 2), (1, 0, 3)))
            triangle_indices.append(((1, i, 0), (1, 0, 1), (1, 0, 3)))

        
        triangle_indices.append(((2, i, 0), (2, i, 1), (1, i, 1)))
        triangle_indices.append(((2, i, 0), (1, i, 1), (1, i, 0)))

        triangle_indices.append(((2, i, 2), (2, i, 3), (1, i, 3)))
        triangle_indices.append(((2, i, 2), (1, i, 3), (1, i, 2)))

        if i != n_int-1:
            triangle_indices.append(((2, i, 0), (1, i, 0), (2, i+1, 1)))
            triangle_indices.append(((1, i, 0), (2, i+1, 1), (1, i+1, 1)))

            triangle_indices.append(((2, i, 2), (1, i, 2), (2, i+1, 3)))
            triangle_indices.append(((1, i, 2), (2, i+1, 3), (1, i+1, 3)))

        else:
            triangle_indices.append(((2, i, 0), (1, i, 0), (2, 0, 1)))
            triangle_indices.append(((1, i, 0), (2, 0, 1), (1, 0, 1)))

            triangle_indices.append(((2, i, 2), (1, i, 2), (2, 0, 3)))
            triangle_indices.append(((1, i, 2), (2, 0, 3), (1, 0, 3)))

    # === STL メッシュを作成して書き出し ===
    mesh = build_mesh_from_indices(hanikamu, triangle_indices)
    
    # 【変更点】現在実行しているファイル（.py）の場所を取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 絶対パスを作成
    file_path = os.path.join(current_dir, "cylindrical_honeycomb.stl")
    
    # エクスポート
    mesh.export(file_path)
    print(f"STLファイルを出力しました: {file_path}")

    # === 3D プロット（面に色をつけて表示） ===
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # trimesh から頂点・面の情報を取り出す
    vertices = mesh.vertices      # (N, 3)
    faces = mesh.faces            # (M, 3)

    # 各三角形の頂点座標 (M, 3, 3) を作る
    tris = vertices[faces]

    # 面付きポリゴンコレクションを作成
    poly = Poly3DCollection(tris, alpha=0.8, linewidth=0.2)
    # 面の色（好きな色に変えてOK）
    poly.set_facecolor((0.6, 0.8, 1.0, 1.0))  # 薄い水色
    # エッジの色
    poly.set_edgecolor('k')

    ax.add_collection3d(poly)

    # 軸の範囲を STL 全体に合わせる
    xs = vertices[:, 0]
    ys = vertices[:, 1]
    zs = vertices[:, 2]

    max_range = np.array([
        xs.max() - xs.min(),
        ys.max() - ys.min(),
        zs.max() - zs.min()
    ]).max() / 2.0

    mid_x = (xs.max() + xs.min()) * 0.5
    mid_y = (ys.max() + ys.min()) * 0.5
    mid_z = (zs.max() + zs.min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    ax.set_box_aspect([1, 1, 1])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Cylindrical honeycomb (surface colored)')

    plt.show()

if __name__ == "__main__":
    main()
