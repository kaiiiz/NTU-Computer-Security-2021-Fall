# Single

首先需要先解出橢圓曲線的係數 a, b，可以直接拿任意兩個點代入方程式即可解出：

![image-20211010025401551](img/image-20211010025401551.png)

有了 a, b 後確認一下 $4*a^3 + 27*b^2 = 0 \ (mod \ p)$ 確定這個曲線是 singular curve：

![image-20211010025939876](img/image-20211010025939876.png)

接著就可以解出兩個根 alpha, beta：

![image-20211010025949173](img/image-20211010025949173.png)

定義上課提到的 phi function，並驗證是否有 homomorphism：

![image-20211010030002176](img/image-20211010030002176.png)

透過 `discrete_log` 解出 dA 後，然後就可以拿到 key，接著再對密文做解密即可取得 flag：

![image-20211010030055525](img/image-20211010030055525.png)