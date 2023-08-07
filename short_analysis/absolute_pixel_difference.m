img1 = imread('C:\Users\omeru\Documents\FND\My Repos\Blender\Objects\obj_0/non_rigid_matte_0_0001.png');
img1 = im2gray(img1);
img2 = imread('C:\Users\omeru\Documents\FND\My Repos\Blender\Objects\obj_0/non_rigid_matte_0_0002.png');
img2=im2gray(img2);
Z = imabsdiff(img1,img2);
%imshow(Z,[])

xcorr2(img2,img1);
