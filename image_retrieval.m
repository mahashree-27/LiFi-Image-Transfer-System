%% Assuming the bitstream is stored in a variable
bitstreamStr = ['100000101010001010100010100010000000000000100100100010101100000000000000000000000000000000000000000000000010100001000000000000000000001010010010101000100011100011100011101000100000111011000010001100011011100010001100001011000000100111111011111000100000001001000000100011101011000001101000001100101011001010110000001010100010000010001010100111010000100011111110010000100010011000000000000000000000111101111010101101000000101100001100111010101001000000100111101011100000100010000010000000100100111100001000111010101000101010111000101000001000001000100000000000101000000000000111000000001010111000101110011000000001100000000000000' ];  % your full bitstream here

%% Pre-processing the Bitstream
bitstreamStr = regexprep(bitstreamStr, '\s+', ''); % Remove whitespace
numBits = length(bitstreamStr);
fprintf('Total bits: %d\n', numBits);

%% Calculate number of bytes
numBytes = floor(numBits/8);
if numBytes * 8 ~= numBits
    % Pad with '0's to make it a multiple of 8
    extraBits = 8 - mod(numBits,8);
    bitstreamStr = [bitstreamStr repmat('0', 1, extraBits)];
    numBits = length(bitstreamStr);
    numBytes = numBits / 8;
    fprintf('Padded bitstream with %d bits to make full bytes.\n', extraBits);
end

fprintf('Total bytes: %d\n', numBytes);

%% Convert Bitstream to Bytes
byteValues = zeros(numBytes, 1, 'uint8');
for k = 1:numBytes
    chunk = bitstreamStr((k-1)*8 + 1 : k*8);
    byteValues(k) = uint8(bin2dec(chunk));
end

%% Set Image Dimensions Based on Data Size
imgWidth = 22;
imgHeight = 22;
expectedBytes = imgWidth * imgHeight;

% Adjust byteValues to fit image size
if numBytes < expectedBytes
    % Pad with zeros if not enough bytes
    paddingNeeded = expectedBytes - numBytes;
    fprintf('Not enough data: expected %d bytes, got %d. Padding with %d zeros.\n', ...
        expectedBytes, numBytes, paddingNeeded);
    byteValues = [byteValues; zeros(paddingNeeded, 1, 'uint8')];
elseif numBytes > expectedBytes
    % Trim extra bytes
    fprintf('More data than needed: expected %d bytes, got %d. Trimming extra data.\n', ...
        expectedBytes, numBytes);
    byteValues = byteValues(1:expectedBytes);
end

%% Reshape Bytes into Image
imgData = reshape(byteValues, [imgWidth, imgHeight])';
% Transpose for correct orientation

%% Display and Save Image
figure;
imshow(imgData, []);
title('Reconstructed Image');
imwrite(imgData, 'reconstructed_image.png');
