import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt

def get_peak_multipole(L):
    """
    计算给定边长 L 的 3D 晶格在 Stride-10 信号下的主谐振频率
    """
    N = L**3
    # 1. 构造拉普拉斯算子
    adj = sp.dok_matrix((N, N))
    for x in range(L):
        for y in range(L):
            for z in range(L):
                u = x*L*L + y*L + z
                for dx, dy, dz in [(1,0,0), (0,1,0), (0,0,1)]:
                    nx, ny, nz = x+dx, y+dy, z+dz
                    if nx < L and ny < L and nz < L:
                        v = nx*L*L + ny*L + nz
                        adj[u, v] = adj[v, u] = 1
    adj = adj.tocsr()
    degree = np.array(adj.sum(axis=1)).flatten()
    laplacian = sp.diags(degree) - adj

    # 2. 构造 Stride-10 信号
    signal = np.zeros(N)
    stride = 10
    for i in range(min(stride, L)):
        idx = i*L*L + i*L + i
        signal[idx] = 1.0
    signal /= np.linalg.norm(signal)

    # 3. 寻找谱空间的主响应 (取前 200 个低频模)
    k_modes = 200
    vals, vecs = eigsh(laplacian, k=k_modes, which='SM')
    gft = vecs.T @ signal
    power = np.abs(gft)**2
    
    # 排除 0 频率，找到最高响应的本征值 lambda
    peak_idx = np.argmax(power[1:]) + 1
    lambda_peak = vals[peak_idx]
    
    # 返回该尺度下的本征多极矩: l_eff = sqrt(lambda) * L
    return np.sqrt(lambda_peak) * L

def run_scaling_audit():
    print("N.E.A. Scaling Law Audit: Is l proportional to N^(1/3)?")
    print("-" * 60)
    
    # 测试不同的晶格尺度 L (对应不同的 N)
    L_sizes = [8, 10, 12, 14, 16]
    observed_ls = []
    
    for L in L_sizes:
        l_val = get_peak_multipole(L)
        observed_ls.append(l_val)
        print(f"Lattice L={L:2d} (N={L**3:5d}) | Observed l_eff: {l_val:8.4f}")

    # 执行线性回归判定缩放律
    # 如果 l = (1/gamma) * L, 那么斜率就是 1/gamma
    slope, intercept = np.polyfit(L_sizes, observed_ls, 1)
    gamma_eff = 1.0 / slope
    
    print("-" * 40)
    print(f"Audit Conclusion:")
    print(f"Effective Scaling Slope: {slope:.4f}")
    print(f"Extracted Packing Factor (gamma): {gamma_eff:.4f}")
    print(f"Target gamma from Paper VI: 1.4500")
    
    # 4. 预测宇宙尺度的 l_peak
    # 宇宙的 L_max = N_max^(1/3) = e^(10*sqrt(3)/3)
    L_cosmos = np.exp(10 * np.sqrt(3) / 3.0)
    l_predicted = slope * L_cosmos + intercept
    
    print(f"Predicted Cosmic l_peak (at L={L_cosmos:.2f}): {l_predicted:.2f}")
    print(f"Planck 2018 Observed: 220.6")
    print(f"Final Error: {abs(l_predicted - 220.6)/220.6*100:.4f}%")

if __name__ == "__main__":
    run_scaling_audit()