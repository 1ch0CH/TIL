# (Modern) SLAM을 이해하기 위한 요소
## 1. Rotation
- Rotation을 표현하는 방법 : Angle-axis(rotation vector, rotvec) / quaternion / SO(3) ( Euler angles라는 parametrization 으로 값 3개를 통해 SO(3) 표현가능 )
### SLAM에서 Rotation Parametrization을 해야하는 이유
- 우리가 살고 있는 state는 Position(x, y, z)와 orientation(=rotation rx, ry, rz)로 공간을 정의 할 수 있다
- vector공간에 존재하는 요소의 최적화는 쉬우나 position은 vector space에 존재한다

## 2. Least-Square Optimization
## 3. Exploiting Sparsity



[출처]
[https://gisbi-kim.github.io/blog/2021/10/03/slam-textbooks.html?fbclid=IwAR1-l1ITWZJ80aZsOpCExxA8louJhNHAZpOAJPlGt-ZY3sKYGFV0MSsOxfA](https://gisbi-kim.github.io/blog/2021/10/03/slam-textbooks.html?fbclid=IwAR1-l1ITWZJ80aZsOpCExxA8louJhNHAZpOAJPlGt-ZY3sKYGFV0MSsOxfA)

--------
# 1. Quaternion kinematics for the error-state Kalman filter
- [Download](https://gisbi-kim.github.io/materials/study/soal17eskf.pdf)
- [내용정리]
