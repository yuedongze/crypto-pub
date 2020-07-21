# Lattice学习笔记04

### q阶随机格（q-ary random lattices）

在密码学的应用中，一般来说我们都会随机选取一个Lattice来做任何数学运算。这个随机的Lattice的每一个格点都应该是在整数格$\mathbb{Z}^n$中的，这样其中的每一个格点的坐标都是整数。

因为计算机系统的特点，并且也为了方便计算，我们一般都会选择一个比较大的数字$q$来作为我们所有涉及到的数字的上限。

结合上面两条要求，我们一般在密码学算法中用到的格，都被称作q阶随机格（q-ary random lattice）。一个q阶随机Lattice $\Lambda$需要满足如下的要求：
$$
q\mathbb{Z}^n \subseteq \Lambda \subseteq \mathbb{Z}^n
$$
其中，$q\mathbb{Z}^n$代表了包含了一个mod q的循环群。这样一来，所有和q阶Lattice有关的计算，都可以通过q模的数学运算来完成。

### 生成q阶随机格

最常见的生成随机格的方式主要为两种。首先，我们都需要随机的生成一个随机矩阵$\mathbf{A} \in \mathbb{Z}^{n \times d}_q$。

当我们获得了$\mathbf{A}$矩阵之后，我们首先可以做的，就是把这个矩阵的每一行作为我们生成的格的基向量，得到第一个Lattice：
$$
\Lambda_q(\mathbf{A}) = \{\mathbf{x} : \mathbf{x} \text{ mod } q \in \mathbf{A}^T \mathbb{Z}^{n}_q\} \subseteq \mathbb{Z}^d
$$
也就是说，我们得到的格$\Lambda_q$，$\mathbf{A}$与$\mathbb{Z}^n_q$中的所有点的线性组合组成的集合。

除此之外，我们还有一种反过来的方式，可以定义另一个随机格：找到所有的向量$\mathbf{x}$，使得$\mathbf{Ax} = 0$。
$$
\Lambda_q^\perp(\mathbf{A}) = \{\mathbf{x}: \mathbf{Ax} = 0 \text{ mod } q\} \subseteq \mathbb{Z}^d
$$
我们生成的这两个Lattice，即$\Lambda_q, \Lambda_q^\perp$，都符合我们上一部分提到的这个约束，即$q\mathbb{Z}^n \subseteq \Lambda \subseteq \mathbb{Z}^n$。并且值得注意的是，我们根据同一个$\mathbf{A}$生成的两个格是完全不一样的两个系统，几乎所有的格点都大相径庭，但是这两个Lattice之间却又有着很微妙的对偶关系。

### q阶随机格的对偶关系

首先，我们基于同一个随机矩阵$\mathbf{A}$，通过这两种方式生成的随机格，$\Lambda_q, \Lambda_q^\perp$是完全不同的两个矩阵。但是比较有趣的是，如果我们基于$\mathbf{A}$得到了$\Lambda_q$的话，那么一定存在另一个矩阵$\mathbf{A'}$，使得：
$$
\Lambda_q(\mathbf{A} \in \mathbb{Z}_q^{n \times d}) = \Lambda_q^\perp(\mathbf{A'} \in \mathbb{Z}_q^{k \times d})
$$
同理可得，如果我们根据$\mathbf{A}$得到了$\Lambda_q^\perp$的话，那一定也存在一个矩阵$\mathbf{A'}$，并且这个矩阵的$\Lambda_q$与之前的$\Lambda_q^\perp$相等。这两个生成的q阶随机格之间相互是对偶的关系。具体的关系是这样的：
$$
\Lambda_q(\mathbf{A})^\vee = \frac{1}{q}\Lambda_q^\perp(\mathbf{A})\\
\Lambda_q^\perp(\mathbf{A})^\vee = \frac{1}{q}\Lambda_q(\mathbf{A})
$$
我们生成的这两个随机格之间，就是缩放了$q$倍之后的对偶格。

### Ajtai提出的One-way Function（SIS）

当我们拥有了这两种随机格的生成方法之后，我们就可以尝试把它用于密码学上的应用了。

密码学中最基础的building block就是单向函数（OWF）了。当我们拥有了OWF之后，就可以基于它建造各种其他的密码学中的组件，比如说伪随机数生成器PRG等等。

Ajtai在1996年提出了基于我们看到的q阶随机格的OWF，并且给出了安全的论证。

![image-20200720132800686](/Users/stevenyue/work/lattice/image-20200720132800686.png)

这个OWF的构造是这样的。首先，我们随机选取一个$n \times m$阶的矩阵$\mathbf{A} \in \mathbb{Z}_q^{n \times m}$，然后我们这个OWF的输入就是一个二进制向量$\mathbf{x} \in \{0,1\}^m$。这个OWF的输出则是：
$$
f_\mathbf{A}(\mathbf{x}) = \mathbf{Ax} \text{ mod } q
$$
也就是说，我们任意选择一个二进制的短向量，这个向量和随机矩阵的乘积就是OWF的输出了。这个OWF输出的值，其实就是$\Lambda_q(\mathbf{A})$中的一个格点。

还有一个比较有趣的地方，因为$f_\mathbf{A}(\mathbf{x})$其实就是和矩阵$\mathbf{A}$的乘积，根据定义，另一个Lattice $\Lambda_q^\perp$中的所有格点$\mathbf{v} \in \Lambda_q^\perp$在这个OWF中的输出都会是零：
$$
f_\mathbf{A}(\mathbf{v} \in \Lambda_q^\perp) = 0 \text{ mod }q
$$
这样的关系在线性代数中，我们一般称$\Lambda_q^\perp(\mathbf{A})$为$f_\mathbf{A}$的kernel（核）。这也就是说，只要能够找到一个短向量$\mathbf{v} \in \Lambda_q^\perp$，已知向量$\mathbf{x}$以及OWF的结果$f_\mathbf{A}(\mathbf{x})$，我们就可以找到这个OWF的一个collision：
$$
\begin{align*}
f_\mathbf{A}(\mathbf{x + v}) &= \mathbf{A}(\mathbf{x + v})\\
&= \mathbf{Ax + Av} (\text{mod }q)\\
&= \mathbf{Ax}\ (\text{mod }q)\\
&= f_\mathbf{A}(\mathbf{x})
\end{align*}
$$
当我们把OWF的输入格式reduce成一个向量$\mathbf{x}$加上对偶格中的某个格点$\mathbf{v}$之后，根据OWF的输出还原出$\mathbf{x}$就变成了一个CVP问题：问题给出的向量就是$\mathbf{t} = \mathbf{x} + \Lambda_q^\perp(\mathbf{A})$，然后我们只要能够找到附近的格点$\mathbf{v}$，就可以相减算出$\mathbf{x}$了。

不过呢，这里我们不一定要找到最近的那个解，因为这个OWF有collision的存在，所以任何一个合适的格点都可以。这也就是说我们这里变相的是在求解ADD版本的CVP问题啦。

因为Ajtai的这个OWF基于的是未知的短向量作为输入，所以我们一般把这个体系描述为Short Integer Solution（SIS）问题。根据我们上面推理所得，SIS大致上就可以规约到approximate版的ADD问题上来，然后ADD问题又可以进一步reduce到SIVP问题上。这样SIS的困难度就可想而知了。

### Regev提出的Learning With Errors（LWE）

2015年的时候，Regev提出了一个新的基于格的难题，即LWE问题。

LWE我们在之前介绍FHE的文章中讲过了，这次主要了解一下在已知的格中难题上的规约。

![image-20200720161748498](/Users/stevenyue/work/lattice/image-20200720161748498.png)

一个LWE的定义是这样的。首先，我们随机的选取一个矩阵$\mathbf{A} \in \mathbb{Z}_q^{m \times k}$，一个随机向量$\mathbf{s} \in \mathbb{Z}_q^k$，和一个随机的噪音$\mathbf{e} \in \varepsilon^m$。我们定义一个LWE系统的输出$g_\mathbf{A}(\mathbf{s, e})$为：
$$
g_\mathbf{A}(\mathbf{s, e}) = \mathbf{As + e} \text{ mod }q
$$
一个LWE问题就是，给定一个矩阵$\mathbf{A}$，和LWE系统的输出$g_\mathbf{A}(\mathbf{s, e})$，还原$\mathbf{s}$。

首先我们可以观察一下，如果噪音$\mathbf{e}$是0的话，那么LWE系统输出的$\mathbf{As}$其实就是Lattice $\Lambda(\mathbf{A^T})$中的一个格点。这也就是说，加入噪音不是0的话，那么我们得到的结果就是在$\Lambda$的某个格点附近的一个向量。这个时候，我们就只需要求解CVP问题，就可以还原出这个格点了。我们之前也探讨过，CVP问题可以被规约到SIVP问题的求解上来。

Regev在05年的paper中正式定义了：如果最坏情况的SIVP问题很难求解，那么LWE的问题函数$g_\mathbf{A}(\mathbf{s, e})$就很难被invert。这也就是说LWE问题的困难度是基于最坏情况的SIVP困难度的。

一般来说，我们需要用这个矩阵$\mathbf{A}$形成的Lattice $\Lambda$来决定噪音$\mathbf{e}$的大小。不过一般的话：
$$
\lvert \lvert \mathbf{e} \rvert \rvert \le \frac{1}{2} \lvert \lvert \lambda_1(\Lambda(\mathbf{A}^T)) \rvert \rvert
$$
在这个噪音范围之内，我们可以确保一定能还原出一开始问题指定的$\mathbf{s}$上来。因为这个范围的限制，和我们之前看到的BDD是一样的，所以LWE问题可以被规约成approximate版本的BDD问题。

