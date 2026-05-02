import numpy as np
import matplotlib.pyplot as plt

def generate_band_diagram():
    print("Generating N.E.A. Spectral Band Diagram...")
    
    # 定义空间尺度 (从 Planck 到 1m)
    r = np.logspace(-35, 0, 500)
    
    # 1. 电磁力 (EM): 全域刷新总线
    w_em = np.ones_like(r) * 0.8
    
    # 2. 弱力 (Weak): 寻址协议握手信号 (Stride-10 尺度)
    w_weak = np.exp(-(np.log10(r) + 18)**2 / 10) * 1.0
    
    # 3. 强力 (Strong): K4 内部应力锁定 (核子尺度)
    w_strong = np.exp(-(np.log10(r) + 15)**2 / 5) * 1.5
    
    # 4. 引力 (Gravity): 壳间缝合协议
    # 关键：在 10^-10m 以下 ROI 为负，不激活
    w_grav = np.zeros_like(r)
    activation_threshold = 1e-10
    w_grav[r > activation_threshold] = 0.5 * (1 - np.exp(-(r[r > activation_threshold] - activation_threshold)*1e8))
    # 加上维度坍缩趋势 (q -> 1)
    w_grav *= (1 + 0.1 * np.log10(r + 1e-20)) 

    # 绘图
    plt.figure(figsize=(12, 7))
    plt.loglog(r, w_em, label='Electromagnetic (C8 Phase Sync)', linewidth=2, color='blue')
    plt.loglog(r, w_weak, label='Weak Force (Address Locking)', linewidth=2, color='green')
    plt.loglog(r, w_strong, label='Strong Force (K4 Anchoring)', linewidth=2, color='red')
    plt.loglog(r, w_grav, label='Gravity (Inter-cell Stitching)', linewidth=3, color='black')
    
    plt.axvline(x=1e-10, color='gray', linestyle='--', label='Atomic Threshold (10^-10 m)')
    plt.axvline(x=1e-35, color='orange', linestyle=':', label='Planck Wall')
    
    plt.title("N.E.A. Spectral Band Diagram: Force Protocol Domains", fontsize=14)
    plt.xlabel("Spatial Scale r (meters)", fontsize=12)
    plt.ylabel("Protocol Weight / ROI", fontsize=12)
    plt.legend(loc='lower left')
    plt.grid(True, which="both", alpha=0.2)
    plt.ylim(1e-3, 2.5)
    
    print("Diagram generated. Check plot windows.")
    plt.show()

if __name__ == "__main__":
    generate_band_diagram()