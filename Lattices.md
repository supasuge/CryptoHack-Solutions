# Linear Independence, Basis, and Vector Properties

We say a set of vectors $ \mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_k \in V $ are linearly independent if the only solution to the equation:

$$
a_1 \cdot \mathbf{v}_1 + a_2 \cdot \mathbf{v}_2 + \ldots + a_k \cdot \mathbf{v}_k = 0
$$

is for $a_1 = a_2 = \ldots = a_k = 0$.

> 💡 **To visualise this:** Think of a vector directed out of a point. Given a set of linearly independent vectors, the only way to return back to the original point is by moving along the original vector. No combination of any of the other vectors will get you there.

---

A **basis** is a set of linearly independent vectors $ \bf{v}_1, \bf{v}_2, \ldots, \bf{v}_n \in V $ such that any vector $ \bf{w} \in V $ can be written as:

$$
\bf{w} = a_1 \cdot \hbf{v}_1 + a_2 \cdot \hbf{v}_2 + \ldots + a_k \cdot \bf{v}_n
$$

The number of elements in the basis is also the **dimension** of the vector space.

---

We define the **size** of a vector, denoted $ \|\mathbf{v}\| $, using the inner product of the vector with itself:

$$
\|\mathbf{v}\|^2 = \mathbf{v} \cdot \mathbf{v}
$$

---

A **basis is orthogonal** if for a vector basis $ \mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_n \in V $, the inner product between any two different vectors is zero:

$$
\mathbf{v}_i \cdot \mathbf{v}_j = 0, \quad i \neq j
$$

A basis is **orthonormal** if it is orthogonal and $ \|\mathbf{v}_i\| = 1 $, for all $ i $.

---

That's a lot of stuff, but we'll be needing it. **Time for the flag.** Given the vector $ \mathbf{v} = (4, 6, 2, 5) $, calculate its size.

## Vector Size (Norm) Calculation for $v = (4,6,2,5)$

## Definition Reminder
- The **size** (or **norm**) of a vector $v$ in an inner product space is given by:
$$
\|v\|^2 = v \cdot v.

$$
  This typically implies:
  
$$
\|v\| = \sqrt{v \cdot v}.
$$

## Steps to Calculate the Size of $v$
Given $v = (4,6,2,5)$:

1. **Compute the dot product** of $v$ with itself:
   - $v \cdot v = 4^2 + 6^2 + 2^2 + 5^2.$
   - Numerically: $4^2 = 16$, $6^2 = 36$, $2^2 = 4$, $5^2 = 25.$
   - Sum: $16 + 36 + 4 + 25 = 81.$

2. **Take the square root**:
   - $\|v\| = \sqrt{81} = 9.$

Hence, the size (norm) of the vector $v$ is $9$.

---

## SageMath Code

```python
# Define the vector v
v = vector(RR, [4,6,2,5])

# Compute the dot product of v with itself
dot_val = v.dot_product(v)

# Compute the norm (size) of v
norm_val = sqrt(dot_val)

# Print results
print("Dot product (v . v):", dot_val)
print("Size (norm):", norm_val)
```


## Gram Schmidt

# 1. Notation and the Gram–Schmidt Algorithm

Given a set of basis vectors  
$v_1, v_2, v_3, v_4 \in \mathbb{R}^4$,

the **Gram–Schmidt** algorithm constructs an **orthogonal** set of vectors  
$u_1, u_2, u_3, u_4$  
such that for each $i$, the span of $\{u_1, \dots, u_i\}$ is the same as the span of $\{v_1, \dots, v_i\}$. Concretely, the algorithm goes as follows (indexing $i=1$ to $4$ in our case):

1. **Initialize**:
   - $u_1 = v_1$.

2. **For each** $i = 2, \dots, 4$:
   1. For each $j = 1, \dots, i-1$, compute  
      $$
      \mu_{i,j} \;=\; \frac{v_i \cdot u_j}{\|u_j\|^2},
      $$
      where $\cdot$ is the dot product and $\|u_j\|^2 = u_j \cdot u_j$.
   2. Subtract out the projections onto the earlier $u_j$’s:  
      $$
      u_i \;=\; v_i - \sum_{j=1}^{\,i-1} \mu_{i,j}\,u_j.
      $$

At the end, $\{u_1,u_2,u_3,u_4\}$ (i.e., $u_1, u_2, u_3, u_4$) is an **orthogonal** basis for the same space spanned by $\{v_1,v_2,v_3,v_4\}$.

> **Important**  
> - **Orthogonal** means each pair of distinct $u_i,u_j$ has zero dot product.  
> - **Orthonormal** means orthogonal **and** each $u_i$ has unit length ($\|u_i\|=1$). To make it orthonormal, you’d divide each $u_i$ by its norm after you compute it.

---

# 2. Our Specific Vectors

We have the following vectors in $\mathbb{R}^4$:

- $v_1 = (4,\,1,\,3,\,-1)$  
- $v_2 = (2,\,1,\,-3,\,4)$  
- $v_3 = (1,\,0,\,-2,\,7)$  
- $v_4 = (6,\,2,\,9,\,-5)$  

Below is a step-by-step derivation of $u_1,u_2,u_3,u_4$ using the Gram–Schmidt algorithm. We then extract the **second component** of $u_4$ to **5 significant figures**.

---

## 2.1. Compute $u_1$

By definition:
$$
u_1 = v_1 = (4,\;1,\;3,\;-1).
$$

We will need $\|u_1\|^2$:
$$
\|u_1\|^2 = 4^2 + 1^2 + 3^2 + (-1)^2 = 16 + 1 + 9 + 1 = 27.
$$

---

## 2.2. Compute $u_2$

1. Compute  
   $$
   \mu_{2,1} = \frac{v_2 \cdot u_1}{\|u_1\|^2}.
   $$
   - $v_2 \cdot u_1 = 2\cdot4 + 1\cdot1 + (-3)\cdot3 + 4\cdot(-1) = 8 + 1 - 9 - 4 = -4$.  
   - Hence, $\mu_{2,1} = -4/27$.

2. Subtract this projection from $v_2$:  
   $$
   u_2 = v_2 - \mu_{2,1}\,u_1 
        = (2,\,1,\,-3,\,4) - \left(-\frac{4}{27}\right)(4,\,1,\,3,\,-1).
   $$  
   Numerically,  
   $$
   u_2 \approx (2 + \tfrac{16}{27},\;1 + \tfrac{4}{27},\;-3 + \tfrac{12}{27},\;4 - \tfrac{4}{27})  
        \approx (2.59259,\;1.14815,\;-2.55556,\;3.85185).
   $$

3. $\|u_2\|^2 = u_2 \cdot u_2 \approx 29.41753$ (we’ll use this later).

---

## 2.3. Compute $u_3$

Remove from $v_3$ the projections onto $u_1$ and $u_2$:

1. First, project out $u_1$:
   $$
   \mu_{3,1} = \frac{v_3 \cdot u_1}{\|u_1\|^2} 
             = \frac{(1\cdot4) + (0\cdot1) + (-2\cdot3) + (7\cdot(-1))}{27} 
             = \frac{4 - 6 - 7}{27} 
             = -\frac{9}{27} = -\tfrac{1}{3}.
   $$
   So we form
   $$
   v_3 + \tfrac{1}{3}u_1 \approx (1,\,0,\,-2,\,7) + \tfrac{1}{3}(4,\,1,\,3,\,-1)
                            \approx (2.3333,\;0.3333,\;-1,\;6.6667).
   $$

2. Next, project out $u_2$:
   $$
   \mu_{3,2} = \frac{v_3 \cdot u_2}{\|u_2\|^2} \approx \frac{\text{(some dot product)}}{29.41753}.
   $$  
   Numerically, $\mu_{3,2} \approx 1.1780$.

3. Hence,  
   $$
   u_3 = \bigl(v_3 + \tfrac{1}{3}u_1\bigr) - \mu_{3,2}\,u_2 
        \approx (-0.72016,\;-1.02033,\;2.01463,\;2.12622).
   $$

4. $\|u_3\|^2 \approx 10.13925$.

---

## 2.4. Compute $u_4$

Remove from $v_4$ the projections onto $u_1$, $u_2$, and $u_3$:

$$
u_4 
= v_4 \;-\; \mu_{4,1}u_1 \;-\; \mu_{4,2}u_2 \;-\; \mu_{4,3}u_3,
$$

where
$$
\mu_{4,j} = \frac{v_4 \cdot u_j}{\|u_j\|^2}.
$$

1. **Subtract $\mu_{4,1}\,u_1$**  
   - $v_4 \cdot u_1 = 6\cdot4 + 2\cdot1 + 9\cdot3 + (-5)\cdot(-1) = 24 + 2 + 27 + 5 = 58$.  
   - $\mu_{4,1} = 58/27 \approx 2.14815$.  
   - Subtracting gives an intermediate vector  
     $$
     (6,\,2,\,9,\,-5) - 2.14815(4,\,1,\,3,\,-1)
     \approx (-2.59259,\;-0.14815,\;2.55556,\;-2.85185).
     $$

2. **Subtract $\mu_{4,2}\,u_2$**  
   - $\mu_{4,2} \approx \frac{v_4 \cdot u_2}{29.41753} \approx -0.82917$.  
   - Subtraction yields another intermediate vector  
     $$
     \approx (-0.44276,\;0.80393,\;0.43539,\;0.34345).
     $$

3. **Subtract $\mu_{4,3}\,u_3$**  
   - $\mu_{4,3} \approx \frac{v_4 \cdot u_3}{10.13925} \approx 0.11237$.  
   - Finally,  
     $$
     u_4 
     \approx (-0.44276,\;0.80393,\;0.43539,\;0.34345) 
            - 0.11237\bigl(-0.72016,\;-1.02033,\;2.01463,\;2.12622\bigr)
     \approx (-0.36179,\;0.91862,\;0.20886,\;0.10445).
     $$

---

# 3. Final Flag: Second Component of $u_4$ to 5 s.f.

The second component of $u_4$ is approximately **0.91862**.

> **Flag** (to 5 significant figures):  
> $$\boxed{0.91862}$$

---

# 4. Making an Orthonormal Basis

If we wanted an **orthonormal** basis, we would simply **divide** each $u_i$ by its norm $\|u_i\|$ after each step. Then each $u_i$ would have length 1, and any two distinct $u_i, u_j$ would remain orthogonal.

---

# 5. SageMath Code

```sage

# 1) Define the original vectors v1, v2, v3, v4
v1 = vector(RR, [4, 1, 3, -1])
v2 = vector(RR, [2, 1, -3, 4])
v3 = vector(RR, [1, 0, -2, 7])
v4 = vector(RR, [6, 2, 9, -5])

V = [v1, v2, v3, v4]

# 2) Gram-Schmidt function
def gram_schmidt(V):
    U = []
    for i in range(len(V)):
        v_i = V[i]
        for j in range(i):
            u_j = U[j]
            mu_ij = (v_i.dot_product(u_j)) / (u_j.dot_product(u_j))
            v_i = v_i - mu_ij*u_j
        U.append(v_i)
    return U

# 3) Compute the orthogonal vectors
U = gram_schmidt(V)

# 4) Display results
for idx, vec in enumerate(U, start=1):
    print(f"u{idx} = {vec}")

# 5) Extract the second component of u4
second_component_u4 = U[3][1]  # 0-based indexing: U[3] is u4, [1] is 2nd component
print("Second component of u4 to 5 s.f.:", round(second_component_u4, 5))
```

```python
# Using sage API to solve it.
V = matrix(QQ, [[4.0,1.0,3.0,-1.0], [2.0,1.0,-3.0,4.0], [1.0,0.0,-2.0,7.0], [6.0, 2.0, 9.0, -5.0]])
print(V.gram_schmidt())

# (
# [         4          1          3         -1]
# [     70/27      31/27      -23/9     104/27]
# [  -287/397   -405/397    799/397    844/397]
# [-1456/4023    273/298  1729/8046   455/4023],

# [       1        0        0        0]
# [   -4/27        1        0        0]
# [    -1/3  468/397        1        0]
# [   58/27 -659/794 439/4023        1]
# )

print(float(V.gram_schmidt()[0][3][1]))
# 0.9161073825503355
```

#### Using python3
```python
#!/usr/bin/env python3
import numpy as np
v = [
    np.array([4,1,3,-1]), 
    np.array([2,1,-3,4]), 
    np.array([1,0,-2,7]), 
    np.array([6,2,9,-5]),
]

"""
u1 = v1
Loop i = 2,3...,n
   Compute μij = vi ∙ uj / ||uj||2, 1 ≤ j < i.
   Set ui = vi - μij * uj (Sum over j for 1 ≤ j < i)
End Loop
"""

u = [v[0]]
for vi in v[1:]:
    mi = [np.dot(vi, uj) / np.dot(uj, uj) for uj in u]
    u += [vi - sum([mij * uj for (mij, uj) in zip(mi,u)])]

print(round(u[3][1], 5))
```

```python
import math
import numpy as np


def gram_schmidt(A):
    n, k = len(A), len(A[0])
    U = np.zeros((n, k))
    U[0, :] = A[0, :]
    for i in range(1, n):
        U[i, :] = A[i, :]
        for j in range(0, i):
            mu_ij = U[j, :].dot(U[i, :]) / U[j, :].dot(U[j, :])
            U[i, :] = U[i, :] - mu_ij * U[j, :]
    return U


basis = np.array(
    [
        np.array((4, 1, 3, -1)),
        np.array((2, 1, -3, 4)),
        np.array((1, 0, -2, 7)),
        np.array((6, 2, 9, -5)),
    ]
)

ortho = gram_schmidt(basis)
print(ortho)
print("{0:.5f}".format(ortho[3][1]))
```


## What even is a lattice?

# Volume of the Fundamental Domain in 3D

Given three basis vectors  
$v_1 = (6, 2, -3)$,  
$v_2 = (5, 1, 4)$,  
$v_3 = (2, 7, 1)$,  

we form the matrix $A$ by using each $v_i$ as a **row**:

$$
A =
\begin{pmatrix}
6 & 2 & -3 \\
5 & 1 & 4 \\
2 & 7 & 1
\end{pmatrix}.
$$

---

## 1) Determinant Calculation

To find the volume of the fundamental domain in $\mathbb{R}^3$, we take the **absolute value** of the determinant of $A$:

$$
\text{Volume} \;=\; \bigl|\det(A)\bigr|.
$$

### Step-by-Step Determinant

- First row expansion (or any other method you prefer):

$$
\det(A) 
= 6 \times \bigl[(1)(1) \,-\, (4)(7)\bigr]
\;-\;
2 \times \bigl[(5)(1) \,-\, (4)(2)\bigr]
\;+\;
(-3) \times \bigl[(5)(7) \,-\, (1)(2)\bigr].
$$

1. **Term for 6**:

   $$
   (1)(1) - (4)(7) = 1 - 28 = -27, 
   \quad
   6 \times (-27) = -162.
   $$

2. **Term for -2** (remember the minus sign before the 2):

   $$
   (5)(1) - (4)(2) = 5 - 8 = -3, 
   \quad
   -2 \times (-3) = +6.
   $$

3. **Term for -3**:

   $$
   (5)(7) - (1)(2) = 35 - 2 = 33,
   \quad
   -3 \times 33 = -99.
   $$

Summing up:

$$
\det(A) = (-162) + 6 + (-99) = -255.
$$

Therefore,

$$
\text{Volume} 
= |\det(A)| 
= |-255|
= 255.
$$

Hence, the volume of the fundamental domain (our flag) is **255**.

---

## 2) Full SageMath Code

```python
# Define the vectors
v1 = vector(RR, [6, 2, -3])
v2 = vector(RR, [5, 1, 4])
v3 = vector(RR, [2, 7, 1])

# Construct the matrix A (rows are v1, v2, v3)
A = matrix(RR, [v1, v2, v3])

# Compute determinant
det_val = A.det()

# Volume is the absolute value of the determinant
volume = abs(det_val)

print("Det(A) =", det_val)
print("Volume of the fundamental domain:", volume)

```

## Gaussian Reduction
# Gauss's Algorithm for 2D Lattice Reduction

We have two vectors:

$$
v = (846835985,\; 9834798552), \quad
u = (87502093,\; 123094980).
$$

We will apply **Gauss's two-dimensional lattice-reduction algorithm** to obtain a reduced basis 
$$
\bigl(v_1',\,v_2'\bigr)
$$ 
from our initial basis 
$$
\bigl(v_1,\,v_2\bigr),
$$ 
where we set $v_1 = v$ and $v_2 = u$.

---

## 1) Gauss's Algorithm Steps

1. **Compare norms**  
   - If $\|v_2\| < \|v_1\|$, **swap** $v_1$ and $v_2$.  

2. **Compute**  
   $$
   m \;=\; \Bigl\lfloor \dfrac{v_1 \cdot v_2}{v_1 \cdot v_1} \Bigr\rceil,
   $$
   where the fraction is **rounded** to the nearest integer.

3. **If** $m = 0$, **terminate**. The pair $(v_1, v_2)$ is reduced.

4. Otherwise, **subtract**:  
   $$
   v_2 \; \leftarrow \; v_2 \;-\; m \, v_1,
   $$
   and **go back** to step 1.

This repeats until you cannot reduce any further.

---

## 2) Applying to Our Vectors

- **Initial vectors**:

  $$
  v_1 = (846835985,\; 9834798552), \quad
  v_2 = (87502093,\; 123094980).
  $$

1. **Norm check**:  
   $\|v_1\|$ is roughly $9.85\times 10^9$,  
   $\|v_2\|$ is roughly $1.51\times 10^8$.  
   Since $\|v_2\|$ is smaller, **swap** them.

   Hence we now have
   $$
   v_1 \;=\; (87502093,\; 123094980), \quad
   v_2 \;=\; (846835985,\; 9834798552).
   $$

2. **Compute**  
   $$
   m \;=\;
   \Bigl\lfloor \dfrac{v_1 \cdot v_2}{v_1 \cdot v_1} \Bigr\rceil.
   $$

   Numerically,
   - $v_1 \cdot v_2 \approx 1.28\times 10^{18}$,
   - $v_1 \cdot v_1 \approx 2.28\times 10^{16}$,

   so $m \approx \text{round}(56.36) = 56$.

3. **Subtract**  
   $$
   v_2 \;\leftarrow\; v_2 \;-\; 56\,v_1.
   $$

   That is,  
   $$
   (846835985,\; 9834798552)
   \;-\;
   56 \times (87502093,\; 123094980)
   =
   \bigl(-4053281223,\; 2941479672\bigr).
   $$

4. **Check norms**:

   - $\|v_1\| \approx 1.51\times 10^8$  
   - $\|v_2\| \approx 5.01\times 10^9$

   $\|v_1\|$ is still smaller, so **no swap**.

5. **Compute**  
   $$
   m \;=\;
   \Bigl\lfloor \dfrac{v_1 \cdot v_2}{v_1 \cdot v_1} \Bigr\rceil.
   $$

   This ratio is about $0.3$, so $m = 0$.  
   **Algorithm terminates**.

- **Final reduced basis**:

  $$
  v_1' = (87502093,\; 123094980),\quad
  v_2' = \bigl(-4053281223,\; 2941479672\bigr).
  $$

---

## 3) The Flag

The problem asks for the **inner product** of the new basis vectors:

$$
\text{Flag}
= v_1' \cdot v_2'
=
(87502093)\,(-4053281223)
\;+\;
(123094980)\,(2941479672).
$$

You can compute this exactly (using big-integer arithmetic). A short Python or Sage snippet:

```python
v1 = (87502093, 123094980)
v2 = (-4053281223, 2941479672)

dot_val = v1[0]*v2[0] + v1[1]*v2[1]
print("Inner product =", dot_val)
```


**Below is rust source code to perform Gauss Reduction. I am not the author of this but it's a good reference for rustaceans thus I will leave it for good fortune.**

```rust
use num_bigint::BigInt;

#[derive(Debug, Clone)]
struct Vector(Vec<BigInt>);

impl std::ops::Deref for Vector {
    type Target = Vec<BigInt>;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

trait Extended {
    fn scale(&self, x: &BigInt) -> Self;
    fn size(&self) -> BigInt;
    fn gaussian_reduction(v: [Self; 2]) -> [Self; 2]
    where
        Self: Sized;
}

impl Extended for Vector {
    fn scale(&self, x: &BigInt) -> Self {
        Self(self.iter().map(|a| a * x).collect())
    }
    fn size(&self) -> BigInt {
        (self * self).sqrt()
    }
    fn gaussian_reduction(v: [Self; 2]) -> [Self; 2] {
        let (v1, mut v2) = if v[1].size() < v[0].size() {
            (v[1].clone(), v[0].clone())
        } else {
            (v[0].clone(), v[1].clone())
        };
        loop {
            let m = (&v1 * &v2) / (&v1 * &v1);
            if m == BigInt::ZERO {
                return [v1, v2];
            }
            v2 = (v2 - v1.scale(&BigInt::from(m))).clone();
        }
    }
}

impl std::ops::Add for &Vector {
    type Output = Vector;
    fn add(self, rhs: Self) -> Self::Output {
        assert!(self.len() == rhs.len());
        Vector(self.iter().enumerate().map(|(i, a)| a + &rhs[i]).collect())
    }
}
impl std::ops::Sub for &Vector {
    type Output = Vector;
    fn sub(self, rhs: Self) -> Self::Output {
        assert!(self.len() == rhs.len());
        Vector(
            self.iter()
                .enumerate()
                .map(|(i, a)| a - &rhs[i])
                .collect::<Vec<_>>(),
        )
    }
}

impl std::ops::Mul for &Vector {
    type Output = BigInt;
    fn mul(self, rhs: Self) -> Self::Output {
        assert!(self.len() == rhs.len());
        self.iter().enumerate().map(|(i, a)| a * &rhs[i]).sum()
    }
}

impl std::ops::Sub for Vector {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self::Output {
        assert!(self.len() == rhs.len());
        Self(self.iter().enumerate().map(|(i, a)| a - &rhs[i]).collect())
    }
}

fn main() {
    let v = Vector(vec![
        BigInt::from(846835985),
        BigInt::parse_bytes(b"9834798552", 10).unwrap(),
    ]);
    let u = Vector(vec![
        BigInt::from(87502093),
        BigInt::parse_bytes(b"123094980", 10).unwrap(),
    ]);
    let [b1, b2] = Vector::gaussian_reduction([v, u]);
    println!("{:?}", &b1 * &b2);
}
```
