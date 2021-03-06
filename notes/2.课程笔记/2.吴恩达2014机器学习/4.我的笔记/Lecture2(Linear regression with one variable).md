## Lecture2(Linear regression with one variable) 第二课:单变量线性回归
14年吴恩达机器学习课程.第二课:单变量线性回归.介绍了模型表达,成本函数和梯度下降算法.

房价问题

Hypothesis:
$$
    h_\theta=\theta_0+\theta_1x
$$
Parameters:
$$
    \theta_0,\theta_1
$$
Cost Function:
$$
    J(\theta_0,\theta_1)=\frac{1}{2m}\sum_{i=1}^m\left(h_\theta(x^{(i)}-y^{(i)}\right)^2
$$
Goal:
$$
    \min_{\theta_0,\theta_1}J(\theta_0,\theta_1)
$$
$
    Gradient descent algorithm:\\
    repeat until convergence \{\\
    \qquad \theta_j:=\theta_j-\alpha\frac{\partial}{\partial\theta_j}J(\theta_0,\theta_1)\\
    \qquad (for\;j=0\;and\;j=1)\\
    \}
$

正确代码:同时更新参数  
$$
    temp0:=\theta_0-\alpha\frac{\partial}{\partial\theta_j}J(\theta_0,\theta_1)\\
    temp0:=\theta_0-\alpha\frac{\partial}{\partial\theta_j}J(\theta_0,\theta_1)\\
    \theta_0:=temp0\\
    \theta_1:=temp1
$$

错误代码:  (坐标下降)
$$
    temp0:=\theta_0-\alpha\frac{\partial}{\partial\theta_j}J(\theta_0,\theta_1)\\
    \theta_0:=temp0\\
    temp0:=\theta_0-\alpha\frac{\partial}{\partial\theta_j}J(\theta_0,\theta_1)\\
    \theta_1:=temp1
$$

<font class="todo" color="red">TODO:为什么需要同时更新参数?</font>   
>我们一般说的梯度下降算法就是指同时更新的梯度下降算法,错误代码有时也会得到局部最小值.但是和正确代码有些微小差别,具有不同的性质.

<font class="todo" color="red">TODO:如何设置学习率$\alpha$?</font>

"Batch" Gradient Descent

"Batch": Each step of gradient descent uses all the training examples.
关于梯度下降算法,可以查看[更多](../../7.机器学习总结/梯度下降算法.md).