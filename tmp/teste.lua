require 'nn'
paths.dofile('/home/mf/Toolkits/Codigo/git/dbclt_teste/tmp/splittablev2.lua')

a = torch.Tensor(10,4):uniform()
s = nn.SplitTableV2(1,2)

r = s:forward(a)

print(r)

print(a)
print(r[1])
print(r[2])

print(r)