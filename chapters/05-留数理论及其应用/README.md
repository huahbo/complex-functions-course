# 第5章 留数理论及其应用

> 本章是复变函数的核心应用章节：在“孤立奇点”的洛朗展开基础上引入**留数**，并利用**留数定理**把闭曲线上的复积分转化为若干孤立奇点留数之和，进而用它计算一类实定积分与特殊定积分。

## 教学目标

1. 理解留数的定义（洛朗展开中 $(z-z_0)^{-1}$ 项的系数），掌握留数定理及其证明；
2. 熟练计算有限极点的留数：洛朗展开法、$m$ 阶极点公式、一阶极点公式、商函数 $P(z)/Q(z)$ 公式；
3. 理解并会用“无穷远点留数”与“全体奇点留数之和为零”定理；
4. 会用留数计算三类常见实定积分：$\int_{-\infty}^{\infty}R(x)\mathrm dx$、$\int_{-\infty}^{\infty}R(x)\mathrm e^{\alpha\mathrm i x}\mathrm dx$、$\int_0^{2\pi}R(\sin\theta,\cos\theta)\mathrm d\theta$；
5. 会用留数计算特殊定积分：$\int_0^{\infty}\frac{\sin x}{x}\mathrm dx$ 与 Fresnel 积分。

## 本章结构

| 小节 | 内容 | 对应幻灯片 |
| --- | --- | --- |
| 5.1 留数 | 留数定义、留数定理、留数计算方法、无穷远点留数 | 第2–17页 |
| 5.2 留数在积分计算上的应用 | $\int R(x)\mathrm dx$、$\int R(x)\mathrm e^{\alpha\mathrm i x}\mathrm dx$、$\int R(\sin\theta,\cos\theta)\mathrm d\theta$、特殊定积分（$\sin x/x$、Fresnel） | 第18–33页 |

## 课时建议

- 留数的定义与留数定理：2 学时；
- 留数的计算方法（极点公式、商函数公式）+ 例 5.2–5.6：2 学时；
- $\int_{-\infty}^{\infty}R(x)\mathrm dx$ 与例 5.7–5.8：1.5 学时；
- $\int R(x)\mathrm e^{\alpha\mathrm i x}\mathrm dx$（Jordan 不等式）与例 5.9：1.5 学时；
- $\sin x/x$、$\int_0^{2\pi}R(\sin\theta,\cos\theta)$（例 5.10–5.11）：1.5 学时；
- Fresnel 积分与本章总结：1–1.5 学时。

## 教学重点

- 留数定理：$\oint_C f\mathrm dz=2\pi\mathrm i\sum_k\operatorname{Res}[f,z_k]$；
- $m$ 阶极点留数公式：$\operatorname{Res}=\dfrac{1}{(m-1)!}\lim\dfrac{\mathrm d^{m-1}}{\mathrm dz^{m-1}}\{(z-z_0)^mf(z)\}$；
- 商函数留数公式：$\operatorname{Res}[P/Q,z_0]=P(z_0)/Q'(z_0)$；
- 三类实积分化闭路复积分的方法，以及“圆弧积分趋于 $0$”的条件（$n-m\ge2$、Jordan 不等式等）。

## 教学难点

- 积分周线的选择：半圆、避开奇点的小圆弧、扇形周线；
- 圆弧上积分的量级估计（$|R(z)|\le M/|z|^{n-m}$、$\sin\theta\ge\dfrac{2\theta}{\pi}$）；
- 无穷远点留数（$\operatorname{Res}[f,\infty]=-b_{-1}$）及其符号；
- 例 5.5 中二阶极点留数的导数计算；例 5.8 中“$2\pi\mathrm i$”与“$2\pi$”的区别；Fresnel 积分的正确结果。
