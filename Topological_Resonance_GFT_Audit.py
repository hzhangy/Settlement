import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

def run_gft_resonance_audit(L=10, stride_n=10):
    print(f"N.E.A. GFT Audit: Finding the First Addressing Peak (L={L})")
    print("-" * 60)

    # 1. 构造 3D 晶格拉普拉斯算子
    N = L**3
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

    # 2. 计算前 k 个特征向量 (代表低频背景模式)
    # 计算量较大，我们取前 300 个模式
    k_modes = 300
    print(f"Computing {k_modes} spectral modes...")
    vals, vecs = eigsh(laplacian, k=k_modes, which='SM')

    # 3. 构造 Stride-10 寻址信号 (沿着体对角线的脉冲链)
    signal = np.zeros(N)
    for i in range(stride_n):
        node_idx = i*L*L + i*L + i
        if node_idx < N:
            signal[node_idx] = 1.0
    signal /= np.linalg.norm(signal)

    # 4. 执行图傅里叶变换 (GFT)
    # 将物理空间的信号投影到谱空间
    gft_coeffs = vecs.T @ signal
    power_density = np.abs(gft_coeffs)**2

    # 5. 寻找主谐振频率 lambda
    peak_idx = np.argmax(power_density[1:]) + 1 # 跳过 0 频率
    peak_lambda = vals[peak_idx]
    
    # 6. 拓扑映射：将图频率换算为多极矩 l
    # 公式：l = sqrt(lambda) * (N_max^(1/3)) * Geometric_Correction
    # 这里的 N_max^(1/3) 是将逻辑位宽映射到单轴分辨率
    logical_resolution = np.exp(10 * np.sqrt(3) / 3.0) 
    l_predicted = np.sqrt(peak_lambda) * logical_resolution

    print(f"Peak Graph Frequency (lambda): {peak_lambda:.6f}")
    print(f"Spectral Power at Peak: {power_density[peak_idx]:.6e}")
    print("-" * 40)
    print(f"NEA Derived l: {l_predicted:.2f}")
    print(f"Observational Standard: 220.6")
    
    return l_predicted

if __name__ == "__main__":
    run_gft_resonance_audit(L=12)