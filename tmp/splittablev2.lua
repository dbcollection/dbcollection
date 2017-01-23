local SplitTable, parent = torch.class('nn.SplitTableV2', 'nn.Module')

function SplitTable:__init(dimension, nTensors)
   parent.__init(self)
   self.dimension = dimension
   self.nTensors = nTensors
   self.joinTable = nn.JoinTable(dimension)
end

function SplitTable:getSize(input)
    return math.floor(input:size(self.dimension)/self.nTensors)
end

function SplitTable:updateOutput(input)
   assert(input:dim()>=self.dimension, ('Input size is smaller than the specified dimension: '.. 
        'size=%d / dimension=%d '):format(input:dim(), self.dimension))
   assert(input:size(self.dimension) >= self.nTensors, ('Input size smaller than the specified split size: ' .. 
        'input size=%d / nsplits=%d '):format(input:size(self.dimension), self.nTensors))
   local tensor_size = self:getSize(input)
   self.output = input:split(tensor_size,self.dimension)
   return self.output
end

function SplitTable:updateGradInput(input, gradOutput)
   if self.gradInput then
      self.gradInput:resizeAs(input)
   else
      self.gradInput = input:clone()
   end
   self.gradInput:resizeAs(input):copy(self.joinTable:forward(gradOutput))
   return self.gradInput
end
