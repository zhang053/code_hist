import numpy as np
import matplotlib.pyplot as plt

# --- パラメータ設定 ---
frequency = 50  # 周波数 (Hz)
amp_in = 4.6  # 入力波形の振幅 (V)
amp_out = 3.0  # 出力波形の振幅 (V)
cycles = 2.5  # 表示する周期の数

# --- データ生成 ---
# 時間軸の作成 (秒)
period = 1 / frequency  # 周期 T = 0.02s (20ms)
t = np.linspace(0, cycles * period, 1000)

# 入力波形 (正弦波)
# V_in = 4.6 * sin(2πft)
v_in = amp_in * np.sin(2 * np.pi * frequency * t)

# 出力波形 (全波整流波形)
# V_out = 3.0 * |sin(2πft)|
# 全波整流なので絶対値(abs)を使い、振幅を3.0Vにスケーリングします
v_out = amp_out * np.abs(np.sin(2 * np.pi * frequency * t))

# --- グラフ描画 ---
plt.figure(figsize=(10, 6))

# 入力波形のプロット (赤色)
plt.plot(
    t * 1000,
    v_in,
    label=f"Input ($V_{{in}}$): {amp_in}V, 50Hz",
    color="red",
    linestyle="--",
    linewidth=1.5,
    alpha=0.7,
)

# 出力波形のプロット (青色)
plt.plot(
    t * 1000,
    v_out,
    label=f"Output ($V_{{out}}$): {amp_out}V (Full-wave)",
    color="blue",
    linewidth=2.0,
)

# グラフの装飾
plt.title("Input vs Full-Wave Rectified Output (Overlay)")
plt.xlabel("Time (ms)")  # 横軸をミリ秒表示に変換
plt.ylabel("Voltage (V)")
plt.axhline(0, color="black", linewidth=0.8)  # 0Vの基準線
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right")

# Y軸の範囲調整 (見やすくするため少し余裕を持たせる)
plt.ylim(-amp_in - 1, amp_in + 1)

# 表示
plt.tight_layout()
plt.show()
