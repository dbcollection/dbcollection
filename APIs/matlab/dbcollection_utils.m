classdef dbcollection_utils
    % Utility methods for dbcollection.

    properties
        pad
        string_ascii
    end

    methods
        function obj = dbcollection_utils()
            obj.pad = dbcollection_utils_pad
            obj.string_ascii = dbcollection_utils_string_ascii
        end
    end

end
