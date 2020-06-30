# 浅谈零知识证明之四：zkSNARK证明体系的实现（下）

前段时间略忙，主要时间在研究全同态算法FHE和可信多方计算MPC方面的内容，所以迟迟没有写完zkSNARK具体实现的下篇。这次回来补上下篇！

回顾一下上一期，我们讲到了**PCP定理**，并且从PCP定理出发约束到了**LPCP**。随后我们讲到了如何用Fiat-Shamir把交互式的协议压缩成非交互式协议。最后我们学习了**R1CS矩阵程序**，以及如何从R1CS矩阵得到对应的**多项式表达式**。

## 从R1CS到LPCP

上一期结束的时候，我们大致的介绍过如何把区间证明的电路转换成R1CS矩阵程序，最后再转换成多项式。想必大家都了解了R1CS转换成多项式的过程——通过范德蒙矩阵$V$来把$A, B, C$三个矩阵转换成三个多项式$P(x), Q(x), R(x)$。

### R1CS转换为多项式

考虑到大家已经看过一个例子了，这一期我们先来总结一下**从R1CS是如何转换到多项式的**。

1. 首先，我们使用$m, n$来定义R1CS的三个矩阵$A, B, C \in \mathbb{F}^{m \times (n+1)}$的维度。对于R1CS程序对应的公有和私密输入，我们使用$\vec{z} = \begin{bmatrix}1\\x\\w\end{bmatrix} \in \mathbb{F}^{n + 1}$来表达。
2. 随后，我们将$A$**还原为多项式**$f(x)$。就像前一篇所述，我们找到多项式$f(x)$的多个取值点：$f(i) = (A \cdot \vec{z})_i \text{ for } i = 1, ..., m$。我们一共会得到$m$个取值点，然后就可以使用**范德蒙反矩阵**把这些取值点还原成一个$m-1$阶的多项式。
3. 对于$B$，我们也进行同样的操作，还原$g(x)$。
4. 最后对于$C$，我们首先设定$h(i) = (C \cdot \vec{z})_i \text{ for } i = 1, ..., m$，然后由于$h$的阶度会是$f, g$相乘之和（即$2m - 2$），我们需要额外定义$m - 1$个点的取值。所以我们额外设定$h(i) = f(i) \cdot g(i) \text{ for } i = m+1, ..., 2m-1$。当我们拥有这$2m-1$个点之后，我们就可以使用范德蒙矩阵成功还原出$2m - 2$阶的多项式$h(x)$。

因为多项式**保持了原先矩阵之间的关系**，如果R1CS矩阵之间满足$(A \cdot \vec{z}) \circ (B \cdot \vec{z}) = C \cdot \vec{z}$，通过这个方法得到的$f, g, h$一定会满足$f(i) \cdot g(i) = h(i)$。**反过来也是一样**，如果我们可以找到三个多项式并且$h = f \cdot g$，那么代表这三个多项式所对应的R1CS矩阵程序一定也满足$(A \cdot \vec{z}) \circ (B \cdot \vec{z}) = C \cdot \vec{z}$的关系。

这一关系就是**把R1CS转换成LPCP的核心思路了**。只要我们可以验证三个多项式满足$h = f \cdot g$的关系，而且这三个多项式代表了我们想要证明的问题所对应的R1CS矩阵的话，那么就代表这个R1CS矩阵程序是**正确的**，进而代表证明方的**私密输入$w$也是正确的**！

如果放在LPCP的语言里来说的话，我们想要**随机抽查一个点$r$**，验证这三个多项式在这一点的关系$f(r) \cdot g(r) \stackrel{?}{=} h(r)$。如果这个验证通过的话，那LPCP可以保证原来的多项式绝大概率上满足$f \cdot g = h$。

### 多项式转换为LPCP

在之前的文章中，我们了解过**范德蒙矩阵$V$**式如何通过多项式的取值来**还原多项式的系数**的。同理可得，我们也可以用一样的**矩阵相乘**来表达一个多项式$f$在$r$这个点上的取值：
$$
f(r) =
\begin{bmatrix}
1 & r^2 & ... & r^{m-1}
\end{bmatrix}
\begin{bmatrix}
f_0 \\ f_1 \\ \vdots \\ f_{m-1}
\end{bmatrix}
= 
\begin{bmatrix}
1 & r^2 & ... & r^{m-1}
\end{bmatrix}
V^{-1}
\begin{bmatrix}
f(0) \\ f(1)\\
\vdots\\ f(m-1)
\end{bmatrix}
\\ = \begin{bmatrix}
1 & r^2 & ... & r^{m-1}
\end{bmatrix}
V^{-1}
(A \cdot \vec{z})
$$
一旦转换成最后形态的表达式之后，我们马上可以发现，由于$V$与R1CS矩阵$A$是证明方和验证方都公开的内容，$r$是验证方选择的随机抽验的取值点，所以我们可以把整个表达式分成**两个部分**：
$$
f(r) = (\begin{bmatrix}
1 & r^2 & ... & r^{m-1}
\end{bmatrix}
V^{-1}
A) \cdot \vec{z} = \langle q_1, z \rangle\\
q_1 = \begin{bmatrix}
1 & r^2 & ... & r^{m-1}
\end{bmatrix}
V^{-1}
A
$$
左边部分我们用一个矢量$q$来表示，代表证明方想要验证的**query**。右边部分就是包含了证明电路中公有和私密输入的矩阵$z$。对于多项式$g$，我们也如法炮制，得到另一对**内积组合**$\langle q_2, z \rangle$。

最后对于多项式$h$，我们进行类似的操作。为了让整体的维度保持一致，我们需要**额外加上一组单位矩阵**：
$$
h(r) = \begin{bmatrix}
1 & r^2 & ... & r^{2m-1}
\end{bmatrix}
V^{-1}
\begin{bmatrix}
C\\ I_{m-1}
\end{bmatrix}
\cdot 
\begin{bmatrix}
\vec{z}\\ h(m+1)\\ \vdots\\ h(2m-1)
\end{bmatrix}
= \langle q_3, [z, h(m+1), ..., h(2m-1)] \rangle\\
q_3 = \begin{bmatrix}
1 & r^2 & ... & r^{2m-1}
\end{bmatrix}
V^{-1}
\begin{bmatrix}
C\\ I_{m-1}
\end{bmatrix}
$$
具体的数学公式看似比较复杂，但是其实理解起来很简单：我们只需要把三个多项式$f, g, h$在$r$上的取值转换为了两个矢量的内积$\langle q_i, z \rangle$。

如果我们细心观察的话， 我们发现$q_1, q_2, q_3$这三个矢量可以由验证方生成，而证明方只需要准备好电路的输入$z$就好了。这样一来，我们**变相的把所有的计算难度放在了验证方的一侧**，而证明方则不需要太多的运算。

### LPCP验证协议

当我们成功的把多项式随机取值问题分解为三个query矢量$q_1, q_2, q_3$之后，我们就可以**正式地进入真正的LPCP验证协议了**。

1. 首先，**证明方Prover**事先计算好证明$\pi = [w, h(m+1), ..., h(2m-1)]$，并且把证明保存起来。
2. **验证方Verifier**随机的抽选一个验证点$r \stackrel{R}{\leftarrow} \mathbb{F}$，并且根据$r$的取值计算得到三个query的矢量$q_1, q_2, q_3$。
3. 由于证明方的输入矢量$z = \begin{bmatrix}1\\ x\\ w \end{bmatrix}$，验证方事先已经可以得知整个矢量的上半部分$\begin{bmatrix}1\\ x\end{bmatrix}$。所以验证方可以把query矢量$q_i$进行进一步分割，变成$[q_i^L, q_i^R]$两部分。这样的话，原本的计算也可以一分为二，然后把两部分的内积分别对叠起来：

$$
\langle q_i, z \rangle = \begin{bmatrix} \langle q_i^L, \begin{bmatrix}1\\x\end{bmatrix} \rangle\\ \langle q_i^R, \begin{bmatrix}w\end{bmatrix} \rangle\end{bmatrix}
$$

4. 通过进一步的分割，我们发现对于$q_i^L$部分的计算，验证方**已经全部知道了**了，所以我们可以**进一步的优化证明方需要做的计算**，只把$q_i^R$发送给证明方，让证明方仅仅与私密输入$w$相乘。
5. 综上所述，验证方现在可以发送$q_1^R, q_2^R, q_3^R$三个query矢量给证明方。
6. 证明方收到query矢量之后，**只需要把每个值和自己的证明矢量$\pi$相乘**。

$$
a = \langle [q_1^R 0^{m-1}], \pi \rangle\\
b = \langle [q_2^R 0^{m-1}], \pi \rangle\\
c = \langle q_3^R, \pi \rangle\\
$$

由于证明矢量$\pi$后面还带了多项式$h$的额外$m-1$个取值点，所以我们需要在$q_1^R, q_2^R$的背后**补上一个空白矩阵**，才可以适配矩阵相乘的维度。

随后，**证明方把$a, b, c$三个值发回给验证方**。

7. 最后，验证方只需要**把左侧query的内积补上**，最后检查等式是否相等：

$$
(\langle q_1^L, [1, x] \rangle + a) \cdot (\langle q_2^L, [1, x] \rangle + b) \stackrel{?}{=} (\langle q_3^L, [1, x] \rangle + c)
$$

组合起来之后，这也就是变相**检查等式$\langle q_1, z \rangle \cdot \langle q_2, z \rangle \stackrel{?}{=} \langle q_3, z \rangle$是否相等**。

如果得到的$a, b, c$所组成的等式的确相等，那么就代表$h(r) = f(r) \cdot g(r)$。根据我们上文讨论的关系，这也就直接代表了$(A \cdot \vec{z}) \circ (B \cdot \vec{z}) = C \cdot \vec{z}$！

这样一来，我们就得到了**完全版的LPCP协议**啦。通过抽查三个多项式在某个点上的随机取值，我们达到了简短证明的目的。只要证明方与验证方严格遵守上述描写的协议，那么就可以有效的通过**简短交互**来验证一个**R1CS矩阵所对应的多项式是否满足我们想要的关系**。

## 从LPCP到Trusted Setup SNARK

**我们距离最后的胜利，已经非常接近了！**得到了实现简短证明的LPCP协议之后，紧接着下一步就可以把LPCP协议转换为**SNARK协议**。

因为距离上一期又过去了一段时间，我们再来回顾一下这个系列第二篇文章提到的**简短证明体系(SNARK)的三个核心算法：Setup，Prove和Verify**。

1. $Setup(C) \rightarrow (S_p, S_v)$：通过实现约定好的电路，生成后续需要使用的随机参数$S_p$和$S_v$。
2. $Prove(S_p, x, w) \rightarrow \pi$：通过公有输入$x$和私密输入$w$，生成零知识证明。
3. $Verify(S_v, x, \pi) \rightarrow Yes/No$：验证证明。

这个协议的**正确性（Correctness）**说明了，只要两方不违反协议，使用正确的Setup参数，那么一个诚实的（honest）证明方可以极大概率地通过验证方的验证。

为了能够有效地把LPCP转换为SNARK，我们还需要最后一样密码学的工具——**单向线性加密系统**。

### 单向线性加密系统Linear-only Encoding













