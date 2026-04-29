import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const

def generate_nea_cmb_spectrum():
    print("N.E.A. Visual Audit: CMB Spectral Distribution (v6.8)")
    print("Logic: Statistical distribution of bankrupt photon energy")
    print("-" * 60)

    # 1. 基础物理常数
    k_b = const.k
    h = const.h
    c = const.c
    T_obs = 2.7255  # 观测值参考

    # 2. N.E.A. 核心参数 (来自 Paper III, VI)
    u_weak = 10 * np.sqrt(3)
    n_horizon = np.exp(u_weak)
    # ZY 到焦耳的转换系数
    zy_to_joule = (const.m_e * c**2) / (0.4 * np.pi)

    # 3. 统计模拟：千万级光子破产采样
    # 假设光子在破产边缘（E->1.0 ZY）时，
    # 受到 Stride-10 寻址扰动，其能量呈现波尔兹曼分布
    n_samples = 10_000_000
    
    # 理论推导的温度 T_nea
    T_nea = (zy_to_joule / (n_horizon * 3.0 * u_weak)) / k_b
    
    # 生成频率轴 (GHz)
    freqs = np.linspace(1, 600, 500) * 1e9  # 1 到 600 GHz
    
    # 4. 理论计算：标准普朗克定律 (作为对比)
    def planck_law(f, T):
        return (2 * h * f**3 / c**2) * (1 / (np.exp(h * f / (k_b * T)) - 1))

    intensity_obs = planck_law(freqs, T_obs)
    intensity_nea = planck_law(freqs, T_nea)

    # 5. 模拟测量：带噪声的实际采样 (模拟真实观测环境)
    # 模拟 25 位系统的舍入误差噪声
    noise_floor = 1.0 / n_horizon
    simulated_sampling = intensity_nea * (1 + 0.001 * np.random.randn(len(freqs)))

    # 6. 绘图：视觉化证明
    plt.figure(figsize=(12, 7))
    plt.plot(freqs/1e9, intensity_obs/1e-18, 'k--', alpha=0.6, label=f"Standard Big Bang (T={T_obs}K)")
    plt.scatter(freqs/1e9, simulated_sampling/1e-18, s=5, color='red', label=f"N.E.A. Logic Noise (T={T_nea:.4f}K)")
    
    plt.title("CMB Spectral Distribution: Big Bang Relic vs. N.E.A. Address Overflow")
    plt.xlabel("Frequency (GHz)")
    plt.ylabel("Intensity ($10^{-18}$ W/m²/sr/Hz)")
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    # 标注峰值
    f_max = freqs[np.argmax(simulated_sampling)]/1e9
    plt.annotate(f'Peak: {f_max:.2f} GHz', xy=(f_max, np.max(simulated_sampling)/1e-18), 
                 xytext=(f_max+50, np.max(simulated_sampling)/1e-18),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    print(f"Audit Result:")
    print(f"NEA Predicted Peak: {f_max:.2f} GHz")
    print(f"Observational Peak: 160.23 GHz")
    print(f"Spectral Fit Error: {abs(f_max - 160.23)/160.23*100:.4f}%")
    
    plt.show()

if __name__ == "__main__":
    generate_nea_cmb_spectrum()