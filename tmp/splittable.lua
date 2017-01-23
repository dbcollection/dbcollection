local SplitTable, parent = torch.class('nn.SplitTableV2', 'nn.Module')

function SplitTable:__init(dimension, nTensors)
   parent.__init(self)
   self.dimension = dimension
   self.nTensors = nTensors
end

function SplitTable:getTensorSize(input)
    if self.nTensors then
        assert(input:dim()>=self.dimension, ('Input size is smaller than the specified dimension: '.. 
            'size=%d / dimension=%d '):format(input:dim(), self.dimension))
        return math.floor(input:size(self.dimension)/self.nTensors)
    else
        return input:size(self.dimension)
    end
end

function SplitTable:updateOutput(input)
   local nelems = self:getTensorSize(input)
   local output = {}
   local index = 1
   local tensor_size = input:size(self.dimension)
   for i=1, self.nTensors do
      local nElems = ((index + nelems-1) <= tensor_size and nelems) or tensor_size-(index+nelems)
      table.insert(output, input:narrow(self.dimension,index, nElems))
      index = index + nelems
   end
   self.output = output
   return output
end

function SplitTable:updateGradInput(input, gradOutput)
    if self.gradInput then
      self.gradInput:resizeAs(input)

      local nelems = self:getTensorSize(input)
      local index = 1
      local tensor_size = input:size(self.dimension)
      for i=1,self.nTensors do
         local currentGradInput = gradOutput[i];
         local nElems = ((index + nelems-1) <= tensor_size and nelems) or tensor_size-(index+nelems)
         self.gradInput:narrow(self.dimension,index,nElems):copy(currentGradInput)
      end
   end
   return self.gradInput
end
