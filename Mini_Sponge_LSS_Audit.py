import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def run_lss_simulation():
    print("N.E.A. Large-Scale Structure Audit: Mini-Sponge (v6.9)")
    print("Logic: Gravity bankruptcy at logical horizon (L_H)")
    print("-" * 60)

    # 1. 模拟参数
    n_particles = 5000     # 5000个星系点
    n_steps = 100          # 演化步数
    dt = 0.5               # 演化步长
    box_size = 500.0       # 模拟空间大小 (单位：百万光年)
    
    # 2. 继承 N.E.A. 视界参数
    # 在这个模拟尺度下，我们按比例设定引力破产距离 L_H
    # 假设视界占据模拟盒子的 30% 左右，用于观察空洞形成
    L_H = 150.0  
    
    # 3. 初始化：网络重启后的均匀分布
    pos = np.random.rand(n_particles, 3) * box_size
    vel = np.zeros((n_particles, 3))
    
    print(f"Initialization complete. Simulating {n_particles} nodes with L_H = {L_H}...")

    # 4. 演化核心循环
    plt.ion()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for step in range(n_steps):
        # 计算两两之间的位移向量
        # (由于算力限制，使用简单的向量化块计算)
        acc = np.zeros((n_particles, 3))
        
        # 为了防由于 O(N^2) 导致过慢，我们分批处理引力
        for i in range(n_particles):
            diff = pos - pos[i]
            dist_sq = np.sum(diff**2, axis=1) + 1e-2 # 防止除以0
            dist = np.sqrt(dist_sq)
            
            # --- N.E.A. 核心修正：引力破产因子 ---
            # 超过 L_H 后，缝合边断裂，引力呈指数级衰减
            bankruptcy_factor = np.exp(-dist / L_H)
            
            # 计算受力：F = G * m1 * m2 * factor / r^2
            force_mag = (bankruptcy_factor / dist_sq)
            acc[i] = np.sum(diff * force_mag[:, np.newaxis], axis=0)

        # 更新位置和速度 (简单 Euler 积分)
        vel += acc * dt
        pos += vel * dt
        
        # 边界处理：周期性边界 (让星系从另一头跑回来)
        pos = np.mod(pos, box_size)

        # 5. 可视化：实时观察“海绵结构”的形成
        if step % 5 == 0:
            ax.clear()
            ax.scatter(pos[:,0], pos[:,1], pos[:,2], s=1, color='blue', alpha=0.5)
            ax.set_title(f"N.E.A. Universe Evolution: Step {step}\nGravity Bankruptcy Line: {L_H} Mly")
            ax.set_axis_off()
            plt.pause(0.01)
            print(f"Step {step}/{n_steps} settled...")

    plt.ioff()
    print("-" * 60)
    print("VERDICT: Simulation complete.")
    print("Observation: Check for 'Filaments' and 'Voids' without Dark Matter.")
    plt.show()

if __name__ == "__main__":
    run_lss_simulation()