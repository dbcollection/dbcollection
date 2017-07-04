classdef dbcollection_utils_string_ascii
    % String-to-ascii and ascii-to-string convertion functions.

    properties
    end

    methods
        function ascii_matrix = convert_str_to_ascii(obj, input)
            % Convert a string to an array in the ASCII format
            %
            % Parameters
            % ----------
            % input : string, cell
            %     String or cell to convert to ascii.
            %
            % Returns
            % -------
            % double
            %   Matrix containing the ASCII representation of the string
            %   or list of strings.

            assert(~(~exist('input', 'var') || isempty(input)), 'Missing input arg: input')

            if ischar(input)
                ascii_matrix = padarray(double(input), [0 1], 0, 'post');
            else
                % get string maximum length of the cell list
                maximum_lenght = get_str_maxmimum_lenght(input) + 1;

                % pre-allocate the array
                ascii_matrix = zeros(size(input,1), maximum_lenght);

                for i=1:length(input)
                    ascii_matrix(i, 1:length(input{i})) = double(input{i});
                end
            end
        end

        function str = convert_ascii_to_str(obj, input)
            % Convert an array/matrix in ASCII to string format.
            %
            % Parameters
            % ----------
            % input : double
            %     ASCII matrix
            %
            % Returns
            % -------
            % char
            %   Matrix containing the converted ASCII data to char.

            assert(~(~exist('input', 'var') || isempty(input)), 'Missing input arg: input')

            str = char(input(:,1:end-1));
        end
    end

end


% -------------------------- Utility functions --------------------------

function size = get_str_maxmimum_lenght(input_cell)
    size = 0;
    for i=1:length(input_cell)
        size = max(size, length(input_cell{i}));
    end
end