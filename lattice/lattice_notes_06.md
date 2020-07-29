# Lattice学习笔记05：详解SIS

### CVP与对偶格

在开始详细学习SIS之前，不妨再来重新回顾一下CVP问题。

![image-20200722220911200](/Users/stevenyue/work/lattice/image-20200722220911200.png)

我们知道，CVP问题就是给定一个任意的点$\mathbf{t} \in \mathbb{R}^n$，和一个Lattice $\Lambda$，找到一个在$\lvert \lvert \mathbf{e} \rvert \rvert$范围内的格点$\mathbf{v} \in \Lambda$。我们也可以使用格点向量$\mathbf{v}$与误差向量$\mathbf{e}$的形式来表示我们的目标向量：
$$
\mathbf{t = v + e}
$$
我们之前也学过对偶格的定义。假设我们找到了$\Lambda$的对偶格$\Lambda^\vee$，并且用$\mathcal{L}(\mathbf{D})$来表示。（即$\mathbf{D}$是对偶格$\Lambda^\vee$的基向量组成的矩阵。）根据对偶格的定义，对偶格的基向量乘以任何一个$\Lambda$中的格点都会得到一个整数。所以我们可以观察一下$\mathbf{D}$与$\mathbf{t}$的乘积：
$$
\begin{align*}
s &= \langle \mathbf{D}, \mathbf{t} \rangle \text{ mod }1\\
&= \langle \mathbf{D}, \mathbf{v} \rangle + \langle \mathbf{D}, \mathbf{e} \rangle \text{ mod }1\\
&= \langle \mathbf{D}, \mathbf{e} \rangle \text{ mod }1
\end{align*}
$$
因为我们知道$\langle \mathbf{D, v} \rangle$是一个整数，然而$\mathbf{e}$并不在格上，所以会得到一个$\mathbb{R}$中的任意小数。最后得到的$\mathbf{s}$就是表示这个误差特性的一个小数，而且不管$\mathbf{t}$在什么方位，其实真正决定了$\mathbf{s}$的值的是误差$\mathbf{e}$。在译码学中，我们一般把$\mathbf{s}$这个数值称作**伴随式译码（syndrome encoding）**。

在有噪信道传输的应用场景中（前文有所提到），我们可以基于格把一个要发送的数据$m$映射到格点$\mathbf{v}$上，然后发送过去。在接受的过程中，因为噪音的原因叠加了一个噪音向量$\mathbf{e}$，最后得到了$\mathbf{t = v + e}$。这个时候，我们只需要计算$\mathbf{t}$的syndrome $\mathbf{s}$，就可以得到这个噪音对应的一个独特的数值。

因为噪音本身与格点的方位没有关联，所以我们可以把噪音向量$\mathbf{e}$平移很多分，分到所有其他的格点上。

![image-20200722222454962](/Users/stevenyue/work/lattice/image-20200722222454962.png)

我们观察发现，这等于是在这个空间中，按照$\Lambda$的Determinant空间分成了很多份，然后每一份的parallelpiped中，都拥有这么一个点可以得到相同的syndrome！如果用集群的方法来表达的话，那么这个噪音向量$\mathbf{e}$属于一个coset（陪集）当中，这个coset为：
$$
\mathbf{t} + \Lambda = \{\mathbf{x} : \langle \mathbf{D, x} \rangle = \mathbf{s} \text{ mod }1\}
$$
当我们知道了syndrome之后，我们知道在整个$\mathbb{R}^n$的空间中，存在无限多个可以满足这个syndrome的点。这个时候我们只需要在原点附近，找到一个最短的向量$\mathbf{e}$，使得$\langle \mathbf{D, e} \rangle = \mathbf{s} \text{ mod }1$。找到这个向量$\mathbf{e}$之后，我们只需要从$\mathbf{t}$中减去它，就可以解决CVP问题啦。

通过这种方法解决的CVP问题，我们一般称为**伴随式解码问题（syndrome decoding problem）**。

### CVP构造的One-way Function

知道了CVP问题可以被转化为在一个Lattice的基础空间（即Determinant构成的空间）中搜索一个短向量$\mathbf{e}$之后，我们可以根据短向量的和Lattice的基础空间（即Determinant组成的空间），尝试构造出如下的OWF。

![image-20200722230623289](/Users/stevenyue/work/lattice/image-20200722230623289.png)

首先，我们OWF的key就是随机选取一个困难的Lattice $\Lambda$。然后输入一个短向量$\mathbf{x}$，并且这个向量的长度我们使用$\beta$来约束：
$$
\lvert \lvert \mathbf{x} \rvert \rvert \le \beta
$$
这个OWF的输出非常简单，就是这个短向量在这个Lattice中求模运算得出的结果：
$$
f_\Lambda(\mathbf{x}) = \mathbf{x} \text{ mod } \Lambda
$$
上面的图很好的表述了这个OWF做的事情：我们其实就是把一个距离原点半径为$\beta$范围内的一个球体中的任意一个向量，映射到了这个Lattice的Determinant组成的基础空间中。这个空间的映射，其实和我们上面说到的syndrome encoding有异曲同工之妙，都是把一个向量映射到了这么一块空间中，只是输出的格式不同而已。

我们如果仔细观察$\beta$这个上限的值，会发现这对于我们构造的OWF会有质的影响。

首先，如上图所示，如果$\beta < \lambda_1(\Lambda)/2$，也就是说$\beta$小于了这个格中最短向量的一半的话，我们可以发现，映射到基础空间之后，我们之前的一个球体会被拆分成各个小块散落在每个格点周围。因为格点之间的距离肯定不能短于Lattice的最短向量，而我们球体的半径比最短向量的一半还小，可想而知我们的映射结果不会有任何重合。这种情况下的OWF是单射（injective）的，即每一个映射空间（即基础空间）中的点，都对应了至多一个输入空间中的点。

![image-20200722231510102](/Users/stevenyue/work/lattice/image-20200722231510102.png)

当我们放大$\beta$的值，使得$\beta > \lambda_1/2$之后，我们发现很多球面的部分重合了。这说明这个OWF会有多个输入都映射到同一个输出上，即collision。这也就代表了我们构造的OWF $f_\Lambda$不再是一个injective的函数。

![image-20200722231606895](/Users/stevenyue/work/lattice/image-20200722231606895.png)

如果我们继续扩大$\beta$的值的话，当$\beta$大于整个Lattice的覆盖半径之后，即$\beta \ge \mu$，根据覆盖半径的定义，我们知道整个映射空间都被我们的球体给覆盖住了。这个时候，所有的映射空间中的点都有至少一个对应的输入空间中的点，这个OWF也就变成了一个满射（surjective）的函数了。

![image-20200722231816871](/Users/stevenyue/work/lattice/image-20200722231816871.png)

当然，就像我们之前一篇提到的，我们也可以继续扩大这个圆的半径，使得这个基础空间被基本上均匀覆盖。这样一来，我们就可以说OWF $f_\Lambda(\mathbf{x})$是一个均匀（uniform）覆盖输出空间的OWF了。

这样一个OWF的构造似乎令人满意，并且看似也很难被找到对应的反函数（inverse）。

### Ajtai提出的OWF：SIS问题

上文提出的OWF构造的精髓我们其实已经get到了：我们把一个短向量映射到格当中，然后这个映射可以被看作是一个单向的映射，因为很难通过映射本身来找回原始的输入值。但是我们之前看到的体系是基于几何意义上的OWF，在计算机系统中很难被有效的运用

1996年，密码学家Ajtai基于这一思路，提出了在整数格中实现的OWF，即SIS问题（Short Integer Solution）。在前面的笔记中对于SIS已经有所介绍了，我们这里再稍微回顾一下。

![image-20200720132800686](/Users/stevenyue/work/lattice/image-20200720132800686.png)

一个SIS构成的OWF有以下一系列的参数：

- 矩阵的维度和模组的大小：$m, n, q \in \mathbb{Z}$。
- OWF的key：$\mathbf{A} \in \mathbb{Z}^{n \times m}_q$，即一个随机的$n \times m$阶的矩阵。
- OWF的输入：$\mathbf{x} \in \{0,1\}^m$，即一个长度为$m$的二进制向量。这里要求二进制的原因是为了确保这个向量的长度足够的短（符合短向量的条件）。理论上也可以使用$O(1)$范围内任何区间。
- OWF的输出：$f_\mathbf{A}(\mathbf{x}) = \mathbf{Ax} \text{ mod }q$。

Ajtai在paper中提出，只要矩阵的维度符合$m > n \cdot log(q)$这一标准，并且SIVP问题困难的话，那么此$f_\mathbf{A}(\mathbf{x})$就是一个合理的OWF。

我们不禁会问，为什么这是一个OWF呢？在前面的一篇笔记里应该有所提到，不过我们这里可以系统性的来证明一下这个OWF的安全性。

### SIS的单向性证明

我们首先想要证明，基于SIS的OWF真的是One-way的。

即然要讨论One-way，那么我们可以定义一下SIS的反问题：如果给定了矩阵$\mathbf{A}$与向量$\mathbf{y}$，能否找到一个短向量$\mathbf{x} \in \{0, 1\}^m$，并且可以满足$\mathbf{Ax = y} \text{ mod }q$。我们可以经过一些转换，把这个反问题转换为一个Lattice中的问题。

首先，因为这个等式$\mathbf{Ax = y} \text{ mod }q$就是一个普通的线性组合等式，所以我们可以非常轻松的找到一个解$\mathbf{t}$，使得$\mathbf{At = y} \text{ mod }q$。只需要使用高斯消除法，我们就可以很简单的找到一个合适的$\mathbf{t}$。

虽然$\mathbf{t}$好找，但是事实是，通过高斯消除法得到的$\mathbf{t}$可能会是一个随机的很大的向量，几乎不可能能找到我们想要的的**短向量**，即一个二进制向量，所以我们并没有解决这个问题。但是因为$\mathbf{x, t}$都可以满足这个等式，所以我们就可以运用前面学到的知识，把所有满足$\mathbf{Ax = y}$的解向量，都描述为一个coset $\mathbf{t} + \Lambda^\perp$。这里的$\Lambda^\perp$即垂直于$\Lambda$的另一个Lattice：
$$
\Lambda^\perp(\mathbf{A}) = \{\mathbf{x} \in \mathbb{Z}^m: \mathbf{Ax = 0} \text{ mod }q\}
$$
经过如此转换，我们就可以把问题转换为：如何在coset $\mathbf{t} + \Lambda^\perp$中找到最短的一个向量$\mathbf{x}$。这个最短的向量就是满足我们这个OWF的二进制向量了。这就是一个syndrome decoding problem。

同理可得，我们也可以把这个问题转换为CVP：找到距离$\mathbf{t}$最近的一个$\Lambda^\perp$中的格点$\mathbf{v}$。最后输出$\mathbf{t - v}$就是SIS的答案。

这也就是说，如果要解决SIS的反问题，那么我们起码需要解决CVP问题。因为CVP问题被相信是一个难题，所以SIS不可逆，这也就是个OWF了。

### SIS的Collision Resistance证明

其次，我们还可以证明，SIS是Collision Resistant的（即难以找到碰撞）。碰撞的意思就是说，我们可以找到两个不同的输入$\mathbf{x, y}$，使得$f_\mathbf{A}(\mathbf{x}) = f_\mathbf{A}(\mathbf{y})$。

这一点我们在之前的一篇文章中也有所描述。如果我们可以找到SIS的碰撞，即两个二进制向量$\mathbf{x, y}$，并且$\mathbf{Ax = Ay} \text{ mod }q$，我们可以观察这两个碰撞输入的差：
$$
\mathbf{z = x - y} \in \{-1, 0, 1\}^m
$$
因为$\mathbf{x, y}$都是二进制向量，所以它们相减得到的向量，也是二进制的。（我们可以把-1和1看作是一样的，因为在距离上看是相等的。）这也就是说：
$$
\mathbf{Az = Ax - Ay =0} \text{ mod }q
$$
通过找到了一组碰撞，我们就可以找到$\Lambda^\perp$这个Lattice中的一个短向量！这个向量的无限范数$\lvert \lvert \mathbf{z} \rvert \rvert_\infty = max_i \lvert z_i \rvert = 1$。这样一来，我们就等于解决了$\Lambda^\perp$这个格中的SVP（或者SIVP）问题。同理，因为SVP/SIVP是困难的，所以我们不能找到SIS的碰撞啦。