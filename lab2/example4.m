A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere
D1 = A.+B' ; # add element-wise A with transpose of B
D2 -= A.-B' ; # substract element-wise A with transpose of B
D3 *= A.*B' ; # multiply element-wise A with transpose of B
D4 /= A./B' ; # divide element-wise A with transpose of B

E1 = [ [ 1, 2, 3],
       [ 4, 5, 6],
       [ 7, 8, 9] ];

res1 = 60.500;
res2 = 60.-65.7;
res3 = .500;
res4 = 60.52E2;
str = "Hello world"; str2 = "Good bye";
res5 = 12e+13;
res6 = -1.87e-3;
a = 1 + 2 + 3;
if (m==n) {
    if (m >= n)
        print res;
}
