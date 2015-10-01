using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;
using System.Drawing.Imaging;

namespace Piconator.Classes
{
    class ImageLib
    {

        //http://www.vcskicks.com/csharp_animated_gif2.php
        // possibly use this:  https://magick.codeplex.com/


        public static List<String> AnalyzeV1(string gifPath)
        {
            var result = new List<String>();

            // Analyzes gif info System.Drawing.Imaging

            result.Add(String.Format("Full Path = {0}", System.IO.Path.GetFullPath(gifPath)));

            Image gifImage = Image.FromFile(gifPath);
            

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
    }


}
