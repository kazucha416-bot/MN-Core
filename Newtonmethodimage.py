import numpy as np
import matplotlib.pyplot as plt

# Plot settings for presentation
plt.rcParams.update({'font.size': 14, 'font.family': 'sans-serif'})

def f(x):
    """Function example: y = x^2 - 2 (Target root is sqrt(2))"""
    return x**2 - 2

def df(x):
    """Derivative: y' = 2x"""
    return 2*x

# x range
x = np.linspace(0.5, 3.5, 100)
y = f(x)

# Target root
target_x = np.sqrt(2)

# Initial guess x0
x0 = 3.0
y0 = f(x0)

# 1st Iteration x1
# x1 = x0 - f(x0)/f'(x0)
slope0 = df(x0)
x1 = x0 - y0 / slope0
y1 = f(x1)

# Create figure
fig, ax = plt.subplots(figsize=(8, 6))

# 1. Plot function
ax.plot(x, y, label='$f(x) = x^2 - C$', color='#2c3e50', linewidth=3)
ax.axhline(0, color='black', linewidth=1) # x-axis

# 2. Initial Guess x0
ax.plot([x0, x0], [0, y0], linestyle='--', color='gray')
ax.scatter([x0], [y0], color='#e74c3c', s=100, zorder=5)
ax.text(x0 + 0.1, y0, '$x_0$\n(Initial Guess)', va='center', color='#e74c3c', fontweight='bold')

# 3. Tangent Line
tangent_line_x = np.linspace(x1 - 0.5, x0 + 0.5, 10)
tangent_line_y = slope0 * (tangent_line_x - x0) + y0
ax.plot(tangent_line_x, tangent_line_y, color='#e74c3c', linestyle='-', linewidth=2, label="Tangent at $x_0$")

# 4. Next Estimate x1
ax.scatter([x1], [0], color='#e67e22', s=100, zorder=5) # Point on axis
ax.plot([x1, x1], [0, y1], linestyle='--', color='gray')
ax.scatter([x1], [y1], color='#e67e22', s=100, zorder=5) # Point on curve
ax.text(x1, -1.8, '$x_1$\n(1st Iteration)', ha='center', color='#e67e22', fontweight='bold')

# 5. True Root
ax.scatter([target_x], [0], color='#27ae60', s=150, marker='*', zorder=10)
ax.text(target_x - 0.1, 0.5, 'True Root', ha='right', color='#27ae60', fontweight='bold')

# 6. Arrow annotation
ax.annotate('', xy=(x1, 0), xytext=(x0, y0),
            arrowprops=dict(arrowstyle="->", color="gray", linestyle="dashed", linewidth=1.5))

# Labels and Title
ax.set_title('Newton-Raphson Method Visualization', fontsize=18, fontweight='bold', pad=15)
ax.set_xlabel('$x$', fontsize=16)
ax.set_ylabel('$f(x)$', fontsize=16)
ax.set_ylim(-3, 8)
ax.set_xlim(0.5, 3.8) # Adjusted for labels
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left', fontsize=12)

plt.tight_layout()
plt.savefig('newton_graph_en.png', dpi=300)
print("Saved: newton_graph_en.png")
plt.show()