# 格密码学进阶06：ABE属性加密（BGG+13）

### Lattice ABE的大致结构

上一期我们看到了【AFV11】的内积ABE的构造。在AFV11中，密文中带有向量$\mathbf{x}$，而解密者拥有向量$\mathbf{y}$。如果$\langle \mathbf{x, y} \rangle = 0$，那么解密者就可以成功的用他的密钥解开密文。

在上期最后，我们给出了基于格的ABE属性加密的大致结构。我们一共需要三个部分：

首先，我们需要把要加密的原文$\mu$使用一组随机选择生成的One-Time Pad $\mathbf{u}^t \mathbf{s}$覆盖住：
$$
C = \mathbf{u}^t \mathbf{s} + noise + \mu
$$
这里的$\mathbf{u}$是公开的，而$\mathbf{s}$与$noise$都是加密方自己随机生成的。

随后，解密的目的就在于计算出近似$\mathbf{u}^t \mathbf{s}$的值，然后就可以从$C$中移除这个OTP，进而还原出$\mu$。我们目前先把这个密文放在一边，来构造属性密文。我们想要把加密方选择的属性输入变相的encode在密文当中。假设属性输入为一系列的二进制向量$\mathbf{x} \in \mathbb{Z}_2^n$，我们根据每一个输入构建一个对应的密文：
$$
C_i = (\mathbf{A}_i + \mathbf{x}_i \mathbf{G})^t \mathbf{s} + \mathbf{noise}
$$
其中$\mathbf{A}_i$是事先公开生成的，而$\mathbf{s}$与$\mathbf{noise}$都是加密方选择的，其中$\mathbf{s}$的值需要和之前的一致。

我们观察发现，如果解密方可以在$\{C_i\}$一系列的密文上直接同态计算一个属性函数$f$，那么就可以得到一个带有$f$的功能信息的密文$C_f$：
$$
C_{f(x)} = (\mathbf{A}_f + f(x) \cdot \mathbf{G})^t \mathbf{s} + \mathbf{noise}
$$
这个时候就和我们上期观察到的一样，只要$f(x) = 0$，那么带有$x$信息的部分就从这个密文中消失了，整个密文就变成了一个描述函数$f$的encoding：
$$
C_f = \mathbf{A}_f^t \mathbf{s} + \mathbf{noise}
$$
因为$\mathbf{A}_f$只需要知道公共参数$\{\mathbf{A}_i\}$和$f$就可以计算出来了，所以我们就可以实现计算出$\mathbf{A}_f$并且使用MP12 Trapdoor生成对应$\mathbf{A}_f$的密钥$\mathbf{e}_f$：
$$
\mathbf{A}_f \cdot \mathbf{e}_f = \mathbf{u} \text{ mod }q
$$
当解密者拥有了$\mathbf{e}_f$，成功的在密文$\{C_i\}$上同态计算了$f$，并且恰巧$f(x) = 0$的时候，他就可以直接把得到的结果乘以密钥$\mathbf{e}_f$而得到一个近似于$\mathbf{u}^t \mathbf{s}$的值！
$$
(\mathbf{A}_f^t \mathbf{s} + \mathbf{noise}) \cdot \mathbf{e}_f \approx \mathbf{u}^t \mathbf{s}
$$
这样一来，解密方就可以从原本的密文$C$中移除这个OTP，再进行一些thresholding过滤掉噪音，就可以还原原本的密文啦。



### AFV11回顾

在上期的结尾也提到过，如果用这个视角看【AFV11】的话，其实AFV11就是实现了所有线性组合的$f$下的ABE。这也就是说，我们可以通过同态计算来得到**属性**与**约束**的内积：
$$
C_{\langle \mathbf{x, y} \rangle} = (\mathbf{A}_\mathbf{y}, \langle \mathbf{x,y} \rangle \cdot \mathbf{G})^t \mathbf{s} + \mathbf{noise}
$$
此时，如果内积恰好是0，并且解密方拥有对应的密钥$\mathbf{e}_\mathbf{y}$的话，那就可以通过我们上述提到的ABE框架来进行解密了。



### 【BGG+14】扩展至所有电路

因为在AFV11中，解密方已知了$\mathbf{y}$向量的值，所以在进行同态计算的时候，等于只需要进行加法计算而已，并不需要乘法。

熟悉FHE体系（比如GSW）的话，我们就知道乘法才是决定了FHE成败的关键之处。







