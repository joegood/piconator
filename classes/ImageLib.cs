using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

namespace Piconator.Classes
{
    class ImageLib
    {
        //http://www.vcskicks.com/csharp_animated_gif2.php
        // possibly use this:  https://magick.codeplex.com/


        // Images will be pulled in and picked apart pixel by pixel and stored in a an array of RGB values.  The 
        // GetPixel function on the Image object has to deal with a lot of image types and carries some overhead that
        // I do not want to use more than once.

        public static List<String> Analyze(string pathToImage)
        {
            var result = new List<String>();

            // Analyzes gif info System.Drawing.Imaging

            result.Add(String.Format("Full Path = {0}", System.IO.Path.GetFullPath(pathToImage)));

            Image gifImage = Image.FromFile(pathToImage);


            FrameDimension dimension = new FrameDimension(gifImage.FrameDimensionsList[0]);
            int frameCount = gifImage.GetFrameCount(dimension);

            result.Add(String.Format("FrameCount = {0}", frameCount));

            var flags = (ImageFlags)gifImage.Flags;

            if (flags.HasFlag(ImageFlags.Scalable)) result.Add("Flag.Scalable");
            if (flags.HasFlag(ImageFlags.HasAlpha)) result.Add("Flag.HasAlpha");
            if (flags.HasFlag(ImageFlags.HasTranslucent)) result.Add("Flag.HasTranslucent");
            if (flags.HasFlag(ImageFlags.PartiallyScalable)) result.Add("Flag.PartiallyScalable");
            if (flags.HasFlag(ImageFlags.ColorSpaceRgb)) result.Add("Flag.ColorSpaceRgb");
            if (flags.HasFlag(ImageFlags.ColorSpaceCmyk)) result.Add("Flag.ColorSpaceCmyk");
            if (flags.HasFlag(ImageFlags.ColorSpaceGray)) result.Add("Flag.ColorSpaceGray");
            if (flags.HasFlag(ImageFlags.ColorSpaceYcbcr)) result.Add("Flag.ColorSpaceYcbcr");
            if (flags.HasFlag(ImageFlags.ColorSpaceYcck)) result.Add("Flag.ColorSpaceYcck");
            if (flags.HasFlag(ImageFlags.HasRealDpi)) result.Add("Flag.HasRealDpi");
            if (flags.HasFlag(ImageFlags.HasRealPixelSize)) result.Add("Flag.HasRealPixelSize");
            if (flags.HasFlag(ImageFlags.ReadOnly)) result.Add("Flag.ReadOnly");
            if (flags.HasFlag(ImageFlags.Caching)) result.Add("Flag.Caching");

            result.Add(String.Format("Height = {0}", gifImage.Height));
            result.Add(String.Format("Width = {0}", gifImage.Width));
            result.Add(String.Format("HorizontalResolution = {0}", gifImage.HorizontalResolution));
            result.Add(String.Format("VerticalResolution = {0}", gifImage.VerticalResolution));

            result.Add(String.Format("PixelFormat = {0}", gifImage.PixelFormat));

            return result;

        }

        public ImageLib()
        {
            PlayList = new List<PlaylistItem>();

        }



        public bool LoadImage(string pathToImage)
        {
            if (!File.Exists(pathToImage)) throw new FileNotFoundException("The image file [{0}] was not found.");

            // This will load an image as if it was loaded by a single image playlist.

            var img = new System.Drawing.Bitmap(pathToImage); 

            // If the image is different than 32x32, what do we do now?  I can use the GDI to resize it but will bail for now.

            if (img.Width != 32 || img.Height != 32) throw new Exception("Currently, the image size is limited to 32x32.");

            return AddToPlaylist(img);

        }

        public bool LoadPlaylist(string pathToPlaylist)
        {
            throw new NotImplementedException("Not yet implemented.");
            //return false;

        }

        /// <summary>
        ///  Adds an image to the playlist.  In the case of a multi-framed image, like animated gif, it will add an image for each frame.
        /// </summary>
        /// <param name="img"></param>
        /// <returns></returns>
        private bool AddToPlaylist(Bitmap img)
        {
            if (img == null) return false;

            // Because single images, like PNG or JPG, still operate in the FrameDimension object but just return a 1,
            // we can just do a simple loop and catch them all.

            // I don't care about native GIF frame timings.  I am going to default to 0.25s per frame externally in the animator logic
            // and also allow a playlist file to define their own frame speed.  

            FrameDimension dimension = new FrameDimension(img.FrameDimensionsList[0]);
            int frameCount = img.GetFrameCount(dimension);

            bool result = true;  // default to true but use a logical AND to force a failed result on the first failed item.

            for (int index = 0; index < frameCount; index++)
            {
                img.SelectActiveFrame(dimension, index);                        // find the frame
                var item = new PlaylistItem((Bitmap)img.Clone());                // clone the frame away from the parent
                if (PlayList == null) PlayList = new List<PlaylistItem>();      // safety check
                PlayList.Add(item);                                             // add it 
                result &= PlayList.Contains(item);
            }

            return result;
        }

        private List<PlaylistItem> PlayList { get; set; }


        private class PlaylistItem
        {
            public PlaylistItem(Bitmap img)
            {
                if (img == null) { return; }

                var matrix = new Color[32, 32];
                
                for (int x = 0; x < img.Width; x++)
                {
                    for (int y=0; y<img.Height; y++)
                    {
                        matrix[x,y] = img.GetPixel(x, y);
                    }
                }

                Pixels = matrix;
            }

            public Color[,] Pixels
            {
                get;
                set;
            }

            public string Filename { get; set; }
            public string FilePath { get; set; }
            public string Name { get; set; }
            public int Duration { get; set; }
            public int FadeInMS { get; set; }
            public int FadeOut { get; set; }

        }


    }
}

